import tkinter as tk

class BattleCreatorTeam():
    def __init__(self, callback_handler, parent_frame, index) -> None:
        self.frame = tk.Frame(parent_frame)
        self._callback_handler = callback_handler

        self.index = index

        self.name_frame = tk.Frame(self.frame)
        self.name_frame.grid(column=self.index, row=0)

        self.name_holder = tk.StringVar(self.name_frame)
        self.name = tk.Entry(self.name_frame)
        self.name.configure(textvariable=self.name_holder)
        self.name.grid(column=0, row=0)

        self.button_rename = tk.Button(self.name_frame)
        self.button_rename.configure(text= "rename", command= lambda: self._rename())
        self.button_rename.grid(row=0, column=1)

        self._money_holder = tk.StringVar(self.frame)

        self.message_money = tk.Message(self.frame)
        self.message_money.configure(textvar = self._money_holder)
        self.message_money.grid(column=self.index, row=1)

        self.team_members_holder = tk.StringVar()
        self.listbox_members = tk.Listbox(self.frame, listvariable=self.team_members_holder)
        self.listbox_members.grid(column=self.index, row=2)

        self.frame.grid(column=self.index, row=1)

        self.enabled = True

    def full_update(self, cost, money_limit, member_list, name):
        self.update_money(cost= cost, money_limit= money_limit)
        self.update_team_members(member_list= member_list)
        self.update_name(new_name=name)

    def update_money(self, cost, money_limit):
        self._money_holder.set(f'{cost} / {money_limit}')

    def update_team_members(self, member_list):

        unit_name_list = [unit.name for unit in member_list]

        self.team_members_holder.set(unit_name_list)

    def update_name(self, new_name):
        self.name_holder.set(new_name)

    def _rename(self):
        new_name = self.name_holder.get()

        self._callback_handler.battle_creator_rename_team(new_name, self.index)
