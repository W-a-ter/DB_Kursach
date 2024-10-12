import psycopg2
from src.connectDB import config


class DBManager:
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def get_companies_and_vacancies_count(self):

        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        cur = conn.cursor()  # Курсор для работы с DB

        cur.execute("""
        SELECT company.name, COUNT(vacancies.id_company)
        FROM company
        INNER JOIN vacancies ON company.id_company=vacancies.id_company
        GROUP BY company.name
        """)
        result = cur.fetchall()
        cur.close()  # Закрытие курсора
        conn.close()
        return result

    def get_all_vacancies(self):
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""
        SELECT company.name, vacancies.name, vacancies.salary, vacancies.url
        FROM company
        RIGHT JOIN vacancies USING(id_company)
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_avg_salary(self):
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""
        SELECT AVG(vacancies.salary)
        FROM vacancies
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""
        SELECT *
        FROM vacancies
        WHERE vacancies.salary >= (SELECT AVG(vacancies.salary) FROM vacancies)
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"""
        SELECT *
        FROM vacancies
        WHERE name LIKE '%{keyword}%'
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result


if __name__ == '__main__':
    res = DBManager('company', config('../DB.ini'))
