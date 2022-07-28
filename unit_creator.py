from unit import Unit
import traceback

class UnitCreator():
    def __init__(self, db_controler) -> None:
        self._db_controller = db_controler

    def get_input_unit_stats(self):
        name = input("Unit name: ")
        
        base_health = 0
        while base_health < 1:
            print("Base health must be at least 1!")   
            base_health = int(input("Base Health: "))
        
        min_attack = -1
        while min_attack < 0:
            print("Min attack cannot be negative!")
            min_attack = int(input("Minimum Attack: "))
        
        max_attack = min_attack -1
        while max_attack < min_attack:
            print("Max attack must be greater than min attack!")
            max_attack = int(input("Max Attack: "))

        min_initiative = 0
        while min_initiative <= 0:
            print("min initiative must be greater than zero!")
            try:
                min_initiative = float(input("Minimum Initiative: "))
            except ValueError:
                traceback.print_exc()
        
        max_initiative = min_initiative -1
        while max_initiative < min_initiative:
            print("Max initiative must be greater than min!")
            max_initiative = float(input("Max Initiative: "))

        return Unit(name, base_health, min_attack, max_attack, min_initiative, max_initiative, ai_type= "basic")

    def save_unit_to_db(self, unit):
        if not unit.is_invalid:
            self._db_controller.save_unit(unit)

    def get_unit_from_db_by_name(self, unit_name):
        unit_data = self._db_controller.get_unit_data_by_name(unit_name)
        unit = Unit(name=unit_data['name'], base_health=unit_data['base_health'], min_attack=unit_data['min_attack'], max_attack=unit_data['max_attack'], min_initiative=unit_data['min_initiative'], max_initiative=unit_data['max_initiative'], ai_type=unit_data['ai_type'], price=unit_data['price'], game_version=unit_data['game_version'], attack_verb=unit_data['attack_verb'])

        return unit