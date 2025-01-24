from statistics import fmean

import networkx as nx


class GraphEvaluator:
    """Helper-Class to provide some simple evaluation metrics for the generated graph-scheme."""
    def __init__(self, scheme):
        # create a directed graph that allows self-loops and parallel edges
        self.graph = nx.MultiDiGraph()
        self.missing_nodes = set()

        node_ids = list(map(lambda x: x['concept_id'], scheme['concepts']))
        edges = scheme['relations']

        # add proposed nodes to graph
        for node in node_ids:
            self.graph.add_node(node)

        # add proposed edges to graph if they can be matched to proposed source- and target-nodes
        for edge in edges:
            if edge["from_concept"] not in node_ids:
                self.missing_nodes.add(edge["from_concept"])
                continue

            if edge["to_concept"] not in node_ids:
                self.missing_nodes.add(edge["to_concept"])
                continue

            self.graph.add_edge(edge["from_concept"], edge["to_concept"])

    def get_missing_nodes(self):
        """returns a list of missing nodes (nodes mentioned within relations but not within the nodes-array)"""
        return self.missing_nodes

    def count_missing_nodes(self):
        """returns the number of missing nodes (nodes mentioned within relations but not within the nodes-array)"""
        return len(self.missing_nodes)

    def get_disconnected_components(self):
        """returns all disconnected components of the graph (subgraphs that are not connected to each other)"""
        undirected_graph = self.graph.to_undirected()
        return list(nx.connected_components(undirected_graph))

    def count_disconnected_components(self):
        """returns the number of disconnected components of the graph (subgraphs that are not connected to each
        other)"""
        return len(self.get_disconnected_components())

    def get_lonely_nodes(self):
        """returns all lonely nodes (nodes without relations)"""
        undirected_graph = self.graph.to_undirected()
        components = nx.connected_components(undirected_graph)

        return [undirected_graph.subgraph(c).copy() for c in components if len(c) == 1]

    def count_lonely_nodes(self):
        """returns the number of lonely nodes (nodes without relations)"""
        return len(self.get_lonely_nodes())

    def get_normalized_degree_centrality(self):
        """returns the normalized degree centrality of each node"""
        return _sort_dict_by_value(nx.degree_centrality(self.graph.to_undirected()))

    def get_closeness_centrality(self):
        """returns the closeness centrality of each node"""
        return _sort_dict_by_value(nx.closeness_centrality(self.graph.to_undirected()))

    def get_betweenness_centrality(self):
        """returns the betweenness centrality of each node"""
        return _sort_dict_by_value(nx.betweenness_centrality(self.graph.to_undirected()))

    def get_avg_edges(self):
        """returns the average number of edges per node"""
        degrees = list(dict(self.graph.degree()).values())
        return fmean(degrees)

    def get_max_edges(self):
        """returns the maximum number of edges per node"""
        degrees = list(dict(self.graph.degree()).values())
        return max(degrees)

    def get_summary(self):
        """returns a dict summarizing all metrics"""
        return {
            'missing_nodes': self.count_missing_nodes(),
            'disconnected_components': self.count_disconnected_components(),
            'lonely_nodes': self.count_lonely_nodes(),
            'avg_edges': self.get_avg_edges(),
            'max_edges': self.get_max_edges(),
            'centrality': {
                'normalized_degree': self.get_normalized_degree_centrality(),
                'closeness': self.get_closeness_centrality(),
                'betweenness': self.get_betweenness_centrality()
            }
        }


def _sort_dict_by_value(dictionary):
    """Helper-function to sort a dictionary by its values (descending)"""
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}
