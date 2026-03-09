import os
import sys
from enum import Enum


class Environment(Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEV = "dev"
    BUILD = "build"
    TESTING = "testing"

    def __str__(self):
        return self.value

    def display_name(self):
        if self == self.PRODUCTION:
            return ""
        if self == self.STAGING:
            return "TEST"
        return str(self).upper()

    @property
    def deployed(self) -> bool:
        return self in {self.PRODUCTION, self.STAGING}


def mod(pkg: str, modules: list[str]) -> list[str]:
    return [".".join([t for t in [pkg, module] if t]) for module in modules]


def is_testing():
    return "test" in sys.argv or "PYTEST_VERSION" in os.environ


def get_environment(config, debug: bool) -> Environment:
    if is_testing():
        return Environment.TESTING
    if debug:
        return Environment.DEV
    return Environment(config("ENVIRONMENT", "production"))


def get_beercss_dir(static_dir) -> str:
    """
    Get the BeerCSS directory name in the form `beercss-x.y.z`
    """
    try:
        return list(static_dir.glob("beercss-*"))[-1].name
    except IndexError:
        raise IndexError(f"BeerCSS is not install properly in {static_dir}")
