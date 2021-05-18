"""Errors for calculating the YAML source map."""


class BaseError(Exception):
    """Base class for all errors."""


class InvalidYamlError(BaseError):
    """Raised when YAML is invalid."""


class InvalidInputError(BaseError):
    """Raised when input is not a string."""
