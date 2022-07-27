class Team():
    def __init__(self, name, money) -> None:
        self.name = name
        self.members = []
        self.money = money

    def _add_unit(self, unit):
        self.members.append(unit)
        unit.set_callback_team(self)

    def _remove_unit(self, unit):
        self.members.remove(unit)

    def kill_unit(self, unit):
        if unit in self.members & unit in self.alive_members:
            self.dead_members.append(unit)
            self.living_members.remove(unit)

    def buy(self, unit):
        if self.money >= unit.price:
            self._add_unit(unit)
            self.money -= unit.price
            
        else:
            print("Insufficient money.")

    def sell(self, unit_to_remove):
        if unit_to_remove in self.members:
            self._remove_unit(unit_to_remove)
        self.money += unit_to_remove.price

    def combat_init(self):
        self.living_members = self.members
        self.dead_members = []