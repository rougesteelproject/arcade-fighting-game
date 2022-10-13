import arcade
import arcade.gui

import logging

import constants

from team import Team

class VictoryScreen(arcade.View):
    def __init__(self, window: arcade.Window = None, game_loop = None, victor:Team = None):
            super().__init__(window)

            self._game_loop = game_loop

            self._ui_manager = arcade.gui.UIManager()
            self._ui_manager.enable()

            self.v_box = arcade.gui.UIBoxLayout(space_between=5)

            if victor is not None:
                self._victory_label = arcade.gui.UILabel(text=f'{victor.name} has won!')
            else:
                self._victory_label = arcade.gui.UILabel(text=f'It\'s a Draw!')

            self.v_box.add(self._victory_label)

            self._battle_button = arcade.gui.UIFlatButton(text="Battle Again!", width=constants.MAIN_MENU_BUTTON_WIDTH)

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

        self._game_loop.create_battle()