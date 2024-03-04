#!/usr/bin/env python3

"""
This is a module that Edge Data.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2023, NT Team"


import os
from typing import Annotated
import logging
import uvicorn
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse

from utils.inference import detect_anomaly_data
from pydantic_models.schemas.realtime_data_schema import RealTimeRequestBody
from pydantic_models.examples.realtime_data_example import (
    realtime_data_exam as realtime_ex)


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


@app.post("/getAnomalyData",
          tags=['Real-Time Process'],
          status_code=200,
          name='Get Real-Time Data')
async def get_anomaly_data(request_body:
                           Annotated[RealTimeRequestBody,
                                     Body(openapi_examples=realtime_ex)]):
    """
        You can check the information of missing values \n
        Receive data verification results for selected tags\n
        - Params:\n
            - DEVICE_ID: str
            - TAGS: LIst[Any]
            - DATE_TIME: str
        - Returns:\n
            - result: "ok"
    """
    contents = request_body.TAGS
    dt = request_body.DATE_TIME
    try:
        df = pd.DataFrame(contents)
        df.fillna(0, inplace=True)
        df = df.drop(labels='NODE_ID', axis=1)
        if detect_anomaly_data(df, dt) is None:
            raise Exception()  # pylint: disable=broad-exception-raised

        return {'result': "ok"}

    except Exception as err:  # pylint: disable=broad-except
        logging.warning("%s", err)


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
    uvicorn.run(
        "anomaly_detection_server:app", host="0.0.0.0", port=5005, reload=True)
