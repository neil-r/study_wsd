from nltk.corpus import semcor
from nltk.corpus import wordnet as wn

import typing
import wse
import wse_prompts
import db
import testing_model
import time


# Prepare the creator of the prompts
prompt_factory = wse_prompts.DefaultWsePromptFactory()

# Prepare the model that reads and responds to the prompt
discussion_model_factory = testing_model.SimpleDiscussionStrategyFactory()

# Prepare the database that will store the discussion results
database = db.DatabaseSqlLite()


# Create Word Sense Disambigutation Evalutions from the semcor dataset
wse_evaluations:typing.List[wse.WordSenseEvaluation] = []

# Access SemCor instances
sents = semcor.tagged_sents(tag="both")

# Print the first few instances for demonstration
for sent in sents:
    regular_sentence = " ".join(t.leaves()[0] for t in sent)

    # remove extra spaces
    regular_sentence = regular_sentence.replace(" 's ", "'s ")
    regular_sentence = regular_sentence.replace(" `` ", " `")
    regular_sentence = regular_sentence.replace(" '' ", "' ")
    regular_sentence = regular_sentence.replace(" ,", ",")
    regular_sentence = regular_sentence.replace(" .", ".")

    for t in sent:
        # print(t)

        p = str(t[0])

        # Only process the nouns, ignore proper nouns NNP*
        if p.startswith("(NN") and not p.startswith("(NNP"):
            lemma = t._label
            if not hasattr(lemma, "_synset"):
                print(f"Skipping word {lemma} since it does not appear to be related to a wordnet synset.")
                continue
            synset = lemma._synset
            # print(lemma)
            word, _ = lemma._key.split("%")
            # lookup all the senses for a word from wordnet
            synset_options = wn.synsets(word, pos=wn.NOUN)
            
            '''
            for a_synset in synset_options:
                definition = a_synset._definition
                if synset._offset == a_synset._offset:
                    # at least one should match the annotated word in the sentence
                    print(f"SAME: {a_synset}")
                else:
                    print(f"DIF: {a_synset}")
            '''
            if synset_options is None or len(synset_options) <= 1:
                print(f"Skipping word {word} since it only has one synset.")
                continue
            
            wse_evaluations.append(wse.WordSenseEvaluation(
                regular_sentence, word, synset, synset_options
            ))

print(f"The number of word sense evaluations is {len(wse_evaluations)}")

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
    