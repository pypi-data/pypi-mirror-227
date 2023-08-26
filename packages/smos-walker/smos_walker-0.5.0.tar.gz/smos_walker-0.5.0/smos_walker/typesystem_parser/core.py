from typing import TypedDict, Union
from typing_extensions import NotRequired
from smos_walker.config import SmosWalkerConfig
from smos_walker.constants import (
    AttributeName,
    NodeProperty,
    PrimitiveTypeTagNameMapping,
    TagName,
)
from smos_walker.core.exception import SmosWalkerException
from smos_walker.xml_reader.node_wrapper import (
    get_attributes,
    get_children,
    get_first_child,
    get_last_child,
    get_name,
)


class RawNode(TypedDict):
    """A raw node resulting from the XML parsing."""

    name: str
    type: NotRequired[Union[str, "RawNode"]]
    attributes: NotRequired[dict[str, str]]
    varName: NotRequired[str]


# -- Mypy does not handle case _
def render_typesystem_parsed_tree(data, node) -> RawNode:  # type: ignore[return]
    """Get an intermediate enhanced view over the type system described in the XML Schema

    The role of this function is to exploit the raw XML schema data and convert it to
    a friendlier data-structure, as well as unfolding the type references. The raw flat
    representation of the type system is converted to a treelike developed structure.

    Args:
        data (_type_): Root Node of the Raw representation of the XML schema
        node (_type_): Current Node of the raw representation of the XML Schema

    Returns:
        _type_: _description_
    """
    node_name = get_name(node)

    match node_name:
        case TagName.binx:
            # Only keep the <dataset>, not the <definitions>
            return render_typesystem_parsed_tree(
                data, get_last_child(node)
            )  # Empirically, the <dataset> tag is the last child of <binx>

        case TagName.useType:
            return render_use_type_node(data, node)

        # Skip details for primitive type nodes
        case node_name if node_name in PrimitiveTypeTagNameMapping:
            return render_leaf_node(data, node)

        case _:
            return render_default(data, node)


def explore_type(data, type_name: str) -> RawNode:
    node = lookup_define_type_node(data, type_name)
    return render_typesystem_parsed_tree(data, node)


def render_default(data, node):
    children = render_children(data, node)
    if children:
        return {
            NodeProperty.name: get_name(node),
            NodeProperty.attributes: get_attributes(node),
            NodeProperty.children: children,
        }
    return {
        NodeProperty.name: get_name(node),
        NodeProperty.attributes: get_attributes(node),
    }


def render_children(data, node: RawNode) -> list[RawNode] | None:
    children = get_children(node)

    if children:
        return [render_typesystem_parsed_tree(data, child) for child in children]
    return None


def render_leaf_node(data, node: RawNode):
    if SmosWalkerConfig.LEVEL_OF_DETAILS == 0:
        return get_attributes(node)[AttributeName.varName]

    if SmosWalkerConfig.LEVEL_OF_DETAILS == 1:
        return {
            NodeProperty.name: get_name(node),
            AttributeName.varName: get_attributes(node)[AttributeName.varName],
        }

    if SmosWalkerConfig.LEVEL_OF_DETAILS == 2:
        return {
            NodeProperty.name: "primitive",
            NodeProperty.type: get_name(node),
            AttributeName.varName: get_attributes(node)[AttributeName.varName]
            if AttributeName.varName in get_attributes(node)
            else None,
        }

    if SmosWalkerConfig.LEVEL_OF_DETAILS > 99:
        return render_default(data, node)

    return None


def render_use_type_node(data, node):
    return {
        NodeProperty.name: get_name(node),
        NodeProperty.attributes: get_attributes(node),
        NodeProperty.type: explore_type(
            data, get_attributes(node)[AttributeName.typeName]
        ),
    }


def lookup_define_type_node(data, type_name: str):
    # Returns a <defineType> node (useful to jump to type definitions)
    assert TagName.definitions == get_name(get_first_child(data))
    search_result = list(
        x for x in data[2][1:] if x[1][AttributeName.typeName] == type_name
    )
    if len(search_result) == 0:
        raise SmosWalkerException(f"No type node found for given {type_name=}")
    if len(search_result) > 1:
        raise SmosWalkerException(
            f"Multiple type nodes found for given {type_name=}: count={len(search_result)}"
        )
    return search_result[0]
