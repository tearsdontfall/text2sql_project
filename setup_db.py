import sqlite3
import pandas as pd
from faker import Faker
import random
import numpy as np
import uuid
import datetime

fake = Faker('ru_RU')
db_name = 'yandex_metrica_fake_data.db'
table_name = 'metrica_hits'

def create_fake_data(n=10000, n_users=1500):

    user_ids = [str(uuid.uuid4()) for i in range(n_users)]

    metrica = []
    for i in range(n):
        metrica.append(
            {
            'session_date': fake.date_between_dates(datetime.date(2025,1,1), datetime.date(2025,12,31)),
            'session_id': str(uuid.uuid4()),
            'client_id': random.choice([i for i in range(10000,15000)]),
            'city': fake.city_name(),
            'utm_source': random.choice(['yandex', 'vkads', 'telegram', 'hybrid', 'soloway', 'mintegral', 'organic']),
            'event_type': random.choice(['page_view', 'ib_draft_created', 'sdelka_draft_created']),
            'user_id': random.choice(user_ids)
            }

        )

    df_metrica = pd.DataFrame(metrica)

    conn = sqlite3.connect(db_name)
    df_metrica.to_sql(table_name, conn, if_exists='replace', index=True)
    print(f'Success creating {db_name}.{table_name}')
    conn.close()

if __name__ == "__main__":
    create_fake_data()