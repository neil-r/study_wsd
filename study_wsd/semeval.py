import xml.etree.ElementTree as ET
from study_wsd import wse
from study_wsd import babelnet_api


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

                        synset_options_raw = babelnet_api.get_synsets(word=word, pos=pos)

                        for option_raw in synset_options_raw:
                            synset_option_id = option_raw["id"]
                            synset_details = babelnet_api.get_synset_details(synset_option_id)
                            if synset_details["synsetType"] != "NAMED_ENTITY" and len(
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
