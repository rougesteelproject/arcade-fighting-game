import arcade

class Team(arcade.SpriteList):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.members = []
        self.cost = 0

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

    def buy(self, unit, game_version, money_limit):
        if unit.get_raw_power(game_version) is not None:

            if self.cost + unit.get_raw_power(game_version) <= int(money_limit):
                self._add_unit(unit)
                self.cost += unit.get_raw_power(game_version)


    def sell(self, unit_to_remove, game_version):
        if unit_to_remove in self.members:
            self._remove_unit(unit_to_remove)
        self.cost -= unit_to_remove.get_raw_power(game_version)

    def setup(self, arena_slot):
        self._arena_slot = arena_slot
        self._living_members = self.members
        self.extend(self.members)
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

    def list_outdated_members(self, new_game_version):

        troop_disposition = """"""

        unit_type = ""
        unit_count = 0

        for unit in self.members:
            if unit._game_version < new_game_version:
                if unit.name != unit_type:
                    unit_type = unit.name

                    unit_count = sum(unit.name == unit_type for unit in self.members)

                    troop_disposition += f'{unit.name} x {unit_count}'
                

        return troop_disposition

    def sell_outdated_units(self, previous_game_version, new_game_version):

        outdated_units = [unit for unit in self.members if unit._game_version < new_game_version]

        for outdated_unit in outdated_units:
            self.sell(outdated_unit, previous_game_version)

    def change_game_version_recalculate_units(self, previous_game_version, new_game_version):
        
        units_to_recalculate = [unit for unit in self.members]

        for unit_to_recalculate in units_to_recalculate:
            self.cost -= unit_to_recalculate.get_raw_power(previous_game_version)
            self.cost += unit_to_recalculate.get_raw_power(new_game_version)
