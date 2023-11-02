import typing
import study_wsd.prompt as prompt

class WordSenseEvaluation:

    def __init__(self, sentence, word, synset_answer, synset_options, pos = "NOUN"):
        self.sentence = sentence
        self.word = word
        self.synset_answer = synset_answer
        self.synset_options = synset_options
        self.pos = pos

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
            "answer":self.synset_answer._name,
            "options":list(o._name for o in self.synset_options),
        }

class SynsetOption:

    def __init__(self, id, gloss):
        self.id = id
        self.gloss = gloss
