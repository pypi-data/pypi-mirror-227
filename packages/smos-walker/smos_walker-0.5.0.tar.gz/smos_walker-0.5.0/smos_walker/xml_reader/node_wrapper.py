# ------------------------------------------------------------------------
# Utilities to access node (represented by lists)
# ------------------------------------------------------------------------


def get_name(node):
    return node[0]


def get_attributes(node):
    if len(node) < 2 or not isinstance(node[1], dict):
        return None
    return node[1]


def get_children(node):
    if get_attributes(node):
        return node[2:]  # eg [tagName, {attr1: value1}, child_1, ..., child_n]
    return node[1:]  # eg [tagName, child_1, ..., child_n]


def get_first_child(node):
    return get_children(node)[0]


def get_last_child(node):
    return get_children(node)[-1]
