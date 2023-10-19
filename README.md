# Word sense disambiguation (WSD) Experiment

The un-centrized development of written language often result in ambiguties in the words used to represent things and concepts. This results in the need by readers of written langauge to leverage context to resolve ambiguties, i.e., word sense disambigutation (WSD). In this experiment, we evalute the capability of LLMs to perform WSD. The experiment looks into a number of different aspects of WSD. Each question below forms a foundation for each aspect. To explore each question, assumptions and the setup of a sub-experiment is listed.  The experiment considers two or more LLMs: something like OpenAI GPT 3.5, OpenAI GPT 4.0, PALM, and LLAMA. 

## Question 1: What is the capability of LLMs to accurately identify the sense of a word?

### Assumptions and Setup

0. SemCor and Wordnet datasetse are used. SemCor provides annotated sentences. SemCor annotations identify the sense/definition from WordNet for each word in the sentence.

1. All senses for a word are provided and the LLM must select the correct one.
2. Different prompts are tested to evaluate "How does the prompt strategy affect LLMs performance?"
3. Each 

### Example Prompt


What is the meaning of the word "investigation" in "The Fulton said Friday an investigation of Atlanta's recent primary produced 'no evidence' that any irregularities took ."?


Options:
1. an inquiry into unfamiliar or questionable activities
2. the work of inquiring into something thoroughly and systematically'


## Question 2: What is the capability of LLMs to accurately identify a sense of a word that is not implied?

This question investigates the ability of LLMs to internalize defintiions of words through their training and identify when a prompt fails to identify the true defintiion.

### Assumptions and Setup

1. An "Other" option is provided in the prompt to allow the LLM to indicate none of the provided suggested senses match the true sense-usage in the sentence.
2. Different prompts are tested to evaluate "How does the prompt strategy affect LLMs performance?"

### Example Prompt

What is the meaning of the word "investigation" in "The Fulton said Friday an investigation of Atlanta's recent primary produced 'no evidence' that any irregularities took ."?


Options:
1. the work of inquiring into something thoroughly and systematically'
2. Other


## Question 3: What is the capability of LLMs to accurately describe a definition of a new word from one-shot learning prompt that provides an example of the word in a paragraph?

### Assumptions and Setup

0. Verbs and nouns are created. 
1. New made-up words are generated to represent an advanced concept. Attributes of the advanced concept are identified. A passge of text uses the word with carefully constructured text that provides hints to the attributes of the advanced concept.
2. LLMs are asked to create a definition of the made-up word.
3. The responses from each LLM are ranked (or scored?) according to the number of attributes it captured in the defintion.

### Example Prompt



## Question 4: What is the capability of LLMs to identify words within a passage of text that uses two different senses?

### Assumptions and Setup

0. Verbs and nouns are created. 
1. New made-up words are generated to represent an advanced concept. Attributes of the advanced concept are identified. A passge of text uses the word with carefully constructured text that provides hints to the attributes of the advanced concept.
2. LLMs are asked to create a definition of the made-up word.
3. The responses from each LLM are ranked (or scored?) according to the number of attributes it captured in the defintion.

### Example Prompt



## Question 5: How can the OpenAI API be used to support WSD?



### Assumptions and Setup

0. Create a function to lookup wordnet senses.
1. Create a prompt strategy to take a sentence and the function to generate a prompt and handle responses to run function.
2. 

### Example Prompt
