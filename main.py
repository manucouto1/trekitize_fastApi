from app import MainApp
from service.routers import queries, documents, users, pool, user_pool

MainApp.app.include_router(user_pool.router)
MainApp.app.include_router(pool.router)
MainApp.app.include_router(users.router)
MainApp.app.include_router(queries.router)
MainApp.app.include_router(documents.router)

app = MainApp.app