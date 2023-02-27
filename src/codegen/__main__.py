import logging
import pathlib
import sys
import click
from collections import namedtuple

import codegen.generator as generator

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def _get_logging_level(verbose, quiet):
    if 0 < verbose and 0 < quiet:
        click.exceptions.error("Mixing --verbose and --quiet is contradictory")
    verbosity = 2 + quiet - verbose
    verbosity = max(verbosity, 0)
    verbosity = min(verbosity, 4)
    logging_level = {
        0: logging.DEBUG,
        1: logging.INFO,
        2: logging.WARNING,
        3: logging.ERROR,
        4: logging.CRITICAL,
    }[verbosity]

    return logging_level


@click.command()
@click.option("--dest", type=pathlib.Path)
@click.option("--verbose", type=int, default=0, required=False)
@click.option("--quiet", type=int, default=0, required=False)
def main(dest, verbose, quiet):
    logging_level = _get_logging_level(verbose, quiet)

    log_format = "[%(relativeCreated)6d] %(levelname)-5s %(funcName)s: %(message)s"
    logging.basicConfig(level=logging_level, format=log_format)

    try:
        generator.generate(dest)
    except Exception:
        _logger.exception("Failed to generate")
        return 1


if __name__ == "__main__":
    sys.exit(main())