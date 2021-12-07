import tkinter as tk
from threading import Thread
from time import sleep
from queue import Queue
import sys
#test.txt srelgiuhsr


class App(tk.Frame):
    data = [["???" for y in range(10)] for x in range(10)]  #None # эту переменную выводите на экран
    max_pages = 1
    page = 1
    queue = Queue()
    row = 1
    col = 2
    cell_value = 5

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.entrythingy = tk.Entry()
        #self.entrythingy.pack()

        # Create the application variable.
        #self.contents = tk.StringVar()
        # Set it to some value.
        #self.contents.set('this is a variable')
        
        # кнопки управления страницами
        self.bt2 = tk.Button(master, text="Backward", activebackground='#eeeeee', activeforeground='#000000',
                             bg='#a0a000', fg='#ffffff', width=10, command=self.get_prev_page)
        self.bt2.place(x=10, y=550)
        self.bt3 = tk.Button(master, text="Refresh", activebackground='#eeeeee', activeforeground='#000000',
                             bg='#00a000', fg='#ffffff', width=10, command=self.get_page_query)
        self.bt3.place(x=160, y=550)
        self.btn = tk.Button(master, text="Forward", activebackground='#eeeeee', activeforeground='#000000',
                             bg='#a0a000', fg='#ffffff', width=10, command=self.get_next_page)
        self.btn.place(x=310, y=550)

        # таблица (command=self.edit_query заменить лямбда-функцией)
        i = 0
        while i < 10:
            j = 0
            while j < 10:
                if j % 2 == 0:
                    self.tab = tk.Button(self.master, text=self.data[i][j], activebackground='#111111', activeforeground='#ffffff', bg='#bbbbff', fg='#000000', height=2, width=13, relief = tk.RIDGE, wraplength=140, command=self.edit_query)
                else:
                    self.tab = tk.Button(self.master, text=self.data[i][j], activebackground='#111111', activeforeground='#ffffff', bg='#bbffbb', fg='#000000', height=2, width=13, relief = tk.RIDGE, wraplength=140, command=self.edit_query)
                self.tab.place(x=10+(150*j), y=50+(50*i))
                j += 1
            i += 1
            
        #self.draw_page
        
        # Tell the entry widget to watch this variable.
        #self.entrythingy['textvariable'] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-F5>', self.get_page_query)
        self.entrythingy.bind('<Key-F4>', self.get_prev_page)
        self.entrythingy.bind('<Key-F6>', self.get_next_page)
        self.entrythingy.bind('<Key-F1>', self.edit_query)
        self.entrythingy.bind('<Key-F2>', self.confirm_edit)
        self.entrythingy.bind('<Key-F3>', self.rollback_edit)
        self.entrythingy.bind('<Key-Return>', self.print_contents)

    def print_contents(self, event):
        print('Hi. The current entry content is:', self.contents.get())

    def send_to_master(self, query):
        self.queue.put(query)
        print('send_to_master:', query)

    def get_page_query(self):
        self.send_to_master(['get', self.page])

    def get_next_page(self):
        self.page += 1
        self.get_page_query()

    def get_prev_page(self):
        self.page -= 1
        self.get_page_query()

    def edit_query(self, row, col):
        self.send_to_master(['edit', self.page, row, col])

    def confirm_edit(self, event):
        self.send_to_master(['confirm', self.cell_value])

    def rollback_edit(self, event):
        self.send_to_master(['rollback'])

    def set_data(self, data):
        self.data = data
        #print('gui_data = ', self.data)
        self.draw_page(self.data)

    def draw_page(self, data):
        #print('GUI got data ')
        # таблица в функции (command=self.edit_query заменить лямбда-функцией)
        self.data = data
        max_x = 10
        max_y = 10
        i = 0
        while i < max_y:
            j = 0
            while j < max_x:
                if j % 2 == 0:
                    self.tab = tk.Button(self.master, text=self.data[i][j], activebackground='#111111', activeforeground='#ffffff', bg='#bbbbff', fg='#000000', height=2, width=13, relief=tk.RIDGE, wraplength=140, command=self.edit_query)
                else:
                    self.tab = tk.Button(self.master, text=self.data[i][j], activebackground='#111111', activeforeground='#ffffff', bg='#bbffbb', fg='#000000', height=2, width=13, relief=tk.RIDGE, wraplength=140, command=self.edit_query)
                self.tab.place(x=10+(150*j), y=50+(50*i))
                j += 1
            i += 1
        print('GUI got data ', data)


class GuiThread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print('GUI thread started!')
        self.app = App()
        self.app.master.title('Window')
        self.app.master.maxsize(1800, 800)
        self.app.mainloop()
        print('GUI thread ended!')

    def output_data(self, data):
        self.app.set_data(data)
        #print(f'{data=}')

    def get_query(self):
        if self.app.queue.empty():
            return None
        else:
            return self.app.queue.get(self)

    def set_data(self, data):
        self.app.set_data(data)

    def set_number_of_pages(self, num):
        self.app.max_pages = num
        print(f'Pages: {self.app.max_pages}')
