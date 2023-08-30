import click
from verba_rag.ingestion.init_schema import init_schema
from verba_rag.ingestion.init_cache import init_cache
from verba_rag.ingestion.init_suggestion import init_suggestion
from verba_rag.ingestion.import_data import import_data
from verba_rag.ingestion.import_weaviate import import_weaviate


@click.group()
def cli():
    """Main command group for verba."""
    pass


@cli.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    help="OpenAI Model name to initialize. (default gpt-3.5-turbo)",
)
def init(model):
    """
    Initialize schemas
    """
    init_schema(model=model)
    init_cache()
    init_suggestion()


@cli.command()
def clear_cache_command():
    init_cache()


@cli.command()
@click.option(
    "--path",
    default="./data",
    help="Path to data directory",
)
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    help="OpenAI Model name to initialize. (default gpt-3.5-turbo)",
)
def import_data_command(path, model):
    init_schema(model=model)
    init_cache()
    init_suggestion()
    import_data(dir_path=path)


@cli.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    help="OpenAI Model name to initialize. (default gpt-3.5-turbo)",
)
def import_weaviate_command(model):
    init_schema(model=model)
    init_cache()
    init_suggestion()
    import_weaviate()
