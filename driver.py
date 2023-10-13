from nltk.corpus import semcor
from nltk.corpus import wordnet as wn

import typing
import wse
import wse_prompts
import db
import testing_model
import time

# Download SemCor dataset if not already downloaded
#nltk.download('semcor')

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
for sent in sents[:5]:
    print(sent)
    for t in sent:
        # print(t)
        regular_sentence = " ".join(t.leaves()[0] for t in sent)

        regular_sentence = regular_sentence.replace(" 's ", "'s ")
        regular_sentence = regular_sentence.replace(" `` ", " `")
        regular_sentence = regular_sentence.replace(" '' ", "' ")

        p = str(t[0])

        # Only process the nouns
        if p.startswith("(NN"):
            
            lemma = t._label
            synset = lemma._synset
            print(lemma)
            word, _ = lemma._key.split("%")
            # lookup all the senses for a word from wordnet
            synset_options = wn.synsets(word, pos=wn.NOUN)
            for a_synset in synset_options:
                definition = a_synset._definition
                if synset._offset == a_synset._offset:
                    # at least one should match the annotated word in the sentence
                    print(f"SAME: {a_synset}")
                else:
                    print(f"DIF: {a_synset}")
            
            wse_evaluations.append(wse.WordSenseEvaluation(
                regular_sentence, word, synset, synset_options
            ))

for w in wse_evaluations:
    prompt = prompt_factory.generate_prompt(w)
    prompt_strategy = prompt.__class__.__name__

    # first check to ensure not already in database
    if database.has_wsd_discussion(
        w,
        prompt_strategy
    ):
        print("Skipping evalution since it is already in database")
        continue
    

    start = time.time()
    
    d_model = discussion_model_factory.create()
    response = d_model.speak(prompt.content)
    follow_on = prompt.handle_response(response[0].content)
    while follow_on is not None:
        follow_on_response = d_model.speak(follow_on.content)
        follow_on = follow_on.handle_response(follow_on_response[0].content)
    end = time.time()

    database.add_wsd_discussion(
        w,
        log=d_model.discussion.to_json(),
        prompt_strategy=prompt_strategy,
        answer_value=prompt.answer_value,
        discussion_duration=end-start,
        answer_response=prompt.answer_response,
        correct=prompt.answer_value==prompt.answer_response,
    )
    