"""smos_walker module

This package exposes the following functions from the `api.facade` module:

- `index_datablock` - Index a _datablock_ (DBL) according to its schema.
- `create_query` - Query object over an indexed _datablock_.

"""
__version__ = "0.5.0"

from smos_walker.api.facade import index_datablock, create_query, SmosWalker

from smos_walker.xml_reader.facade import extract_tag_content_from_earthexplorer_hdr
