from study_wsd import openai_model
from study_wsd import wse_prompts
from study_wsd import wse


eval1 = wse_prompts.WordSenseEvaluation(
  sentence="If you need more information about your medical condition or your treatment, read the Package Leaflet (also part of the EPAR) or contact your doctor or pharmacist.",
  word="need",
  pos="VERB",
  synset_answer="probe.n.01",
  synset_options=[
    wse.SynsetOption('probe.n.01', 'an inquiry into unfamiliar or questionable activities'),
    wse.SynsetOption('investigation.n.02', 'the work of inquiring into something thoroughly and systematically')
  ]
)

eval2 = wse_prompts.WordSenseEvaluation(
  sentence='Nevertheless, "we feel that in Fulton should receive some portion of these available funds", the jurors said.',
  word="portion",
  pos="NOUN",
  synset_answer="parcel.n.02",
  synset_options=[
    wse.SynsetOption('part.n.01', 'something determined in relation to something that includes it'),
    wse.SynsetOption('part.n.02', 'something less than the whole of a human artifact'),
    wse.SynsetOption('parcel.n.02', 'the allotment of some amount by dividing something'),
    wse.SynsetOption('share.n.01', 'assets belonging to or due to or contributed by an individual person or group'),
    wse.SynsetOption('fortune.n.04', 'your overall circumstances or condition in life (including everything that happens to you)'),
    wse.SynsetOption('dowry.n.01', 'money or property brought by a woman to her husband at marriage'),
    wse.SynsetOption('helping.n.01', 'an individual quantity of food or drink taken as part of a meal')
  ]
)

prompt2 = wse_prompts.DefaultWsePrompt(eval2)

discussion_strategy = openai_model.OpenAiDiscussionStrategy("gpt-3.5-turbo-1106")

response = discussion_strategy.speak(prompt2.content)

print(response)
