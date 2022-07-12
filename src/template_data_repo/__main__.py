import rich_click as click


@click.group()
def cli():
    pass


def main():
    cli()


@cli.command()
def example():
    print("This is an example function")


if __name__ == "__main__":
    main()
