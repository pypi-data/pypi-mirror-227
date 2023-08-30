#%%
import spacy
import pytextrank

from typing import List, Tuple
nlp = spacy.load("en_core_web_md")
nlp.add_pipe("textrank")
#%%

def get_key_phrases(text: str, threshold: float = None) -> List[Tuple[str, float, int]]:
    assert isinstance(threshold , float) or threshold is None
    
    doc = nlp(text)
    result = []
    for phrase in doc._.phrases:
        if threshold and phrase.rank < threshold: continue
        result.append([phrase.text, phrase.rank, phrase.count])

    return result


# %%
