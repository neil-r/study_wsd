from nltk.corpus import semcor
from nltk.corpus import wordnet as wn

import typing

import study_wsd.wse as wse


def get_semcor_wsd_evaluations():
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
              synset_options = []
              added_map = {}
              for wn_synset in wn.synsets(word, pos=wn.NOUN):
                if wn_synset._name not in added_map:
                    synset_options.append(wse.SynsetOption(wn_synset._name, wn_synset._definition))
                    added_map[wn_synset._name] = True
                else:
                   1+2 # why here?!
                if wn_synset._name == synset._name:
                   assert wn_synset._offset == synset._offset
                      
              
              if synset_options is None or len(synset_options) <= 1:
                  print(f"Skipping word {word} since it only has one synset.")
                  continue
              
              wse_evaluations.append(wse.WordSenseEvaluation(
                  regular_sentence, word, synset._name, synset_options
              ))
  return wse_evaluations
