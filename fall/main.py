from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import *
from sdk.api.message import Message
import time

fall_router = APIRouter()

@fall_router.post("/fall")
def predict_image(phone: str = ""):
    params = dict()
    params['type'] = 'sms'
    params['to'] = phone
    params['from'] = PHONE_NUMBER
    params['text'] = f"Falltect : {time.strftime('%Y.%m.%d - %H:%M:%S')} 사람 쓰러짐이 감지되었습니다."

    cool = Message(API_KEY, API_SECRET)

    try:
        cool.send(params)
    except:
        pass

    return None



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