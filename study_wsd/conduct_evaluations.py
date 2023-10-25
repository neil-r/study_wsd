import time
import typing

import study_wsd.wse as wse
import study_wsd.prompt as prompt
import study_wsd.db as db
import study_wsd.discussion as discussion

def conduct_evaluations(
  wse_evaluations: typing.Iterator[wse.WordSenseEvaluation],
  prompt_factory: prompt.PromptFactory,
  database: db.DatabaseSqlLite,
  discussion_model_factory: discussion.DiscussionStrategyFactory
):
  for w in wse_evaluations:
      prompt = prompt_factory.generate_prompt(w)
      prompt_strategy_name = prompt.__class__.__name__

      # first check to ensure not already in database
      if database.has_wsd_discussion(
          w,
          prompt_strategy_name
      ):
          print("Skipping evalution since it is already in database")
          continue
      

      start = time.time()
      
      d_model = discussion_model_factory.create()
      prompt_txt = prompt.content
      response = d_model.speak(prompt_txt)
      follow_on_prompt = prompt.handle_response(response[0].content)
      while follow_on_prompt is not None:
          follow_on_response = d_model.speak(follow_on_prompt.content)
          follow_on_prompt = follow_on_prompt.handle_response(follow_on_response[0].content)
      end = time.time()

      database.add_wsd_discussion(
          w,
          log=d_model.discussion.to_json(),
          prompt_strategy=prompt_strategy_name,
          answer_value=prompt.answer_value,
          discussion_duration=end-start,
          answer_response=prompt.answer_response,
          correct=prompt.answer_value==prompt.answer_response,
      )