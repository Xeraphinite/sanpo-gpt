from typing import ClassVar, Generator
import pandas as pd
from core import (
    MultipleChoice,
    Brain,
    Message
)

class KanjiMondai(MultipleChoice):
    INSTRUCTION: ClassVar = "問題 1 &nbsp&nbsp  <u>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</u>の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。"
    MONDAI_ID: ClassVar   = 1

def csv_to_kanji_mondais(path: str):
    """Read Kanji Mondai from csv file, return a list of kanji mondai.

    Args:
        base_path (str): the path of kanji mondai.
    Returns:
        kanji_mondai (list[KanjiMondai]): a list of kanji mondai.
    """
    df = pd.read_csv(path)

    kanji_mondais = [
        KanjiMondai(
            id=id,
            description=description.replace(r"（(.*?)）", r"<u><b>\1</b></u>"),
            choices=choices.split(";"),
            answer_idx=answer_idx,
        )
        for _, (id, description, choices, answer_idx) in df.iterrows()
    ]

    return kanji_mondais
    
def mondai1_analyse(mondai: KanjiMondai) -> Generator:
    """Analyse the mondai1.

    Args:
        mondai (KanjiMondai): the mondai to be analysed.
    Returns:
        stream (Generator): the generator stream.
    """
    brain = Brain()
    
    instruct_message = [
        Message(role="system", content="问题解析需要包括：\n"
                "1. 整句话的含义；\n"
                "2. 正确选项读音的汉字含义；\n"
                "3. 其他选项读音的汉字含义（若有），若其他选项在 JLPT N1 范围内没有对应的常见汉字，则应当输出“其他选项无对应常见汉字，为干扰项”；\n")
    ]
    
    one_shot_mondai1 = KanjiMondai(
        id=1,
        description="学生に<u><b>慕われる</b></u>教師になりたい。",
        choices=["したわれる", "したがわれる", "うやまわれる", "ともなわれる"],
        answer_idx=0,
    )
    
    one_shot_mondai2 = KanjiMondai(
        id=1,
        description="申込書にパスポートのコピーを<u><b>添付</u></b>した。",
        choices=["でんふ", "てんふ", "でんぷ", "てんぷ"],
        answer_idx=3
    )
    
    one_shot_messages = [
        Message(role="system", content=one_shot_mondai1.INSTRUCTION),
        Message(role="system", content=one_shot_mondai1.description),
        Message(role="system", content="""想成为受学生敬仰的老师。
1.したう（慕う）【他五】敬慕,敬仰,景仰。「したわれる」是它的被动态。
2.したがう（従う）【自五】按照,遵从。「したがわれる」是它的被动态。
3.うやまう（敬う）【他五】尊敬,尊重。「うやまわれる」是它的被动态。
4.ともなう（伴う）【自他五】伴随,陪同。「ともなわれる」是它的被动态。"""),
        Message(role="system", content=one_shot_mondai2.description),
        Message(role="system", content="""申请书上附上了护照复印件。
4.添付（てんぷ）:【名】【他サ】添上;付上。
其他选项均为干扰项。"""),
    ]

    context_messages = [
        Message(role="user", content=mondai.INSTRUCTION),
        Message(role="user", content=mondai.description),
    ]
    
    stream = brain.general_analyse_stream(instruct_message, one_shot_messages, context_messages)
    
    return stream
