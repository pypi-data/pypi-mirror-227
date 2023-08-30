import glog
import networkx as nx
from ascend.sdk.client import Client


def _node_value(node):
  return node[0].value if len(node) else 1


class LineageContext:
  def __init__(self, centroid) -> None:
    if not centroid or not hasattr(centroid, 'uuid'):
      raise ValueError('A centroid is required to establish lineage context')
    self.graph = nx.DiGraph()
    self.centroid = centroid
    self.data_services = set()

  def _assert_centroid(self):
    if not self.centroid or not getattr(self.centroid, 'uuid', None):
      raise ValueError('Cannot generate lineage without a component to use as a relative starting point. Did you build_graph()?')

  def _nodes_as_map(self):
    return {n[0]: n[1]['component'] for n in self.graph.nodes(data=True)}

  def upstream(self) -> list:
    """Return the upstream lineage ending with the centroid component"""
    self._assert_centroid()
    nodes = self._nodes_as_map()
    return [nodes[n] for n in list(nx.bfs_tree(self.graph, self.centroid.uuid, reverse=True))[::-1]]

  def downstream(self) -> list:
    """Return the downstream lineage starting with centroid component"""
    self._assert_centroid()
    nodes = self._nodes_as_map()
    return [nodes[n] for n in list(nx.bfs_tree(self.graph, self.centroid.uuid, reverse=False))]

  def readers(self) -> list:
    """Return the readers for this context"""
    self._assert_centroid()
    return [s for s in self.upstream() if s.type == 'source']

  def writers(self) -> list:
    """Return the writers for this context"""
    self._assert_centroid()
    return [s for s in self.downstream() if s.type == 'sink']

  def end_to_end(self) -> list:
    """Return the end to end lineage passing through the centroid."""
    self._assert_centroid()
    up = self.upstream()
    down = self.downstream()
    if up and down:
      return up + down[1:]
    elif up:
      return up
    else:
      return down

  def __str__(self) -> str:
    return f'LineageContext for {self.centroid}'


class LineageSupport:
  def __init__(self, client: Client):
    self._client = client

  def build_graph(self, data_service_id: str, dataflow_id: str = None, component_id: str = None) -> LineageContext:
    if not data_service_id:
      raise ValueError('A Data Service is required to calculate lineage.')

    components, edges = self._assemble_graph(data_service_id)

    cen = [v for v in components.values() if v.organization.id == data_service_id and v.project.id == dataflow_id and v.id == component_id]
    if not cen:
      raise ValueError(f'Could not find component {data_service_id}.{dataflow_id}.{component_id} to use as lineage centroid')

    context = LineageContext(cen[0])
    context.graph.add_nodes_from([(node, {'component': attr}) for (node, attr) in components.items()])
    context.graph.add_edges_from(edges)
    return context

  def _assemble_graph(
      self,
      data_service_id: str,
      data_services: set = None,
      components: dict = None,
      component_id_map: dict = None,
  ) -> (dict, list):
    """A recursive function that progressively steps through data services until there are no new ones in the sharing lineage"""
    if data_services is None:
      data_services = set()
    elif data_service_id in data_services:
      return {}, []

    if not components:
      components = {}

    if not component_id_map:
      component_id_map = {}

    glog.debug(f'Assembling graph for {data_service_id}')
    data_services.add(data_service_id)

    data_service_components = self._client.list_data_service_components(data_service_id).data

    for c in data_service_components:
      components[c.uuid] = c
      # also have to map ComponentID
      if hasattr(c, 'ComponentID'):
        component_id_map[c.ComponentID] = c

    edges = []
    subscribers = set()
    # build the network edges
    for k, v in components.items():
      if v.type in ['source']:
        # no inputs to sources
        glog.debug(f'component with source type: {v.organization.id}.{v.project.id}.{v.id}')
        continue
      elif getattr(v, 'inputs', None):
        glog.debug(f'component with inputs: {v.organization.id}.{v.project.id}.{v.id}')
        for c_in in v.inputs:
          edges.append((c_in.uuid, v.uuid))
      elif getattr(v, 'inputComponentIDs', None):
        glog.debug(f'component with inputComponentIDs: {v.organization.id}.{v.project.id}.{v.id}')
        input_ids = v.inputComponentIDs.split(',')
        if not input_ids:
          glog.info(f'Data Share Component has no input ids: {v.organization.id}.{v.project.id}.{v.id}')
        elif len(input_ids) > 1:
          glog.warn(f'Data Share Component has more than one input: {v.organization.id}.{v.project.id}.{v.id} -> {v.inputComponentIDs}')
        if input_ids:
          edges.append((component_id_map[input_ids[0]].uuid, v.uuid))
      elif hasattr(v, 'pubUUID'):
        glog.debug(f'component with pubUUID: {v.organization.id}.{v.project.id}.{v.id}')
        edges.append((v.pubUUID, v.uuid))
      elif hasattr(v, 'inputUUID'):
        glog.debug(f'component with inputUUID: {v.organization.id}.{v.project.id}.{v.id}')
        edges.append((v.inputUUID, v.uuid))
      else:
        glog.info(f'No mapping data for {v}')

      if v.type in ['data_share']:
        glog.debug(f'pulling data share connectors for share {v.organization.id}.{v.project.id}.{v.id}')
        # query for other services.
        for c in self._client.get_data_share_connectors_for_data_share(v.organization.id, v.project.id, v.id).data:
          subscribers.add(c.organization.id)
      elif v.type in ['pub']:
        glog.debug(f'pulling data feed connectors for share {v.organization.id}.{v.project.id}.{v.id}')
        for c in self._client.get_data_feed_subscribers(v.organization.id, v.project.id, v.id).data:
          subscribers.add(c.organization.id)

    for ds in subscribers:
      glog.debug(f'Recursion for subscriber data service {ds}')
      c, e = self._assemble_graph(ds, data_services, components, component_id_map)
      components.update(c)
      edges.extend(e)

    return components, edges