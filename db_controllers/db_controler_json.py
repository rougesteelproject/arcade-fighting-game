import simplejson as json
import traceback

class JSONDB():
    def __init__(self) -> None:
        self._create_db_if_not_exists()

    def _create_db_if_not_exists(self):
        pass

    def save_unit(self, unit):
        
        unit_dict = {"name": unit.name, "health": unit._base_health,"min_attack": unit._min_attack, "max_attack": unit._max_attack, "min_initiative": unit._min_initiative,"max_initiative": unit.get_max_initiative() ,"ai_type" : unit._ai.name, "price": unit.get_price(), "attack_verb": unit.attack_verb}

        try:
            pack_name = f'/unit_data/{unit.name}.json'
            #each unit gets it's own json file

            with open(pack_name, 'w') as pack:
        
                json.dump(unit_dict, pack)
        except:
            traceback.print_exc()

    def get_unit_by_name(self, unit_name):
        
        #TODO load form a pack with that name

        return fetched_unit


    def get_unit_list_by_name(self, unit_name):
        #TODO a way to search the file names, then load each file

        return unit_list