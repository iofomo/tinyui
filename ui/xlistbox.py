# -*- encoding:utf-8 -*-
# @Author: ...
# @Date:   2023.08.10 14:40:50

from framework.resource import Resource

try:
    from Tkinter import *
except ImportError:
    from tkinter import *


# ----------------------------------------------------------------------------------------------------------------------
class XListBox:
    def __init__(self, winRoot):
        win = PanedWindow(winRoot, orient=HORIZONTAL)
        winRoot.add(win)
        select_all_button = Button(win, text=Resource.getString('text-select-all'), command=self.select_all)
        select_all_button.pack(side='left')

        invert_selection_button = Button(win, text=Resource.getString('text-select-invert'), command=self.invert_selection)
        invert_selection_button.pack(side='left')

        deselect_all_button = Button(win, text=Resource.getString('text-select-clear'), command=self.deselect_all)
        deselect_all_button.pack(side='left')

        lb = Label(win, text=Resource.getString('text-multi-select-keyboard'), foreground='darkgray')
        lb.pack(side='left')

        win = PanedWindow(winRoot, orient=HORIZONTAL)
        winRoot.add(win)

        self.listbox = Listbox(win, selectmode='extended')
        self.listbox.pack(fill='both', expand=True)

    def select_all(self):
        self.listbox.selection_set(0, END)

    def deselect_all(self):
        self.listbox.selection_clear(0, END)

    def invert_selection(self):
        selected = self.listbox.curselection()
        all_items = range(self.listbox.size())
        unselected = [item for item in all_items if item not in selected]
        self.listbox.selection_clear(0, END)
        for item in unselected:
            self.listbox.selection_set(item)

    def append_item(self, value):
        self.listbox.insert('end', value)

    def insert_item(self, index, value):
        self.listbox.insert('%d' % index, value)

    def delete_selection(self):
        selected = self.listbox.curselection()
        for index in reversed(selected):
            self.listbox.delete(index)

    def get_selection(self):
        return self.listbox.curselection()
