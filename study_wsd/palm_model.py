import study_wsd.discussion as discussion
import google.generativeai as palm


class PalmDiscussionStrategyFactory:

    def __init__(self, model_name="PaLM"):
        palm.configure(api_key='AIzaSyDnJMmBI3VXZBtavMugrU07YpkMkZicPpI')
        models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
        self.model = models[0].name
        self.model_name = model_name
        pass

    def create(self):
        return PalmDiscussionStrategy(self.model)
    
    @property
    def model_id(self):
        return f"{self.model_name}"


class PalmDiscussionStrategy:

    def __init__(self, model):
        self.discussion = discussion.Discussion()
        self.model = model


    def speak(self, content, role="user"):

        self.discussion.messages.append(discussion.Message(role,content))
        
        # Generate and store response from llm
        completion = palm.generate_text(
            model=self.model,
            prompt=content,
            temperature=0,
            max_output_tokens=10,
        )
        response_content = completion.result

        response_msg = discussion.Message(
            role="system",
            content=response_content,
        )        
        self.discussion.messages.append(response_msg)

        return response_msg, response_msg
