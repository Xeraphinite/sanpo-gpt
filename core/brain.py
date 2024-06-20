from typing import Literal
from pydantic import BaseModel, Field
from litellm import completion
import os

from core.exam import MultipleChoice

class Message(BaseModel):
    content: str = Field(default="", max_length=114514)
    role: Literal["system"] | Literal["user"] | Literal["assistant"] = Field(default="user")

class Brain(BaseModel):
    BASE_URL: str = Field(default=os.getenv("BASE_URL"))
    MODEL_NAME: str = Field(default=os.getenv("MODEL_NAME"))
    OPENAI_API_KEY: str = Field(default=os.getenv("OPENAI_API_KEY"))
    prompt:   str = Field(default="", max_length=114514)
    response: str = Field(default="", max_length=114514)

    def stream(self, messages: list[Message]):
        messages = [message.model_dump() for message in messages]
        
        print(self.BASE_URL, self.MODEL_NAME, self.OPENAI_API_KEY)
        
        response = completion(
            base_url=self.BASE_URL,
            model=self.MODEL_NAME,
            api_key=self.OPENAI_API_KEY,
            stream=True,
            messages=messages,
        )

        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            yield content

    def general_analyse_stream(self, question: MultipleChoice):
        messages = [
            Message(role="system", content="你是一个循循善诱的 JLPT 日语老师，现在你需要帮助学生详细解析下面的问题"),
            Message(content=str(question)),
            Message(role="system", content="使用中文解析，请注意：在所有的解析中，注音的时候用平假名，不要用罗马音。你不需要重新输出题干，只需要解析即可。同时，你不应当输出解释性语句，如“好的，让我们一步步”"),
        ]
        
        return self.stream(messages)

    # Use completion without streaming
    # def structured_query(self, json_schema, messages: list[Message]):
    #     json_messages = Message(
    #         role="system",
    #         content="You are an expert assitant for summarizing and extracting insights from sales call transcripts.\n"
    #         "Generate a valid JSON following the given schema below:\n"
    #         f"{json_schema}",
    #     )

    #     response = litellm.completion(
    #         model=self.MODEL_NAME,
    #         base_url=self.BASE_URL,
    #         messages=json_messages + messages,
    #     )

    #     return response["choices"][0]["message"]["content"]
