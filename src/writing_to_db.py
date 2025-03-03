import os
import psycopg2
from src.external_api import ConnectAPIHeadHunter
import configparser


class WriteToDB:
    __default_employers = [
        "78638",  # Т-Банк
        "3529",  # Сбербанк
        "882",  # 1С
        "3776",  # МТС
        "4181",  # ВТБ
        "4219",  # Теле 2
        "780654",  # Ламода
        "2460946",  # Самокат
        "1740",  # Яндекс
        "1057",  # Касперский
    ]

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path_file = os.path.join(base_dir, "data", 'settings.ini')

        config = configparser.ConfigParser()
        config.read(full_path_file)

        dbname = config['database']['dbname']
        user = config['database']['user']
        password = config['database']['password']
        port = config['database']['port']
        host = config['database']['host']

        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            port=port,
            host=host
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS employers 
                    (id VARCHAR(255) PRIMARY KEY, 
                    name VARCHAR(255), 
                    url VARCHAR(255));''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS vacancies 
                    (id SERIAL PRIMARY KEY, 
                    employer_id VARCHAR(255), 
                    vacancy_id VARCHAR(32) UNIQUE,
                    vacancy_name VARCHAR(255),
                    vacancy_city VARCHAR(255),
                    url VARCHAR(255), 
                    salary INT, 
                    FOREIGN KEY (employer_id) REFERENCES employers (id));''')

        self.conn.commit()

    def write_data(self, list_employers: list = None, city: str = None):
        if list_employers is None or list_employers == []:
            list_employers = WriteToDB.__default_employers

        if city is None or city == "":
            city = "Москва"

        data_api = ConnectAPIHeadHunter()

        for i in list_employers:
            data = data_api.get_employers(i, city)

            for el in data:
                employer_id = el['employer']['id']
                employer_name = el['employer']['name']
                employer_url = el['employer']['url']

                vacancy_id = el['id']
                vacancy_url = el['alternate_url']
                vacancy_name = el['name']
                vacancy_city = el['area']['name']
                salary = el['salary']['from'] if el['salary'] else None

                insert_query = '''
                INSERT INTO employers (id, name, url) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;'''
                self.cur.execute(insert_query, (employer_id, employer_name, employer_url))
                self.conn.commit()

                insert_query = '''
                INSERT INTO vacancies (employer_id, vacancy_id, vacancy_name, vacancy_city, url, salary) 
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING;'''
                self.cur.execute(
                    insert_query, (employer_id, vacancy_id, vacancy_name, vacancy_city, vacancy_url, salary))
                self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
