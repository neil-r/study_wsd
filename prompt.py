import typing


Topic = typing.TypeVar("Topic")


class Prompt(typing.Generic[Topic]):

    @property
    def content(self) -> str:
        raise NotImplementedError("Abstract class, not implemented")
    
    def handle_response(self, response:str) -> typing.Optional["Prompt[Topic]"]:
        return None


class DialogStrategy(typing.Generic[Topic]):

    def generate_prompt(self, topic:Topic) -> Prompt[Topic]:
        raise NotImplementedError("Abstract class, not implemented")
