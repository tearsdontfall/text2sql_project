from src.analyst import DataAnalyst
from tabulate import tabulate

def main():
    analyst = DataAnalyst()
    print("🤖 CLI Аналитик готов (режим авто-исправления включен)")
    
    while True:
        question = input("\n💬 Вопрос: ")
        if question.lower() in ['exit', '/clear']: break
        
        df, sql, error = analyst.ask(question)
        
        print(f"💻 Итоговый SQL: {sql}")
        if error:
            print(f"❌ Ошибка: {error}")
        else:
            print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    main()
