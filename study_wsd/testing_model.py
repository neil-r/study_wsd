import study_wsd.discussion as discussion


class SimpleDiscussionStrategyFactory:

    def __init__(self):
        pass
    def create(self):
        return SimpleDiscussionStrategy()
    
    @property
    def model_id(self):
        return "simpleA"


class SimpleDiscussionStrategy:

    def __init__(self):
        self.discussion = discussion.Discussion()

    def speak(self, content, role="user"):

        self.discussion.messages.append(discussion.Message(role,content))

        # Creating a simple response that always picks A
        response_msg = discussion.Message(
            role="system",
            content="A)",
        )        
        self.discussion.messages.append(response_msg)

        return response_msg, response_msg
