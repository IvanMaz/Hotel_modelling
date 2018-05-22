from EventGenerator import EventGenerator
from Hotel import Hotel
from random import randint


class Experiment:
    # конструктор
    def __init__(self, step=5, n_rooms=24, simulation_period=30, max_time_for_new_application=5):
        # шаг
        self.step = step
        # число номеров в гостнице
        self.n_rooms = n_rooms
        # период моделирования
        self.period = simulation_period
        # верхняя граница времени до новой заявки
        self.max_time = max_time_for_new_application
        # текущее время эксперимента
        self.curr_time = 0
        # текущий день эксперимента
        self.curr_day = 0
        # текущее время дня
        self.time = 0
        # время до поступления заявки
        self.time_for_new_application = -1
        # данные о занятости номеров
        self.data = []

        app_types = {1: "booking", 2: "checking-in"}
        room_types = {1: "standart", 2: "suite", 3: "junior_suite"}
        room_cap = [1, 2, 3]

        # генератор событий
        self.event_generator = EventGenerator(app_types, room_types, room_cap)
        # гостиница
        self.hotel = Hotel(self.n_rooms, app_types, room_types, room_cap)
        # сообщение о подтверждении брони
        self.message = ""

    # один шаг эксперимента
    def make_step(self):
        self.bills = ""
        self.check = ""

        if self.time == self.period * 24:
            return self.bills, self.check, self.data, self.hotel.report()

        self.bills += "Step %d\n" % (self.time//self.step)
        self.check += "Step %d\n" % (self.time//self.step)

        for _ in range(self.step):

            if self.time % 24 == 0:
                self.bills += "Day %d\n" % (self.time//24)
                self.check += "Day %d\n" % (self.time//24)

            self.curr_time = self.time % 24
            self.curr_day = self.time // 24

            if self.time_for_new_application < 0:
                self.time_for_new_application = randint(1, self.max_time)
            elif self.time_for_new_application == 0:
                application = self.event_generator.get_new_application()

                self.bills += self.hotel.process_application(application)
                self.time_for_new_application = randint(1, self.max_time)
            else:
                self.time_for_new_application -= 1

            self.hotel.get_data(self.curr_day, self.period, self.data)
            self.check += self.hotel.process_one_tick()

            self.time += 1

        return self.bills, self.check, self.data, self.hotel.report()

    # провести эксперимент до конца
    def complete(self):
        full_in = ""
        full_out = ""
        while True:
            in_, out_, data, report = self.make_step()
            if len(in_) and len(out_):
                full_in += in_
                full_out += out_
            else:
                full_in += "FINISH\n"
                return full_in, full_out, data, report
