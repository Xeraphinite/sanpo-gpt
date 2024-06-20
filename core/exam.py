from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Literal

@dataclass
class MultipleChoice(BaseModel):
    id: int = Field(ge=1, le=70) # 题号，在每一张试卷中是固定的，range(1, 71)
    description: str             # 问题的 description，小题的题干
    choices: list[str]           # 选项，一共 4 个选项
    answer_idx: int              # 正确答案的 index，从 0 开始
    
    def check_answer(self, choice: str | int) -> bool:
        if isinstance(choice, int):
            return choice == self.answer_idx
        else:
            return choice == self.choices[self.answer_idx]
        
class MondaiSet(BaseModel):
    instruction: str                    # 大题的题干
    context: str | None                 # 大题的 Context，在阅读和完形填空中是一个 str，而在其他题型中没有
    mondai_set: list[MultipleChoice]

class Exam(BaseModel):
    level: Literal["N1", "N2", "N3", "N4", "N5"] = "N1" # JLPT 等级
    test_id: tuple[int, int]  # 年份，月份，例如 (2021, 1)
    mondai_sets: list[MondaiSet]  # 一套试卷的所有题目，70 题，返回 5 个 list
