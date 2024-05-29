# Word sense disambiguation (WSD) Experiment
The un-centralized development of language often results in ambiguities in the words used to represent things and concepts. This results in the need by readers and interpreters of language to leverage context to resolve ambiguities, i.e., word sense disambiguation (WSD). In this experiment, we evaluate the capability of LLMs to perform WSD. The experiment looks into several different aspects of WSD. Each question below forms a foundation for each aspect. To explore each question, assumptions and the setup of a sub-experiment are listed.  The experiment considers multiple LLMs that vary in size and origin. 

## Evaluation Datasets

The evaluation datasets are derived from BabelNet, WordNet, SemEval, SensEval, and SemCor. They are saved as json files in the root directory of this repository. Code was used to generate these datasets from the original data sources. Some manual cleaning was done on the generated semeval2015 dataset after executing the dataset generation code to fix some odd parsing and formatting issues. We mainly used the semeval2015 dataset for the initial execution of this experiment. The other datasets may still have a few odd parsing and formatting issues.

To recreate the datasets, download and extract the datasets containing SemEval from here: https://sapienzanlp.github.io/xl-wsd/. WordNet and SemCor can be downloaded by running load_data.py. BabelNet needs to be downloaded and installed using their instructions https://babelnet.org/downloads. The study_wsd.datasets module includes code to create evaluation datasets from SenEval, BabelNet, and SemEval datasets.

## Question 1: What is the capability of LLMs to accurately identify the sense of a word?

This question investigates the ability of LLMs to identify a word's proper sense given a listing of alternative word senses and a single sentence providing context to the word's usage.

### Assumptions and Setup

0. A word in a sentence is annotated with its part-of-speech and the intended sense. The word's alternative senses are gathered.
1. The sentence and all senses for the word are listed as options in a prompt and the LLM must select the correct one.
2. LLMs process the prompt and respond with the selected sense.
3. The selection is parsed from the LLM response and gathered in a database.

### Example Prompt (see DirectWsePrompt in study_wsd.wse_prompts.py for implementation logic)


What is the meaning of the word "investigation" in "The Fulton said Friday an investigation of Atlanta's recent primary produced 'no evidence' that any irregularities took."?


Options:
1. an inquiry into unfamiliar or questionable activities
2. the work of inquiring into something thoroughly and systematically


## Question 2: What is the capability of LLMs to accurately identify a sense of a word that is not implied?

This question investigates the ability of LLMs to internalize definitions of alternative word senses through their training and identify when a prompt fails to identify the true sense.

### Assumptions and Setup

0. A word in a sentence is annotated with its part-of-speech and the intended sense. The word's alternative senses are gathered.
1. A prompt is generated asking to determine if the true definition sense of a word in the given sentence is provided.
2. LLMs process the prompt and respond with true or false.
3. The selection is parsed from the LLM response and gathered in a database.

### Example Prompt (see OtherWsePrompt in study_wsd.wse_prompts.py for implementation logic)

True or false, does the word "investigation" in the following sentence mean "the work of inquiring into something thoroughly and systematically'"?

The Fulton said Friday an investigation of Atlanta's recent primary produced 'no evidence' that any irregularities took.

## Question 3: What is the capability of LLMs to accurately identify the sense of a new word from one-shot learning prompt that provides an example of the word in a sentence?

### Assumptions and Setup

0. A word in a sentence is annotated with its part-of-speech and the intended sense. The word's alternative senses are gathered.
1. A new made-up word is generated and replaces the original word in the given sentence.
2. The revised sentence and all senses for the word are listed as options in a prompt and the LLM must select the correct one.
3. LLMs process the prompt and respond with the selected sense.
4. The selection is parsed from the LLM response and gathered in a database.

### Example Prompt (see RandomWsePrompt in study_wsd.wse_prompts.py for implementation logic)

What is the meaning of the word "inbestication" in "The Fulton said Friday an inbestication of Atlanta's recent primary produced 'no evidence' that any irregularities took."?


Options:
1. an inquiry into unfamiliar or questionable activities
2. the work of inquiring into something thoroughly and systematically
