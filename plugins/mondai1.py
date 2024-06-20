from typing import Literal
import pandas as pd
from core import MultipleChoice

class KanjiMondai(MultipleChoice):
    INSTRUCTION = "問題 1 &nbsp&nbsp  <u>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</u>の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。"
    MONDAI_ID   = 1

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
    
    
