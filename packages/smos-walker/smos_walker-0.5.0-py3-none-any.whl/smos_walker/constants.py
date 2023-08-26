from typing import Any, Type, TypedDict
import numpy as np
import numpy.typing as npt


# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


class TagName:
    """Tag names used during the walk

    Note: camelCase is used for the sake of not having to juggle between 2 different naming conventions
    """

    binx = "binx"
    dataset = "dataset"
    useType = "useType"
    defineType = "defineType"
    struct = "struct"
    arrayFixed = "arrayFixed"
    arrayVariable = "arrayVariable"
    sizeRef = "sizeRef"
    dim = "dim"
    definitions = "definitions"


class PrimitiveTypeTagName:
    """Tag names that represent primitive types"""

    byte8 = "byte-8"
    short16 = "short-16"
    integer32 = "integer-32"
    long64 = "long-64"

    unsignedByte8 = "unsignedByte-8"
    unsignedShort16 = "unsignedShort-16"
    unsignedInteger32 = "unsignedInteger-32"
    unsignedLong64 = "unsignedLong-64"

    float32 = "float-32"
    double64 = "double-64"

    character8 = "character-8"
    unicode32 = "unicode-32"

    string = "string"


class PrimitiveTypeTagNameMappingKeyType(TypedDict):
    """Description of schema that cannot be successfully statically decorated"""

    byte_count: int
    np: Type[np.signedinteger] | Type[np.unsignedinteger] | Type[np.floating] | None


PrimitiveTypeTagNameMapping: dict[str, PrimitiveTypeTagNameMappingKeyType] = {
    PrimitiveTypeTagName.byte8: {"byte_count": 1, "np": np.int8},
    PrimitiveTypeTagName.short16: {"byte_count": 2, "np": np.int16},
    PrimitiveTypeTagName.integer32: {"byte_count": 4, "np": np.int32},
    PrimitiveTypeTagName.long64: {"byte_count": 8, "np": np.int64},
    PrimitiveTypeTagName.unsignedByte8: {"byte_count": 1, "np": np.uint8},
    PrimitiveTypeTagName.unsignedShort16: {"byte_count": 2, "np": np.uint16},
    PrimitiveTypeTagName.unsignedInteger32: {"byte_count": 4, "np": np.uint32},
    PrimitiveTypeTagName.unsignedLong64: {"byte_count": 8, "np": np.uint64},
    PrimitiveTypeTagName.float32: {"byte_count": 4, "np": np.float32},
    PrimitiveTypeTagName.double64: {"byte_count": 8, "np": np.float64},
    PrimitiveTypeTagName.character8: {"byte_count": 1, "np": np.uint8},
    PrimitiveTypeTagName.unicode32: {"byte_count": 4, "np": np.uint32},
    PrimitiveTypeTagName.string: {"byte_count": 4, "np": None},
}


class AttributeName:
    varName = "varName"
    typeName = "typeName"
    indexTo = "indexTo"
    name = "name"


class NodeProperty:
    name = "name"
    attributes = "attributes"
    children = "children"
    type = "type"


class CustomTagName:
    primitive = "primitive"


PathType = tuple[str, ...]
DataBlockType = npt.NDArray[np.uint8]

# Any is used since the dtype of the array depends on the schema and cannot be known in advance.
NumpifiedDataBlockType = npt.NDArray[Any]

BooleanNumpyArrayType = npt.NDArray[np.bool_]
