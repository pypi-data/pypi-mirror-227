from datetime import date

import click
import pandas as pd
from click import style
from dateutil.relativedelta import relativedelta

from cs_demand_model import (
    DemandModellingDataContainer,
    ModelPredictor,
    PopulationStats,
)
from cs_demand_model.config import Config
from cs_demand_model.datastore import fs_datastore

try:
    import matplotlib.pyplot as pp
except ImportError:
    pp = None


def style_prop(value, fg="green", bold=True, **kwargs):
    if hasattr(value, "strftime"):
        value = value.strftime("%Y-%m-%d")

    return style(value, fg=fg, bold=bold, **kwargs)


def plot_option(*args, help=None, **kwargs):
    if not pp:
        help = "Requires matplotlib"
    return click.option(*args, help=help, **kwargs)


class CliSetup:
    def __init__(self, source: str, start: date = None, end: date = None):
        self.config = Config()
        self.datastore = fs_datastore(source)
        self.dc = DemandModellingDataContainer(self.datastore, self.config)
        self.stats = PopulationStats(self.dc.enriched_view, self.config)

        # The default start date in 6m before the end of the dataset
        if start is None:
            start = self.dc.end_date - relativedelta(months=6)

        # The default end date is the end of the dataset
        if end is None:
            end = self.dc.end_date

        self.start = start
        self.end = end


@click.group()
def cli():
    pass


@cli.command()
@click.argument("source")
def list_files(source: str):
    """
    Opens SOURCE and lists the available files and metadata. This is for testing of source folders.
    """
    ds = fs_datastore(source)
    files = sorted(ds.files, key=lambda x: (x.metadata.year, x.metadata.name))
    for file in files:
        click.secho(f"{file.name}", fg="green", bold=True)
        click.secho(f"  Year: {click.style(file.metadata.year, fg='blue')}")
        if file.metadata.table:
            click.secho(f"  Table: {click.style(file.metadata.table, fg='blue')}")
        else:
            click.secho(f"  Table: {click.style('UNKNOWN', fg='red')}")
        click.secho(f"  Size: {click.style(file.metadata.size, fg='blue')}")
        click.echo()


@cli.command()
@click.argument("source")
@click.option("--start", "-s", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--end", "-e", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--export", type=click.Path(writable=True))
def analyse(source: str, start: date, end: date, export):
    """
    Opens SOURCE and runs analysis on the data between START and END. SOURCE can be a file or a filesystem URL.
    """
    setup = CliSetup(source, start, end)
    click.echo(
        f"Running analysis between {style_prop(setup.start)} and {style_prop(setup.end)})"
    )
    click.echo("Transition rates:")
    click.echo(setup.stats.transition_rates(setup.start, setup.end))

    if export:
        setup.stats.to_excel(export, setup.start, setup.end)
        click.echo(f"Saved analysis to {style_prop(export)}")


@cli.command()
@click.argument("source")
@click.option("--start", "-s", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--end", "-e", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--prediction_date", "--pd", type=click.DateTime(formats=["%Y-%m-%d"]))
@plot_option("--plot", "-p", is_flag=True, help="Plot the results")
@click.option("--export", type=click.Path(writable=True))
def predict(
    source: str, start: date, end: date, prediction_date: date, plot: bool, export
):
    """
    Analyses SOURCE between start and end, and then predicts the population at prediction_date.
    """
    setup = CliSetup(source, start, end)
    start, end = setup.start, setup.end

    if prediction_date is None:
        prediction_date = end + relativedelta(months=12)

    click.echo(
        f"Running analysis between {style_prop(setup.start)} and {style_prop(setup.end)} "
        f"and predicting to {style_prop(prediction_date)}"
    )

    predictor = ModelPredictor.from_model(setup.stats, start, end)
    prediction_days = (prediction_date - end).days
    predicted_pop = predictor.predict(prediction_days, progress=True)

    click.echo("Predicted population:")
    click.echo(predicted_pop)

    if export:
        predicted_pop.to_excel(export)
        click.echo(f"Saved prediction to {style_prop(export)}")

    if plot:
        if not pp:
            click.secho("Plotting requires matplotlib", fg="red")
        else:
            historic_pop = setup.stats.stock.loc[:end]

            pd.concat([historic_pop, predicted_pop], axis=0).plot()
            pp.axvline(end, alpha=0.4)
            pp.axvspan(start, end, alpha=0.1)
            pp.show()


if __name__ == "__main__":
    cli()
