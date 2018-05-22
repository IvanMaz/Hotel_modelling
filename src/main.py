from tkinter import Tk, Frame, Button, Label, Text, Scrollbar
from Experiment import Experiment


def draw(in_, out_, report, data):

    check_in.text.insert("end", in_)
    check_in.text.see("end")

    check_out.text.insert("end", out_)
    check_out.text.see("end")

    total.total['text'] = "Total income: %d" % report[0]
    total.proc['text'] = "Total applications proceeded: %d" % report[1]
    total.rej['text'] = "Total applications rejected: %d" % report[2]

    if len(data) != 0:
        for idx, row in enumerate(table._widgets):
            for jdx, _ in enumerate(row):
                if data[idx][jdx] == 0:
                    table._widgets[idx][jdx]['bg'] = "red"
                elif data[idx][jdx] == 1:
                    table._widgets[idx][jdx]['bg'] = "yellow"
                elif data[idx][jdx] == 2:
                    table._widgets[idx][jdx]['bg'] = "blue"
                else:
                    table._widgets[idx][jdx]['bg'] = "green"


def step():
    complete = False
    in_, out_, data, report = experiment.make_step()

    if len(in_) == 0 and len(out_) == 0:
        complete = True
        in_, out_,  data, report = experiment.complete()

    draw(in_, out_, report, data)

    if complete:
        buttons.stepb['state'] = 'disabled'
        buttons.runb['state'] = 'disabled'


def run():
    in_, out_, data, report = experiment.complete()

    draw(in_, out_, report, data)

    buttons.stepb['state'] = 'disabled'
    buttons.runb['state'] = 'disabled'


class Buttons(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.stepb = Button(self, text='step',
                            command=step, height=5, width=15)
        self.runb = Button(self, text='run', command=run, height=5, width=15)
        """stepb.pack(side="left", fill='both', expand=True)
        runb.pack(side="right", fill='both', expand=True)"""
        self.stepb.grid(row=1, column=1, padx=(20, 20))
        self.runb.grid(row=1, column=2, padx=(20, 20))


class Total(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.total = Label(self, text="Total income: 0", width=30, anchor='w')
        self.proc = Label(
            self, text="Total applications proceeded: 0", width=30, anchor='w')
        self.rej = Label(
            self, text="Total applications rejected: 0", width=30, anchor='w')

        self.total.grid(row=0, column=0, padx=(20, 20))
        self.proc.grid(row=1, column=0, padx=(20, 20))
        self.rej.grid(row=2, column=0, padx=(20, 20))


class CheckIn(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.text = Text(self, height=20, width=60)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)


class CheckOut(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.text = Text(self, height=20, width=60)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)


class SimpleTable(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="black")
        self._widgets = []

        label = Label(self, text="Rom type / Day",
                      borderwidth=0, width=15)
        label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        for column in range(experiment.period):
            label = Label(self, text="%d" % column,
                          borderwidth=0, width=4)
            label.grid(row=0, column=column+1, sticky="nsew", padx=1, pady=1)

        row_num = 1
        for room_name in experiment.hotel.rooms:
            for room in experiment.hotel.rooms[room_name]:
                current_row = []
                label = Label(self, text="%s" % room_name,
                              borderwidth=0, width=15)
                label.grid(row=row_num, column=0,
                           sticky="nsew", padx=1, pady=1)

                for column in range(experiment.period):
                    label = Label(self, text="-",
                                  borderwidth=0, width=4)
                    label.grid(row=row_num, column=column+1,
                               sticky="nsew", padx=1, pady=1)
                    current_row.append(label)
                self._widgets.append(current_row)
                row_num += 1


experiment = Experiment()
root = Tk()
buttons = Buttons(root)
total = Total(root)
check_in = CheckIn(root)
check_out = CheckOut(root)
table = SimpleTable(root)

buttons.grid(row=1, column=1, sticky="w")
total.grid(row=1, column=2, sticky="w")
check_in.grid(row=2, column=1)
check_out.grid(row=2, column=2)
table.grid(row=3, column=1, columnspan=2)

root.minsize(1000, 600)
root.resizable(False, False)
root.mainloop()
