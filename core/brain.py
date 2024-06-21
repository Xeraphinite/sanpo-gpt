from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from litellm import completion
import os

class Message(BaseModel):
    content: str = Field(default="", max_length=114514)
    role: Literal["system"] | Literal["user"] | Literal["assistant"] = Field(default="user")

class Brain(BaseModel):
    BASE_URL: str = Field(default=os.getenv("BASE_URL"))
    MODEL_NAME: str = Field(default=os.getenv("MODEL_NAME"))
    OPENAI_API_KEY: str = Field(default=os.getenv("OPENAI_API_KEY"))
    prompt:   str = Field(default="", max_length=114514)
    response: str = Field(default="", max_length=114514)

    def __init__(self, *args, **kwargs):
        load_dotenv()
        super().__init__(*args, **kwargs)
    
    def stream(self, messages: list[Message]):
        messages = [message.model_dump() for message in messages]   # type: ignore

        response = completion(
            base_url=self.BASE_URL,
            model=self.MODEL_NAME,
            api_key=self.OPENAI_API_KEY,
            stream=True,
            messages=messages,
        )

        for chunk in response:
            content = chunk.choices[0].delta.content or ""  # type: ignore
            yield content

    def general_analyse_stream(self, instruction: list[Message], few_shots: list[Message], context: list[Message]):
        wrapped_messages = [
            Message(role="assistant", content="你是一个循循善诱的 JLPT 日语老师，现在你需要帮助学生详细解析下面的问题，让学生更好地理解题目。你应当使用**中文**解析。你应当仿照以下例子输出解析的结果。问题的要求如下："),
        ] + instruction + [
            Message(role="system", content="问题解析例如下：")
        ] + few_shots + [
            Message(role="system", content="接下来是你需要解析的问题："),
        ] + context + [
            Message(role="system", content="请注意：在所有的解析中，注音的时候用平假名，不要用罗马音。你不需要重新输出题干，只需要解析即可。你不应当输出解释性语句，如“好的，让我们一步步”"),
            Message(role="system", content="请开始解析：")
        ]
        
        return self.stream(wrapped_messages)

    # Use completion without streaming
    def structured_query(self, json_schema, messages: list[Message]):
        json_messages = Message(
            role="system",
            content="You are an expert assitant for summarizing and extracting insights from sales call transcripts.\n"
            "Generate a valid JSON following the given schema below:\n"
            f"{json_schema}",
        )

        response = completion(
            base_url=self.BASE_URL,
            model=self.MODEL_NAME,
            api_key=self.OPENAI_API_KEY,
            messages=[json_messages] + messages,
        )

        return response["choices"][0]["message"]["content"] # type:ignore
