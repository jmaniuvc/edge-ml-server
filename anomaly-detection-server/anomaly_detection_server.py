from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse
import uvicorn
from typing import Annotated
import pandas as pd
import json
from joblib import load
from dotenv import load_dotenv
import os
from utils.mqtt_send_anomaly_data import public_message
from pydantic_models.schemas.realtime_data_schema import RealTimeRequestBody
from pydantic_models.examples.realtime_data_example import realtime_data_exam
#from exception.base_exception import InvalidDataException


DESCRIPTION = """
The ML API of Flexing CPS helps you do awesome stuff. 🚀

You will be able to:

## Real-Time Detection
"""

app = FastAPI(
        title="CPS ML Server",
        description=DESCRIPTION,
        summary="Flexing CPS Machine Learning Server",
        version="0.0.1",
        contact={
            "name": "Jeong Min Lee",
            "url": "https://github.com/uvcdev/flexing-cps-server-python",
            "email": "jmani@uvc.co.kr",
        },
        license_info={
            "name": "Apache 2.0",
            "identifier": "MIT",
        },
    )



load_dotenv()
SAVE_DIR = os.getenv('RESOURCE_PATH')


def detect_anomaly_data(df):
    model = load(f'{SAVE_DIR}/dbscan.pkl')
    scaler = load(f'{SAVE_DIR}/scaler.joblib')
    onehot = load(f'{SAVE_DIR}/onehot_encoder.joblib')
    dim_reduction = load(f'{SAVE_DIR}/dime_reduction.joblib')
    with open(f'{SAVE_DIR}/meta_info.json', 'r', encoding='UTF-8') as f:
        meta = json.load(f)
    ###
    category_data_encoded = onehot.fit_transform(df[meta['categorical']])
    category_df = pd.DataFrame(category_data_encoded, columns=onehot.get_feature_names_out(meta['categorical']))
    df = pd.concat([df[meta['numeric']], category_df], axis=1)
    print(df)
    df = scaler.transform(df)
    df = dim_reduction.transform(df)

    predicted_label = model.predict(df).tolist()
    print(predicted_label)
    print("predicted_label")
    #result = {i+1: value for i, value in enumerate(predicted_label)}
    if -1 in predicted_label:
        public_message('anomaly')


@app.post("/getAnomalyData",
          tags=['Real-Time Process'],
          status_code=200,
          name='Get Real-Time Data')
async def get_anomaly_data(request_body:
                           Annotated[RealTimeRequestBody,
                                     Body(openapi_examples=realtime_data_exam)]):
    """
        You can check the information of missing values \n
        Receive data verification results for selected tags\n
        - Params:\n
            - body: \n
                - selectedTagList
                - contents:
                    - columns(list)
                    - index(list)
                    - data(list)
        - Returns:\n
            - result: \n
                {index: 1 or -1}
    """
    contents = request_body.TAGS

    try:
        df = pd.DataFrame(contents)
        df.fillna(0, inplace=True)
        result = detect_anomaly_data(df)

        return {'result': "ok"}

    except Exception as err:
        raise InvalidDataException() from err


@app.exception_handler(Exception)
async def global_exception_handler(_: Request, __: Exception):
    """
    Unexpected error handler
    """
    return JSONResponse(
        status_code=410,
        content={"detail": "An unexpected error occurred."},
    )


if __name__ == "__main__":
    # TODO Edge Config GateWay Config API 호출
    uvicorn.run("anomaly_detection_server:app", host="0.0.0.0", port=5005, reload=True)
