import typing

import study_wsd.wse as wse
import study_wsd.wse_prompts as wse_prompts
import study_wsd.db as db
import study_wsd.testing_model as testing_model
from study_wsd.conduct_evaluations import conduct_evaluations
import study_wsd.semcor as semcor
from study_wsd import babelnet_api
from study_wsd import huggingface_torch

import dotenv


# Load environment variables from local ".env" file
dotenv.load_dotenv()

# Prepare the creator of the prompts
prompt_factory = wse_prompts.DefaultWsePromptFactory()

# Prepare the model that reads and responds to the prompt
#discussion_model_factory = testing_model.SimpleDiscussionStrategyFactory()
discussion_model_factory = huggingface_torch.HuggingFaceT5DiscussionStrategyFactory()

# Prepare the database that will store the discussion results
database = db.DatabaseSqlLite()

# Create Word Sense Disambigutation Evalutions from the semcor dataset
wse_evaluations:typing.List[wse.WordSenseEvaluation] = semcor.get_semcor_wsd_evaluations() 

print(f"The number of word sense evaluations is {len(wse_evaluations)}")

conduct_evaluations(wse_evaluations, prompt_factory, database, discussion_model_factory)
