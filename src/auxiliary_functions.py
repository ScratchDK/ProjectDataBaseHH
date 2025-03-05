from src.writing_to_db import WriteToDB


def init_db() -> None:
    print("Укажите имя базы, если база данных с таким именем не существует, то она будет создана!")

    user_input_choice_bd = ""

    while user_input_choice_bd == "":
        user_input_choice_bd = input("Введите имя базы данных: ").lower()

    connect_to_db = WriteToDB(user_input_choice_bd)

    connect_to_db.create_table()

    print("В дальнейшем если вы при запросе, не укажете компании или город, "
          "то в базу данных будет добавлен список компаний по умолчанию!")
    print("Список компаний по умолчанию: Т-Банк, Сбербанк, 1С, МТС, ВТБ, Теле 2, Ламода, Самокат, Яндекс, Касперский")

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
