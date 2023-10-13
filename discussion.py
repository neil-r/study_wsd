

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