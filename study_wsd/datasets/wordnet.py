from nltk.corpus import wordnet as wn
import random


def get_random_lemma_search(root_synset_id:str, ignore_lemmas_with_spaces: bool = True):
    s = wn.synset(root_synset_id)

    children = s.hyponyms()

    if len(children) == 0:
        lemma = s.lemmas()[0].name()
        if ignore_lemmas_with_spaces and lemma.find("_") > 0:
            return None
        else:
            return lemma
    else:
        children_check_count = 0
        while children_check_count < 5:
            t = get_random_lemma_search(random.choice(children).name())
            if t is not None:
                return t
            else:
                children_check_count += 1
        lemma = s.lemmas()[0].name()
        if ignore_lemmas_with_spaces and lemma.find("_") > 0:
            return None
        else:
            return lemma
    


def get_random_lemma(pos:str = "NOUN") -> str:
    if pos == "NOUN":
        return get_random_lemma_search('entity.n.01')
    return ""


# all constants except y
_constants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r","s","t","v","w","x","z"]

def create_fake_lemma(root_lemma:str, varied_randomness:float = 0.5) -> str:
    constant_mask = list(True if _constants.count(c) == 1 else False for c in root_lemma.lower())
    # count constants
    valid_lemma = True
    check_lemma = root_lemma
    while valid_lemma:
        for i in range(len(root_lemma)):
            if constant_mask[i] and random.random() > varied_randomness:
                check_lemma = check_lemma[:i] + random.choice(_constants) + check_lemma[i+1:]

        valid_lemma = len(wn.synsets(check_lemma)) > 0
    return check_lemma
