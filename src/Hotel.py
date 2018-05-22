from collections import defaultdict
from Room import Room
from copy import copy


class Hotel:
    # конструктор
    def __init__(self, n_rooms, app_types, room_types, room_cap):
        # номера гостницы
        self.rooms = self.__generate_rooms__(n_rooms)
        # выручка
        self.profit = 0
        # типы заявок
        self.app_types = app_types
        # типы номеров
        self.room_types = room_types
        # местность номеров
        self.room_cap = room_cap
        # список поступивших заявок
        self.all_apps = defaultdict()
        # число отклоненных заявок
        self.rejected = 0

    # заполнение гостиницы номерами
    def __generate_rooms__(self, n_rooms):
        return {
            "standart_1":       self.__compute_ratio__("standart", 100, 1, n_rooms, 50, 25),
            "standart_2":       self.__compute_ratio__("standart", 120, 2, n_rooms, 50, 50),
            "standart_3":       self.__compute_ratio__("standart", 140, 3, n_rooms, 50, 25),
            "junior_suite_1":   self.__compute_ratio__("junior_suite", 150, 1, n_rooms, 30, 25),
            "junior_suite_2":   self.__compute_ratio__("junior_suite", 180, 2, n_rooms, 30, 50),
            "junior_suite_3":   self.__compute_ratio__("junior_suite", 210, 3, n_rooms, 30, 25),
            "suite_1":          self.__compute_ratio__("suite", 200, 1, n_rooms, 20, 25),
            "suite_2":          self.__compute_ratio__("suite", 240, 2, n_rooms, 20, 50),
            "suite_3":          self.__compute_ratio__("suite", 280, 3, n_rooms, 20, 25),
        }

    def __compute_ratio__(self, class_, price, cap, n_rooms, ratio1, ratio2):
        ratio = n_rooms*ratio1//100*ratio2//100
        return [Room(class_, price, cap) for i in range(ratio)]

    # обработка заявки
    def process_application(self, application):
        res = ""

        room_type = self.room_types[application.room_type] + \
            "_"+str(application.people)
        for room_idx, room in enumerate(self.rooms[room_type]):
            found_room = 1
            for app in room.app_array:
                if set(range(app.time_before_booking, app.time_to_book)) & set(range(application.time_before_booking*24, application.time_to_book*24)):
                    found_room = 0
                    break

            if found_room:
                self.all_apps[application.uid] = copy(application)
                res += "id %d %s booked for %d people in %dd for %dd\n" % (application.uid,                                                                            self.room_types[application.room_type],
                                                                           application.people,                                                                            application.time_before_booking,                                                                            application.time_to_book)
                application.time_before_booking *= 24
                application.time_to_book *= 24
                self.rooms[room_type][room_idx].app_array.append(application)
                return res

        res += "No suitable room for %s for %d people from %d for %d\n" % (self.room_types[application.room_type],
                                                                           application.people,
                                                                           application.time_before_booking,
                                                                           application.time_to_book)
        self.rejected += 1
        return res

    # обновление времени
    def process_one_tick(self):
        res = ""

        for key in self.rooms:
            for room_idx, room in enumerate(self.rooms[key]):
                for app_idx, app in enumerate(room.app_array):
                    if app.time_before_booking == 0:
                        if app.time_to_book == 0:
                            cost = room.price * \
                                self.all_apps[app.uid].time_to_book
                            self.profit += cost
                            res += "id %d check-out from %s for %d with cost %d\n" % (app.uid,
                                                                                      self.room_types[app.type],
                                                                                      app.people,
                                                                                      cost)
                            self.rooms[key][room_idx].app_array.remove(app)
                        else:
                            self.rooms[key][room_idx].app_array[app_idx].time_to_book -= 1
                    else:
                        self.rooms[key][room_idx].app_array[app_idx].time_before_booking -= 1
        return res

    # получение данных о занятости номеров
    def get_data(self, day, max_days, data):
        new = False
        if len(data) == 0:
            new = True

        idx = 0
        for key in self.rooms:
            for room in self.rooms[key]:
                if new:
                    days = [-1]*max_days
                else:
                    days = data[idx]

                for app in room.app_array:
                    if app.time_before_booking == 0:
                        days[day] = 2
                        for i in range(day+1, min(day+app.time_to_book//24+1, max_days)):
                            days[i] = 0
                    else:
                        for i in range(min(day+app.time_before_booking//24+1, max_days), min(day+app.time_before_booking//24+1+app.time_to_book//24+1, max_days)):
                            days[i] = 1

                if new:
                    data.append(days)
                else:
                    data[idx] = days
                idx += 1
        return data

    # получение данных о состоянии гостиницы
    def report(self):
        return self.profit, len(self.all_apps), self.rejected
