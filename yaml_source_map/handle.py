"""Calculate the JSON source map for a value."""

from yaml_source_map import errors
import yaml

from . import types


def value(*, loader: yaml.Loader) -> types.TSourceMapEntries:
    """
    Calculate the source map of any value.

    Args:
        source: The JSON document.
        current_location: The current location in the source.

    Returns:
        A list of JSON pointers and source map entries.

    """
    if isinstance(loader.peek_token(), yaml.FlowSequenceStartToken):
        return sequence(loader=loader)
    return primitive(loader=loader)


def sequence(*, loader: yaml.Loader) -> types.TSourceMapEntries:
    """
    Calculate the source map of an array value.

    Args:
        loader: Source of YAML tokens.

    Returns:
        A list of JSON pointers and source map entries.

    """
    # Look for sequence start
    token = loader.get_token()
    if not isinstance(token, yaml.FlowSequenceStartToken):
        raise errors.InvalidYamlError(f"expected sequence start but received {token=}")
    value_start = types.Location(
        token.start_mark.line, token.start_mark.column, token.start_mark.index
    )

    # Handle values
    sequence_index = 0
    entries: types.TSourceMapEntries = []
    while not isinstance(loader.peek_token(), yaml.FlowSequenceEndToken):
        value_entries = value(loader=loader)
        entries.extend(
            (f"/{sequence_index}{pointer}", entry) for pointer, entry in value_entries
        )
        sequence_index += 1

        if isinstance(loader.peek_token(), yaml.FlowEntryToken):
            loader.get_token()

    # Look for sequence end
    token = loader.get_token()
    if not isinstance(token, yaml.FlowSequenceEndToken):
        raise errors.InvalidYamlError(f"expected sequence end but received {token=}")
    value_end = types.Location(
        token.end_mark.line, token.end_mark.column, token.end_mark.index
    )

    return [("", types.Entry(value_start=value_start, value_end=value_end))] + entries


def primitive(*, loader: yaml.Loader) -> types.TSourceMapEntries:
    """
    Calculate the source map of a primitive type.

    Args:
        loader: Source of YAML tokens.

    Returns:
        A list of JSON pointers and source map entries.

    """
    token = loader.get_token()
    if not isinstance(token, yaml.ScalarToken):
        raise errors.InvalidYamlError(f"expected scalar but received {token=}")

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
