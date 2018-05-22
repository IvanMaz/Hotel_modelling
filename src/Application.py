class Application:
    def __init__(self, uid, app_type, room_type, people, time_to_book, time_before_booking=0):
        # тип заявки
        self.type = app_type
        # тип номера в заявке
        self.room_type = room_type
        # число человек на заселение
        self.people = people
        # время бронирования/заселения
        self.time_to_book = time_to_book
        # время до заселения (если заявка на бронь)
        self.time_before_booking = time_before_booking
        # уникальный номер заявки
        self.uid = uid
