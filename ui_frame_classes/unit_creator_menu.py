import tkinter as tk
import constants
from sys import maxsize

from unit import Unit

#TODO fields for gmail and for modpack

class UnitCreatorMenu(tk.Frame):
    def __init__(self, callback_handler) -> None:
        super().__init__(callback_handler.top_level)

        self._callback_handler = callback_handler
        self._game_loop = self._callback_handler._game_loop

        self.game_version_holder = tk.StringVar(self)
        self.game_version_holder.set(constants.DEFAULT_GAME_VERSION)
        self.game_version_holder.trace('w', lambda x,y,z: self._switch_game_version())
        self.optionmenu_game_version = tk.OptionMenu(
            self, self.game_version_holder, *constants.GAME_VERSION_OPTIONS)
        self.optionmenu_game_version.pack(side="top")

        self.entry_name = tk.Entry(self)
        _text_ = "Name"
        self.entry_name.delete("0", "end")
        self.entry_name.insert("0", _text_)
        self.entry_name.pack(side="top")

        vcmd= (self.register(self._validate_is_number), '%P', '%W')

        self._hp_label = tk.Label(self)
        self._hp_label.configure(text= "Max HP")
        self._hp_label.pack(side="top")
        #TODO every 'from_' and 'increment' below should be a constants.WHATEVER reference
        self.hp_holder = tk.StringVar(self)
        self.spinbox_hp = tk.Spinbox(self)
        self.spinbox_hp.configure(textvariable=self.hp_holder, from_=1, to=maxsize, increment=1, validatecommand=vcmd)
        self.spinbox_hp.pack(side="top")

        #The commands for the following look like they're named backwards, but the point is to limit min to be from 0 to max, limit max from min to infinity
        #TODO better naming scheme?
        #if max goes below min, min goes down?
        #and vice-versa?

        # %P is the value if the edit were allowed
        # %s is the value prior to the edit
        
        self._attack_label = tk.Label(self)
        self._attack_label.configure(text="Attack")
        self._attack_label.pack(side="top")
        self.min_attack_holder = tk.StringVar(self)
        self.spinbox_min_attack = tk.Spinbox(self)
        self.spinbox_min_attack.configure(textvariable=self.min_attack_holder, from_=0, to=maxsize, increment=1, command=lambda: self._update_max_attack(), validatecommand=vcmd)
        self.spinbox_min_attack.pack(side="top")

        self.max_attack_holder = tk.StringVar(self)
        self.spinbox_max_attack = tk.Spinbox(self)
        self.spinbox_max_attack.configure(textvariable=self.max_attack_holder,from_=1, to=maxsize, increment=1, command=lambda: self._update_min_attack(), validatecommand=vcmd)
        self.spinbox_max_attack.pack(side="top")

        self._init_label = tk.Label(self)
        self._init_label.configure(text="Initiative")
        self._init_label.pack(side="top")
        self.min_init_holder = tk.StringVar(self)
        self.spinbox_min_init = tk.Spinbox(self)
        self.spinbox_min_init.configure(textvariable=self.min_init_holder, from_=0.01, to=maxsize, increment=0.01, command=lambda: self._update_max_init(), validatecommand=vcmd)
        self.spinbox_min_init.pack(side="top")

        self.max_init_holder = tk.StringVar(self)
        self.spinbox_max_init = tk.Spinbox(self)
        self.spinbox_max_init.configure(textvariable=self.max_init_holder, from_=0.01, to=maxsize, increment=0.01, command=lambda: self._update_min_init(), validatecommand=vcmd)
        self.spinbox_max_init.pack(side="top")

        self.button_save_unit = tk.Button(self)
        self.button_save_unit.configure(text="Create", command=lambda :self._save_unit())
        self.button_save_unit.pack(side="top")

        self.button_exit_unit_creator = tk.Button(self)
        self.button_exit_unit_creator.configure(text="Main Menu", command=lambda: self._callback_handler.create_main_menu())
        self.button_exit_unit_creator.pack(side="top")

        self.pack(side="top")

    def _save_unit(self):
        game_version = int(self.game_version_holder.get())

        unit_dict = {'name' : self.entry_name.get(),
        'base_health' : self.hp_holder.get(),
        'min_attack': self.spinbox_min_attack.get(),
        'ai_types' : ["basic"], 'attack_verb': 'attacked',
        'game_version' : game_version}

        if game_version >= 2:
            unit_dict.update({'min_initiative': self.spinbox_min_init.get()})
        
        if game_version >= 3:
            unit_dict.update({'max_attack': self.spinbox_max_attack.get(), 'max_initiative': self.spinbox_max_init.get()})        

        self._game_loop.save_unit(Unit.from_dict(unit_dict))

    #these update functions work even when the user can input numbers directly into the spinbox
    #via the textvariable
    
    #if max goes below min, min goes down,
        #and vice-versa
    def _update_max_attack(self):
        if self.min_attack_holder.get() > self.max_attack_holder.get():
            self.max_attack_holder.set(self.min_attack_holder.get())

    def _update_max_init(self):
        if self.min_init_holder.get() > self.max_init_holder.get():
            self.max_init_holder.set(self.min_init_holder.get())

    def _update_min_attack(self):
        if self.max_attack_holder.get() < self.min_attack_holder.get():
            self.min_attack_holder.set(self.max_attack_holder.get())
        
    def _update_min_init(self):
        if self.max_init_holder.get() < self.min_init_holder.get():
            #when the max is set, min.configure(to_=max)
            self.min_init_holder.set(self.max_init_holder.get())
            
    def _validate_is_number(self, P, W):
        if P.is_digit() and P >= self.top_level.nametowidget(W).cget('from_') :
            #get the lower limit/'from_ via spinbox.cget() W is the widget's name
            return True
        else:
            self.bell()
            #the windows error ding
            return False

    def _switch_game_version(self):
        game_version = int(self.game_version_holder.get())

        if game_version >= 3:
            #V3 Has Variance (min and max) and Initiative
            self.spinbox_max_attack.configure(state=tk.NORMAL)
            self.spinbox_min_init.configure(state=tk.NORMAL)
            self.spinbox_max_init.configure(state=tk.NORMAL)
        elif game_version == 2:
            #V2 has Initiative, but no variance
            self.spinbox_max_attack.configure(state=tk.DISABLED)
            self.spinbox_min_init.configure(state=tk.NORMAL)
            self.spinbox_max_init.configure(state=tk.DISABLED)
        elif game_version == 1:
            #V1 has neither Initiative, nor variance
            self.spinbox_max_attack.configure(state=tk.DISABLED)
            self.spinbox_min_init.configure(state=tk.DISABLED)
            self.spinbox_max_init.configure(state=tk.DISABLED)
