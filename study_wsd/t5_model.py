import study_wsd.discussion as discussion
from transformers import T5Tokenizer, T5ForConditionalGeneration


class T5DiscussionStrategyFactory:

    def __init__(self,t5_name="t5-small"):
        self.tokenizer = T5Tokenizer.from_pretrained(t5_name)
        self.model = T5ForConditionalGeneration.from_pretrained(t5_name)
        self.t5_name = t5_name
        pass

    def create(self):
        return T5DiscussionStrategy(self.model,self.tokenizer)
    
    @property
    def model_id(self):
        return f"huggingface-{self.t5_name}"


class T5DiscussionStrategy:

    def __init__(self, model, tokenizer):
        self.discussion = discussion.Discussion()
        self.model = model
        self.tokenizer = tokenizer

        

    def speak(self, content, role="user"):

        self.discussion.messages.append(discussion.Message(role,content))

        # Creating a simple response that always picks A
        input_ids = self.tokenizer(f"{content}", return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids)
        response_content = self.tokenizer.decode(outputs[0], skip_special_tokens=True)


        response_msg = discussion.Message(
            role="system",
            content=response_content,
        )        
        self.discussion.messages.append(response_msg)

        return response_msg, response_msg
