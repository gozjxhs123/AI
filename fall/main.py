from fastapi import APIRouter, UploadFile, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.param_functions import File
from fall_prediction import Fall_prediction
from config import *
from PIL import Image
import os
from sdk.api.message import Message
import time

fall_router = APIRouter()

@fall_router.post("/fall")
def predict_image(image: UploadFile = File(...), phone: str = ""):
    length = len(os.listdir("../image"))
    if length == 3:
        number = max([int(name.split(".")[0]) for name in os.listdir("../image")]) + 1
    else:
        number = length
    file_path = f"../image/{number}.png"
    with open(file_path, "wb") as file:
        file.write(image.file.read())
    if length == 3:
        os.remove(f"../image/{min([int(name.split('.')[0]) for name in os.listdir('../image')])}.png")
    else: return False
    images = [Image.open(f"../image/{link}") for link in os.listdir("../image")]
    response = Fall_prediction(*images)

    if response:
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
        return True

    return False



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

if _name_ == '_main_':
    uvicorn.run("main:app", reload=True)