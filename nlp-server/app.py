from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
import json
from typing import Annotated
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic_models.schemas.rpa_recipe_schema import RPARecipeRequestBody
from pydantic_models.examples.rpa_recipe_example import rpa_recipe_exam

load_dotenv()
DESCRIPTION = """
The ML API of Flexing CPS helps you do awesome stuff. 🚀

You will be able to:

## Real-Time Detection
"""
app = FastAPI()
templates = Jinja2Templates(directory="templates")
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

with open("prompt2.txt", "r", encoding='utf-8') as f:
    text = f.read()

llm = ChatOpenAI(temperature=0,               # 창의성 (0.0 ~ 2.0)
                 max_tokens=2800,             # 최대 토큰수
                 model_name='gpt-3.5-turbo')  # 모델명


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

prompt = PromptTemplate.from_template(text)

@app.post("/getFreeTextRPARecipe")
def get_freetext_rpa_receipe(request:
                             Annotated[RPARecipeRequestBody,
                                       Body(openapi_examples=rpa_recipe_exam)]):
    # question = "에어압력계의 에어 누출이 없고 에어압력 지침이 4~6Mpa인지 확인하고 안된다면 에어 레귤레이터의 점검/수리/교체를 해야해."
    recipe_name = request.data.recipeName
    msg = request.data.msg
    print(type(msg))
    prompt_q = prompt.format(text=msg)
    result = llm.predict(prompt_q)
    print(result)
    result = json.loads(result)
    return result


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
    uvicorn.run("app:app", host="0.0.0.0", port=5004, reload=True)
