from litestar import Litestar
from litestar.di import Provide

from app.auth.api import UserController
from app.database import Database
from app.settings import settings


async def provide_database():
    database = Database()
    await database.connect(settings.db_uri, settings.pool_db)
    yield database
    await database.close()


app = Litestar(route_handlers=[UserController], debug=True, dependencies={"db": Provide(provide_database)})
