import typing
import dotenv

import study_wsd.wse as wse
import study_wsd.wse_prompts as wse_prompts
import study_wsd.db as db
import study_wsd.testing_model as testing_model
from study_wsd.conduct_evaluations import conduct_evaluations
import study_wsd.datasets.semcor as semcor
from study_wsd.datasets import babelnet_api
from study_wsd import t5_model, llama2_7B_model, llama2_13B_model, guanaco_7B_model, palm_model, vicuna_7B_model, openai_model


# Load environment variables from local ".env" file
dotenv.load_dotenv()

# Prepare the creator(s) of the prompts
p_factories = [
  wse_prompts.DefaultWsePromptFactory(),
  # wse_prompts.DirectWsePromptFactory(),
]

# Prepare the model(s) that reads and responds to the prompt
dm_factories = [
  # testing_model.SimpleDiscussionStrategyFactory(),
  # t5_model.T5DiscussionStrategyFactory(),
  # guanaco_7B_model.GuanacoDiscussionStrategyFactory(),
  # vicuna_7B_model.VicunaDiscussionStrategyFactory(),
  # palm_model.PalmDiscussionStrategyFactory(),
  # llama2_13B_model.Llama2_13BDiscussionStrategyFactory(),
  # llama2_7B_model.Llama2_7BDiscussionStrategyFactory(),
  # openai_model.OpenAiDiscussionStrategyFactory(model="gpt-3.5-turbo-1106"),
  openai_model.OpenAiDiscussionStrategyFactory(model="gpt-4-0613")
]

# Prepare the database that will store the discussion results
database = db.DatabaseSqlLite()

# Load the Word Sense Disambigutation Evalutions and process them
datasets = [
  "semcor_evaluations.json",
  "semeval2010_evaluations.json",
  "semeval2013_evaluations.json",
  "semeval2015_evaluations.json",
  "senseval2_evaluations.json",
  "senseval3_evaluations.json"
]

for dataset_file_path in datasets:
  wse_evaluations:typing.List[wse.WordSenseEvaluation] = wse.WordSenseEvaluation.Load_from_json(dataset_file_path)

  print(f"The number of word synset evaluations is {len(wse_evaluations)}")

  for prompt_factory in p_factories:
    for discussion_model_factory in dm_factories:
      # conduct_evaluations(wse_evaluations[:100], prompt_factory, database, discussion_model_factory)
      pass
