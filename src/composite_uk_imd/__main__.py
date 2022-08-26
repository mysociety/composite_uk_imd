import rich_click as click
from .create_missing_overall_scores import fill_in_scores
from .merge_indexes import produce_indexes_and_analysis


def update_data_and_build():
    fill_in_scores()
    produce_indexes_and_analysis()


@click.group()
def cli():
    pass


def main():
    cli()


@cli.command()
def build():
    update_data_and_build()


if __name__ == "__main__":
    main()
