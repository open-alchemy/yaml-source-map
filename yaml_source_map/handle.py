"""Calculate the JSON source map for a value."""

import yaml

from yaml_source_map import errors

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
    if isinstance(
        loader.peek_token(), (yaml.FlowSequenceStartToken, yaml.BlockSequenceStartToken)
    ):
        return sequence(loader=loader)
    if isinstance(
        loader.peek_token(), (yaml.FlowMappingStartToken, yaml.BlockMappingStartToken)
    ):
        return mapping(loader=loader)
    return primitive(loader=loader)


def mapping(*, loader: yaml.Loader) -> types.TSourceMapEntries:
    """
    Calculate the source map of a mapping value.

    Args:
        loader: Source of YAML tokens.

    Returns:
        A list of JSON pointers and source map entries.

    """
    # Look for mapping start
    token = loader.get_token()
    if not isinstance(token, (yaml.FlowMappingStartToken, yaml.BlockMappingStartToken)):
        raise errors.InvalidYamlError(f"expected mapping start but received {token=}")
    value_start = types.Location(
        token.start_mark.line, token.start_mark.column, token.start_mark.index
    )

    # Handle values
    entries: types.TSourceMapEntries = []
    while not isinstance(
        loader.peek_token(),
        (
            yaml.FlowMappingEndToken,
            yaml.BlockEndToken,
            yaml.DocumentEndToken,
            yaml.StreamEndToken,
        ),
    ):
        # Retrieve key
        key_token = loader.get_token()
        if not isinstance(key_token, yaml.KeyToken):
            raise errors.InvalidYamlError(f"expected key but received {key_token=}")
        key_value_token = loader.get_token()
        assert isinstance(key_value_token, yaml.ScalarToken)
        key_start = types.Location(
            key_value_token.start_mark.line,
            key_value_token.start_mark.column,
            key_value_token.start_mark.index,
        )
        key_end = types.Location(
            key_value_token.end_mark.line,
            key_value_token.end_mark.column,
            key_value_token.end_mark.index,
        )
        key_value = key_value_token.value

        # Retrieve values
        assert isinstance(loader.get_token(), yaml.ValueToken)
        value_entries = iter(value(loader=loader))
        value_entry = next(value_entries)

        # Write pointers
        entries.append(
            (
                f"/{key_value}",
                types.Entry(
                    value_start=value_entry[1].value_start,
                    value_end=value_entry[1].value_end,
                    key_start=key_start,
                    key_end=key_end,
                ),
            )
        )
        entries.extend(
            (f"/{key_value}{pointer}", entry) for pointer, entry in value_entries
        )

        # Skip flow entry
        if isinstance(loader.peek_token(), (yaml.FlowEntryToken)):
            loader.get_token()

    # Look for mapping end
    token = loader.get_token()
    if not isinstance(token, (yaml.FlowMappingEndToken, yaml.BlockEndToken)):
        raise errors.InvalidYamlError(f"expected mapping end but received {token=}")
    value_end = types.Location(
        token.end_mark.line, token.end_mark.column, token.end_mark.index
    )

    return [("", types.Entry(value_start=value_start, value_end=value_end))] + entries


def sequence(*, loader: yaml.Loader) -> types.TSourceMapEntries:
    """
    Calculate the source map of a sequence value.

    Args:
        loader: Source of YAML tokens.

    Returns:
        A list of JSON pointers and source map entries.

    """
    # Look for sequence start
    token = loader.get_token()
    if not isinstance(
        token, (yaml.FlowSequenceStartToken, yaml.BlockSequenceStartToken)
    ):
        raise errors.InvalidYamlError(f"expected sequence start but received {token=}")
    value_start = types.Location(
        token.start_mark.line, token.start_mark.column, token.start_mark.index
    )

    # Handle values
    sequence_index = 0
    entries: types.TSourceMapEntries = []
    while not isinstance(
        loader.peek_token(),
        (
            yaml.FlowSequenceEndToken,
            yaml.BlockEndToken,
            yaml.DocumentEndToken,
            yaml.StreamEndToken,
        ),
    ):
        # Skip block entry
        if isinstance(loader.peek_token(), yaml.BlockEntryToken):
            loader.get_token()

        # Retrieve values
        value_entries = value(loader=loader)
        entries.extend(
            (f"/{sequence_index}{pointer}", entry) for pointer, entry in value_entries
        )
        sequence_index += 1

        # Skip flow entry
        if isinstance(loader.peek_token(), (yaml.FlowEntryToken)):
            loader.get_token()

    # Look for sequence end
    token = loader.get_token()
    if not isinstance(token, (yaml.FlowSequenceEndToken, yaml.BlockEndToken)):
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
