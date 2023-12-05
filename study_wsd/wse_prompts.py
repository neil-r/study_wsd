import typing
import re

from study_wsd.prompt import PromptFactory, Prompt
from study_wsd.wse import WordSenseEvaluation


def find_letter_response(response:str) -> typing.Optional[str]:
    l_response = None

    i = response.find(")")
    # ensure this character was found, and if so, return previous character
    if i > 0:
        l_response = response[i-1]

    return l_response


def find_letter_response_llama(response:str) -> typing.Optional[str]:
    l_response = None

    pattern = r'### ANSWER: \[/INST\].*?\b([A-Z])\b(?=\))'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        l_response = match.group(1)

    return l_response


def find_letter_response_vicuna(response:str) -> typing.Optional[str]:
    l_response = None

    # pattern = r'### ANSWER:[^)]*?([A-Z])\)'
    pattern = r'### ANSWER:[\s\S]*?([A-Z])\)'
    match = re.search(pattern, response)
    if match:
        l_response = match.group(1)

    return l_response


def find_letter_response_guanaco(response:str) -> typing.Optional[str]:
    l_response = None

    pattern = r'ANSWER:[^A-Z]*([A-Z])'
    match = re.search(pattern, response)
    if match:
        l_response = match.group(1)

    return l_response 


def find_letter_response_palm(response:str) -> typing.Optional[str]:
    l_response = response

    return l_response 
    

class DefaultWsePrompt(PromptFactory[WordSenseEvaluation]):

    def __init__(self,
                 topic:WordSenseEvaluation,
                 response_interpretter_function=find_letter_response_vicuna
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
                 response_interpretter_function=find_letter_response_vicuna
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
