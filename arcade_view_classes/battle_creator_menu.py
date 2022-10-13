import arcade
import arcade.gui

import logging

import constants

class BattleCreatorMenu(arcade.View):
    def __init__(self, window: arcade.Window = None, game_loop = None):
            super().__init__(window)

            self._game_loop = game_loop

            self._ui_manager = arcade.gui.UIManager()
            self._ui_manager.enable()

            self.v_box = arcade.gui.UIBoxLayout(space_between=5)

            self._battle_button = arcade.gui.UIFlatButton(text="Battle!", width=constants.MAIN_MENU_BUTTON_WIDTH)

            self._battle_button.on_click = self._battle

            self.v_box.add(self._battle_button)

            self._main_menu_button = arcade.gui.UIFlatButton(text="Main Menu", width=constants.MAIN_MENU_BUTTON_WIDTH)

            self._main_menu_button.on_click = self._main_menu

            self.v_box.add(self._main_menu_button)

            self._ui_manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.v_box)
            )

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.GRAY)

        # Create a box group to align the 'open' button in the center
        

    def on_hide_view(self):
        self._ui_manager.disable()
        return super().on_hide_view()

    def on_draw(self):
        """ Draw the menu """
        self.clear()

        self._ui_manager.draw()

    def _main_menu(self, event):
        self._game_loop.run_main_menu()

    def _battle(self, event):

        game_version = constants.DEFAULT_GAME_VERSION
        
        results = self._game_loop.search_units_by_name("Sugar Ant", game_version)

        self._buy_unit(0, "team_1")

        results = self._game_loop.search_units_by_name("Sugar Ant", game_version)

        self._buy_unit(0, "team_1")
        
        results = self._game_loop.search_units_by_name("Black Widow", game_version)

        self._buy_unit(0, "team_2")
        

        self._game_loop.run_battle()

    def _buy_unit(self, unit_index, team_name):
        #team_name = self.buy_team_holder.get()

        try:
            self._game_loop.battle_creator_buy_unit(unit_index, team_name)
            #note that curselection only works if you've selected something, even if there's no other option
        except IndexError:
            logging.exception("Tried to buy a unit with none selected.")

        #self._get_team_updates()

        #self.buy_team_holder.set(team_name)

    def _get_search_results(self, unit_name):
        #game_version = int(self.game_version_holder.get())
        game_version = constants.DEFAULT_GAME_VERSION

        results = self._game_loop.search_units_by_name(unit_name, game_version)

        unit_prompts = []
        
        if len(results) != 0:
            for index, unit_data in enumerate(results):

                unit_power = unit_data[f'raw_power_v{game_version}']
                #diferent power for diferent game versions

                unit_prompts.append(f'{index}: {unit_data["name"]}: {unit_power} \n')

        self._search_results_holder = unit_prompts

        #self._adjust_listbox_width(self.listbox_search_results)

    #TODO this should be a dummy that just loads up a couple units and a couple teams (come back and flesh out after the battler works)