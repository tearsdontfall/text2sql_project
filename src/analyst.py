import sqlite3
import pandas as pd
from src.llm_client import SQLGenerator

class DataAnalyst:
    def __init__(self, db_path='yandex_metrica_fake_data.db', max_retries=2):
        self.db_path = db_path
        self.max_retries = max_retries
        self.llm = SQLGenerator()

    def execute_sql(self, sql):
        try:
            conn = sqlite3.connect(f'file:{self.db_path}?mode=ro', uri=True)
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return df, None
        except Exception as e:
            return None, str(e)

    def ask(self, question):
        current_prompt = question
        last_sql = ""
        
        for attempt in range(self.max_retries + 1):
            sql = self.llm.get_sql(current_prompt)
            last_sql = sql
            
            df, error = self.execute_sql(sql)
            
            if error is None:
                return df, last_sql, None # Успех
            
            # Если ошибка, готовим новый промпт для следующей итерации
            current_prompt = f"Твой предыдущий SQL запрос: {sql} \nВыдал ошибку: {error}. Исправь его."
        
        return None, last_sql, error # Провал после всех попыток