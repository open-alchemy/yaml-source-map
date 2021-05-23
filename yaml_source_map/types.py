"""Types for calculating the YAML source map."""

import dataclasses
import typing


class TLocationDict(
    typing.TypedDict
):  # pylint: disable=inherit-non-class,too-few-public-methods
    """The location of a source map entry."""

    line: int
    column: int
    pos: int


@dataclasses.dataclass
class Location:
    """
    The location of a source map entry.

    Attrs:
        line: The number of new line characters before the location in the source.
        column: The number of characters before the location in the source since the
            last new line character.
        position: The number of characters before the location in the source.

    """

    line: int
    column: int
    position: int


class TEntryDictBase(
    typing.TypedDict
):  # pylint: disable=inherit-non-class,too-few-public-methods
    """The base for start and end location dictionary for a value in the source."""

    value: TLocationDict
    valueEnd: TLocationDict


class TEntryDict(TEntryDictBase, total=False):  # pylint: disable=too-few-public-methods
    """The start and end location for a value dictionary in the source."""

    key: TLocationDict
    keyEnd: TLocationDict


@dataclasses.dataclass
class Entry:
    """
    The start and end location for a value in the source.

    Attrs:
        value_start: The start location of the value.
        value_end: The end location of the value.
        key_start: The start location of the key included if the item is directly within
            an object.
        key_end: The end location of the key included if the item is directly within an
            object.

    """

    value_start: Location
    value_end: Location
    key_start: typing.Optional[Location] = None
    key_end: typing.Optional[Location] = None


TSourceMapEntries = typing.List[typing.Tuple[str, Entry]]
TSourceMap = typing.Dict[str, Entry]
