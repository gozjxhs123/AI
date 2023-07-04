from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.app.fall import fall_router
import uvicorn


def create_app():
    app = FastAPI()
    include_router(app)
    add_cors_middleware(app)
    return app


def include_router(app: FastAPI):
    app.include_router(fall_router)


def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = create_app()

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)