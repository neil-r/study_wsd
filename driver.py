import typing
import dotenv

import study_wsd.wse as wse
import study_wsd.wse_prompts as wse_prompts
import study_wsd.db as db
import study_wsd.testing_model as testing_model
from study_wsd.conduct_evaluations import conduct_evaluations
import study_wsd.semcor as semcor
from study_wsd import babelnet_api
from study_wsd import t5_model, llama2_7B_model, llama2_13B_model, guanaco_7B_model, palm_model, vicuna_7B_model


# Load environment variables from local ".env" file
dotenv.load_dotenv()

# Prepare the creator of the prompts
prompt_factory = wse_prompts.DefaultWsePromptFactory()

# Prepare the model that reads and responds to the prompt
# discussion_model_factory = testing_model.SimpleDiscussionStrategyFactory()
# t5_discussion_model_factory = t5_model.T5DiscussionStrategyFactory() 
# guanaco_discussion_model_factory = guanaco_7B_model.GuanacoDiscussionStrategyFactory()
# vicuna_discussion_model_factory = vicuna_7B_model.VicunaDiscussionStrategyFactory()
# palm_discussion_model_factory = palm_model.PalmDiscussionStrategyFactory()
# llama2_13B_discussion_model_factory = llama2_13B_model.Llama2_13BDiscussionStrategyFactory()
llama2_7B_discussion_model_factory = llama2_7B_model.Llama2_7BDiscussionStrategyFactory()

# Prepare the database that will store the discussion results
database = db.DatabaseSqlLite()

# Create Word Sense Disambigutation Evalutions from the semcor dataset
wse_evaluations:typing.List[wse.WordSenseEvaluation] = semcor.get_semcor_wsd_evaluations() 

print(f"The number of word sense evaluations is {len(wse_evaluations)}")

conduct_evaluations(wse_evaluations, prompt_factory, database, llama2_7B_discussion_model_factory)
