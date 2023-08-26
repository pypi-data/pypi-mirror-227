from smos_walker.constants import AttributeName, CustomTagName, NodeProperty, TagName
from smos_walker.core.node import (
    ArrayFixedNode,
    ArrayVariableNode,
    BaseNode,
    LeafNode,
    StructNode,
)
from smos_walker.typesystem_parser.node_wrapper import (
    get_attribute,
    get_children,
    get_first_child,
    get_name,
    select_child,
)


# Source: Product from the typesystem_parser node: type_parsed_xml_tree
def statically_decorate_tree(node) -> BaseNode | list[BaseNode]:
    match get_name(node):
        case TagName.sizeRef:
            return statically_decorate_tree(get_first_child(node))
        case TagName.dataset:
            return statically_decorate_tree(get_first_child(node))
        case CustomTagName.primitive:  # Days: integer-32
            return LeafNode(node[AttributeName.varName], node[NodeProperty.type])
        case TagName.useType:
            if AttributeName.varName in node[NodeProperty.attributes]:
                var_name = get_attribute(node, AttributeName.varName)
            else:
                var_name = ""  # is empty for type used in arrays (variable and fixed)
            type_name = get_attribute(node, AttributeName.typeName)
            type_node = node[NodeProperty.type]
            struct_node = statically_decorate_tree(type_node)
            children = struct_node[0]

            # Artificial struct node wrapper, as some type have arrays as direct children.
            return StructNode(var_name, type_name, children)
        case TagName.arrayFixed:  # Max_Valid[2] or List_of_OTT_Data[pol=8][model=3]
            dim_node = select_child(node, TagName.dim)
            name = get_attribute(node, AttributeName.varName)
            dimensions = extract_dimensions_from_dim_node(dim_node)

            struct_node = select_child(node, TagName.useType)
            if struct_node:
                child = statically_decorate_tree(struct_node)
            else:
                # Hoping the data type is always the first child!
                child = statically_decorate_tree(get_first_child(node))

            return ArrayFixedNode(
                name,
                dimensions,
                child,
            )
        case TagName.arrayVariable:
            size_ref_node = statically_decorate_tree(
                select_child(node, TagName.sizeRef)
            )
            name = get_attribute(node, AttributeName.varName)
            child = statically_decorate_tree(select_child(node, TagName.useType))
            return ArrayVariableNode(name, child, size_ref_node)
        case _:
            return convert_children(node)


def extract_dimensions_from_dim_node(dim_node):
    if get_children(dim_node):
        children_dimensions = extract_dimensions_from_dim_node(
            get_first_child(dim_node)
        )
    else:
        children_dimensions = []

    name = get_attribute(dim_node, AttributeName.name)
    # +1 because the actual data format is an end index
    size = int(get_attribute(dim_node, AttributeName.indexTo)) + 1

    # Dimensions can be anonymous
    current_dimension = {"name": name, "size": size}

    # Order is deepest last
    return [current_dimension, *children_dimensions]


def convert_children(node) -> list[BaseNode]:
    children = get_children(node)

    if not children:
        return None

    children_lines = (statically_decorate_tree(child) for child in children)
    pruned = [c for c in children_lines if c is not None]

    return pruned if pruned else None
