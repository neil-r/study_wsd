import xml.etree.ElementTree as ET
from study_wsd import wse
from study_wsd.datasets import babelnet_api


def _get_root_word(base_word:str, synset_obj) -> str:
    root_word = None
    for sense in synset_obj["senses"]:
        if (
            sense["properties"]["fullLemma"] == base_word or 
            sense["properties"]["simpleLemma"] == base_word or
            sense["properties"]["fullLemma"] == base_word.lower() 
        ):
            root_word = base_word
            break
    
    if root_word is None:
        if base_word.endswith("ies"):
            root_word = f"{base_word[:-3]}y"
        elif base_word.endswith("iest"):
            root_word = f"{base_word[:-4]}y"
        elif base_word.endswith("s") and not base_word.endswith("es"):
            root_word = f"{base_word[:-1]}"
        else:
            r_base_word = f"{base_word[:-4]}"
            if base_word.endswith("ing"):
                r_base_word = f"{base_word[:-3]}"
            elif base_word.endswith("ied"):
                r_base_word = f"{base_word[:-3]}y"
            elif base_word.endswith("ed"):
                r_base_word = f"{base_word[:-2]}"
            for sense in synset_obj["senses"]:
                if (
                    sense["properties"]["fullLemma"].startswith(r_base_word) or 
                    sense["properties"]["simpleLemma"].startswith(r_base_word) or
                    sense["properties"]["fullLemma"] == base_word.lower() 
                ):
                    root_word = sense["properties"]["fullLemma"]
                    break
    return root_word

def _get_root_word2(base_word:str, synset_obj) -> str:
    from study_wsd.datasets import babelnet_rpc_api
    root_word = None
    for sense in synset_obj.senses(babelnet_rpc_api.Language.EN):
        if (
            sense.full_lemma == base_word or 
            sense.lemma == base_word or
            sense.full_lemma.lower() == base_word.lower() 
        ):
            root_word = base_word
            break
    
    if root_word is None:
        if base_word.endswith("ies"):
            root_word = f"{base_word[:-3]}y"
        elif base_word.endswith("iest"):
            root_word = f"{base_word[:-4]}y"
        elif base_word.endswith("s") and not base_word.endswith("es"):
            root_word = f"{base_word[:-1]}"
        else:
            r_base_word = f"{base_word[:-4]}"
            if base_word.endswith("ing"):
                r_base_word = f"{base_word[:-3]}"
            elif base_word.endswith("ied"):
                r_base_word = f"{base_word[:-3]}y"
            elif base_word.endswith("ed"):
                r_base_word = f"{base_word[:-2]}"
            for sense in synset_obj.senses(babelnet_rpc_api.Language.EN):
                if (
                    sense.full_lemma.startswith(r_base_word) or 
                    str(sense.lemma).startswith(r_base_word) or
                    sense.full_lemma.lower() == base_word.lower() 
                ):
                    root_word = str(sense.lemma)
                    break
    return root_word

def _construct_wsd_from_http_api(babel_net_id:str, pos:str, word:str, sentence:str) -> wse.WordSenseEvaluation:
    synset_options = []

    synset_options_raw = babelnet_api.get_synsets(word=word, pos=pos)
    
    for option_raw in synset_options_raw:
        synset_option_id = option_raw["id"]
        synset_details = babelnet_api.get_synset_details(synset_option_id)
        if len(
            synset_details["glosses"]
        ) > 0:
            gloss = synset_details["glosses"][0]["gloss"]
            synset_options.append(wse.SynsetOption(synset_option_id, gloss))
    return wse.WordSenseEvaluation(
        sentence,
        word=word,
        synset_answer=babel_net_id,
        synset_options=synset_options,
        pos=pos
    )

valid_sources = {"WN", "BABELNET"}
def _construct_wsd_from_rpc_api(babel_net_id:str, pos:str, word:str, sentence:str) -> wse.WordSenseEvaluation:
    from study_wsd.datasets import babelnet_rpc_api
    synset_options = []

    # root_synset = babelnet_rpc_api.get_synset_details(babel_net_id)
    # print(root_synset.tags)

    # ensure word is a root word, if not replace with root word
    synset_options_raw = babelnet_rpc_api.get_synsets(word=word, pos=pos)
    
    for option_raw in synset_options_raw:
        synset_option_id = option_raw.id
        synset_details = babelnet_rpc_api.get_synset_details(synset_option_id)
        valid_source = synset_option_id.id == babel_net_id
        # print("Sources")
        for source in synset_details.sense_sources:
            if source.is_from_any_wordnet or source.is_from_babelnet:
                valid_source = True
            #print(source)
        if valid_source:
            gloss = synset_details.main_gloss(babelnet_rpc_api.Language.EN)
            if gloss != None:
                #if len(synset_details.glosses(language=babelnet_rpc_api.Language.EN)) > 0:
                #    gloss = synset_details.glosses(language=babelnet_rpc_api.Language.EN)[0].gloss
                synset_options.append(wse.SynsetOption(synset_option_id.id, gloss.gloss))
            else:
                print(f"Skipping option since it doesn't appear to have a gloss {synset_option_id}")
    return wse.WordSenseEvaluation(
        sentence,
        word=word,
        synset_answer=babel_net_id,
        synset_options=synset_options,
        pos=pos
    )

