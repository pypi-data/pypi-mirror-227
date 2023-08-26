# ------------------------------------------------------------------------
# Utilities to access node (intermediate dict-like data structure)
# ------------------------------------------------------------------------


import warnings
from smos_walker.constants import AttributeName, NodeProperty, TagName


def get_name(node):
    return _property_or_none(node, NodeProperty.name)


def get_type(node):
    return _property_or_none(node, NodeProperty.type)


def get_attributes(node):
    return _property_or_none(node, NodeProperty.attributes)


def get_children(node):
    return _property_or_none(node, NodeProperty.children)


def get_attribute(node, attribute_name: str):
    attributes = get_attributes(node)
    return _property_or_none(attributes, attribute_name)


def get_first_child(node):
    return get_children(node)[0]


def get_last_child(node):
    return get_children(node)[-1]


def select_child(node, _property):
    children = get_children(node)
    if not children:
        return None
    selected = list(child for child in children if get_name(child) == _property)
    return selected[0] if len(selected) == 1 else None


def has_children(node):
    return NodeProperty.children in node


def is_leaf(node):
    warnings.warn(
        "Uses the presence of varName in the node to determine in leaf, used in old code",
        DeprecationWarning,
        stacklevel=2,
    )
    return AttributeName.varName in node


def is_array_fixed(node):
    return get_name(node) == TagName.arrayFixed


def is_array_variable(node):
    return get_name(node) == TagName.arrayVariable


def is_type_node(node):
    return _has_property(NodeProperty.type, node)


def _property_or_none(node, _property):
    return (
        node[_property]
        if (node is not None and _has_property(node, _property))
        else None
    )


def _has_property(node, _property):
    return _property in node
