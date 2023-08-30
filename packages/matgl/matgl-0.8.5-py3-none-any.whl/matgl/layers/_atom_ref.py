from __future__ import annotations

import dgl
import numpy as np
import torch
from torch import nn


class AtomRef(nn.Module):
    """Get total property offset for a system."""

    def __init__(
        self,
        property_offset: np.array,  # type: ignore
    ) -> None:
        """
        Args:
            property_offset (np.array): a array of elemental property offset.
        """
        super().__init__()
        self.property_offset = torch.tensor(property_offset)
        self.max_z = self.property_offset.size(dim=0)

    def get_feature_matrix(self, graphs: list) -> np.typing.NDArray:
        """Get the number of atoms for different elements in the structure.

        Args:
            graphs (list): a list of dgl graph

        Returns:
            features (np.array): a matrix (num_structures, num_elements)
        """
        n = len(graphs)
        features = np.zeros(shape=(n, self.max_z))
        for i, s in enumerate(graphs):
            atomic_numbers = s.ndata["node_type"].numpy().tolist()
            features[i] = np.bincount(atomic_numbers, minlength=self.max_z)
        return features

    def fit(self, graphs: list, properties: np.typing.NDArray) -> None:
        """Fit the elemental reference values for the properties.

        Args:
            graphs: dgl graphs
            properties (np.ndarray): array of extensive properties
        """
        features = self.get_feature_matrix(graphs)
        self.property_offset = np.linalg.pinv(features.T.dot(features)).dot(features.T.dot(properties))
        self.property_offset = torch.tensor(self.property_offset)

    def forward(self, g: dgl.DGLGraph, state_attr: torch.Tensor | None = None):
        """Get the total property offset for a system.

        Args:
            g: a batch of dgl graphs
            state_attr: state attributes

        Returns:
            offset_per_graph
        """
        num_elements = (
            self.property_offset.size(dim=1) if self.property_offset.ndim > 1 else self.property_offset.size(dim=0)
        )
        one_hot = torch.eye(num_elements)[g.ndata["node_type"]]
        if self.property_offset.ndim > 1:
            offset_batched_with_state = []
            for i in range(self.property_offset.size(dim=0)):
                property_offset_batched = self.property_offset[i].repeat(g.num_nodes(), 1)
                offset = property_offset_batched * one_hot
                g.ndata["atomic_offset"] = torch.sum(offset, 1)
                offset_batched = dgl.readout_nodes(g, "atomic_offset")
                offset_batched_with_state.append(offset_batched)
            offset_batched_with_state = torch.stack(offset_batched_with_state)  # type: ignore
            return offset_batched_with_state[state_attr]  # type: ignore
        property_offset_batched = self.property_offset.repeat(g.num_nodes(), 1)
        offset = property_offset_batched * one_hot
        g.ndata["atomic_offset"] = torch.sum(offset, 1)
        offset_batched = dgl.readout_nodes(g, "atomic_offset")
        return offset_batched
