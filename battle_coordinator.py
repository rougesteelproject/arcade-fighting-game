class BattleCoordinator():
    def __init__(self) -> None:
        self._teams = []

        self._alive_units = []
        self._dead_units = []

    def add_unit(self, unit, team:int):
        self._teams[team].append(unit)

    def run_battle(self):
        pass