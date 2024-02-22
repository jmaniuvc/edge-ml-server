
import os
from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from langchain_openai import ChatOpenAI

app = FastAPI()
templates = Jinja2Templates(directory="templates")
openai_api_key = os.getenv('OPENAI_API_KEY')

prompt_1 = """
    받은 텍스트를 action, condition 키를 가진 해야할 일, 조건으로 나눠서
    action 키 안에는 fact, message 키를 가진 설비명, 해야할 일 목록을 생성해줘.
    또한, condition 키 안에는 조건 별로
    fact, tag, value, operator 키를 가진 설비명, 태그, 값, 비교연산 목록을 생성해야해.
    operator는 equal, notEqual, greaterThan, smallerThan 중에 하나만 들어가야해.
    태그가 특정 범위 사이가 조건이라면 목록을 나눠서 생성해줘.

    예를 들어
    user: '윤활부, 냉각부, 세퍼레이터가 초기 가동시 각종 게이지 정상 작동여부를 확인하고 문제가 있다면 수리 또는 교체를 진행하라.
            또한, 냉각부의 온도 값이 -10보다 낮거나 50보다 높으면 알림을 설정해줘. '
    answer:
    {
        "action": [
            {
            "fact": "윤활부",
            "message": "수리 또는 교체"
            },
            "fact": "냉각부",
            "message": "수리 또는 교체"
            },
            "fact": "세퍼레이터",
            "message": "수리 또는 교체"
            },
            "fact": "윤활부",
            "message": "알림"
            },
        ],
        "condition": [
            {
            "fact": "윤활부",
            "tag": "게이지",
            "value": "정상",
            "operator": "equal"
            },
            {
            "fact": "냉각부",
            "tag": "게이지 지침",
            "value": "정상",
            "operator": "equal"
            },
            {
            "fact": "세퍼레이터",
            "tag": "게이지 지침",
            "value": "정상",
            "operator": "equal"
            },
            {
            "fact": "윤활부",
            "tag": "온도",
            "value": "-10",
            "operator": "smallerThan"
            },
            {
            "fact": "윤활부",
            "tag": "온도",
            "value": "50",
            "operator": "greaterThan"
            }
        ]
    }
    위 예시를 참고하여 다음 문장을 json 형태로 변경시켜줘.
"""

llm = ChatOpenAI(temperature=0,               # 창의성 (0.0 ~ 2.0) 
                 max_tokens=2048,             # 최대 토큰수
                 model_name='gpt-3.5-turbo')  # 모델명


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/getRecipe")
def speak(request: Request):
    question = "에어압력계의 에어 누출이 없고 에어압력 지침이 4~6Mpa인지 확인하고 안된다면 에어 레귤레이터의 점검/수리/교체를 해야해."
    result = llm.predict(prompt_1+question)
    print(result)
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
