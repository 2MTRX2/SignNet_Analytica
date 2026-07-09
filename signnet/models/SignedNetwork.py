class SignedNetwork:

    def __init__(self, edges):
        """
        edges: pandas DataFrame with columns:
        source, target, sign
        """

        self.edges = edges

    @property
    def nodes(self):
        sources = set(self.edges["source"])
        targets = set(self.edges["target"])

        return sources.union(targets)

    @property
    def number_of_nodes(self):
        return len(self.nodes)

    @property
    def number_of_edges(self):
        return len(self.edges)