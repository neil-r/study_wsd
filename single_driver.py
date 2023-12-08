from study_wsd import openai_model
from study_wsd import wse_prompts
from study_wsd import wse


eval1 = wse_prompts.WordSenseEvaluation(
  sentence="The Fulton said Friday an investigation of Atlanta's recent primary produced \"no evidence\" that any irregularities took.",
  word="investigation",
  pos="NOUN",
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

eval3 = wse_prompts.WordSenseEvaluation(
  sentence='The jury further said in term end presentments that the City, which had over-all charge of the election, "deserves the praise and thanks of the City" for the manner in which the election was conducted.',
  word="manner",
  pos="NOUN",
  synset_answer="a",
  synset_options=[
    wse.SynsetOption('a', 'how something is done or how it happens'),
    wse.SynsetOption('b', 'a way of acting or behaving'),
    wse.SynsetOption('c', 'a kind'),
  ]
)

eval4 = wse_prompts.WordSenseEvaluation(
  sentence='"Only a relative handful of such reports was received", the jury said, "considering the widespread interest in the election, the number of voters and the size of city".',
  word="number",
  pos="NOUN",
  synset_answer="a",
  synset_options=[
    wse.SynsetOption('a', 'the property possessed by a sum or total or indefinite quantity of units or individuals'),
    wse.SynsetOption('b', 'a concept of quantity involving zero and units'),
    wse.SynsetOption('c', 'a short theatrical performance that is part of a longer program'),
    wse.SynsetOption('d', 'the number is used in calling a particular telephone'),
    wse.SynsetOption('e', 'a symbol used to represent a number'),
    wse.SynsetOption('f', 'one of a series published periodically'),
    wse.SynsetOption('g', 'a select company of people'),
    wse.SynsetOption('g', 'a numeral or string of numerals that is used for identification'),
    wse.SynsetOption('g', 'a clothing measurement'),
    wse.SynsetOption('g', 'the grammatical category for the forms of nouns and pronouns and verbs that are used depending on the number of entities involved (singular or dual or plural)'),
    wse.SynsetOption('g', 'an item of merchandise offered for sale'),
  ]
)

evaluations = [eval1, eval2, eval3, eval4]
stratgies = [
  wse_prompts.RandomWsePrompt,
  # wse_prompts.OtherWsePrompt,
]

for Strategy in stratgies:
  for e in evaluations:
    prompt = Strategy(e)
    print(prompt.content)

'''
discussion_strategy = openai_model.OpenAiDiscussionStrategy("gpt-3.5-turbo-1106")

response = discussion_strategy.speak(prompt2.content)
print(response)
'''


