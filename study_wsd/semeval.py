import xml.etree.ElementTree as ET
from study_wsd import wse
from study_wsd import babelnet_api


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


def get_wsd_evaluations(xml_file_path:str, solution_key_file_path:str):
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
        if f_node.tag == "text":
            for s_node in f_node:
                if s_node.tag == "sentence":
                    text_parts = []

                    evaluation_tuples = []
                    for t_node in s_node:
                        
                        text_parts.append(t_node.text)
                        if t_node.tag == "instance":
                            evaluation_tuples.append((t_node.text, t_node.attrib["id"], t_node.attrib["pos"]))
                    regular_sentence = " ".join(text_parts)
                     # remove extra spaces
                    regular_sentence = regular_sentence.replace(" 's ", "'s ")
                    regular_sentence = regular_sentence.replace(" `` ", " `")
                    regular_sentence = regular_sentence.replace(" '' ", "' ")
                    regular_sentence = regular_sentence.replace(" ,", ",")
                    regular_sentence = regular_sentence.replace(" .", ".")
                    regular_sentence = regular_sentence.replace("( ", "(")
                    regular_sentence = regular_sentence.replace(" )", ")")
                    regular_sentence = regular_sentence.replace(") .", ").")
                    regular_sentence = regular_sentence.replace(" ?", "?")
                    regular_sentence = regular_sentence.replace(" !", "!")
                    regular_sentence = regular_sentence.replace(" %", "%")
                    for e in evaluation_tuples:
                        print(e)
                        print(regular_sentence)
                        synset_options = []
                        word = e[0]
                        pos = e[2]
                        babel_net_id = instance_to_synset_map[e[1]]

                        root_synset = babelnet_api.get_synset_details(babel_net_id)

                        # ensure word is a root word, if not replace with root word
                        root_word = _get_root_word(word, root_synset)
                        if root_word.find("-") >= 0:
                            synset_options_raw = babelnet_api.get_synsets(word=root_word.replace("-",""), pos=pos)
                            if len(synset_options_raw) == 0:
                                synset_options_raw = babelnet_api.get_synsets(word=root_word, pos=pos)
                        else:    
                            synset_options_raw = babelnet_api.get_synsets(word=root_word, pos=pos)
                        
                        for option_raw in synset_options_raw:
                            synset_option_id = option_raw["id"]
                            synset_details = babelnet_api.get_synset_details(synset_option_id)
                            if len(
                                synset_details["glosses"]
                            ) > 0:
                                gloss = synset_details["glosses"][0]["gloss"]
                                synset_options.append(wse.SynsetOption(synset_option_id, gloss))
                        wsd_evaluations.append(
                            wse.WordSenseEvaluation(
                                regular_sentence,
                                word=word,
                                synset_answer=babel_net_id,
                                synset_options=synset_options,
                                pos=pos
                            )
                        )

    return wsd_evaluations
