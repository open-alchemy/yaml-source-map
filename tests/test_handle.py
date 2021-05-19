"""Tests for functions that handle different types of values."""

import pytest
import yaml

from yaml_source_map.errors import InvalidYamlError
from yaml_source_map.handle import mapping, primitive, sequence, value
from yaml_source_map.types import Entry, Location

VALUE_TESTS = [
    pytest.param(
        "0",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 1, 1)))],
        id="primitive",
    ),
    pytest.param(
        "[]",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="sequence",
    ),
    pytest.param(
        "{}",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="mapping",
    ),
]


@pytest.mark.parametrize(
    "source, expected_entries",
    VALUE_TESTS,
)
def test_value(source, expected_entries):
    """
    GIVEN source and expected entries
    WHEN loader is created and value is called with the loader
    THEN the expected entries are returned.
    """
    loader = yaml.Loader(source)
    loader.get_token()

    returned_entries = value(loader=loader)

    assert returned_entries == expected_entries


MAPPING_TESTS = [
    pytest.param(
        "{}",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="empty",
    ),
    pytest.param(
        " {}",
        [("", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 3, 3)))],
        id="empty whitespace before",
    ),
    pytest.param(
        "{ }",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3)))],
        id="empty whitespace between",
    ),
    pytest.param(
        "{} ",
        [("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 2, 2)))],
        id="empty whitespace after",
    ),
    pytest.param(
        "{key: 0}",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 8, 8))),
            (
                "/key",
                Entry(
                    value_start=Location(0, 6, 6),
                    value_end=Location(0, 7, 7),
                    key_start=Location(0, 1, 1),
                    key_end=Location(0, 4, 4),
                ),
            ),
        ],
        id="single primitive",
    ),
    pytest.param(
        "{ key: 0}",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 9, 9))),
            (
                "/key",
                Entry(
                    value_start=Location(0, 7, 7),
                    value_end=Location(0, 8, 8),
                    key_start=Location(0, 2, 2),
                    key_end=Location(0, 5, 5),
                ),
            ),
        ],
        id="single primitive whitespace before",
    ),
    pytest.param(
        "{key : 0}",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 9, 9))),
            (
                "/key",
                Entry(
                    value_start=Location(0, 7, 7),
                    value_end=Location(0, 8, 8),
                    key_start=Location(0, 1, 1),
                    key_end=Location(0, 4, 4),
                ),
            ),
        ],
        id="single primitive whitespace after key",
    ),
    pytest.param(
        "{key: 0}",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 8, 8))),
            (
                "/key",
                Entry(
                    value_start=Location(0, 6, 6),
                    value_end=Location(0, 7, 7),
                    key_start=Location(0, 1, 1),
                    key_end=Location(0, 4, 4),
                ),
            ),
        ],
        id="single primitive whitespace before value",
    ),
    pytest.param(
        "{key: 0 }",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 9, 9))),
            (
                "/key",
                Entry(
                    value_start=Location(0, 6, 6),
                    value_end=Location(0, 7, 7),
                    key_start=Location(0, 1, 1),
                    key_end=Location(0, 4, 4),
                ),
            ),
        ],
        id="single primitive whitespace after value",
    ),
    pytest.param(
        "{key_1: 0,key_2: 0}",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 19, 19))),
            (
                "/key_1",
                Entry(
                    value_start=Location(0, 8, 8),
                    value_end=Location(0, 9, 9),
                    key_start=Location(0, 1, 1),
                    key_end=Location(0, 6, 6),
                ),
            ),
            (
                "/key_2",
                Entry(
                    value_start=Location(0, 17, 17),
                    value_end=Location(0, 18, 18),
                    key_start=Location(0, 10, 10),
                    key_end=Location(0, 15, 15),
                ),
            ),
        ],
        id="multi primitive",
    ),
    pytest.param(
        "{key_1: 0,key_2: 0,key_3: 0}",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 28, 28))),
            (
                "/key_1",
                Entry(
                    value_start=Location(0, 8, 8),
                    value_end=Location(0, 9, 9),
                    key_start=Location(0, 1, 1),
                    key_end=Location(0, 6, 6),
                ),
            ),
            (
                "/key_2",
                Entry(
                    value_start=Location(0, 17, 17),
                    value_end=Location(0, 18, 18),
                    key_start=Location(0, 10, 10),
                    key_end=Location(0, 15, 15),
                ),
            ),
            (
                "/key_3",
                Entry(
                    value_start=Location(0, 26, 26),
                    value_end=Location(0, 27, 27),
                    key_start=Location(0, 19, 19),
                    key_end=Location(0, 24, 24),
                ),
            ),
        ],
        id="many primitive",
    ),
    pytest.param(
        "key: 0",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 6, 6))),
            (
                "/key",
                Entry(
                    value_start=Location(0, 5, 5),
                    value_end=Location(0, 6, 6),
                    key_start=Location(0, 0, 0),
                    key_end=Location(0, 3, 3),
                ),
            ),
        ],
        id="single primitive no curly brackets",
    ),
    pytest.param(
        """key_1: 0
key_2: 0""",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(1, 8, 17))),
            (
                "/key_1",
                Entry(
                    value_start=Location(0, 7, 7),
                    value_end=Location(0, 8, 8),
                    key_start=Location(0, 0, 0),
                    key_end=Location(0, 5, 5),
                ),
            ),
            (
                "/key_2",
                Entry(
                    value_start=Location(1, 7, 16),
                    value_end=Location(1, 8, 17),
                    key_start=Location(1, 0, 9),
                    key_end=Location(1, 5, 14),
                ),
            ),
        ],
        id="multi primitive no curly brackets",
    ),
    pytest.param(
        """key_1: 0
key_2: 0
key_3: 0""",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(2, 8, 26))),
            (
                "/key_1",
                Entry(
                    value_start=Location(0, 7, 7),
                    value_end=Location(0, 8, 8),
                    key_start=Location(0, 0, 0),
                    key_end=Location(0, 5, 5),
                ),
            ),
            (
                "/key_2",
                Entry(
                    value_start=Location(1, 7, 16),
                    value_end=Location(1, 8, 17),
                    key_start=Location(1, 0, 9),
                    key_end=Location(1, 5, 14),
                ),
            ),
            (
                "/key_3",
                Entry(
                    value_start=Location(2, 7, 25),
                    value_end=Location(2, 8, 26),
                    key_start=Location(2, 0, 18),
                    key_end=Location(2, 5, 23),
                ),
            ),
        ],
        id="multi primitive no curly brackets",
    ),
]


