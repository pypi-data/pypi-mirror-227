""" shil.__main__
"""

from pathlib import Path

from fleks import app, cli
from fleks.util import lme

from . import fmt, invoke

LOGGER = lme.get_logger(__name__)
DEFAULT_INPUT_FILE = "/dev/stdin"

rich_flag = cli.click.flag("--rich", help="use rich output")


@cli.click.group(name=Path(__file__).parents[0].name)
def entry():
    """
    CLI tool for `shil` library
    """


def report(output, rich=False) -> None:
    if rich:
        should_rich = hasattr(output, "__rich__") or hasattr(output, "__rich_console__")
        lme.CONSOLE.print(
            output
            if should_rich
            else app.Syntax(
                f"{output}",
                "bash",
                word_wrap=True,
            )
        )
    else:
        if hasattr(output, "json"):
            import json

            print(json.dumps(json.loads(output.json(exclude_none=True)), indent=2))
        else:
            print(f"{output}")


@cli.click.flag("--rich", help="use rich output")
@cli.click.argument("cmd")
@entry.command(name="invoke")
def _invoke(rich: bool = False, cmd: str = "echo") -> None:
    """Invocation tool for (line-oriented) bash"""
    return report(
        invoke(
            command=cmd,
        ),
        rich=rich,
    )
    # print(output)


@entry.command(name="fmt")
@cli.click.argument("filename", default=DEFAULT_INPUT_FILE)
@rich_flag
def _fmt(
    filename: str = DEFAULT_INPUT_FILE,
    rich: bool = False,
) -> None:
    """
    Pretty-printer for (line-oriented) bash
    """
    if filename == "-":
        filename = DEFAULT_INPUT_FILE
    try:
        with open(filename) as fhandle:
            text = fhandle.read()
    except FileNotFoundError:
        LOGGER.warning(f"input @ {filename} is not a file; parsing as string")
        text = filename
    return report(fmt(text), rich=rich)


if __name__ == "__main__":
    entry()
