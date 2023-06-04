import datetime
import re

import openpyxl
import requests
import vk_api
import bs4
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import config
import sqlite3
from googletrans import Translator

from Schedule import Schedule


class Bot:
    def __init__(self):
        self.number_week = divmod((datetime.datetime.now() - datetime.datetime(2023, 2, 6)).days, 7)[0] + 1
        self.key_access = config.TOKEN
        self.vk_session = vk_api.VkApi(token=self.key_access)
        self.longpoll = VkLongPoll(self.vk_session)
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.schedule_data = []
        self.parse_schedule_file()
        self.schedule = Schedule(self.schedule_data)
        self.translator = Translator()
        print(11)

    def start(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.handle_message(event)

    @staticmethod
    def load_schedule_file():
        page = requests.get(config.SCHEDULE_URL)
        t = bs4.BeautifulSoup(page.text, "html.parser")
        res = t.find(string="Институт информационных технологий") \
                  .find_parent("div") \
                  .find_parent("div").findAll('a', {'class': 'uk-link-toggle'})[3:6]
        course_r = r'([1-3]) курс'
        for i in res:
            course = i.find('div', 'uk-link-heading').text.lower().strip()
            course_num = re.match(course_r, course)
            if course_num:
                course_num = course_num.group(1)
                f = open(f'{course_num}.xlsx', "wb")
                link = i.get('href')
                resp = requests.get(link)
                f.write(resp.content)
                f.close()

    def parse_schedule_file(self):
        for c in range(3):
            book = openpyxl.load_workbook(f'{c + 1}.xlsx')
            sheet = book.active
            num_cols = sheet.max_column
            last_group_cell = 0
            for i in range(6, num_cols):
                if last_group_cell >= 4:
                    last_group_cell = -1
                    continue
                column = []
                for j in range(2, 88):
                    v = str(sheet.cell(column=i, row=j).value)
                    if j == 52 and i == 126:
                        print(0)
                    v = re.sub(r'\n+', '\n', v)
                    if j == 2 and re.match(r'\w{4}-\d{2}-\d{2}', v):
                        last_group_cell = 0
                    column.append(v)
                if last_group_cell != -1:
                    self.schedule_data.append(column)
                    last_group_cell += 1

    def get_user_group(self, user_id):
        self.cur.execute("SELECT userid, user_group FROM users WHERE userid=?", (user_id,))
        row = self.cur.fetchone()
        if row is not None:
            user_id, user_group = row
            return user_group
        else:
            return None

    def add_user_group(self, user_id, new_group):
        self.cur.execute("SELECT userid FROM users WHERE userid=?", (user_id,))
        existing_record = self.cur.fetchone()
        if existing_record:
            self.cur.execute("UPDATE users SET user_group=? WHERE userid=?", (new_group, user_id))
        else:
            self.cur.execute("INSERT INTO users(userid, user_group) VALUES (?, ?)", (user_id, new_group))
        self.conn.commit()

    def send_message(self, user_id, sendMessage, random_id=0):
        self.vk_session.method('messages.send',
                               {'user_id': user_id, 'message': sendMessage, 'random_id': random_id})

    def handle_message(self, event):
        u_id = event.user_id
        f_message = event.text.lower()
        group_pattern = r"[а-яА-Я]{4}-\d{2}-\d{2}"
        match = re.match(group_pattern, f_message)
        # ввод группы студента
        if match:
            if f_message.upper() not in self.schedule.str_groups:
                self.send_message(u_id, 'Вы ввели неправильную группу')
                return
            else:
                self.add_user_group(u_id, f_message.upper())
                self.send_message(u_id, 'Я запомнил группу - ' + f_message.upper())
                return

        # наличие группы
        group = self.get_user_group(u_id)
        if not group:
            self.send_message(u_id, 'Я не знаю вашей группы, введите свою группу')
            return

        f_message_sp = f_message.split()

        # смена группы по команде "бот ..."
        if len(f_message_sp) >= 2:
            if f_message_sp[0] == 'бот':
                sp = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
                if len(f_message_sp) == 2 and f_message_sp[1].upper() in self.schedule.str_groups:
                    self.add_user_group(u_id, f_message_sp[1].upper())
                    self.send_message(u_id, 'Я запомнил группу - ' + f_message_sp[1].upper())
                elif f_message_sp[1] in sp:
                    if len(f_message_sp) == 3 and f_message_sp[2].upper() in self.schedule.str_groups:
                        self.send_message(u_id, 'Четная неделя:\n' +
                                          self.schedule.groups[self.schedule.str_groups.index(f_message_sp[2].upper())].week[
                                              sp.index(f_message_sp[1])].str(0))
                        self.send_message(u_id, 'Нечетная неделя:\n' +
                                          self.schedule.groups[self.schedule.str_groups.index(f_message_sp[2].upper())].week[
                                              sp.index(f_message_sp[1])].str(1))
                    else:
                        self.send_message(u_id, 'Четная неделя:\n' + self.schedule.groups[self.schedule.str_groups.index(group)].week[sp.index(f_message_sp[1])].str(0))
                        self.send_message(u_id, 'Нечетная неделя:\n' + self.schedule.groups[self.schedule.str_groups.index(group)].week[sp.index(f_message_sp[1])].str(1))
                else:
                    self.send_message(u_id, 'Я не знаю такой команды')
                return

        match f_message:
            case 'начать':
                self.send_message(u_id, config.START_MESSAGE)
            case 'помощь':
                self.send_message(u_id, config.HELP_MESSAGE)
            case 'бот':
                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button('на сегодня', color=VkKeyboardColor.POSITIVE)
                keyboard.add_button('на завтра', color=VkKeyboardColor.NEGATIVE)
                keyboard.add_line()
                keyboard.add_button('на эту неделю', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('на следующую неделю', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('какая неделя?', color=VkKeyboardColor.SECONDARY)
                keyboard.add_button('какая группа?', color=VkKeyboardColor.SECONDARY)

                self.vk_session.method('messages.send',
                                       {'user_id': u_id,
                                        'message': f_message,
                                        'random_id': 1,
                                        'keyboard': keyboard.get_keyboard()})

            case 'на сегодня':
                if datetime.datetime.now().weekday() == 6:
                    self.send_message(u_id, 'Сегодня выходной')
                else:
                    self.send_message(
                        u_id,
                        self.schedule.groups[self.schedule.str_groups.index(group)].week[
                            datetime.datetime.now().weekday()].str(self.number_week % 2))
                return
            case 'на завтра':
                if datetime.datetime.now().weekday() == 5:
                    self.send_message(u_id, 'Завтра выходной')
                elif datetime.datetime.now().weekday() == 6:
                    self.send_message(
                        u_id,
                        self.schedule.groups[self.schedule.str_groups.index(group)].week[0].str(
                            (self.number_week + 1) % 2))
                else:
                    self.send_message(
                        u_id,
                        self.schedule.groups[self.schedule.str_groups.index(group)].week[
                            (datetime.datetime.now().weekday() + 1) % 7].str(self.number_week % 2))
                return
            case 'на эту неделю':
                self.send_message(
                    u_id,
                    self.schedule.groups[self.schedule.str_groups.index(group)].str(self.number_week % 2))
                return
            case 'на следующую неделю':
                self.send_message(
                    u_id,
                    self.schedule.groups[self.schedule.str_groups.index(group)].str((self.number_week + 1) % 2))
                return
            case 'какая неделя?':
                self.send_message(u_id, 'Сейчас ' + str(self.number_week) + ' неделя')
                return
            case 'какая группа?':
                self.send_message(u_id, 'Расписание для группы ' + group.upper())
                return
            case 'погода':
                api_key = 'e4bd1e894a7a54294374b554452de587'
                city_name = 'Moscow'
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    weather = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    pressure = data['main']['pressure']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    wind_direction = data['wind']['deg']

                    if wind_direction >= 337.5 or wind_direction <= 22.5:
                        wind_direction = "Северный"
                    elif wind_direction >= 22.5 or wind_direction <= 67.5:
                        wind_direction = "Северо-восточный"
                    elif wind_direction >= 67.5 or wind_direction <= 112.5:
                        wind_direction = "Восточный"
                    elif wind_direction >= 112.5 or wind_direction <= 157.5:
                        wind_direction = "Юго-Восточный"
                    elif wind_direction >= 157.5 or wind_direction <= 202.5:
                        wind_direction = "Южный"
                    elif wind_direction >= 202.5 or wind_direction <= 247.5:
                        wind_direction = "Юго-Западный"
                    elif wind_direction >= 247.5 or wind_direction <= 292.5:
                        wind_direction = "Западный"
                    elif wind_direction >= 292.5 or wind_direction <= 337.5:
                        wind_direction = "Северо-Западный"

                    wind_text = ''
                    if wind_speed >= 29:
                        wind_text = 'Ураган'
                    elif wind_speed >= 19:
                        wind_text = 'Шторм'
                    elif wind_speed >= 12:
                        wind_text = 'Сильный'
                    elif wind_speed >= 2:
                        wind_text = 'Слабый'
                    else:
                        wind_text = 'Штиль'

                    weather = self.translator.translate(weather, dest='ru').text

                    weather_str = f'Погода в городе Москва: {weather}\n' \
                                  f'Температура: {temperature} °C\n' \
                                  f'Давление: {pressure} мм рт.ст.\n' \
                                  f'Влажность: {humidity}%\n' \
                                  f'Ветер: {wind_text}, {wind_speed} м/c, {wind_direction}'
                    self.send_message(u_id, weather_str)
                return