@pytest.mark.parametrize(
    "source, expected_entries",
    MAPPING_TESTS,
)
def test_mapping(source, expected_entries):
    """
    GIVEN source and expected entries
    WHEN loader is created and mapping is called with the loader
    THEN the expected entries are returned.
    """
    loader = yaml.Loader(source)
    loader.get_token()

    returned_entries = mapping(loader=loader)

    assert returned_entries == expected_entries


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
    pytest.param(
        "[0]",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3))),
            ("/0", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 2, 2))),
        ],
        id="single primitive",
    ),
    pytest.param(
        "- 0",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 3, 3))),
            ("/0", Entry(value_start=Location(0, 2, 2), value_end=Location(0, 3, 3))),
        ],
        id="single primitive - syntax",
    ),
    pytest.param(
        """- 0
- 0""",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(1, 3, 7))),
            ("/0", Entry(value_start=Location(0, 2, 2), value_end=Location(0, 3, 3))),
            ("/1", Entry(value_start=Location(1, 2, 6), value_end=Location(1, 3, 7))),
        ],
        id="multi primitive - syntax",
    ),
    pytest.param(
        """- 0
- 0
- 0""",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(2, 3, 11))),
            ("/0", Entry(value_start=Location(0, 2, 2), value_end=Location(0, 3, 3))),
            ("/1", Entry(value_start=Location(1, 2, 6), value_end=Location(1, 3, 7))),
            ("/2", Entry(value_start=Location(2, 2, 10), value_end=Location(2, 3, 11))),
        ],
        id="many primitive - syntax",
    ),
    pytest.param(
        "[[0]]",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 5, 5))),
            ("/0", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 4, 4))),
            ("/0/0", Entry(value_start=Location(0, 2, 2), value_end=Location(0, 3, 3))),
        ],
        id="single primitive nested",
    ),
    pytest.param(
        "- - 0",
        [
            ("", Entry(value_start=Location(0, 0, 0), value_end=Location(0, 5, 5))),
            ("/0", Entry(value_start=Location(0, 2, 2), value_end=Location(0, 5, 5))),
            ("/0/0", Entry(value_start=Location(0, 4, 4), value_end=Location(0, 5, 5))),
        ],
        id="single primitive nested - syntax",
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


SEQUENCE_ERROR_TESTS = [
    pytest.param("", id="not sequence"),
    pytest.param("[", id="no closing bracket"),
]


@pytest.mark.parametrize(
    "source",
    SEQUENCE_ERROR_TESTS,
)
def test_sequence_error(source):
    """
    GIVEN source
    WHEN loader is created and sequence is called with the loader
    THEN InvalidYamlError is raised.
    """
    loader = yaml.Loader(source)
    loader.get_token()

    with pytest.raises(InvalidYamlError):
        sequence(loader=loader)


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
        " 0",
        [("", Entry(value_start=Location(0, 1, 1), value_end=Location(0, 2, 2)))],
        id="start whitespace",
    ),
    pytest.param(
        "0 ",
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
