# ------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------


from typing import Literal


class SmosWalkerConfig:
    # Additional output, set to False if the goal is to redirect the output of the script to a file
    VERBOSE: bool = False

    # For leaf node, show full node or simplified representation
    LEVEL_OF_DETAILS: Literal[0] | Literal[1] | Literal[2] = 2

    # StructNodes can be anonymous. This is a placeholder name use to build a tree's path when it happens.
    ANONYMOUS_STRUCT_IDENTIFIER: str = "<anonymous_struct>"


class SmosWalkerFeatureFlag:
    # Load double-nested Arrays Variable as masked numpy arrays for invalid values. Can produce masked arrays.
    NUMPIFY_DYNAMIC_1D_ARRAY_VARIABLE: bool = False

    # Numpify Arrays Fixed containing Arrays Variable, when possible. Can produce masked arrays.
    NUMPIFY_DYNAMIC_1D_ARRAY_FIXED: bool = True

    # Not implemented for multidimensional Arrays Fixed.
    NUMPIFY_DYNAMIC_ND_ARRAY_FIXED: bool = False

    # For 1-dynamic-dimensional nodes, return a pre-built generator for the user
    GENERATOR_DYNAMIC_1D: bool = True
