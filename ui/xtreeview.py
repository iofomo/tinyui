# -*- encoding:utf-8 -*-
# @Brief: Python的3.x版本自带了ttk模块，默认支持，而2.x版本则需要安装ttk
# @Author: ...
# @Date:   2023.08.10 14:40:50

from framework.resource import Resource

try:
    from Tkinter import *
    import Tkinter.ttk as ttk
except ImportError:
    from tkinter import *
    import tkinter.ttk as ttk


# ----------------------------------------------------------------------------------------------------------------------
class XTreeView:
    def __init__(self, winRoot, columns):
        win = PanedWindow(winRoot, orient=HORIZONTAL)
        winRoot.add(win)
        select_all_button = Button(win, text=Resource.getString('text-select-all'), command=self.select_all)
        select_all_button.pack(side='left')

        invert_selection_button = Button(win, text=Resource.getString('text-select-invert'),
                                         command=self.invert_selection)
        invert_selection_button.pack(side='left')

        deselect_all_button = Button(win, text=Resource.getString('text-select-clear'), command=self.deselect_all)
        deselect_all_button.pack(side='left')

        lb = Label(win, text=Resource.getString('text-multi-select-keyboard'), foreground='darkgray')
        lb.pack(side='left')

        win = PanedWindow(winRoot, orient=HORIZONTAL)
        winRoot.add(win)

        self.tree = ttk.Treeview(win, columns=columns, selectmode='extended')
        # self.tree.heading('#0', text='Index')
        for column in columns: self.tree.heading(column, text=column)
        self.tree.pack(fill='both', expand=True)

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())

    def deselect_all(self):
        self.tree.selection_set(())

    def invert_selection(self):
        all_items = set(self.tree.get_children())
        selected_items = set(self.tree.selection())
        unselected_items = all_items - selected_items
        self.tree.selection_set(tuple(unselected_items))

    def append_item(self, values):
        self.tree.insert('', 'end', values=values)
        # self.tree.insert('', 'end', text=len(self.tree.get_children()), values=values)

    def insert_item(self, index, values):
        self.tree.insert('', '%d' % index, values=values)
        # self.tree.insert('', 'end', text=len(self.tree.get_children()), values=values)

    def delete_selection(self):
        selected = self.tree.selection()
        for item in selected: self.tree.delete(item)

    def get_selection(self):
        return self.tree.selection()
