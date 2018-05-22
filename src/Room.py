class Room:
    def __init__(self, class_, price, cap):
        # степень комфорта (тип) номера
        self.class_ = class_
        # стоимость номера
        self.price = price
        # местность номера
        self.cap = cap
        # заявки пришедшие на этот номер
        self.app_array = []
