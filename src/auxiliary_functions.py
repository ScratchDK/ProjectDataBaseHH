from src.writing_to_db import WriteToDB


def init_db() -> None:
    print("В дальнейшем если вы при запросе, не укажете компании или город, "
          "то в базу данных будут добавлены значения по умолчанию!")

    connect_to_db = WriteToDB()

    connect_to_db.create_table()

    user_input_list_employers = input("Чтобы добавить новый список, введите id компании через ', ': ")

    list_employers = user_input_list_employers.split(", ")

    for el in list_employers:
        if el.isdigit() and len(el) < 10:
            pass
        else:
            list_employers.remove(el)

    user_input_city = input("Введите город в котором будут выбраны вакансии: ")

    connect_to_db.write_data(list_employers, user_input_city)

    connect_to_db.close()
