import re
from study_wsd import db


database = db.DatabaseSqlLite()
llm = 'palm' #only specify if checking PaLM results
offset = 1
exitcode = ""

while exitcode != "q":
    wsd_result = database.get_wsd_evaluation(offset)
    result_str = str(wsd_result[0])

    if llm == 'palm':
        raw_pattern = r"{'role': 'system', ('content':.*?)}"
        raw_match = re.search(raw_pattern, result_str)
        if raw_match:
            raw_response = raw_match.group(1)
            print("Raw response:\n", raw_response)
        else:
            print("Raw response not found. Please check the regex.")

        parsed_pattern = r"answer_response='(.*?)'"
        parsed_match = re.search(parsed_pattern, result_str)
        if parsed_match:
            parsed_response = parsed_match.group(0)
            print("\nParsed response:\n",parsed_response)
        else:
            print("\nParsed response:\nLLM outputted \"None\" or parsed response not found.")

    else:
        raw_pattern = r"(### ANSWER:.*?)}"
        raw_match = re.search(raw_pattern, result_str)
        if raw_match:
            raw_response = raw_match.group(1)
            print("Raw response:\n", raw_response)
        else:
            print("Raw response not found. Please check the regex.")

        parsed_pattern = r"answer_response='(.*?)'"
        parsed_match = re.search(parsed_pattern, result_str)
        if parsed_match:
            parsed_response = parsed_match.group(0)
            print("\nParsed response:\n", parsed_response)
        else:
            print("Parsed response:\nLLM outputted \"None\" or parsed response not found.")

    exitcode = input("\nPress enter to continue, \"q\" to exit.")
    offset += 1
