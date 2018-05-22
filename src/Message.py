class Message:
    def __init__(self):
        self.day = 0
        self.step = 0
        self.bills = []
        self.check_outs = []

    def add_bill(self, uid, room_type, people, time_before, time_to):
        self.bills.append("id %d %s booked for %d people in %dd for %dd\n" % (uid,
                                                                              room_type,
                                                                              people,
                                                                              time_before,
                                                                              time_to))

    def add_check_out(self, uid, room_type, people, cost):
        self.check_outs.append("id %d check-out from %s for %d with cost %d\n" % (uid,
                                                                                  room_type,
                                                                                  people,
                                                                                  cost))

    def print_bills(self):
        tmp = "Step %d\nDay %d" % (self.day, self.step)
        for bill in self.bills:
            tmp += bill
        return tmp

    def print_check(self):
        tmp = "Step %d\nDay %d" % (self.day, self.step)
        for check in self.check_outs:
            tmp += check
        return tmp
