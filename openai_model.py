import openai
import discussion


class OpenAiDiscussionStrategyFactory:

    def __init__(self, model):
        self.model = model
    
    def create(self):
        return OpenAiDiscussionStrategy(self.model)


class OpenAiDiscussionStrategy:

    def __init__(self, model):
        self.discussion = discussion.Discussion()
        self.model = model

    def speak(self, content, role="user"):

        self.discussion.messages.append(discussion.Message(role,content))

        messages_json = self.discussion.to_json()

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages_json
        )

        response_msg = discussion.Message(
            role=response.choices[0].message.role,
            content=response.choices[0].message.content,
        )        
        self.discussion.messages.append(response_msg)


        return response_msg, response