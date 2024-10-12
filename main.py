from src.DBManager import DBManager
from src.connectDB import connect_db, create_db, fill_data
from src.config import config


def main():
    connect_db()
    create_db()
    fill_data()
    con = config()
    company = DBManager('company', con)
    user_input = input("""
    Выберите действие:
     1-получает список всех компаний и количество вакансий у каждой компании.

     2-получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.

     3— получает среднюю зарплату по вакансиям.

     4— получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

     5— получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
     """)
    if user_input == '1':
        result = company.get_companies_and_vacancies_count()
        for i in result:
            print(f'{i[0]}, {i[1]} вакансий')
    elif user_input == '2':
        result = company.get_all_vacancies()
        for i in result:
            print(f'{i[0]}, {i[1]}, {i[2]},{i[3]}')
    elif user_input == '3':
        result = company.get_avg_salary()
        average = str(result[0]).split("'")[1]
        avg_salary = float(average[0:8])
        print(f'{avg_salary} рублей')
    elif user_input == '4':
        result = company.get_vacancies_with_higher_salary()
        for i in result:
            print(f"{i[2]}, зарплата:{i[3]} руб., ссылка: {i[4]}")
    elif user_input == '5':
        keyword = input("Введите слово:\n").title()
        result = company.get_vacancies_with_keyword(f"{keyword}")
        for i in result:
            print(f"{i[2]}, зарплата: {i[3]} руб., ссылка: {i[4]}")


if __name__ == '__main__':
    main()
