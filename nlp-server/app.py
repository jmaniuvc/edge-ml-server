# !/usr/bin/env python3
"""
This is a module that does data NLP Server.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2024, AI Team"

from typing import Annotated
from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
from pydantic_models.schemas.rpa_recipe_schema import (
    RPARecipeRequestBody, RPARecipeResponseBody)
from pydantic_models.examples.rpa_recipe_example import rpa_recipe_exam
from utils.manage_model import get_chatgpt_model, get_prompt
from utils.validate_api import ValidationRecipe

load_dotenv()

DESCRIPTION = """
NLP Server helps you do awesome stuff. 🚀

## RPA

You will be able to:

* **Text to Recipe**
* ~ing

"""
app = FastAPI(
        title="NLP Server",
        description=DESCRIPTION,
        # summary="NLP Server",
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


@app.post("/getFreeTextRecipe", tags=['RPA'])
def get_freetext_rpa_receipe(request: Annotated[
                                RPARecipeRequestBody,
                                Body(openapi_examples=rpa_recipe_exam)
                            ]) -> RPARecipeResponseBody:
    """ Free-text to RPA recipe """

    prompt = get_prompt()
    model = get_chatgpt_model()
    msg = request.msg
    tag_map = request.tagIdsAndNames
    prompt_q = prompt.format(text=msg, tag_map=tag_map)
    result = model.predict(prompt_q)
    validation = ValidationRecipe(result)
    recipe = validation.get_recipe()
    return recipe


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
    uvicorn.run("app:app", host="0.0.0.0", port=5004, reload=True)
