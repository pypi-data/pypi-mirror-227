import itertools
import logging

import numpy as np
from smos_walker.config import SmosWalkerFeatureFlag
from smos_walker.constants import DataBlockType, PrimitiveTypeTagNameMapping
from smos_walker.core.exception import SmosWalkerException
from smos_walker.core.node import (
    ArrayFixedNode,
    ArrayVariableNode,
    BaseNode,
    LeafNode,
    NodeVisitor,
    StructNode,
)


class DynamicIndexerNodeVisitor(NodeVisitor):
    """Reads the binary file and computes an index (useful for array variables)

    This mutates and enriches the original tree, be careful.

    Args:
        NodeVisitor (_type_): _description_
    """

    def __init__(self, datablock: DataBlockType):

        # State
        # -----
        # Carries cursor state. Increases through the binary file reading.
        self.cursor = 0
        # Numpy 1d array representing the binary data block to browse
        self.datablock = datablock
        # Each array variable introduces a supplementary dimension.
        # The stack represent the path to uniquely identify a nested node inside an arrayvariable.
        # eg 6, updated when an arrayvariable is encountered
        self.index_stack: list[int] = []

        # Flags
        # ------
        # An array variable is considered quasi-static if its child struct is static
        # This means, the only parameter to determine at runtime is the arrayvariable's length,
        # and there is no need to iterate over its content as all children blocks are of the same size.
        self.flag_quasi_static_optimization = True
        # # For demo purposes, limit the amount of nested information to keep in memory.
        # If the amount is exceeded, excess data is just ignored.
        self.flag_index_limit = False
        self.flag_index_limit_count = 16

    def visit_leaf(self, node: LeafNode):
        self.update_dynamic_offset(node)
        logging.debug("visit_leaf) ")
        # A leaf node is always static
        initial_cursor = self.cursor
        self.cursor += node.block_byte_size
        self.update_dynamic_coverage(node, initial_cursor)

    def visit_struct(self, node: StructNode):
        self.update_dynamic_offset(node)
        logging.debug(f"{self.cursor=:012} (visitStructNode)({node.name=}) ")
        if node.static:  # Fast path
            self.cursor += node.block_byte_size
            logging.debug(
                f"{self.cursor=:012} (visitStructNode)({node.name=}) Fast Path node.static"
            )
            return

        initial_cursor = self.cursor
        for child in node.yield_children():  # Warning: Performance (loop in python)
            child.accept(self)

        # Warning for nested
        self.update_dynamic_coverage(node, initial_cursor)

    def visit_array_fixed(self, node: ArrayFixedNode):
        self.update_dynamic_offset(node)
        logging.debug(
            f"{self.cursor=:012} (visitArrayFixedNode)({node.name=},{node.cardinality=},{node.dimensions=})"
        )

        if node.static:  # Fast path
            initial_cursor = self.cursor
            self.cursor += node.block_byte_size
            self.update_dynamic_coverage(node, initial_cursor)
            logging.debug(
                f"{self.cursor=:012} (visitArrayFixedNode)({node.name=}) Fast Path node.static"
            )
            return

        if not SmosWalkerFeatureFlag.NUMPIFY_DYNAMIC_1D_ARRAY_FIXED:
            raise SmosWalkerException("Dynamic array fixed are not supported yet.")

        if len(node.dimensions) == 1:  # Fast path
            # Memoize
            initial_cursor = self.cursor

            # Array variable functions can be reused!
            self.array_fully_dynamic_strategy(node, node.dimensions[0]["size"])

            # Dimensionality is for children not arrayvariable itself
            self.update_dynamic_coverage(node, initial_cursor)

            logging.debug(
                f"{self.cursor=:012} (visitArrayFixedNode)({node.name=}) Fast Path len(node.dimensions) == 1"
            )
            return

        if not SmosWalkerFeatureFlag.NUMPIFY_DYNAMIC_ND_ARRAY_FIXED:
            raise SmosWalkerException(
                "Dynamic multidimensional array fixed are not supported yet."
            )

        # TODO eschalk This code is UNTESTED, and will likely be hit when analyzing schemas containg non-static
        # `ArrayFixed`. The implementation has to be tested and updated if needed later on.
        # This might cause issues performance-wise. Array Fixed containing non-static children means it cannot be sliced
        # uniformely. An non-static Array Fixed should be treated as a fixed-size list of heterogeneous elements.
        indices = np.zeros(
            len(list(dimension["size"] for dimension in node.dimensions))
        )
        initial_cursor = self.cursor

        for key in itertools.product(
            (dimension["size"] for dimension in node.dimensions)
        ):
            local_initial_cursor = self.cursor
            node.child.accept(self)
            # TODO eschalk find a better way to store (flatten to 1D?).
            # This won't work for nodes nested in array variables.
            indices[key] = self.cursor - local_initial_cursor  # cursor offset

        self.update_dynamic_coverage(node, initial_cursor)

    def visit_array_variable(self, node: ArrayVariableNode):
        self.update_dynamic_offset(node)

        logging.debug(f"{self.cursor=:012} (visitArrayVariableNode)({node.name=}) ")

        # Fetch the ArrayVariable's LOCAL size (the size can be multidimensional)
        local_dynamic_size = self.fetch_dynamic_size_and_move_cursor(node)

        node.dynamic_size = self.consume_index_stack_generic(
            node, node.dynamic_size, local_dynamic_size
        )

        # Memoize
        initial_cursor = self.cursor

        if self.flag_quasi_static_optimization and node.quasi_static:
            self.array_variable_quasi_static_strategy(node, local_dynamic_size)
        else:
            self.array_fully_dynamic_strategy(node, local_dynamic_size)

        # Dimensionality is for children not arrayvariable itself
        self.update_dynamic_coverage(node, initial_cursor)

    def array_variable_quasi_static_strategy(
        self, node: ArrayVariableNode, local_dynamic_size
    ):

        # Fast-forward the cursor:
        # All elements of the ArrayVariable are of constant static length
        # So multiply this static length by the dynamically known size is enough to move the cursor.
        self.cursor += local_dynamic_size * node.child.block_byte_size

    def array_fully_dynamic_strategy(
        self, node: ArrayVariableNode | ArrayFixedNode, length
    ):
        self.index_stack.append(0)

        # Warning: Performance (loop in python)
        for _ in range(length):
            node.child.accept(self)
            self.index_stack[-1] += 1

        self.index_stack.pop()

    def fetch_dynamic_size_and_move_cursor(self, node: ArrayVariableNode):
        # Fetch the numpy type associated to the `sizeRef` node
        numpy_type = PrimitiveTypeTagNameMapping[node.size_ref.primitive_type]["np"]
        local_dynamic_size = (
            self.slice_datablock_from_current_cursor(node.size_ref.block_byte_size)
            .view(numpy_type)[0]
            .item()  # unwrap to python native for serialization
        )

        # Cursor move after the size has been read
        self.cursor += node.size_ref.block_byte_size

        logging.debug(
            f"{self.cursor=:012} (visitArrayVariableNode)({node.name=}) {local_dynamic_size=} {numpy_type=}"
        )

        return local_dynamic_size

    def update_dynamic_offset(self, node: BaseNode):
        node.dynamic_offset = self.consume_index_stack_generic(
            node, node.dynamic_offset, self.cursor
        )

    def consume_index_stack_generic(
        self, node: BaseNode, nested_lists, value: int
    ) -> list | int:
        if node.dynamic_dimensionality is None:
            node.dynamic_dimensionality = len(self.index_stack)

        # Fast paths
        if node.dynamic_dimensionality == 0:
            nested_lists = value
            return nested_lists

        if node.dynamic_dimensionality == 1:
            if not nested_lists:
                nested_lists = []

            if (
                not self.flag_index_limit
                or self.index_stack[-1] < self.flag_index_limit_count
            ):
                nested_lists.append(value)
            return nested_lists

        # Long path
        if not nested_lists:
            logging.debug(f"{nested_lists=}")
            logging.debug(f"{node.dynamic_dimensionality=}")

            nested_lists = []
            for _ in range(node.dynamic_dimensionality - 1):
                nested_lists = [nested_lists]

            logging.debug(f"{nested_lists=}")

        logging.debug(f"{self.index_stack=}")

        nested_index = nested_lists
        for index in self.index_stack[:-1]:  # The last level is not used
            # for index in self.index_stack[:-1]:  # The last level is not used
            # The index should not exceed the len of the current nested_index by more than one
            logging.debug(f"{nested_index=}")
            logging.debug(f"{index=}")
            if index == len(nested_index):
                nested_index.append([])
            nested_index = nested_index[index]
            logging.debug(f"{nested_index=}")

        if (
            not self.flag_index_limit
            or self.index_stack[-1] < self.flag_index_limit_count
        ):
            nested_index.append(value)

        return nested_lists

    def update_dynamic_coverage(self, node: BaseNode, initial_cursor):
        # cursor offset is the dynamic block byte size
        if node.dynamic_coverage is None:
            node.dynamic_coverage = self.cursor - initial_cursor
        else:
            node.dynamic_coverage += self.cursor - initial_cursor

    def slice_datablock_from_current_cursor(self, offset):
        return self._slice_datablock(self.cursor, offset)

    def _slice_datablock(self, start, offset):
        return self.datablock[start : start + offset]
