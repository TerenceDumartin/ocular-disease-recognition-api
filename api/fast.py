#!/usr/bin/env python3
from fastapi import FastAPI, Response, Request, Header, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tensorflow.keras import models
import numpy as np
from PIL import Image
import os
import shutil
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app = FastAPI()

# Instanciate cache object to mem store models
cache_models = {}

# def path_to_image(path, image_size, num_channels, interpolation):
#     img = io_ops.read_file(path)
#     img = image_ops.decode_image(img, channels=num_channels, expand_animations=False)
#     img = image_ops.resize_images_v2(img, image_size, method=interpolation)
#     img.set_shape((image_size[0], image_size[1], num_channels))
#     img = np.array([img])
#     return img


# from PIL import Image
# image = Image.open("path/.../image.png")
# image = image.resize((500,500),Image.ANTIALIAS)

def read_imagefile(file):
    img = Image.open(file)
    img = img.resize((256,256),Image.ANTIALIAS)
    img = np.array([np.array(img)])
    return img

# ---------------------------------------------------------------------------
# - Handle a POST request to handle an image -
# ---------------------------------------------------------------------------
def check_extension(filename):
    ALLOWED_EXTENSION = ["jpg", "jpeg", "png"]
    # Extract extension
    extension = filename.split(".")[-1:][0].lower()
    if extension not in ALLOWED_EXTENSION :
        return False
    else :
        return True

# def read_imagefile(file) -> Image.Image :

#     img_test = path_to_image(file, (256, 256), 3, 'bilinear')
#     img_test = np.array(file)
#     #img_test = np.expand_dims(img_test, axis = 0)
#     return img_test


class PredictPayload(BaseModel):
    key : str
    value : int

@app.on_event("startup")
async def startup_event():
    '''
    On api startup, load and store models in mem
    '''
    print("load model ...")
    dirname = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(dirname,'models','model_v5')
    model = models.load_model('baseline_model_N_C_downsample.h5')
    cache_models["model_1"] = model
    print("model is ready ...")


@app.post("/predict")
async def predict_handler(response : Response, inputImage : UploadFile = File(...)):
    '''
    Check extension
    '''
    check = check_extension(inputImage.filename)

    if check == False :
        response_payload = {
                "status" : "error",
                "message" : "Input file format not valid"
                }
        response.status_code=400
        return response

    '''
    Temp image
    '''
    temp_image = str(int(time.time())) + "_" + inputImage.filename
    with open(temp_image, "wb") as buffer:
        shutil.copyfileobj(inputImage.file, buffer)

    '''
    Prediction worker
    '''
    # Extraction image
    img = read_imagefile(temp_image)

    # load cached model
    model = cache_models["model_1"]

    # prediction
    pred = model.predict(img)
    pred = int(pred[0][0])

    '''
    Delete temp image
    '''
    if os.path.exists(temp_image):
        os.remove(temp_image)


    '''
    Build response
    '''
    response_payload = {"prediction" : pred}
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response_payload['prediction']

'''
If you want to return a file/image (not a json payload):
from fastapi.responses import FileResponse

response.status_code = 200
return FileResponse(file_path)
'''

