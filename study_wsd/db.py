import sqlite3
import typing
import json
import hashlib

def convert_to_id(json_content):
    wse_str = json.dumps(json_content, sort_keys=True)
    id =  hashlib.sha256(wse_str.encode("utf-8")).hexdigest()
    return id



class DatabaseSqlLite:


    def __init__(self, db_file_path = "data.db"):
        self.db_file_path = db_file_path

        with sqlite3.connect(self.db_file_path) as c:
            cur = c.cursor()

            cur.execute("""CREATE TABLE IF NOT EXISTS wsd_results(
                evaluation_id INTEGER NOT NULL,
                evalution TEXT NOT NULL,
                log TEXT NOT NULL,
                discussion_duration REAL NOT NULL,
                prompt_strategy TEXT NOT NULL,
                answer_value TEXT NOT NULL,
                answer_response TEXT,
                correct INTEGER NOT NULL,
                PRIMARY KEY (evaluation_id, prompt_strategy));
            """)

            c.commit()
    
    def add_wsd_discussion(
        self,
        wse,
        log,
        prompt_strategy:str,
        answer_value:str,
        discussion_duration:float,
        answer_response:typing.Optional[str]=None,
        correct:bool=False,
    ):
        with sqlite3.connect(self.db_file_path) as c:
            cur = c.cursor()

            wse_content = wse.to_json()
            wse_str = json.dumps(wse_content, sort_keys=True)

            cur.execute("INSERT INTO wsd_results VALUES (?,?,?,?,?,?,?,?);",(
                convert_to_id(wse_str),
                wse_str,
                json.dumps(log),
                discussion_duration,
                prompt_strategy,
                answer_value,
                answer_response,
                1 if correct else 0
            ))

            c.commit()

    def has_wsd_discussion(self,
        wse,
        prompt_strategy
    ):
        with sqlite3.connect(self.db_file_path) as c:

            o = c.execute("SELECT * FROM wsd_results WHERE evaluation_id = ? AND prompt_strategy = ?", (
                convert_to_id(json.dumps(wse.to_json(), sort_keys=True)),
                prompt_strategy
            )).fetchone()

            return o is not None
