# !/usr/bin/env python3
"""
This is a module that does data NLP Server.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2024, AI Team"


from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


def get_prompt():
    """ Get prompt """
    with open("prompt.txt", "r", encoding='utf-8') as f:
        text = f.read()
    prompt = PromptTemplate.from_template(text)
    return prompt


def get_chatgpt_model():
    """ Get chatGPT Model """
    model = ChatOpenAI(temperature=0,  # 0.0 ~ 2.0
                       max_tokens=2800,
                       model_name='gpt-3.5-turbo')
    return model
