import sqlite3
import typing
import json
import hashlib
import dataclasses

def convert_to_id(wse_str):
    id =  hashlib.sha256(wse_str.encode("utf-8")).hexdigest()
    return id

@dataclasses.dataclass
class WsdResult:
    evalutation_id:int
    evalution: typing.Dict
    log: typing.List
    discussion_duration: float
    prompt_strategy: str
    model_id: str
    answer_value: str
    answer_response: str
    correct: bool

class DatabaseSqlLite:


    def __init__(self, db_file_path = "data_palm.db"):
        self.db_file_path = db_file_path

        with sqlite3.connect(self.db_file_path) as c:
            cur = c.cursor()

            cur.execute("""CREATE TABLE IF NOT EXISTS wsd_results(
                evaluation_id INTEGER NOT NULL,
                evalution TEXT NOT NULL,
                log TEXT NOT NULL,
                discussion_duration REAL NOT NULL,
                prompt_strategy TEXT NOT NULL,
                model_id TEXT NOT NULL,
                answer_value TEXT NOT NULL,
                answer_response TEXT,
                correct INTEGER NOT NULL,
                PRIMARY KEY (evaluation_id, prompt_strategy, model_id));
            """)

            c.commit()
    
    def add_wsd_discussion(
        self,
        wse,
        log,
        prompt_strategy:str,
        model_id:str,
        answer_value:str,
        discussion_duration:float,
        answer_response:typing.Optional[str]=None,
        correct:bool=False,
    ):
        with sqlite3.connect(self.db_file_path) as c:
            cur = c.cursor()

            wse_content = wse.to_json()
            wse_str = json.dumps(wse_content, sort_keys=True)

            cur.execute("INSERT INTO wsd_results VALUES (?,?,?,?,?,?,?,?,?);",(
                convert_to_id(wse_str),
                wse_str,
                json.dumps(log),
                discussion_duration,
                prompt_strategy,
                model_id,
                answer_value,
                answer_response,
                1 if correct else 0
            ))

            c.commit()

    def has_wsd_discussion(self,
        wse,
        prompt_strategy,
        model_id
    ):
        with sqlite3.connect(self.db_file_path) as c:

            o = c.execute(
                "SELECT * FROM wsd_results WHERE evaluation_id = ? AND prompt_strategy = ? AND model_id = ?", (
                convert_to_id(json.dumps(wse.to_json(), sort_keys=True)),
                prompt_strategy,
                model_id
            )).fetchone()

            return o is not None
    
    def get_wsd_evaluation(self, number):
        offset = number - 1
        print(f'\n***Evaluation #{offset}')
        with sqlite3.connect(self.db_file_path) as c:
            results = c.execute(
                "SELECT * FROM wsd_results WHERE evaluation_id IN (SELECT evaluation_id FROM wsd_results ORDER BY evaluation_id LIMIT ?, 1)", (
                offset,
            )).fetchmany()

            if results is not None:
                return list(WsdResult(o[0],json.loads(o[1]),json.loads(o[2]),o[3],o[4],o[5],o[6],o[7],o[8] == 1) for o in results)
            else:
                return None
