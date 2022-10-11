import arcade
import arcade.gui

class SignInMenu(arcade.View):
    def __init__(self, window: arcade.Window = None, game_loop = None, error = None):
        super().__init__(window)
        self._error = error

        self._game_loop = game_loop

        self._ui_manager = arcade.gui.UIManager()
        self._ui_manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        #A LABEL WITH THE ERROR
        if self._error is not None:
            self._error_label = arcade.gui.UILabel(text=self._error)
            self.v_box.add(self._error_label)
        #TODO can I have these entries blank out when clicked on?
        self.email_entry = arcade.gui.UIInputText(text="email")
        self.v_box.add(self.email_entry)
        self.password_entry = arcade.gui.UIInputText(text="password")
        self.v_box.add(self.password_entry)
        #TODO password should obscure the password
        self.login_button = arcade.gui.UIFlatButton(text="login")

        self.login_button.on_click = self._on_login

        self.v_box.add(self.login_button)

        self._ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.WHITE)

        # Create a box group to align the 'open' button in the center
        

    def on_hide_view(self):
        self._ui_manager.disable()
        return super().on_hide_view()

    def on_draw(self):
        """ Draw the menu """
        self.clear()

        self._ui_manager.draw()

    def _on_login(self, event):
        email = self.email_entry.text
        password = self.password_entry.text
        

        self._game_loop.sign_in(email, password)

