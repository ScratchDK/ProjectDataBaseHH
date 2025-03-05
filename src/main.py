from src.work_with_db import DBManager
from src.auxiliary_functions import init_db


def main() -> None:
    print("Добро пожаловать!")
    print("Для работы с приложением нужно внести список компаний в базу данных!\n")

    user_input_bd = ""

    while user_input_bd not in ["1", "2"]:
        print(
            "Если вы хотите загрузить свой список или добавить новые компании в уже существующий, введите '1'\n"
            "Если вы ранее уже загружали список компаний и хотите продолжить работать с ним, введите '2'"
        )
        user_input_bd = input("Введите номер: ")
        print()

    if user_input_bd == "1":
        init_db()
    else:
        pass

    connect_to_db = DBManager()

    if connect_to_db.check_db() is False:
        print("В базе данных отсутствуют данные!\n"
              "Внесите список компаний в базу данных для продолжения работы.\n")
        connect_to_db.close()
        init_db()
        connect_to_db = DBManager()
    else:
        pass

    print("Для продолжения работы с базой данных выберите один из пунктов:\n"
          "Получить список всех компаний и количество вакансий у каждой компании, введите '1'\n"
          "Получить список всех вакансий с указанием: компании, вакансии, зарплаты и ссылки, введите '2'\n"
          "Получить среднюю зарплату по вакансиям, введите '3'\n"
          "Получить список всех вакансий, у которых зарплата выше средней, введите '4'\n"
          "Получить список всех вакансий, в названии которых содержатся ключевое слово, например python, введите '5'\n"
          "Для прекращения работы приложения, введите 'exit'")
    print()

    user_input_choice = ""

    while user_input_choice != "exit":
        user_input_choice = input("Введите номер или 'exit' для выхода из приложения: ")

        if user_input_choice == "1":
            result = connect_to_db.get_companies_and_vacancies_count()

            for el in result:
                print(f"Компания: {el[0]} | Количество вакансий: {el[1]}")
            print()

        elif user_input_choice == "2":
            result = connect_to_db.get_all_vacancies()

            for el in result:
                if el[2] is None:
                    salary = "не указана"
                else:
                    salary = el[2]

                print(f"Компания: {el[0]} | Вакансия: {el[1]} | Заработная плата: {salary} | Ссылка: {el[3]}")
            print()

        elif user_input_choice == "3":
            result = connect_to_db.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям составляет: {round(result[0][0], 2)} руб")
            print()

        elif user_input_choice == "4":
            result = connect_to_db.get_vacancies_with_higher_salary()

            for el in result:
                print(f"Компания: {el[0]} | Заработная плата: {el[1]} | Ссылка: {el[2]}")
            print()

        elif user_input_choice == "5":
            user_input_keyword = input("Введите ключевое слово по которому будут отобраны вакансии: ")
            result = connect_to_db.get_vacancies_with_keyword(user_input_keyword)
            for el in result:
                if el[2] is None:
                    salary = "не указана"
                else:
                    salary = el[2]

                print(f"Компания: {el[0]} | Вакансия: {el[1]} | Заработная плата: {salary} | Ссылка: {el[3]}")
            print()

    print("Завершение работы приложения.")

    connect_to_db.close()


if __name__ == "__main__":
    main()
