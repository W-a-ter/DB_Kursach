import psycopg2
from src.hh_download import top_vacancies, hh_api
from src.config import config


def connect_db():
    params = config()  # Получаем параметры для входа и создания DataBase

    conn = psycopg2.connect(dbname="postgres", **params)  # Коннект с DB
    conn.autocommit = True
    cur = conn.cursor()  # Курсор для работы с DB

    cur.execute(f"DROP DATABASE company")  # Удаление базы данных (обновляем)
    cur.execute(f"CREATE DATABASE company")  # Создание базы данных

    cur.close()  # Закрытие курсора
    conn.close()  # закрытие коннекта


def create_db():
    params = config()  # Получаем параметры для входа и создания DataBase

    conn = psycopg2.connect(dbname="company", **params)  # Коннект с DB
    conn.autocommit = True
    cur = conn.cursor()  # Курсор для работы с DB

    cur.execute("""CREATE TABLE company(
    id SERIAL UNIQUE,
    id_company INT PRIMARY KEY,
    name varchar(100) NOT NULL,
    URL varchar(100))""")  # Создание таблицы

    cur.execute("""CREATE TABLE vacancies(
        id SERIAL UNIQUE,
        id_company INT REFERENCES company(id_company),
        name varchar(100) NOT NULL,
        salary INT,
        URL varchar(100))""")

    cur.close()  # Закрытие курсора
    conn.close()  # закрытие коннекта


def fill_data():
    vacancies_ = top_vacancies()
    companies_ = hh_api()
    params = config()  # Получаем параметры для входа и создания DataBase

    conn = psycopg2.connect(dbname="company", **params)  # Коннект с DB
    conn.autocommit = True
    cur = conn.cursor()
    for i in companies_:
        cur.execute("""INSERT INTO company
        (id_company, name, URL) VALUES (%s, %s, %s)
                RETURNING id_company""", vars=(i['id'], i['name'], i['url']))
        id_company = cur.fetchone()[0]
        for m in vacancies_:
            if int(m['employer_id']) == int(id_company):
                cur.execute("""INSERT INTO vacancies
                (id_company, name, salary, URL) 
                VALUES (%s, %s, %s, %s)""",
                            vars=(id_company, m['name'], m['salary']['to'], i['url']))
            else:
                continue
    cur.close()  # Закрытие курсора
    conn.close()


if __name__ == '__main__':
    connect_db()
    create_db()
    fill_data()
