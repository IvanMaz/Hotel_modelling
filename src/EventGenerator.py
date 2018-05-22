from Application import Application
from random import randint


class EventGenerator:
    # конструктор
    def __init__(self, app_types, room_types, room_cap):
        # типы заявок
        self.app_types = app_types
        # типы номеров
        self.room_types = room_types
        # местность номеров
        self.room_cap = room_cap
        # максимальное время для брони
        self.max_time_to_book = 7
        # максимально время до брони
        self.max_time_before_booking = 7
        # номер заявки
        self.app_id = -1

    # создание новой заявки
    def get_new_application(self):
        app_type = randint(1, len(self.app_types))
        room_type = randint(1, len(self.room_types))
        people = randint(1, len(self.room_cap))

        time_to_book = randint(1, self.max_time_to_book)
        time_before_booking = randint(
            1, self.max_time_before_booking) if self.app_types[app_type] == "booking" else 0
        self.app_id += 1

        return Application(self.app_id, app_type, room_type, people, time_to_book, time_before_booking)
