import os
import sys
from typing import Literal, cast

Environment = Literal["production", "staging", "dev", "testing"]


def mod(pkg: str, modules: list[str]) -> list[str]:
    return [".".join([t for t in [pkg, module] if t]) for module in modules]


def get_environment(config, debug: bool) -> Environment:
    if "test" in sys.argv or "PYTEST_VERSION" in os.environ:
        return "testing"
    if debug:
        return "dev"
    return cast(Environment, config("ENVIRONMENT", "production"))


def get_beercss_dir(static_dir) -> str:
    """
    Get the BeerCSS directory name in the form `beercss-x.y.z`
    """
    try:
        return list(static_dir.glob("beercss-*"))[-1].name
    except IndexError:
        raise IndexError(f"BeerCSS is not install properly in {static_dir}")
