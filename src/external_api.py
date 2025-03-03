from abc import ABC, abstractmethod
from typing import Any

import requests


class ConnectorAPI(ABC):
    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def get_employers(self):
        pass


class ConnectAPIHeadHunter(ConnectorAPI):
    """Класс отвечает за подключение к внешнему api 'hh.ru' и получения списка вакансий"""

    def __init__(self):
        self.__vacancies = {}
        self.__employers = {}  # Данные о работодателях

    def _connect(self, params=None) -> Any:
        response = requests.get('https://api.hh.ru/vacancies', params=params)

        if response.status_code == 200:
            print('Подключение к API HeadHunter установлено успешно!\n')
            return response
        else:
            print('Ошибка подключения к API HeadHunter, код ошибки: {}'.format(response.status_code))

    def get_employers(self, employer_id: str = None, text: str = None) -> list:
        params = {"employer_id": employer_id, "text": text}

        self.__employers = self._connect(params).json()

        return self.__employers["items"]
