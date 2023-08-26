import logging
from pathlib import Path
import time
from smos_walker.api.core import IndexedDataBlock, IndexedDataBlockQuery
from smos_walker.api.tools import output_tree_to_txt
from smos_walker.config import SmosWalkerFeatureFlag
from smos_walker.constants import DataBlockType, NumpifiedDataBlockType
from smos_walker.core.exception import SmosWalkerException
from smos_walker.core.node import BaseNode, ConcreteNodeType
from smos_walker.core.visitors import DictIndexNodeVisitor, render_path
from smos_walker.data_reader.facade import read_dbl
from smos_walker.typesystem_dynamic_decorator.facade import (
    dynamically_decorate_tree,
)
from smos_walker.typesystem_static_decorator.facade import (
    load_statically_decorated_tree,
)
from smos_walker.xml_reader.facade import (
    extract_xml_schema_filename_from_hdr_file,
    get_hdr_path_from_earthexplorer_folder,
    get_dbl_path_from_earthexplorer_folder,
    get_metadata_from_header,
)


class SmosWalker:
    """Instantiate an object to help manipulating datablocks

    See `test_smoswalker_highlevel_api` for a practical example of usage.

    Attributes:
        xsd_path: Path pointing towards the XSD file, also known as "binx.xsd".
        xml_schema_path: Path pointing towards an XML schema file.
        datablock_folder_path: Path pointing towards the folder containing the data block.

        statically_decorated_tree: A statically-decorated tree. Does not require a datablock. Corresponds to "Step 2"
        indexed_datablock: The indexed datablock
    """

    @classmethod
    def from_earthexplorer(
        cls, schemas_home_folder_path: str, datablock_folder_path: str
    ) -> "SmosWalker":
        """An alternate constructor for SmosWalker

        Args:
            schemas_home_folder_path: Path to a folder containing all required  XML schemas (binx, schemas...)
            datablock_folder_path: Path to a folder containing EarthExplorer data (.DBL + .HDR)

        Raises:
            SmosWalkerException: When no unique binx schema was found in the schemas folder
            SmosWalkerException: When no unique .DBL file was found in the EarthExplorer data folder

        Returns:
            An initialized SmosWalker
        """
        schemas_home_folder_path = Path(schemas_home_folder_path)
        datablock_folder_path = Path(datablock_folder_path)

        xml_schema_path_in_hdr = extract_xml_schema_filename_from_hdr_file(
            datablock_folder_path
        )

        xsd_glob = list(schemas_home_folder_path.rglob("binx.xsd"))

        if len(xsd_glob) != 1:
            raise SmosWalkerException(
                f"Expected a unique BINX schema file in given {datablock_folder_path=}. (found: {len(xsd_glob)})"
            )

        xsd_path = xsd_glob[0]

        xml_schema_glob = list(schemas_home_folder_path.rglob(xml_schema_path_in_hdr))

        if len(xml_schema_glob) != 1:
            raise SmosWalkerException(
                f"Expected a unique DBL file in given {datablock_folder_path=}. (found: {len(xml_schema_glob)})"
            )

        xml_schema_path = xml_schema_glob[0]

        return cls(xsd_path, xml_schema_path, datablock_folder_path)

    def __init__(
        self,
        xsd_path: str,
        xml_schema_path: str,
        datablock_folder_path: str | None = None,
    ):
        """Constructor

        Args:
            xsd_path: Path pointing towards the XSD file, also known as "binx.xsd".
            xml_schema_path: Path pointing towards an XML schema file.
            datablock_folder_path: Path pointing towards the folder containing the data block.
        """
        self.xsd_path: str = xsd_path
        self.xml_schema_path: str = xml_schema_path

        # Keep a plain statically decorated tree, as a reference
        # It is not reused when indexing datablock as dynamic decoration occurs in-place.
        # For now, the static analysis is just remade when needed.
        # It can be printed for information with `get_dynamically_decorated_tree_text_representation`
        self.statically_decorated_tree: BaseNode = load_statically_decorated_tree(
            xsd_path, xml_schema_path
        )

        # Annotate nodes with paths
        self.statically_decorated_tree.accept(DictIndexNodeVisitor())

        self.datablock_folder_path: str | None = None
        self.indexed_datablock: IndexedDataBlock | None = None

        self.flag_numpify_dynamic_1d_array_variable: bool = (
            SmosWalkerFeatureFlag.NUMPIFY_DYNAMIC_1D_ARRAY_VARIABLE
        )

        self.flag_generator_dynamic_1d: bool = (
            SmosWalkerFeatureFlag.GENERATOR_DYNAMIC_1D
        )

        # If the datablock is already provided, immediately index it
        if datablock_folder_path:
            self.set_datablock(datablock_folder_path)

    def set_datablock(self, datablock_folder_path: str):
        """Sets the datablock path and index it

        Args:
            datablock_folder_path: Path pointing towards the folder containing the data block.
        """
        self.datablock_folder_path = datablock_folder_path
        self._index_datablock()

    def query_timed(
        self, path: str, *coordinates: int
    ) -> NumpifiedDataBlockType | None:
        start = time.perf_counter()
        result = self.query(path, *coordinates)
        end = time.perf_counter()
        logging.info(f"Query execution time: {end - start:.2f} seconds")
        return result

    def query(
        self,
        path: str,
        *coordinates: int,
    ) -> NumpifiedDataBlockType | None:
        """Fetch data from the index datablock

        Args:
            path: Slash-separated path pointing to a node in the typesystem hierarchy.
                To see a list of available paths, use str_query(path).
            coordinates: Optional extra coordinates to uniquely identify a node
                (some type hierarchies have a high-dimensionality, usually due to the nested
                use of Array Variables in the schema description)
        Raises:
            SmosWalkerException: error message containing help to uniquely identify a node in the typesystem hierarchy.

        Returns:
            A Numpy's ndarray if the node could be located in the typesystem and the datablock.
        """
        self._require_indexed_datablock()

        if (
            not self.flag_numpify_dynamic_1d_array_variable
            and self.flag_generator_dynamic_1d
            and self.get_dimensionality(path) == 1
        ):
            return (
                self.create_query(path).consume_query(
                    index,
                    numpify_2d_array_variable=self.flag_numpify_dynamic_1d_array_variable,
                )
                for index in range(self.get_length(path))
            )

        # Allow user to quickly give extra dynamic coordinates after failure to query the datablock.
        return self.create_query(path).consume_query(
            *coordinates,
            numpify_2d_array_variable=self.flag_numpify_dynamic_1d_array_variable,
        )

    @property
    def datablock_info(self):
        """Information about the indexed datablock"""
        return self.str_indexed_datablock()

    def str_indexed_datablock(self):
        return str(self.indexed_datablock)

    @property
    def paths(self):
        return list(
            render_path(path) for path in self.indexed_datablock.all_available_paths
        )

    @property
    def type_info(self):
        """Information about a path in the typesystem hierarchy"""
        return self.get_type_info()

    def get_type_info(self, path: str | None = None):
        """Information about a path in the typesystem hierarchy"""
        return self.str_query(path)

    def str_query(self, path: str | None) -> str:
        return str(self.create_query(path))

    @property
    def static_tree(self) -> str:
        return self.str_static_tree()

    def str_static_tree(self) -> str:
        """Print a user-friendly representation of the statically decorated tree (aka Step 2 in the XML schema parsing)

        Returns:
            text representation of the statically decorated tree
        """
        return self._get_statically_decorated_tree_text_representation()

    @property
    def info(self) -> str:
        return self.get_info()

    @property
    def hdr_path(self):
        return get_hdr_path_from_earthexplorer_folder(self.datablock_folder_path)

    @property
    def dbl_path(self):
        return get_dbl_path_from_earthexplorer_folder(self.datablock_folder_path)

    @property
    def metadata_from_header(self):
        return get_metadata_from_header(self.datablock_folder_path)

    def _repr_pretty_(self, pretty_printer, _):
        paths = "\n".join(self.paths)
        static_tree_details = output_tree_to_txt(
            self.get_typesystem_node(None),
            write_dimension_name_flag=True,
            write_dynamic_attributes=True,
            write_primitive_type=True,
            write_path=True,
            write_static=True,
            write_block_byte_size=True,
            ignore_static_nodes=False,
            ignore_non_dimensional_nodes=False,
        )
        return pretty_printer.text(
            f"""# SmosWalker Information

## Paths 

- {self.xsd_path=} 
- {self.xml_schema_path=} 
- {self.datablock_folder_path=}
- {self.hdr_path=}
- {self.dbl_path=}

## Metadata 

{self.metadata_from_header}

## Indexed DataBlock

{self.str_indexed_datablock()}

## Static Tree

### Summary

{self.str_static_tree()}

### Details

{static_tree_details}

## Dynamic Tree

{self.str_dynamic_tree()}

## Paths

{paths}
"""
        )

    def get_info(self, path: str | None = None) -> str:
        """alias for`str_dynamic_tree`"""
        return self.str_dynamic_tree(path)

    def str_dynamic_tree(self, path: str | None = None) -> str:
        """Print a user-friendly representation of the dynamically decorated tree (aka Step 3 in the XML schema parsing)

        Requires an indexed datablock. Use `set_datablock` if no datablock is set yet.

        Args:
            path: Slash-separated path pointing to a node in the typesystem hierarchy.
                To see a list of available paths, use str_query().
                No path given means print the whole tree from the root.

        Returns:
            text representation of the dynamically decorated tree
        """
        return self._get_dynamically_decorated_tree_text_representation(
            path,
            write_numpifiable=True,
        )

    def get_typesystem_node(self, path: str | None = None) -> ConcreteNodeType | None:
        """Tries to retrieve the original typesystem node for the given path

        Applies to the dynamically decorated tree obtained from the indexed datablock.

        Args:
            path: Slash-separated path pointing to a node in the typesystem hierarchy.
                To see a list of available paths, use str_query().

        Returns:
            typesystem node if found.
        """
        return self.create_query(path).get_typesystem_node()

    def get_length(self, path: str, *coordinates: int) -> int | None:
        """Gives the max index of the list of dynamic offsets, and navigate through coordinates if needed.

        Args:
            path: Slash-separated path pointing to a node in the typesystem hierarchy.
                To see a list of available paths, use str_query().
            coordinates: Optional extra coordinates to uniquely identify a node
                (some type hierarchies have a high-dimensionality,
                usually due to the nested use of Array Variables in the schema description)

        Returns:
            max index if possible, else None (eg, if the dimension of the node is 0)
        """
        offset = self.get_offset(path, *coordinates)
        return len(offset) if offset else None

    def get_dynamic_size(self, path: str, *coordinates: int) -> int | None:
        return self.create_query(path, *coordinates).get_dynamic_size()

    def get_dimensionality(self, path: str) -> int | None:
        """Get the dimensionality of the node. It is the count of integer indexes to provide when using `query`.

        Args:
            path: Slash-separated path pointing to a node in the typesystem hierarchy.
                To see a list of available paths, use str_query().

        Returns:
            the dimensionality
        """
        return self.create_query(path).get_dimensionality()

    def create_query(self, path: str | None) -> IndexedDataBlockQuery:
        """Factory method to instantiate queries over the indexed datablock.

        Unless needed, use the `query` method directly.

        Args:
            path: Slash-separated path pointing to a node in the typesystem hierarchy.
                To see a list of available paths, use str_query().

        Returns:
            IndexedDataBlockQuery object
        """
        indexed_datablock = self._require_indexed_datablock()

        return create_query(indexed_datablock)[path]

    def _get_statically_decorated_tree_text_representation(self, /, **kwargs):
        return output_tree_to_txt(
            self.statically_decorated_tree,
            write_dynamic_attributes=False,
            write_path=False,
            **kwargs,
        )

    def _get_dynamically_decorated_tree_text_representation(self, path, /, **kwargs):
        self._require_indexed_datablock()
        node = self.get_typesystem_node(path)

        default_kwargs = {
            "write_dynamic_attributes": True,
            "write_path": True,
            "ignore_static_nodes": not node.static,
        }
        kwargs = {**default_kwargs, **kwargs}
        return output_tree_to_txt(
            node,
            **kwargs,
        )

    def _index_datablock(self):
        self.indexed_datablock = index_datablock(
            self.xsd_path, self.xml_schema_path, self.datablock_folder_path
        )

    def get_offset(self, path: str, *coordinates: int) -> list[int] | None:
        return self.create_query(path).get_dynamic_offset(*coordinates)

    def _require_indexed_datablock(self):
        if not self.indexed_datablock:
            raise SmosWalkerException(
                "No indexed_datablock available! Please set it before using this method via `set_datablock`"
            )
        return self.indexed_datablock


def index_datablock(
    xsd_path: str, xml_schema_path: str, datablock_folder_path: str
) -> IndexedDataBlock:
    """Computes an index for a given datablock, with the help of its schema definition.

    Args:
        xsd_path: Path pointing towards the XSD file, also known as "binx.xsd".
        xml_schema_path: Path pointing towards an XML schema file.
        datablock_folder_path: Path pointing towards the folder containing the data block.

    Returns:
        The resulting datablock-specific index.
    """
    decorated_tree: BaseNode = load_statically_decorated_tree(xsd_path, xml_schema_path)

    datablock: DataBlockType | None = read_dbl(datablock_folder_path)

    if datablock is None:
        raise SmosWalkerException("datablock is None")

    dynamically_decorate_tree(decorated_tree, datablock)

    return IndexedDataBlock(decorated_tree, datablock)


def create_query(indexed_datablock: IndexedDataBlock) -> IndexedDataBlockQuery:
    """Creates a query object for a given data block.

    Args:
        indexed_datablock: The indexed data block.

    Returns:
        The query object.
    """
    return IndexedDataBlockQuery(indexed_datablock)
