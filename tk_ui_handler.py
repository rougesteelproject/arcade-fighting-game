import tkinter as tk
from ui_frame_classes.battle_creator_menu import BattleCreatorMenu
from ui_frame_classes.main_menu import MainMenu
from ui_frame_classes.unit_creator_menu import UnitCreatorMenu

class TKUIHandler:
    def __init__(self, game_loop) -> None:
        self._game_loop = game_loop
        
        self.create_top_level()   

    def create_top_level(self):
        if not hasattr(self, "top_level"):

            self.top_level = tk.Tk()
            self.top_level.configure(height=800, width=800)

    def clear_screen(self):
        if hasattr(self, "_battle_creator_menu"):
            self._battle_creator_menu.destroy()

        if hasattr(self, "_main_menu"):
            self._main_menu.destroy()

        if hasattr(self, "_unit_creator_menu"):
            self._unit_creator_menu.destroy()
    
    def create_main_menu(self):
        self.clear_screen()
        
        self._main_menu = MainMenu(self)
        
    def create_battle_creator_menu(self):
        self.clear_screen()

        self._battle_creator_menu = BattleCreatorMenu(self)

    def create_unit_creator_menu(self):
        self.clear_screen()

        self._unit_creator_menu = UnitCreatorMenu(self)

    def run_battle(self):
        
        self._game_loop.battle_creator_run_battle()

        self.clear_screen()
        self.top_level.destroy()

    def battle_creator_disable_variance(self, use_variance):
        self._battle_creator_menu.show_label_variance(use_variance)

    def battle_creator_disable_initiative(self, use_initiative):
        self._battle_creator_menu.show_label_initiative(use_initiative)

    def battle_creator_create_switch_version_popup(self, outdated_list):
        self._battle_creator_menu._create_switch_version_popup(outdated_units=outdated_list)

    def battle_creator_add_team(self):
        self._battle_creator_menu._add_team()

    def battle_creator_rename_team(self, new_name, team_index):
        self._game_loop.battle_creator_rename_team(new_name, team_index)

        self._battle_creator_menu._get_team_updates()

    def exit_game(self):
        self.top_level.destroy()

    def run(self):
        self.top_level.mainloop()