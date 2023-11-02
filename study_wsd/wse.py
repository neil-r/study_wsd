import typing
import study_wsd.prompt as prompt


class SynsetOption:

    def __init__(self, id:str, gloss:str):
        self.id = id
        self.gloss = gloss


class WordSenseEvaluation:

    def __init__(self, sentence, word, synset_answer, synset_options:typing.List[SynsetOption], pos = "NOUN"):
        self.sentence = sentence
        self.word = word
        self.synset_answer = synset_answer
        self.synset_options = synset_options
        self.pos = pos

        found = False
        for opt in synset_options:
            if opt.id == self.synset_answer:
                assert not found # ensure only one option matches answer
                found = True
        assert found

    @property
    def content(self):
        return f"What is the meaning of the word {self.word} in '{self.sentence}'?"

        
    def handle_response(self, response:str) -> typing.Optional["prompt.Prompt[WordSenseEvaluation]"]:
        # abstract class not implemented
        return None
    
    def to_json(self):
        return {
            "sentence":self.sentence,
            "word":self.word,
            "answer":self.synset_answer,
            "options":list({"id":o.id, "gloss":o.gloss } for o in self.synset_options),
        }
