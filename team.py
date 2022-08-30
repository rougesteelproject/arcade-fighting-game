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
        if unit in self.members and unit in self._living_members:
            self.dead_members.append(unit)
            self._living_members.remove(unit)

    def get_living_members(self):
        return self._living_members

    def buy(self, unit):
        if self.money >= unit.get_raw_power():
            self._add_unit(unit)
            self.money -= unit.get_raw_power()
            
        else:
            print("Insufficient money.")

    def sell(self, unit_to_remove):
        if unit_to_remove in self.members:
            self._remove_unit(unit_to_remove)
        self.money += unit_to_remove.get_raw_power()

    def combat_init(self):
        self._living_members = self.members
        self.dead_members = []

    def list_members_grouped(self):

        troop_disposition = """"""

        unit_type = ""
        unit_count = 0

        for unit in self.members:
            if unit.name != unit_type:
                unit_type = unit.name

                unit_count = sum(unit.name == unit_type for unit in self.members)

                troop_disposition += f'{unit.name} x {unit_count}'
                

        return troop_disposition


