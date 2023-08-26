import logging
from typing import Iterable, Iterator

from smos_walker.constants import (
    DataBlockType,
    NumpifiedDataBlockType,
    PathType,
)
from smos_walker.cli.facade import output_tree_to_txt
from smos_walker.core.exception import SmosWalkerException

from smos_walker.core.node import (
    ArrayVariableNode,
    ConcreteNodeType,
    BaseNode,
    RecursiveListOfIntegers,
)

from smos_walker.core.visitors import DictIndexNodeVisitor, render_path
from smos_walker.node_to_ndarray.facade import (
    node_to_ndarray_quasi_static_one_dynamic_dimensional,
    node_to_ndarray_static_one_dynamic_dimensional,
    node_to_ndarray_quasi_static,
    node_to_ndarray_static,
)
from smos_walker.util import json_dumps


class IndexedDataBlock:
    def __init__(
        self,
        dynamically_decorated_tree: BaseNode,
        datablock: DataBlockType,
    ):
        self.datablock: DataBlockType = datablock
        self.index: dict[PathType, ConcreteNodeType] = get_tree_paths(
            dynamically_decorated_tree
        )

    # def __str__(self):
    #     return "Paths unhandled by Numpy: " + self.str_dynamic_paths()

    def __str__(self):
        lines = []
        lines.append("")
        lines.append("### All available paths")
        lines.append("")
        lines.append(self.str_all_available_paths())
        lines.append("")
        lines.append("### Statistics")
        lines.append("")
        lines.append(f"- DataBlock length: {len(self.datablock)}")
        lines.append(f"- Available paths count: {len(list(self.all_available_paths))}")
        return "\n".join(lines)

    def str_dynamic_paths(self):
        return str("\n".join([render_path(path) for path in self.dynamic_paths]))

    def str_numpyizable_paths(self):
        return str("\n".join([render_path(path) for path in self.numpyizable_paths]))

    def str_all_available_paths(self):
        return str("\n".join([render_path(path) for path in self.all_available_paths]))

    def str_all_paths(self):
        return json_dumps(
            {
                (render_path(path)): {
                    "dimensionality": node.dynamic_dimensionality,
                }
                for (path, node) in self.index.items()
            }
        )

    @property
    def dynamic_paths(self) -> Iterator[PathType]:
        # Static blocks are not indexed dynamically, we delegate them to numpy.
        return (
            path
            for path, node in self.index.items()
            if node.dynamic_dimensionality is not None
        )

    @property
    def numpyizable_paths(self) -> Iterable[PathType]:
        return (path for path, node in self.index.items() if node.numpifiable)

    @property
    def all_available_paths(self) -> Iterable[PathType]:
        return (path for path in self.index)

    @property
    def dynamic_paths_info(self) -> Iterable[tuple[PathType, int | None, str]]:
        # Static blocks are not indexed dynamically, we delegate them to numpy.
        for path, node in self.index.items():
            if node.dynamic_dimensionality is not None:
                yield (path, node.dynamic_dimensionality, node.__class__.__name__)

    def is_known_dynamic_path(self, path):
        return path in self.dynamic_paths_info

    def query_type_system_node(self, path: PathType) -> ConcreteNodeType | None:
        if path in self.index:
            return self.index[path]
        return None

    # Raw
    # self.query_datablock(("Data_Block", "List_of_Grid_Points", "Grid_Point_Latitude"), (15,))
    # Nice API
    # self.query_datablock["Data_Block"]["List_of_Grid_Points"]["Grid_Point_Latitude"][15]
    # command_builder["Data_Block"] -> DataBlockContinuation -> next paths: list of path
    # command_builder["Data_Block"]["List_of_Grid_Points"] -> list of paths (reduced)
    # command_builder["Data_Block"]["List_of_Grid_Points"]["Grid_Point_Latitude"][15]["Snapshot_Stop_Time"]["Days"][0]

    # def __getitem__(self, key: str | int):
    #     # Data_Block

    def query_datablock(
        self, path: PathType, *coordinates: int, numpify_2d_array_variable=False
    ):
        return self.query_datablock_with_tuple(
            path, coordinates, numpify_2d_array_variable=numpify_2d_array_variable
        )

    def query_datablock_with_tuple(
        self,
        path: PathType,
        coordinates: tuple[int, ...] = tuple(),
        numpify_2d_array_variable=False,
    ) -> NumpifiedDataBlockType | None:
        """Query the datablock by leveraging the dynamically decorated tree

        Example:
            self.query_datablock(("Data_Block", "List_of_Grid_Points", "Grid_Point_Latitude"), (15,))

        Args:
            path : Tuple of string path elements
            coordinates: Extra integer coordinates

        Returns:
            Numpy view over the datablock
        """
        logging.debug(f"query_datablock_with_tuple: {path=} {coordinates=}")

        node = self.query_type_system_node(path)

        if not node:
            logging.warning("node is falsy")
            return None

        if not node.numpifiable:
            logging.warning(
                "The current node cannot be numpified. Please continue exploring the tree until it is. "
                "Use walker.str_query(path) to see available paths. "
                "Details: Numpification only works for static nodes and quasi static array variables"
            )
            return None

        # Fast path: Dynamic Dimensionality = 1 -> Numpyizable immediately"
        if (
            node.dynamic_dimensionality == 1
            and node.numpifiable
            and len(coordinates) <= node.dynamic_dimensionality
        ):
            if numpify_2d_array_variable and isinstance(node, ArrayVariableNode):
                # If all elements in one-dimensional list are identical, there is no need to mask the array.
                # Indeed, all values will be valid of the numpified array will be valid.
                mask_invalid_flag = len(set(node.dynamic_size)) > 1
                data = node_to_ndarray_quasi_static_one_dynamic_dimensional(
                    node, self.datablock, mask_invalid_flag=mask_invalid_flag
                )
                return _subscribe_to_ndarray(data, coordinates)
            if not isinstance(node, ArrayVariableNode):
                data = node_to_ndarray_static_one_dynamic_dimensional(
                    node, self.datablock
                )
                return _subscribe_to_ndarray(data, coordinates)

        # TODO eschalk
        # Fast path: Siblings array variables
        # or isinstance(self, StructNode)
        # and all(child.numpifiable for child in self.children)

        if len(coordinates) != node.dynamic_dimensionality:
            provide_help_and_raise_exception(node, coordinates)

        if isinstance(node, ArrayVariableNode):
            block_byte_size = node.child.block_byte_size  # static
            offset = node.dynamic_offset  # dynamic
            dynamic_size = node.dynamic_size  # dynamic

            for coordinate in coordinates:
                offset = safe_index(coordinate, offset)
                dynamic_size = safe_index(coordinate, dynamic_size)

            # Offset due to the storage of the array's length
            offset += node.size_ref.block_byte_size

            data = node_to_ndarray_quasi_static(
                node,
                self.slice_datablock(offset, dynamic_size * block_byte_size),
                dynamic_size,
            )
        else:
            block_byte_size = node.block_byte_size  # static
            offset = node.dynamic_offset  # dynamic

            for coordinate in coordinates:
                offset = safe_index(coordinate, offset)

            data = node_to_ndarray_static(
                node, self.slice_datablock(offset, block_byte_size)
            )

        return data

    def slice_datablock(self, start, offset):
        return self.datablock[start : start + offset]


