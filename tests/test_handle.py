"""Tests for functions that handle different types of values."""

import pytest
import yaml

from yaml_source_map.types import Location, Entry
from yaml_source_map.handle import primitive, sequence
from yaml_source_map.errors import InvalidYamlError


SEQUENCE_TESTS = [
    pytest.param(
        "[]",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="empty",
    ),
    pytest.param(
        " []",
        [("", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 3, 3)))],
        id="empty whitespace before",
    ),
    pytest.param(
        "[ ]",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3)))],
        id="empty whitespace between",
    ),
    pytest.param(
        "[] ",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="empty whitespace after",
    ),
    pytest.param(
        "[0]",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3))),
            ("/0", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 2, 2))),
        ],
        id="single primitive",
    ),
    pytest.param(
        "[ 0]",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 4, 4))),
            ("/0", Entry(value_start=Location(0, 2, 2), value_end=Location(0, 3, 3))),
        ],
        id="single primitive whitespace before",
    ),
    pytest.param(
        "[0 ]",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 4, 4))),
            ("/0", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 2, 2))),
        ],
        id="single primitive whitespace after",
    ),
    pytest.param(
        "[0,0]",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 5, 5))),
            ("/0", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 2, 2))),
            ("/1", Entry(value_start=Location(0, 3, 3), value_end=Location(0, 4, 4))),
        ],
        id="multi primitive",
    ),
    pytest.param(
        "[0,0,0]",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 7, 7))),
            ("/0", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 2, 2))),
            ("/1", Entry(value_start=Location(0, 3, 3), value_end=Location(0, 4, 4))),
            ("/2", Entry(value_start=Location(0, 5, 5), value_end=Location(0, 6, 6))),
        ],
        id="many primitive",
    ),
]


@pytest.mark.parametrize(
    "source, expected_entries",
    SEQUENCE_TESTS,
)
def test_sequence(source, expected_entries):
    """
    GIVEN source and expected entries
    WHEN loader is created and sequence is called with the loader
    THEN the expected entries are returned.
    """
    loader = yaml.Loader(source)
    loader.get_token()

    returned_entries = sequence(loader=loader)

    assert returned_entries == expected_entries


PRIMITIVE_TESTS = [
    pytest.param(
        "0",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 1, 1)))],
        id="number primitive",
    ),
    pytest.param(
        "-0",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="negative number primitive",
    ),
    pytest.param(
        "+0",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="positive number primitive",
    ),
    pytest.param(
        "0.0",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3)))],
        id="decimal number primitive",
    ),
    pytest.param(
        "0e0",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3)))],
        id="exponential number primitive",
    ),
    pytest.param(
        "0E0",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3)))],
        id="capital exponential number primitive",
    ),
    pytest.param(
        "00",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="multi character number primitive",
    ),
    pytest.param(
        "000",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3)))],
        id="many character number primitive",
    ),
    pytest.param(
        f" 0",
        [("", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 2, 2)))],
        id="start whitespace",
    ),
    pytest.param(
        f"0 ",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 1, 1)))],
        id="end whitespace",
    ),
    pytest.param(
        "true",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 4, 4)))],
        id="true primitive",
    ),
    pytest.param(
        "false",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 5, 5)))],
        id="false primitive",
    ),
    pytest.param(
        "null",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 4, 4)))],
        id="null primitive",
    ),
    pytest.param(
        '""',
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="empty string primitive",
    ),
    pytest.param(
        '"a"',
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3)))],
        id="single character string primitive",
    ),
    pytest.param(
        "a",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 1, 1)))],
        id="no quote string primitive",
    ),
    pytest.param(
        '"aa"',
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 4, 4)))],
        id="multi character string primitive",
    ),
    pytest.param(
        '"aaa"',
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 5, 5)))],
        id="many character string primitive",
    ),
]


@pytest.mark.parametrize(
    "source, expected_entries",
    PRIMITIVE_TESTS,
)
def test_primitive(source, expected_entries):
    """
    GIVEN source and expected entries
    WHEN loader is created and primitive is called with the loader
    THEN the expected entries are returned.
    """
    loader = yaml.Loader(source)
    loader.get_token()

    returned_entries = primitive(loader=loader)

    assert returned_entries == expected_entries


PRIMITIVE_ERROR_TESTS = [pytest.param("", id="not primitive")]


@pytest.mark.parametrize(
    "source",
    PRIMITIVE_ERROR_TESTS,
)
def test_primitive_error(source):
    """
    GIVEN source
    WHEN loader is created and primitive is called with the loader
    THEN InvalidYamlError is raised.
    """
    loader = yaml.Loader(source)
    loader.get_token()

    with pytest.raises(InvalidYamlError):
        primitive(loader=loader)
