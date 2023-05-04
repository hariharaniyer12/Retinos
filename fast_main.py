from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import h5py
from tensorflow import keras
import keras
from keras.models import load_model
import chardet


# from tensorflow.keras.models import load_model

app = FastAPI()

origin = [
    "http://localhost",
    "http://localhost:3000"
]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODEL = tf.keras.models.load_model("saved_models/1")
MODEL1 = tf.keras.models.load_model("3_class_densenet121.hdf5")
CLASS_NAMES = ["Moderate","No_Dr", "Severe"]

@app.get("/ping")
async def req_handler():
    return "started your fast api server!!!"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    # image = np.array(data)/255.0
    return image

@app.post("/files")

async def UploadImage(file: UploadFile = File(...)):
   
    image = read_file_as_image(await file.read())

    img = np.array(image) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = MODEL1.predict(img)
    print(pred)
    
    pred_class = np.argmax(pred)
    print(pred_class)

    if pred_class == 0:
        pred_label = 'MODERATE'
    elif pred_class == 1:
        pred_label = 'HEALTHY'
    elif pred_class == 2:
        pred_label = 'SEVERE'

    return{
        pred_label  
    }

@app.post("/predict")
def predict():
    import pathlib
    from PIL import Image
    from keras.preprocessing.image import ImageDataGenerator
    import os
    count=0
    tcount=0
    path=pathlib.Path('Test/Severe_Dr');
    for i in os.listdir(path):
        img = Image.open(os.path.join(path, i)).resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)
        pred = MODEL1.predict(img)
        pred_class = np.argmax(pred)
        # predicted_class = CLASS_NAMES[np.argmax(pred[0])]
        # print(predicted_class)
        # print(pred_class)
        if(pred_class==2):
            count=count+1
            tcount=tcount+1
            print("Yes")
        else:
            tcount=tcount+1
    print(count,"/",tcount)

    # count=0
    # tcount=0
    # path=pathlib.Path('Test/Moderate_Dr');
    # for i in os.listdir(path):
    #     img = Image.open(os.path.join(path, i)).resize((224, 224))
    #     img = np.array(img) / 255.0
    #     img = np.expand_dims(img, axis=0)
    #     pred = MODEL.predict(img)
    #     pred_class = np.argmax(pred)
    #     # predicted_class = CLASS_NAMES[np.argmax(pred[0])]
    #     # print(predicted_class)
    #     # print(pred_class)
    #     if(pred_class==0):
    #         count=count+1
    #         tcount=tcount+1
    #     else:
    #         tcount=tcount+1
    # print(count,"/",tcount)


    # count=0
    # tcount=0
    # path=pathlib.Path('Test/No_Dr');
    # for i in os.listdir(path):
    #     img = Image.open(os.path.join(path, i)).resize((224, 224))
    #     img = np.array(img) / 255.0
    #     img = np.expand_dims(img, axis=0)
    #     pred = MODEL.predict(img)
    #     pred_class = np.argmax(pred)
    #     # predicted_class = CLASS_NAMES[np.argmax(pred[0])]
    #     # print(predicted_class)
    #     # print(pred_class)
    #     if(pred_class==1):
    #         count=count+1
    #         tcount=tcount+1
    #     else:
    #         tcount=tcount+1
    # print(count,"/",tcount)

    


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)