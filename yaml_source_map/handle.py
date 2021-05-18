"""Calculate the JSON source map for a value."""

import yaml

from . import types


def primitive(*, loader: yaml.Loader) -> types.TSourceMapEntries:
    """
    Calculate the source map of a primitive type.

    Args:
        loader: Source of YAML tokens.

    Returns:
        A list of JSON pointers and source map entries.

    """
    token = loader.get_token()
    assert isinstance(token, yaml.ScalarToken)

    return [
        (
            "",
            types.Entry(
                value_start=types.Location(
                    token.start_mark.line,
                    token.start_mark.column,
                    token.start_mark.index,
                ),
                value_end=types.Location(
                    token.end_mark.line,
                    token.end_mark.column,
                    token.end_mark.index,
                ),
            ),
        )
    ]
