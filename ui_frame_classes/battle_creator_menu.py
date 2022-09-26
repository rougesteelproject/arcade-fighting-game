import logging
import tkinter as tk
from tkinter import font
import constants
from ui_frame_classes.battle_creator_team import BattleCreatorTeam

class BattleCreatorMenu(tk.Frame):
    def __init__(self, callback_handler) -> None:
        super().__init__(callback_handler.top_level)

        self._callback_handler = callback_handler
        self._game_loop = self._callback_handler._game_loop

        self._create_frame_team_list()

        self._create_frame_feature_toggle()
        
        #self.battle_creator_ready = True
        
        self._create_frame_search_results()
        self._create_frame_search_bar()
        
        self.button_battle = tk.Button(self)
        self.button_battle.configure(text="Battle!", command =lambda: self._callback_handler.run_battle())
        self.button_battle.grid(column=1, columnspan=2, row=3)
        
        self.button_exit_battle_creator = tk.Button(self)
        self.button_exit_battle_creator.configure(text="Main_Menu", command =lambda: self._callback_handler.create_main_menu())
        self.button_exit_battle_creator.grid(column=0, row=3)
        
        self.pack(side="top")
        self.ready = True

    def _create_frame_feature_toggle(self):

        self.feature_toggle = tk.Frame(self)
        
        self.game_version_holder = tk.StringVar(self.feature_toggle)
        self.game_version_holder.set(constants.DEFAULT_GAME_VERSION)
        self.optionmenu_game_version = tk.OptionMenu(
            self.feature_toggle, self.game_version_holder, *constants.GAME_VERSION_OPTIONS)
        self.game_version_holder.trace('w', lambda x,y,z: self._switch_game_version())

        self.optionmenu_game_version.grid(column=0, row=0)

        self.checkbutton_initiative_holder = tk.IntVar(self.feature_toggle)
        self.checkbutton_initiative = tk.Checkbutton(self.feature_toggle)
        self.checkbutton_initiative.configure(text="Initiative", variable= self.checkbutton_initiative_holder, command=lambda :self._toggle_initiative())
        self.checkbutton_initiative.grid(column=0, row=1)
        
        self.checkbutton_variance_holder = tk.IntVar(self.feature_toggle)
        self.checkbutton_variance = tk.Checkbutton(self.feature_toggle)
        self.checkbutton_variance.configure(text="Variance", variable=self.checkbutton_variance_holder, command=lambda :self._toggle_variance())
        self.checkbutton_variance.grid(column=0, row=2)
        
        self.label_initiative_explanation = tk.Label(self.feature_toggle)
        self.label_initiative_explanation.configure(text="initiative not set")
        self.label_initiative_explanation.grid(column=0, row=3)
        
        self.label_variance_explanation = tk.Label(self.feature_toggle)
        self.label_variance_explanation.configure(text="variance not set")
        self.label_variance_explanation.grid(column=0, row=4)

        self.entry_money_limit = tk.Spinbox(self.feature_toggle)
        self.entry_money_limit.configure(from_=0, increment=1)
        self.entry_money_limit.grid(column=0, row=5)

        self.button_money_limit = tk.Button(self.feature_toggle)
        self.button_money_limit.configure(text="Set Money Limit", command=lambda :self._set_money_limit())
        self.button_money_limit.grid(column=0, row=6)
        
        self.feature_toggle.grid(column=0, row=0, rowspan=2)

    #TODO display unit stats in search results and team list
    def _create_frame_search_results(self):
        self.search_results = tk.Frame(self)
        
        self.label_search_results = tk.Label(self.search_results)
        self.label_search_results.configure(text="Results")
        self.label_search_results.grid(column=0, columnspan=2, row=0)
        
        self._search_results_holder = tk.StringVar(value=[])
        self.listbox_search_results = tk.Listbox(self.search_results, listvariable=self._search_results_holder)
        self.listbox_search_results.grid(column=0, columnspan=3, row=1)
        
        self.buy_team_holder = tk.StringVar(self.search_results)

        self.button_buy_unit = tk.Button(self.search_results)
        self.button_buy_unit.configure(text="Buy", command=lambda : self._buy_unit())
        self.button_buy_unit.grid(column=0, row=2)

        self.optionmenu_buy_unit_team = tk.OptionMenu(
            master = self.search_results, variable = self.buy_team_holder, value="", command=lambda :None
        )
        self.optionmenu_buy_unit_team.grid(column=1, row=2)
        self.search_results.grid(column=1, columnspan=2, row=1)

    def _create_frame_search_bar(self):
        self.search_bar_frame = tk.Frame(self)
        
        self._search_bar_holder = tk.StringVar(self.search_bar_frame)
        self.entry_search_bar = tk.Entry(self.search_bar_frame)
        _text_ = "Search"
        self.entry_search_bar.configure(textvariable=self._search_bar_holder)
        self.entry_search_bar.delete("0", "end")
        self.entry_search_bar.insert("0", _text_)
        self.entry_search_bar.grid(column=0, row=0)
        
        self.button_search_bar_enter = tk.Button(self.search_bar_frame)
        self.button_search_bar_enter.configure(text="Enter", command = lambda: self._get_search_results())
        
        self.button_search_bar_enter.grid(column=1, row=0)
        
        self.search_bar_frame.grid(column=1, columnspan=2, row=0)

    def _create_frame_team_list(self):
        self._team_list_frame = tk.Frame(self)

        self._team_list = []        

        self._create_frame_add_team()

        self._number_of_teams_holder = tk.StringVar(self._team_list_frame)
        self._label_number_of_teams = tk.Label(self._team_list_frame, textvariable=self._number_of_teams_holder)
        self._label_number_of_teams.grid(column=0, row=0)

        self.button_sell_unit = tk.Button(self._team_list_frame)
        self.button_sell_unit.configure(text="Sell Unit", command=lambda :self._sell_unit())
        self.button_sell_unit.grid(column=2, columnspan=2, row=3)

        self._team_list_frame.grid(column=0, columnspan=3, row=2)
        
    def _create_frame_add_team(self):
        self._add_team_frame = tk.Frame(self._team_list_frame)
        
        self.entry_team_name = tk.Entry(self._add_team_frame)
        _text_ = "Team Name"
        self.entry_team_name.delete("0", "end")
        self.entry_team_name.insert("0", _text_)
        self.entry_team_name.grid(column=0, row=0)

        self.button_add_team = tk.Button(self._add_team_frame)
        self.button_add_team.configure(text="Add Team", command=lambda :self._send_team_name())
        self.button_add_team.grid(column=0, row=1)

        self._button_remove_team = tk.Button(self._add_team_frame)
        self._button_remove_team.configure(text= "Remove Rightmost Team", command=lambda :self._remove_last_team())
        self._button_remove_team.grid(column=0, row=2)

        self._add_team_frame.grid(column=6, row=1)
    
    def _toggle_initiative(self):
        if self.checkbutton_initiative_holder == 1:
            self._game_loop.battle_creator_use_initiative(True)
        else:
            self._game_loop.battle_creator_use_initiative(False)

    def _toggle_variance(self):
        if self.checkbutton_variance_holder == 1:
            self._game_loop.battle_creator_use_variance(True)
        else:
            self._game_loop.battle_creator_use_initiative(False)

    def _grey_out_variance(self, use_variance):
            if use_variance== False:
                self.checkbutton_variance.deselect()
                self.checkbutton_variance.configure(state=tk.DISABLED)
            else:
                self.checkbutton_variance.configure(state=tk.NORMAL)
                self.checkbutton_variance.select()
                
    def _grey_out_initiative(self, use_initiative):
            if use_initiative == False:
                self.checkbutton_initiative.deselect()
                self.checkbutton_initiative.configure(state=tk.DISABLED)
            else:
                self.checkbutton_initiative.configure(state=tk.NORMAL)
                self.checkbutton_initiative.select()
        
    def show_label_variance(self, use_variance):
        if use_variance == False:
            self.label_variance_explanation.configure(text=constants.VARIANCE_DISABLED_EXPLANATION)
        else:
            self.label_variance_explanation.configure(text=constants.VARIANCE_EXPLANATION)

    def show_label_initiative(self, use_initiative):
        if use_initiative == False:
            self.label_initiative_explanation.configure(text=constants.INITIATIVE_DISABLED_EXPLANATION)
        else:
            self.label_initiative_explanation.configure(text=constants.INITIATIVE_EXPLANATION)

    def _set_money_limit(self):
        self._game_loop.battle_creator_set_money_limit(self.entry_money_limit.get())
        self._get_team_updates()

    def _get_search_results(self):
        results = self._game_loop.search_units_by_name(self._search_bar_holder.get(), self.game_version_holder.get())

        self._search_results_holder.set(results)

        self._adjust_listbox_width(self.listbox_search_results)

    def _adjust_listbox_width(self, list, max_width=100):
        
        f = font.Font(font=list.cget("font"))
        pixels = 0
        for item in list.get(0, "end"):
            pixels = max(pixels, f.measure(item))
        # bump listbox size until all entries fit

        pixels = pixels + 10
        width = int(list.cget("width"))
        for w in range(0, max_width+1, 5):
            if list.winfo_reqwidth() >= pixels:
                break
            list.config(width=width+w)

    def _switch_game_version(self):

        new_game_version = int(self.game_version_holder.get())

        old_game_version = self._get_game_version()

        if new_game_version > old_game_version:
            outdated_list = self._game_loop.battle_creator_get_outdated_list(new_game_version)

            self._create_switch_version_popup(new_game_version, outdated_list)

        else:
            self._create_switch_version_popup(new_game_version)

    def _get_game_version(self):
        game_version = self._game_loop.battle_creator_get_game_version()

        return game_version

    def _create_switch_version_popup(self, new_game_version, outdated_units = ""):
        self._switch_version_popup= tk.Toplevel(self.master)
        #TODO is it correct to call this with self.master?
        #that is, Frame.master
        self._switch_version_popup.geometry("750x250")
        self._switch_version_popup.title("Switch Game Version?")

        if outdated_units != "":
            warning_text = constants.WARNING_OUTDATED_UNITS + outdated_units + constants.WARNING_CHANGE_GAME_VERSION_BATTLE_CREATOR
            sell_outdated = True
        else:
            warning_text = constants.WARNING_CHANGE_GAME_VERSION_BATTLE_CREATOR
            sell_outdated = False

        self.label_switch_warning = tk.Label(self._switch_version_popup, text=warning_text)
        self.label_switch_warning.grid(row=0)

        self.button_switch_yes = tk.Button(self._switch_version_popup)
        self.button_switch_yes.configure(
            anchor="n",
            compound="top",
            justify="center",
            text="Switch Game Version",
            command=lambda :self._switch_version_get_user_choice(True, new_game_version, sell_outdated)
        )
        self.button_switch_yes.grid(row=1)

        self.button_switch_no = tk.Button(self._switch_version_popup)
        self.button_switch_no.configure(
            anchor="n",
            compound="top",
            justify="center",
            text="Don't Switch",
            command=lambda :self._switch_version_get_user_choice(False)
        )
        self.button_switch_no.grid(row=2)
        
    def _switch_version_get_user_choice(self, user_confirmed_change, new_game_version = constants.DEFAULT_GAME_VERSION,  sell_outdated_units = False):
        
        if user_confirmed_change:

            if new_game_version == 1:
                self._grey_out_initiative(use_initiative = False)
                self._grey_out_variance(use_variance = False)

            elif new_game_version >= 2:
                self._grey_out_initiative(use_initiative = True)
                if new_game_version >= 3:
                    self._grey_out_variance(use_variance = True)
                else:
                    self._grey_out_variance(use_variance = False)

            self._game_loop.battle_creator_set_game_version(new_game_version, sell_outdated_units)
            self._get_team_updates()     

        self._switch_version_popup.destroy()

    def _buy_unit(self):
        team_name = self.buy_team_holder.get()

        try:
            self._game_loop.battle_creator_buy_unit(self.listbox_search_results.curselection()[0], self.buy_team_holder.get())
            #note that curselection only works if you've selected something, even if there's no other option
        except IndexError:
            logging.exception("Tried to buy a unit with none selected.")

        self._get_team_updates()

        self.buy_team_holder.set(team_name)

    def _sell_unit(self):

        unit_lists = [team.listbox_members for team in self._team_list]
        #if nothing is selected, curselection returns an empty tuple, and you can only select one thing at a time across all listboxes in the default mode
        for index, team in enumerate(unit_lists):
            if len(team.curselection()) > 0:
                self._game_loop.battle_creator_sell_unit(index, team.curselection()[0])
                break

        self._get_team_updates()

    def _get_team_updates(self):

        #request the team list from the loop (who asks the battle_creator)

        money_limit, fetched_teams = self._game_loop.battle_creator_get_team_updates()

        for index, team in enumerate(fetched_teams):
            self._team_list[index].full_update(team.cost, money_limit, team.members, team.name)

        teams = [team.name_holder.get() for team in self._team_list]

        self.optionmenu_buy_unit_team['menu'].delete(0, 'end')

        self.buy_team_holder.set(teams[0])

        for team in teams:
            self.optionmenu_buy_unit_team['menu'].add_command(label=team, command=tk._setit(self.buy_team_holder, team))

        self._number_of_teams_holder.set(f'Teams: {len(self._team_list)}/{constants.MAX_NUMBER_OF_PLAYERS}')
            
    def _send_team_name(self):
        name = self.entry_team_name.get()
        self._game_loop.battle_creator_add_team(name)

    def _add_team(self):

        #instead of disabling the frame, just have _add_team do nothing

        if len(self._team_list) < constants.MAX_NUMBER_OF_PLAYERS:

            self._team_list.append(BattleCreatorTeam(self._callback_handler, self._team_list_frame, len(self._team_list)))

            self._get_team_updates()
            
    def _remove_last_team(self):

        #instead of disabling the frame, just have _remove_team do nothing
        if len(self._team_list) > constants.MIN_NUMBER_OF_PLAYERS:

            team = self._team_list[-1]
            self._team_list.remove(team)
            team.frame.destroy()
            self._game_loop.battle_creator_remove_team(-1)
            #only remove the last one

            self._get_team_updates()