def safe_index(coordinate: int, offset: RecursiveListOfIntegers | None):
    if not isinstance(offset, list):
        logging.warning(f"{offset=} has no length for {coordinate=}")
        return None
    if coordinate >= len(offset):
        logging.warning(f"Out of bounds: {coordinate=} {len(offset)=}")
        return None
    return offset[coordinate]


def safe_len(offset: RecursiveListOfIntegers | None):
    if not isinstance(offset, list):
        raise SmosWalkerException(
            "The provided `offset` is not a list, therefore `len` cannot be applied."
        )
    return len(offset)


class IndexedDataBlockQuery:
    """One-time usage query"""

    def __init__(self, indexed_datablock: IndexedDataBlock):
        self.path: list[str | int] = []
        self.indexed_datablock = indexed_datablock

    def __repr__(self):
        return super().__repr__() + "<query=" + str(self.path) + ">"

    def __getitem__(self, key: str | int | None):
        if key is None:
            return self
        if isinstance(key, int):
            self.append_to_query(key)
            return self

        for element in key.strip("/").split("/"):
            try:
                self.append_to_query(int(element))
            except ValueError:
                self.append_to_query(element)
        return self

    def __call__(self):
        return self.consume_query()

    def __str__(self):
        return "\n".join(self.render_lines(self.get_typesystem_node()))

    def get_typesystem_node(self) -> ConcreteNodeType | None:
        """Tries to resolve the current path associated to the Query, to fetch the corresponding typesystem node.

        Returns:
            A typesystem node, when found.
        """
        if len(self.path) == 0:
            logging.debug(
                f"No path. Defaulting to the well-known {self.path_fallback=} root."
            )
            return self.indexed_datablock.query_type_system_node(self.path_fallback)

        # The type system does not care about the integer indexes for array, only the type names.
        string_elements_of_path = (p for p in self.path if isinstance(p, str))
        return self.indexed_datablock.query_type_system_node(
            tuple(string_elements_of_path)
        )

    def get_dynamic_offset(self, *coordinates: int) -> list[int] | None:
        """Returns surface-level list of offset. Analogous to an array's length.

        Looks for the ancestor's ones if not found.
        Indeed, lowest-level node are ignored by the dynamic decoration step, as they are numpifiable.
        For that reason, we have to look for the first ancestor carrying this dynamic information.

        If you want the actual recursive list of integers containing the offsets, access `node.dynamic_offset` directly.

        Returns:
            the length of the offset list if available.
        """
        node = self.get_typesystem_node()

        if node is None:
            logging.warning("node is None")
            return None

        while self.path and node.dynamic_offset is None:
            self.path.pop()
            node = self.get_typesystem_node()

        offset = node.dynamic_offset

        if offset is None:
            return None

        for coordinate in coordinates:
            offset = safe_index(coordinate, offset)

        return offset

    def get_dynamic_size(self, *coordinates: int) -> int | None:
        """Returns the first array variable ancestor dynamic size

        Returns:
            the length of the offset list if available.
        """
        node = self.get_typesystem_node()

        if node is None:
            logging.warning("node is None")
            return None

        while self.path and (
            not isinstance(node, ArrayVariableNode) or node.dynamic_size is None
        ):
            self.path.pop()
            node = self.get_typesystem_node()

        size = node.dynamic_size

        if size is None:
            return None

        for coordinate in coordinates:
            size = safe_index(coordinate, size)

        return size

    def get_dimensionality(self) -> int | None:
        """Get the dimensionality of the node, and look for the ancestor's ones if not found

        Indeed, lowest-level node are ignored by the dynamic decoration step, as they are numpifiable.
        For that reason, we have to look for the first ancestor carrying this dynamic information.

        Note:
            Does change state (self.path)
        """
        node = self.get_typesystem_node()

        if node is None:
            logging.warning("node is None")
            return None

        while self.path and node.dynamic_dimensionality is None:
            self.path.pop()
            node = self.get_typesystem_node()

        return node.dynamic_dimensionality

    def query_index_information(self):
        lines = []
        lines.append("## Query's index information:")
        lines.append(str(self.indexed_datablock))

        return "\n".join(lines)

    def clear(self):
        self.path.clear()

    def pop(self):
        self.path.pop()

    @property
    def same_prefix_paths(self):
        string_elements_of_path = (p for p in self.path_fallback if isinstance(p, str))
        current_path_str_prefix = render_path(string_elements_of_path)
        paths = (render_path(path) for path in self.indexed_datablock.index)
        paths = [path for path in paths if path.startswith(current_path_str_prefix)]

        return paths

    @property
    def path_fallback(self):
        return self.path if self.path and len(self.path) > 0 else ("Data_Block",)

    def append_to_query(self, key: str | int):
        self.path.append(key)

    def consume_query(
        self, *user_coordinates: int, numpify_2d_array_variable=False
    ) -> NumpifiedDataBlockType | None:
        logging.debug(f"consume_query: Begin: {self.path=}")

        # The prefixed path for node querying before numpy, without coordinates
        prefix_path: list[str] = []
        # Accumulates dynamic coordinates
        coordinates: list[int] = []

        cursor = 0

        for cursor, element in enumerate(self.path):
            logging.debug(f"consume_query: {element=} {prefix_path=} {coordinates=}")

            if isinstance(element, str):
                prefix_path.append(element)

                node = self.indexed_datablock.query_type_system_node(tuple(prefix_path))

                if node is None:
                    raise SmosWalkerException("Error occured during query consumption")

                if node.numpifiable:
                    logging.debug(
                        "consume_query: Static or Quasi-Static: The node is numpyizable: Break"
                    )
                    break
            elif isinstance(element, int):
                coordinates.append(element)
            else:
                logging.warning("consume_query: Path should be composed of str | int")

            if not tuple(prefix_path) in self.indexed_datablock.dynamic_paths:
                logging.debug("consume_query: break")
                prefix_path.pop()
                break

        # Allow user to give missing dynamic coordinates manually when using the smos walker.
        coordinates.extend(user_coordinates)

        data = self.indexed_datablock.query_datablock_with_tuple(
            tuple(prefix_path),
            tuple(coordinates),
            numpify_2d_array_variable=numpify_2d_array_variable,
        )

        for element in self.path[cursor + 1 :]:
            if data is None:
                logging.warning(
                    "No data was found, likely due to an out of bounds indexing"
                )
                return None
            logging.debug(f"Build: Subscribing to numpy array with {element=}")
            data = data[element]

        return data

    def render_lines(self, current_node):
        lines = []
        lines.append("")

        if not current_node:
            lines.append(
                "Error: The current query does not match any data in the index."
            )
        else:

            lines.append("## Query information:")
            lines.append("")
            lines.append(
                self.__class__.__name__
                + ": Indexed DataBlock Query: path="
                + str(self.path)
            )
            lines.append("")

            if (
                current_node.dynamic_dimensionality
                and current_node.dynamic_dimensionality > 0
            ):
                lines.append("### Node dynamic dimensionality")
                lines.append("")
                lines.append(
                    f"The current has a dynamic dimensionality of {current_node.dynamic_dimensionality}."
                    f" You have to provide such amount of coordinates when querying."
                )
                lines.append("")

            lines.append("### Node raw shallow information")
            lines.append("")
            lines.append(json_dumps(current_node.to_dict()))
            lines.append("")
            lines.append("### Node descendance information")
            lines.append("")
            lines.append(output_tree_to_txt(current_node, write_primitive_type=True))

        available_paths = "\n".join(self.same_prefix_paths)

        lines.append(
            f"""
### Node available paths:

Current:
{render_path(self.path_fallback)}
Available:
{available_paths}
    """
        )

        return lines


