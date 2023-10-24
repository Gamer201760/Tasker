from datetime import date

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from core.exceptions import UnAuthorized
from model.item import Item
from model.token import JWToken


class EJUser(BaseModel):
    token: JWToken | None = None
    username: str

    def login_ej(self, password: str):
        with requests.Session() as session:
            session.post(
                'https://elschool.ru/Logon/Index',
                data={'login': self.username, 'password': password}
            )
        token = session.cookies.get('JWToken')
        if token is None:
            raise UnAuthorized(self.username)
        self.token = JWToken(token=token)

    def homework(self, date: date) -> list[Item]:
        res = self._get()
        hw_all = self._get_hw(res.text, date)
        if len(hw_all) == 0:
            res = self._get(res.url + f'&Week={date.isocalendar().week + 1}')
            hw_all = self._get_hw(res.text, date)

        day = []
        for hw in hw_all:
            text: str = hw.parent.parent.parent.find('div', {'class': 'diary__homework-text'}).text.strip()
            name: str = hw.parent.parent.parent.find('div', {'class': 'flex-grow-1'}).text[3:].strip()
            if text not in day:
                day.append(Item(name=name, homework=text, date_lesson=date))

        return day

    def is_active(self) -> bool:
        if self.token is None:
            return False
        return self.token.active

    def _get(self, url: str = 'https://elschool.ru/users/diaries/') -> requests.Response:
        return requests.get(
            url,
            cookies={'JWToken': str(self.token), 'Path': '/', 'Domain': 'elschool.ru'},
        )

    def _get_hw(self, data: str, date: date) -> list:
        soup = BeautifulSoup(data, 'html.parser')
        return soup.find_all('div', {'data-lesson-date': date.strftime('%d.%m.%Y')})

