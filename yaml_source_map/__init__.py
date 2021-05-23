"""Calculate the YAML source map."""

import yaml
from yaml import parser, scanner

from . import errors, handle, types


def calculate(source: str) -> types.TSourceMap:
    """
    Calculate the source map for a YAML document.

    Assume that the source is valid YAML.

    Args:
        source: The YAML document.

    Returns:
        The source map.

    """
    if not isinstance(source, str):
        raise errors.InvalidInputError(f"source must be a string, got {type(source)}")
    if not source:
        raise errors.InvalidInputError("source must not be empty")
    try:
        yaml.safe_load(source)
    except (scanner.ScannerError, parser.ParserError) as error:
        raise errors.InvalidInputError("YAML is not valid") from error

    loader = yaml.Loader(source)
    loader.get_token()
    return dict(handle.value(loader=loader))
