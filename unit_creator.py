from unit import Unit
import traceback

class UnitCreator():
    def __init__(self, db_controler) -> None:
        self._db_controller = db_controler

    def get_input_unit_stats(self, game_version):

        name = input("Unit name: ")

        #note to self, keep this consistent with unit._check_stat_validity()
        
        base_health = 0
        while base_health < 1:
            print("Base health must be at least 1!")   
            try:
                base_health = int(input("Base Health: "))
            except ValueError:
                    traceback.print_exc()
        
        
        min_attack = -1
        if game_version >= 2:
            while min_attack < 0:
                print("Min attack cannot be negative!")
                try:
                    min_attack = int(input("Minimum Attack: "))
                except ValueError:
                        traceback.print_exc()
        else:
            while min_attack < 0:
                print("Attack cannot be negative!")
                try:
                    min_attack = int(input("Attack: "))
                except ValueError:
                        traceback.print_exc()
        
        if game_version >= 3:
            max_attack = min_attack -1
            while max_attack < min_attack:
                print("Max attack must be greater than or equal to min attack!")
                try:
                    max_attack = int(input("Max Attack: "))
                except ValueError:
                    traceback.print_exc()
        else:
            max_attack = min_attack

        if game_version == 2:
            min_initiative = 1
            max_initiative = -1
            while max_initiative < 0:
                print("Initiative must be at least zero!")
                try:
                    min_initiative = float(input("Initiative: "))
                except ValueError:
                    traceback.print_exc()
            
        elif game_version >= 3:
                min_initiative = 0
                while min_initiative <= 0:
                    print("min initiative must be greater than zero!")
                    try:
                        min_initiative = float(input("Minimum Initiative: "))
                    except ValueError:
                        traceback.print_exc()

                max_initiative = min_initiative -1
                while max_initiative < min_initiative:
                    print("Max initiative must be greater than or equal to min!")
                    try:
                        max_initiative = float(input("Max Initiative: "))
                    except ValueError:
                        traceback.print_exc()

        else:
            min_initiative = None
            max_initiative = None

        return Unit(name, base_health, min_attack, max_attack, min_initiative, max_initiative, ai_type= "basic", game_version=game_version)

    def save_unit_to_db(self, unit):
        self._db_controller.save_unit(unit)

    def get_unit_from_db_by_name(self, unit_name):
        unit_data = self._db_controller.get_unit_data_by_name(unit_name)
        unit = Unit(name=unit_data['name'], base_health=unit_data['base_health'], min_attack=unit_data['min_attack'], max_attack=unit_data['max_attack'], min_initiative=unit_data['min_initiative'], max_initiative=unit_data['max_initiative'], ai_type=unit_data['ai_type'], price_v1=unit_data['price_v1'], price_v2=unit_data['price_v2'], price_v3=unit_data['price_v3'], game_version=unit_data['game_version'], attack_verb=unit_data['attack_verb'])

        return unit