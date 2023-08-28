import typer

from .algo import algo
from .backtest import backtest
from .service import service

cli = typer.Typer()

cli.add_typer(algo, name="algo")
cli.add_typer(backtest, name="backtest")
cli.add_typer(service, name="service")
