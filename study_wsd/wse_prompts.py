import typing
import random

from study_wsd.prompt import PromptFactory, Prompt
from study_wsd.wse import WordSenseEvaluation


def find_letter_response(response:str) -> typing.Optional[str]:
    l_response = None

    i = response.find(")")
    # ensure this character was found, and if so, return previous character
    if i > 0:
        l_response = response[i-1]

    return l_response


def determine_true_false(response:str) -> typing.Optional[str]:
    response_l = response.lower()
    i_t = response_l.find("true")
    i_f = response_l.find("false")
    
    if i_t >= 0 and i_f >=0:
        return "true" if i_t < i_f else "false"
    elif i_t >= 0:
        return "true"
    elif i_f >= 0:
        return "false"
    return "unknown"



def _convert_pos_tag_to_text(pos) -> str:
    if pos == "ADJ":
        return "adjective"
    if pos == "VERB":
        return "verb"
    if pos == "NOUN":
        return "noun"
    raise ValueError(f"Unknown part of speech tag conversion for pos '{pos}'")

class DefaultWsePrompt(PromptFactory[WordSenseEvaluation]):

    def __init__(self,
                 topic:WordSenseEvaluation,
                 response_interpretter_function=find_letter_response
        ):
        self.topic = topic
        self.answer_value = None
        self.answer_response = None
        self.response_interpretter_function = response_interpretter_function

    @property
    def content(self) -> str:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if len(self.topic.synset_options) > len(letters):
            raise ValueError("Not enough letters to support this prompt") 
        options = [
            f"{letter}) {t.gloss}" for letter, t in zip(letters, self.topic.synset_options)
        ]

        for letter, t in zip(letters, self.topic.synset_options):
            if self.topic.synset_answer == t.id:
                self.answer_value = letter
                break
            

        options_str = "\n".join(options)

        return f'''Question:
What is the meaning of the word "{self.topic.word}" in "{self.topic.sentence}"?

Options:
{options_str}
'''
    
    def handle_response(self, response:str) -> typing.Optional["Prompt[WordSenseEvaluation]"]:

        r = self.response_interpretter_function(response)
        if r is not None:
            self.answer_response = r

        return None


class DefaultWsePromptFactory(PromptFactory[WordSenseEvaluation]):

    def generate_prompt(self, topic:WordSenseEvaluation) -> Prompt[WordSenseEvaluation]:
        return DefaultWsePrompt(topic)


class DirectWsePrompt(PromptFactory[WordSenseEvaluation]):

    def __init__(self,
                 topic:WordSenseEvaluation,
                 response_interpretter_function=find_letter_response
        ):
        self.topic = topic
        self.answer_value = None
        self.answer_response = None
        self.response_interpretter_function = response_interpretter_function

    @property
    def content(self) -> str:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if len(self.topic.synset_options) > len(letters):
            raise ValueError("Not enough letters to support this prompt") 
        options = [
            f"{letter}) {t.gloss}" for letter, t in zip(letters, self.topic.synset_options)
        ]

        for letter, t in zip(letters, self.topic.synset_options):
            if self.topic.synset_answer == t.id:
                self.answer_value = letter
                break
            

        options_str = "\n".join(options)

        return f'''What is the meaning of the word "{self.topic.word}" in the following sentence?

{self.topic.sentence}

Options:
{options_str}
'''
    
    def handle_response(self, response:str) -> typing.Optional["Prompt[WordSenseEvaluation]"]:

        r = self.response_interpretter_function(response)
        if r is not None:
            self.answer_response = r

        return None


class DirectWsePromptFactory(PromptFactory[WordSenseEvaluation]):

    def generate_prompt(self, topic:WordSenseEvaluation) -> Prompt[WordSenseEvaluation]:
        return DirectWsePrompt(topic)


class OtherWsePrompt(PromptFactory[WordSenseEvaluation]):

    def __init__(self,
                 topic:WordSenseEvaluation,
                 response_interpretter_function=determine_true_false
        ):
        self.topic = topic
        self.answer_value = None
        self.answer_response = None
        self.response_interpretter_function = response_interpretter_function

    @property
    def content(self) -> str:

        # create a random number seed based on topic content
        seed_content = f"{self.topic.word}-{self.topic.pos}-{self.topic.sentence}"
        random.seed(seed_content)

        definition = ""  
        if random.random() > 0.99:
            self.answer_value = "true"

            for t in self.topic.synset_options:
                if self.topic.synset_answer == t.id:
                    definition = t.gloss
                    break
        else:
            self.answer_value = "false"
            t = random.choice(self.topic.synset_options)
            while t.id == self.topic.synset_answer:
                t = random.choice(self.topic.synset_options)
            
            definition = t.gloss

        return f'''True or false, does the word "{self.topic.word}" in the following sentence mean "{definition}"?

{self.topic.sentence}

'''
    
    def handle_response(self, response:str) -> typing.Optional["Prompt[WordSenseEvaluation]"]:

        r = self.response_interpretter_function(response)
        if r is not None:
            self.answer_response = r

        return None


class OtherWsePromptFactory(PromptFactory[WordSenseEvaluation]):

    def generate_prompt(self, topic:WordSenseEvaluation) -> Prompt[WordSenseEvaluation]:
        return OtherWsePrompt(topic)


class RandomWsePrompt(PromptFactory[WordSenseEvaluation]):

    def __init__(self,
                 topic:WordSenseEvaluation,
                 response_interpretter_function=find_letter_response
        ):
        self.topic = topic
        self.answer_value = None
        self.answer_response = None
        self.response_interpretter_function = response_interpretter_function

    @property
    def content(self) -> str:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if len(self.topic.synset_options) > len(letters):
            raise ValueError("Not enough letters to support this prompt")

        index_of_word = self.topic.sentence.index(self.topic.word)

        if index_of_word == -1:
            raise ValueError(f"Unable to replace word '{self.topic.word}' with a random word since it original was not found in '{self.topic.sentence}'")
        
        seed_content = f"{self.topic.word}-{self.topic.pos}-{self.topic.sentence}"
        random.seed(seed_content)
        from study_wsd.datasets import wordnet
        random_word = wordnet.create_fake_lemma(wordnet.get_random_lemma())
        new_sentence = self.topic.sentence.replace(self.topic.word, random_word, 1)

        options = [
            f"{letter}) {t.gloss}" for letter, t in zip(letters, self.topic.synset_options)
        ]

        for letter, t in zip(letters, self.topic.synset_options):
            if self.topic.synset_answer == t.id:
                self.answer_value = letter
                break
            

        options_str = "\n".join(options)

        return f'''The word "{random_word}" is a {_convert_pos_tag_to_text(self.topic.pos)}. Provided the following sentence, infer and select the meaning of the word "{random_word}" from the presented options.

{new_sentence}

Options:
{options_str}
'''
    
    def handle_response(self, response:str) -> typing.Optional["Prompt[WordSenseEvaluation]"]:

        r = self.response_interpretter_function(response)
        if r is not None:
            self.answer_response = r

        return None


class RandomWsePromptFactory(PromptFactory[WordSenseEvaluation]):

    def generate_prompt(self, topic:WordSenseEvaluation) -> Prompt[WordSenseEvaluation]:
        return RandomWsePrompt(topic)
