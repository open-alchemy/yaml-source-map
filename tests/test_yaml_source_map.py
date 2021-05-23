"""Tests for JsonSourceMap."""

import pytest

from yaml_source_map import calculate, errors, types

CALCULATE_TESTS = [
    pytest.param(
        "0",
        {
            "": types.Entry(
                value_start=types.Location(0, 0, 0), value_end=types.Location(0, 1, 1)
            )
        },
        id="primitive",
    ),
    pytest.param(
        "[0]",
        {
            "": types.Entry(
                value_start=types.Location(0, 0, 0), value_end=types.Location(0, 3, 3)
            ),
            "/0": types.Entry(
                value_start=types.Location(0, 1, 1), value_end=types.Location(0, 2, 2)
            ),
        },
        id="array",
    ),
    pytest.param(
        "{key: 0}",
        {
            "": types.Entry(
                value_start=types.Location(0, 0, 0), value_end=types.Location(0, 8, 8)
            ),
            "/key": types.Entry(
                value_start=types.Location(0, 6, 6),
                value_end=types.Location(0, 7, 7),
                key_start=types.Location(0, 1, 1),
                key_end=types.Location(0, 4, 4),
            ),
        },
        id="object",
    ),
]


@pytest.mark.parametrize("source, expected_source_map", CALCULATE_TESTS)
def test_calculate(source, expected_source_map):
    """
    GIVEN source and expected source map
    WHEN calculate is called with the source
    THEN the source map is returned.
    """
    returned_source_map = calculate(source)

    assert returned_source_map == expected_source_map


CALCULATE_ERROR_TESTS = [
    pytest.param(True, id="not string"),
    pytest.param("", id="empty string"),
    pytest.param("invalid: yaml: value", id="invalid YAML"),
]


@pytest.mark.parametrize("source", CALCULATE_ERROR_TESTS)
def test_calculate_source_not_string(source):
    """
    GIVEN source
    WHEN calculate is called with the source
    THEN InvalidInputError is raised.
    """
    with pytest.raises(errors.InvalidInputError):
        calculate(source)
