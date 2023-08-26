"""Useful high-level tools that are too specific to be part of the API's facade
"""

import json
import logging
from pathlib import Path
from typing import Callable, TypedDict

from typing import Any
from smos_walker.core.exception import SmosWalkerException
from smos_walker.core.node import ArrayVariableNode, BaseNode
from smos_walker.core.visitors import (
    DictExportNodeVisitor,
    ExistentialPredicateNodeVisitor,
    HumanReadableNodeVisitor,
)

from smos_walker.typesystem_static_decorator.facade import (
    load_statically_decorated_tree,
)
from smos_walker.util import dump_to_file


class ProblematicSchema(TypedDict):
    """Description of schema that cannot be successfully statically decorated"""

    path: str
    exception: str


DecoratedTreeConsumer = Callable[[BaseNode, Path], None | bool]


def dump_decoration_tree_consumer(decorated_tree: BaseNode, schema_path: Path):
    dump_to_file(
        output_tree_to_txt(decorated_tree),
        f"test_static_decorator_on_all_schemas/"
        f"{schema_path.parts[-4]}/{schema_path.parts[-3]}/{schema_path.parts[-2]}/{schema_path.stem}",
        "txt",
    )


def property_checker_tree_consumer(node: BaseNode, _):
    return node.accept(
        ExistentialPredicateNodeVisitor(
            lambda node: (
                isinstance(node, ArrayVariableNode)
                and node.dynamic_dimensionality is not None
                and (node.dynamic_dimensionality > 1)
            )
        )
    )


ConsumerResultsType = tuple[dict[str, Any], list[ProblematicSchema]]


def generate_human_readable_statically_decorated_schemas(
    schemas_base_path: Path,
) -> ConsumerResultsType:
    """Generates human-readable text files of statically decorated XML data schemas.

    Args:
        schemas_base_path: Home path containing all schemas as well as the XSD file.

    Returns:
        list: All files that did pose a problem during text generation (empty if full success)
    """
    logging.info("generate_human_readable_statically_decorated_schemas")

    return provide_statically_decorated_trees(
        schemas_base_path, [dump_decoration_tree_consumer]
    )


def provide_statically_decorated_trees(
    schemas_base_path: Path,
    consumers: list[DecoratedTreeConsumer],
    *,
    verbose: bool = True,
) -> ConsumerResultsType:
    """Provide statically decorated trees, by iterating over all binXschema files contained in the given folder.

    Args:
        schemas_base_path:  Home path containing all schemas as well as the XSD file.
        consumers: List of decorated tree consumers. The current path is also provided.
        verbose: Log progress

    Returns:
        list[ProblematicSchema]: _description_
    """

    if verbose:
        logging.info("provide_statically_decorated_trees")

    problematic_schemas: list[ProblematicSchema] = []

    results: dict[str, Any] = {consumer.__name__: {} for consumer in consumers}

    index = 0
    for index, schema_path in enumerate(schemas_base_path.glob("**/*.binXschema.xml")):

        try:
            decorated_tree: BaseNode = load_statically_decorated_tree(
                str(schemas_base_path / "binx/binx.xsd"), str(schema_path)
            )

            if verbose:
                logging.info(f"✅ [{index:04d}] {schema_path.name=}")

            for consumer in consumers:
                result = consumer(decorated_tree, schema_path)
                results[consumer.__name__][schema_path.stem] = result

        except SmosWalkerException as exception:
            if verbose:
                logging.info(
                    f"🟡 [{index:04d}] {schema_path.name=}. Exception caught: {exception}"
                )
            problematic_schemas.append(
                {"path": str(schema_path.stem), "exception": str(exception)}
            )

    if verbose:
        logging.info(
            (
                f"{index} schemas parsed. "
                f"Exceptions encountered with {len(problematic_schemas)} files: {problematic_schemas=}"
            )
        )

    return results, problematic_schemas


def output_tree_to_json(tree: BaseNode) -> str:
    """Outputs a tree to JSON

    Args:
        tree: Statically- or dynamically-decorated type system tree

    Returns:
        JSON-representation of the tree
    """
    dict_export_visitor = DictExportNodeVisitor()
    dictified_tree = tree.accept(dict_export_visitor)
    return json.dumps(dictified_tree, indent=2, sort_keys=True)


def output_tree_to_txt(tree: BaseNode, **kwargs) -> str:
    """Outputs a tree to TXT

    Args:
        tree: Statically- or dynamically-decorated type system tree

    Returns:
        TXT-representation of the tree
    """
    human_readable_visitor = HumanReadableNodeVisitor(**kwargs)
    tree.accept(human_readable_visitor)
    return str(human_readable_visitor)
