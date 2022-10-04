import tkinter as tk

class SignInMenu(tk.Frame):
    def __init__(self, callback_handler, error:str = None) -> None:
        super().__init__(callback_handler.top_level)

        self._callback_handler = callback_handler
        self._game_loop = self._callback_handler._game_loop

        if error is not None:
            self._error_label = tk.Label(self, text=error)
            self._error_label.pack(side="top")

        self.entry_email = tk.Entry(self)
        _text_ = "email"
        self.entry_email.delete("0", "end")
        self.entry_email.insert("0", _text_)
        self.entry_email.pack(side="top")

        self.entry_password = tk.Entry(self)
        _text_ = "password"
        self.entry_password.delete("0", "end")
        self.entry_password.insert("0", _text_)
        self.entry_password.pack(side="top")

        self.button_login = tk.Button(self)
        self.button_login.configure(text="Log In", command=lambda :self._login())
        self.button_login.pack(side="top")

        self.pack(side = "top")

    def _login(self):

        email = self.entry_email.get()

        password = self.entry_password.get()

        self._game_loop.sign_in(email, password)