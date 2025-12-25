import sqlite3
import pandas as pd
from src.llm_client import SQLGenerator
from tabulate import tabulate

def execute_query(sql, db_path='yandex_metrica_fake_data.db'):
    try:
        # Подключаемся в режиме Read-Only для безопасности
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        return f"❌ Ошибка SQL: {e}"

def main():
    print("🤖 SQL-Аналитик с памятью готов!")
    print("Доступные команды: 'exit' - выход, '/clear' - забыть контекст")
    
    llm = SQLGenerator()
    
    while True:
        question = input("\n💬 Ваш вопрос: ")
        
        if question.lower() in ['exit', 'quit', 'выход']:
            break
            
        if question.lower() == '/clear':
            llm.clear_history()
            print("🧠 Память очищена!")
            continue

        print("🔍 Генерация кода...")
        sql_query = llm.get_sql(question)
        
        print(f"\n💻 SQL: {sql_query}")
        
        result = execute_query(sql_query)
        
        if isinstance(result, pd.DataFrame):
            if result.empty:
                print("Ничего не найдено.")
            else:
                print(tabulate(result, headers='keys', tablefmt='psql', showindex=False))
        else:
            print(result)

        

if __name__ == "__main__":
    main()