def get_wsd_evaluations(xml_file_path:str, solution_key_file_path:str, http_api:bool = False, dataset_id=None):
    wsd_evaluations = []
    # solution key content snippet
    '''
senseval2.d000.s000.t000 bn:00005928n
senseval2.d000.s000.t001 bn:00017671n
senseval2.d000.s000.t002 bn:00108295a bn:00108382a
    '''
    instance_to_synset_map = {}
    with open(solution_key_file_path) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            instance_to_synset_map[parts[0]] = parts[1]


    # XML content snippet
    '''
    <corpus lang="en" source="senseval2_senseval3_semeval2010_semeval2013_semeval2015">
<text id="senseval2.d000">
<sentence id="senseval2.d000.s000">
<wf lemma="the" pos="DET">The</wf>
<instance id="senseval2.d000.s000.t000" lemma="art" pos="NOUN">art</instance>

    '''
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for f_node in root:
        #if len(wsd_evaluations) > 10:
        #    break
        s_count = 0
        if f_node.tag == "text" and (dataset_id is None or f_node.attrib["id"].startswith(dataset_id)):
            text_id = f_node.attrib["id"]
            for s_node in f_node:
                text_order_id = f"{s_count}"
                s_count += 1
                #if len(wsd_evaluations) > 10:
                #    break
                if s_node.tag == "sentence":
                    text_parts = []

                    evaluation_tuples = []
                    for t_node in s_node:
                        
                        text_parts.append(t_node.text)
                        if t_node.tag == "instance":
                            evaluation_tuples.append((t_node.text, t_node.attrib["id"], t_node.attrib["pos"], t_node.attrib["lemma"]))
                    regular_sentence = " ".join(text_parts)
                     # remove extra spaces
                    regular_sentence = regular_sentence.replace(" 's ", "'s ")
                    regular_sentence = regular_sentence.replace("``", "\"")
                    regular_sentence = regular_sentence.replace("\" ", "\"", 1)
                    regular_sentence = regular_sentence.replace(" \" ", "\" ", 1)
                    regular_sentence = regular_sentence.replace(" \" ", " \"", 1)
                    regular_sentence = regular_sentence.replace(" \" ", "\" ", 1)
                    regular_sentence = regular_sentence.replace(" ,", ",")
                    regular_sentence = regular_sentence.replace(" .", ".")
                    regular_sentence = regular_sentence.replace("( ", "(")
                    regular_sentence = regular_sentence.replace(" )", ")")
                    regular_sentence = regular_sentence.replace(") .", ").")
                    regular_sentence = regular_sentence.replace(" ?", "?")
                    regular_sentence = regular_sentence.replace(" !", "!")
                    regular_sentence = regular_sentence.replace("s ' ", "s' ")
                    regular_sentence = regular_sentence.replace(" ;", ";")
                    regular_sentence = regular_sentence.replace(" n't", "n't")
                    regular_sentence = regular_sentence.replace(" 'm", "'m")
                    regular_sentence = regular_sentence.replace(" 're", "'re")
                    regular_sentence = regular_sentence.replace(" 'd", "'d")
                    regular_sentence = regular_sentence.replace("&amp;", "&")
                    regular_sentence = regular_sentence.replace(" %", "%")

                    if regular_sentence.endswith("\""):
                        import re
                        regular_sentence = re.sub(' \"$','\"', regular_sentence)
                    for e in evaluation_tuples:
                        print(e)
                        print(regular_sentence)
                        
                        word = e[0]
                        lemma = e[3]
                        pos = e[2]
                        babel_net_id = instance_to_synset_map[e[1]]

                        if http_api:
                            wse = _construct_wsd_from_http_api(babel_net_id, pos, lemma, regular_sentence)    
                        else:
                            wse = _construct_wsd_from_rpc_api(babel_net_id, pos, lemma, regular_sentence)
                            
                        if wse is not None:
                            wse.word = word # replace lemma with word in sentenece
                            wse.text_id = text_id
                            wse.text_order_id = text_order_id
                            wsd_evaluations.append(wse)

    return wsd_evaluations

if __name__ == "__main__":

    import babelnet as bn
    print(bn.version())

    dataset_ids = [
        "senseval2",
        "senseval3",
        "semeval2010",
        "semeval2013",
        "semeval2015"
    ]

    for dataset_id in dataset_ids:
        evaluations = get_wsd_evaluations(
            "WSD_Evaluation_Framework/xl-wsd-data/evaluation_datasets/test-en/test-en.data.xml",
            "WSD_Evaluation_Framework/xl-wsd-data/evaluation_datasets/test-en/test-en.gold.key.txt",
            dataset_id=dataset_id
        )
        import json
        with open(f"{dataset_id}_evaluations.json", "w") as f:
            f.write(json.dumps([e.to_json_complete() for e in evaluations],indent=True))
