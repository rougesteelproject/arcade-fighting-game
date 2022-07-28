from unit import Unit

class DummyDB():
    def __init__(self) -> None:
        self._create_db_if_not_exists()

    def _create_db_if_not_exists(self):
        self._stored_units = []

        sugar_ant = Unit("Sugar Ant", 5, 0, 1, 0.9, 1.2)
        daddy_longlegs = Unit("Daddy Longlegs", 8, 1, 2, 0.8, 1.2)

        self._stored_units.append(sugar_ant)
        self._stored_units.append(daddy_longlegs)

        

    def save_unit(self, unit):
        pass

    def get_unit_by_name(self, unit_name):
        fetched_unit = None

        while fetched_unit == None:
            for unit in self._stored_units:
                if unit.name.lower() == unit_name.lower():
                    fetched_unit = unit

        return fetched_unit


    def get_unit_list_by_name(self, unit_name):
        unit_list = [unit for unit in self._stored_units if unit_name.lower() in unit.name.lower()]

        return unit_list