import click

from lab.core.cli import coro

from app.auth.auth_cli import auth_cli
from app.database import Database
from app.migrations import init_migrations
from app.settings import settings


@click.group()
def raw_sql_cli(): ...


@raw_sql_cli.command()
@coro
async def raw_migrate():
    click.echo("run migrations")
    database = Database()
    await database.connect(settings.db_uri, settings.pool_db)
    await init_migrations(database.fetch)
    click.echo("migrations success")


cli = click.CommandCollection(sources=[raw_sql_cli, auth_cli])

if __name__ == "__main__":
    cli()
