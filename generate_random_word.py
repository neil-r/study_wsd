from study_wsd.datasets import wordnet

for i in range(20):
    root_lemma = wordnet.get_random_lemma()
    made_up_lemma = wordnet.create_fake_lemma(root_lemma)
    print(root_lemma)
    print(made_up_lemma)
