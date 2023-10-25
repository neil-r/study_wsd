import typing


class Message:
    def __init__(self, role:str, content:str):
        self.role = role
        self.content = content


class Discussion:
    def __init__(self):
        self.messages = []
    
    def to_json(self):
        return list(
            {"role":msg.role, "content":msg.content} for msg in self.messages
        )


class DiscussionStrategy:
    
    def speak(self, content, role:str="user") -> typing.Tuple[Message, typing.Any]:
        raise NotImplementedError("Abstract class, implement")

class DiscussionStrategyFactory:

    def create(self) -> DiscussionStrategy:
        raise NotImplementedError("Abstract class, implement")
