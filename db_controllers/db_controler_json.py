from fnmatch import fnmatch
import simplejson as json
import traceback
import os
import fnmatch

class JSONDB():
    def __init__(self) -> None:
        self._create_db_if_not_exists()

    def _create_db_if_not_exists(self):
        pass

    def save_unit(self, unit):
        
        unit_dict = {"name": unit.name, "health": unit._base_health,"min_attack": unit._min_attack, "max_attack": unit._max_attack, "min_initiative": unit._min_initiative,"max_initiative": unit.get_max_initiative() ,"ai_type" : unit._ai.name, "price": unit.get_price(), "attack_verb": unit.attack_verb}

        try:
            pack_name = f'/unit_data/{unit.name.lower()}.json'
            #each unit gets it's own json file

            with open(pack_name, 'w') as pack:
        
                json.dump(unit_dict, pack)
        except:
            traceback.print_exc()

    def get_unit_data_by_name(self, unit_name):
        
        #TODO load form a pack with that name

        try:
            with open(f'{unit_name.lower()}.json') as unit_json:
                unit_data = json.load(unit_json)
                return unit_data
        except:
            traceback.print_exc()

    def get_unit_list_by_name(self, unit_name):
        #TODO a way to search the file names, then load each file

        json_list = []

        for file in os.listdir('unit_data'):
            if fnmatch.fnmatch(file, f'*{unit_name}*.json'):
                json_list.append(file)

        unit_data_list = []

        for json_file in json_list:
            try:
                with open(json_file) as unit_json:
                    unit_data = json.load(unit_json)
                    unit_data_list.append(unit_data)
            except:
                traceback.print_exc()


        return unit_data_list