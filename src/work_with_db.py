import os
import psycopg2
import configparser


class DBManager:
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

    def check_db(self):
        try:
            self.cur.execute('''
                SELECT 1
                FROM employers''')
        except Exception:
            return False
        else:
            return True

    def get_companies_and_vacancies_count(self):
        self.cur.execute('''
            SELECT 
                employers.name,
                COUNT(vacancies.id) AS vacancies_count
            FROM 
                employers
            LEFT JOIN 
                vacancies ON vacancies.employer_id = employers.id
            GROUP BY 
                employers.id, employers.name
                ''')
        query = self.cur.fetchall()
        return query

    def get_all_vacancies(self):
        self.cur.execute('''
            SELECT
                employers.name,
                vacancies.vacancy_name,
                vacancies.salary,
                vacancies.url
            FROM 
                vacancies
            INNER JOIN
                employers ON vacancies.employer_id = employers.id
            ORDER BY
                employers.name ASC
                ''')
        query = self.cur.fetchall()
        return query

    def get_avg_salary(self):
        self.cur.execute('''
            SELECT
                AVG(vacancies.salary) AS average_salary
            FROM 
                vacancies
                ''')
        query = self.cur.fetchall()
        return query

    def get_vacancies_with_higher_salary(self):

        average = self.get_avg_salary()

        self.cur.execute(f'''
            SELECT
                vacancies.vacancy_name,
                vacancies.salary,
                vacancies.url
            FROM 
                vacancies
            WHERE
                vacancies.salary > {int(average[0][0])}
            ORDER BY
                vacancies.salary DESC
                ''')
        query = self.cur.fetchall()
        return query

    def get_vacancies_with_keyword(self, keyword: str):
        self.cur.execute(f'''
            SELECT
                vacancies.vacancy_name,
                vacancies.vacancy_city,
                vacancies.url,
                vacancies.salary
            FROM 
                vacancies
            WHERE
                vacancies.vacancy_name ILIKE '%{keyword}%';
                ''')
        query = self.cur.fetchall()
        return query

    def close(self):
        self.cur.close()
        self.conn.close()
