import numpy as np
from numpy import ma

from smos_walker.constants import (
    BooleanNumpyArrayType,
    DataBlockType,
    NumpifiedDataBlockType,
)
from smos_walker.core.exception import SmosWalkerException
from smos_walker.core.node import (
    ArrayFixedNode,
    ArrayVariableNode,
    LeafNode,
    StructNode,
)
from smos_walker.node_to_ndarray.node_to_ndarray import (
    node_to_type_info,
)


def node_to_ndarray_static(
    node: LeafNode | StructNode | ArrayFixedNode,
    datablock: DataBlockType,
) -> NumpifiedDataBlockType:
    """Numpy-typed view of a datablock's slice using a static node (Leaf, Struct, ArrayFixed)

    Args:
        node: Dynamically-decorated static node
        datablock: A datablock's slice

    Raises:
        SmosWalkerException: When the provided node is **not** static (guard)
        SmosWalkerException: When the provided datablock's size does not match the one described
            by the provided node (guard).

    Returns:
        A numpy-typed view of the datablock's slice
    """
    if not node.static:
        raise SmosWalkerException(
            "The node [" + node.name + "] is not static (node_to_ndarray_static)"
        )
    if node.block_byte_size != len(datablock):
        raise SmosWalkerException(
            f"The node's expected block byte size ({node.block_byte_size=}) does not match with the datablock's slice "
            f"({len(datablock)=}) (delta: {node.block_byte_size - len(datablock)=})"
        )

    type_info = node_to_type_info(node)
    return datablock.view(type_info["type"])


def node_to_ndarray_quasi_static(
    node: ArrayVariableNode,
    datablock: DataBlockType,
    dynamic_size: int,
) -> NumpifiedDataBlockType:
    """Numpy-typed view of a datablock's slice using a quasi-static array variable node

    Args:
        node: Dynamically-decorated node
        datablock: A datablock's slice
        dynamic_size: Dynamic-size of the array variable.
            Note that this has to be an `int`, not a recursive list of `int`, as it is the criteria for quasi-staticity.
            The caller is responsible to provide this scalar value.

    Raises:
        SmosWalkerException: When the provided node is **not** a quasi-static array variable (guard).
        SmosWalkerException: When the provided datablock's size does not match the one described by
            the provided node and provided `dynamic_size` (guard).

    Returns:
        A numpy-typed view of the datablock's slice
    """
    if not (isinstance(node, ArrayVariableNode) and node.quasi_static):
        raise SmosWalkerException("The node is not a quasi-static ArrayVariable.")

    if dynamic_size * node.child.block_byte_size != len(datablock):
        raise SmosWalkerException(
            "The node's child's expected block byte size times the dynamic size "
            "of the node does not match with the binary slice"
        )

    type_info = node_to_type_info(node)
    return datablock.view(type_info["type"])


def node_to_ndarray_static_one_dynamic_dimensional(
    node: LeafNode | StructNode | ArrayFixedNode, datablock: DataBlockType
) -> NumpifiedDataBlockType:
    """_summary_

    Args:
        node: Dynamically-decorated static node
        datablock: A datablock's slice

    Raises:
        SmosWalkerException: When the provided node is **not** static (guard)
        SmosWalkerException: When the provided node's `dynamic_dimensionality` is not 1.
        SmosWalkerException: When the provided datablock's detected contiguous bytes size does not match with
            the expected one described by the provided node (guard).

    Returns:
        A numpy-typed view of the datablock's slice
    """
    if not node.static:
        raise SmosWalkerException(
            "The node ["
            + node.name
            + "] is not static (node_to_ndarray_static_one_dynamic_dimensional)"
        )

    if not node.dynamic_dimensionality == 1:
        raise SmosWalkerException(
            "This method is adapted to numpify static nodes with dynamic_dimensionality = 1 "
            "(given dynamic_dimensionality = " + str(node.dynamic_dimensionality) + ")"
        )

    contiguous_bytes = datablock[
        (
            np.array(node.dynamic_offset).reshape(-1, 1)
            + np.arange(node.block_byte_size).reshape(1, -1)
        ).reshape(-1)
    ]

    if not (
        node.dynamic_coverage
        == len(node.dynamic_offset) * node.block_byte_size
        == len(contiguous_bytes)
    ):
        raise SmosWalkerException(
            f"The node's expected block byte size does not match with the binary slice "
            f"{len(node.dynamic_offset) * node.block_byte_size=}{node.dynamic_coverage=} "
            f"{node.block_byte_size=} {len(node.dynamic_offset)=} {len(contiguous_bytes)=}"
        )

    type_info = node_to_type_info(node)
    return contiguous_bytes.view(type_info["type"])


def node_to_ndarray_quasi_static_one_dynamic_dimensional(
    node: ArrayVariableNode,
    datablock: DataBlockType,
    *,
    mask_invalid_flag: bool = True,
) -> NumpifiedDataBlockType:
    if not (isinstance(node, ArrayVariableNode) and node.quasi_static):
        raise SmosWalkerException("The node is not a quasi-static ArrayVariable.")

    if not node.dynamic_dimensionality == 1:
        raise SmosWalkerException(
            "This method is adapted to numpify quasi-static ArrayVariable nodes with dynamic_dimensionality = 1 "
            + "(given dynamic_dimensionality = "
            + node.dynamic_dimensionality
            + ")"
        )

    # For an arrayvariable, the block byte size is carried by the child
    block_byte_size = node.child.block_byte_size

    # Do not forget the offset introduced by the "size_ref" header of array variables!
    size_ref_offset = node.size_ref.block_byte_size

    # Cardinality of the primary dimension
    size_x = len(node.dynamic_offset)

    # Get maximum cardinality of the secundary dimension for the arrayvariable.
    max_size_y = max(node.dynamic_size)

    index2d = (np.array(node.dynamic_offset) + size_ref_offset).reshape(
        -1, 1
    ) + np.arange(block_byte_size * max_size_y).reshape(1, -1)
    # Beware of Out of Bounds errors
    index1d = np.clip(index2d.reshape(-1), 0, datablock.size - 1)
    contiguous_bytes = datablock[index1d]

    if not size_x * max_size_y * block_byte_size == len(contiguous_bytes):
        raise SmosWalkerException(
            "The node's expected block byte size does not match with the binary slice"
        )

    type_info = node_to_type_info(node)
    ndarray = contiguous_bytes.view(type_info["type"])

    # Note that the first dimension is always valid, but the second will have excess invalid data.
    shape = (size_x, max_size_y)

    # This operation is suboptimized (numpy concatenation)
    if mask_invalid_flag:
        masks = mask_clips(node.dynamic_size)
        masked_array = ma.masked_array(ndarray, mask=masks)
        return masked_array.reshape(shape)
    return ndarray.reshape(shape)


def mask_clips(sizes: list[int]):
    max_size = max(sizes)
    masks_gen = (mask_clip(size, max_size) for size in sizes)
    masks = list(masks_gen)
    return np.concatenate(masks)


def mask_clip(tipping_point: int, size: int) -> BooleanNumpyArrayType:
    """Clip values superior to a given tipping_point.

    No check is performed to verify that tipping_point < size.

    Examples:
        >>> mask_values(5, 8)
        array([False, False, False, False, False,  True,  True,  True])

    Args:
        tipping_point: Before this index, values are not masked, after, they do.
        size: Size of desired mask

    Returns:
        the mask
    """
    mask = np.concatenate(
        (
            np.zeros(tipping_point, dtype=np.bool_),
            np.ones(size - tipping_point, dtype=np.bool_),
        )
    )
    return mask
