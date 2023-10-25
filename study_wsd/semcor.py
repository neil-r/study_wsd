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
  return wse_evaluations