def get_tree_paths(
    dynamically_analyzed_tree: BaseNode,
) -> dict[PathType, ConcreteNodeType]:
    dict_index_visitor = DictIndexNodeVisitor()
    dynamically_analyzed_tree.accept(dict_index_visitor)
    return dict_index_visitor.mapping


def provide_help_and_raise_exception(node: BaseNode, coordinates: tuple[int, ...]):
    """Helps the user when the query could not be executed.

    - Provide the length of the typesystem node parent
    - Provide a quickfix (adding a coordinates).

    Args:
        node: found node
        coordinates: given coordinates

    Raises:
        SmosWalkerException: error message containing help
    """

    missing_coordinates_count = (node.dynamic_dimensionality or 0) - len(coordinates)
    additional_help = ""

    if missing_coordinates_count > 0:
        # We can help the user even more by giving range of validity.
        offset = node.dynamic_offset
        # Keep track of the max_lengths of the dynamic dimensionality
        max_offsets = [safe_len(offset)]
        for coordinate in coordinates:
            offset = safe_index(coordinate, offset)
            max_offsets.append(safe_len(offset))

        if missing_coordinates_count == 1:
            max_offset = max_offsets[-1]
            provided_coordinates = (
                ", " + ", ".join(str(c) for c in coordinates) if coordinates else ""
            )
            additional_help = (
                f"In your case, there is only one missing coordinate. "
                f"Retry with an extra integer coordinate in range({max_offset}). "
                f"eg `walker.query(path{provided_coordinates})` -> "
                f"`walker.query(path{provided_coordinates}, {max_offset - 1})`. "
            )
        else:
            ranges = ", ".join(f"range({max_offset})" for max_offset in max_offsets)
            example_coordinates = ", ".join(
                f"{max_offset - 1}" for max_offset in max_offsets
            )
            provided_coordinates = (
                ", " + ", ".join(str(c) for c in coordinates) if coordinates else ""
            )
            additional_help = (
                f"In your case, there are {missing_coordinates_count} missing coordinates. "
                f"Retry the query by first providing some integer coordinates in respective ranges: [{ranges}]. "
                f"eg `walker.query(path{provided_coordinates})` -> "
                f"`walker.query(path{provided_coordinates}, {example_coordinates})`"
            )
        additional_help = (
            f"{additional_help}"
            f"To get the maximum offset of the current dimension, use: "
            f"`walker.get_length(path{provided_coordinates})"
        )
    else:
        additional_help = f"{-missing_coordinates_count} excess coordinates were given. Retry by removing these."

    logging.debug(
        f"{node.dynamic_dimensionality=} but {coordinates=} ({len(coordinates)=}) was provided (mismatch of lengths)."
    )
    raise SmosWalkerException(f"Query could not be executed. {additional_help}")


def _subscribe_to_ndarray(
    data: NumpifiedDataBlockType, coordinates: tuple[int, ...]
) -> NumpifiedDataBlockType:
    if len(coordinates) == 2:
        return data[coordinates[0], coordinates[1]]
    if len(coordinates) == 1:
        return data[coordinates[0]]
    return data
