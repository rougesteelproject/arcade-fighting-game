import tkinter as tk

class MainMenu(tk.Frame):
    def __init__(self, callback_handler) -> None:
        super().__init__(callback_handler.top_level)

        self._callback_handler = callback_handler
        self._game_loop = self._callback_handler._game_loop

        self.button_battle = tk.Button(self)
        self.button_battle.configure(
            anchor="n",
            compound="top",
            font="TkDefaultFont",
            justify="center",
            text="Battle!",
            command=lambda :self._game_loop.create_battle()
        )
        self.button_battle.pack(side="top")
        
        self.button_create_units = tk.Button(self)
        self.button_create_units.configure(text="Create Units", command=lambda :self._game_loop.run_unit_creator_menu())
        self.button_create_units.pack(side="top")
        
        self.button_exit = tk.Button(self)
        self.button_exit.configure(
            default="normal",
            font="TkDefaultFont",
            justify="left",
            takefocus=True,
            text="Exit",
            command=lambda :callback_handler.exit_game()
        )
        self.button_exit.pack(side="top")
        self.pack(side="top")

        self.ready = True