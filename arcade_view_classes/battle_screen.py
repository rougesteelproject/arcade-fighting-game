import arcade

class BattleScreen(arcade.View):
    def __init__(self, window: arcade.Window = None, game_loop = None):
                super().__init__(window)

                self._game_loop = game_loop

                self.background = None

    def setup(self):
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")