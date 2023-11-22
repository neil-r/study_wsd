import study_wsd.discussion as discussion
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class GuanacoDiscussionStrategyFactory:

    def __init__(self, model_name="TheBloke/guanaco-7B-GPTQ"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, 
                                                          device_map='auto', 
                                                          trust_remote_code=True, 
                                                          revision='main')
        self.model_name = model_name
        pass

    def create(self):
        return GuanacoDiscussionStrategy(self.model, self.tokenizer)
    
    @property
    def model_id(self):
        return f"{self.model_name}"


class GuanacoDiscussionStrategy:

    def __init__(self, model, tokenizer):
        self.discussion = discussion.Discussion()
        self.model = model
        self.tokenizer = tokenizer


    def speak(self, content, role="user"):

        self.discussion.messages.append(discussion.Message(role,content))

        # Generate and store response from llm
        prompt_template = f'''{content}
        ### ANSWER: '''

        input_ids = self.tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
        outputs = self.model.generate(inputs=input_ids, temperature=0.1, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=1)
        response_content = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        response_msg = discussion.Message(
            role="system",
            content=response_content,
        )        
        self.discussion.messages.append(response_msg)

        return response_msg, response_msg
