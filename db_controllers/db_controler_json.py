from fnmatch import fnmatch
import simplejson as json
import logging
import os
import fnmatch

class JSONDB():
    def __init__(self) -> None:
        self._create_db_if_not_exists()

    def _create_db_if_not_exists(self):
        pass

    def _create_file_if_not_exists(self, file_name):
        pass

    def save_unit(self, unit):
        
        unit_dict = {"name": unit.name, "base_health": unit._base_health,"min_attack": unit._min_attack, "max_attack": unit._max_attack, "min_initiative": unit._min_initiative,"max_initiative": unit.get_max_initiative() ,"ai_type" : unit._ai.name, "game_version": unit._game_version, "raw_power_v1": unit.get_raw_power(1), "raw_power_v2": unit.get_raw_power(2), "raw_power_v3": unit.get_raw_power(3), "attack_verb": unit.attack_verb}

        try:
            pack_name = f'./unit_data/{unit.name.lower()}.json'
            #each unit gets it's own json file

            with open(pack_name, 'w+') as pack:
                #'w+' means 'Create if not exists, then write'
        
                json.dump(unit_dict, pack)
        except:
            logging.exception()

    def get_unit_data_by_name(self, unit_name, game_version, enable_other_version_units):
        
        #load form a pack with that name

        try:
            with open(f'{unit_name.lower()}.json') as unit_json:
                unit_data = json.load(unit_json)

                if unit_data['game_version'] == game_version:
                    return unit_data
                elif game_version >= 2 and unit_data['game_version'] >= 2 and enable_other_version_units:
                    return unit_data
                else:
                    return None
                    #this may not be the right aproach. Maybe return None breaks things?
                    
        except:
            logging.exception()

    def get_unit_list_by_name(self, unit_name):
        #a way to search the file names, then load each file

        json_list = []

        for file in os.listdir('unit_data'):
            if fnmatch.fnmatch(file, f'*{unit_name}*.json'):
                json_list.append(file)

        unit_data_list = []

        for json_file in json_list:
            try:
                with open(f'./unit_data/{json_file}') as unit_json:
                    unit_data = json.load(unit_json)
                    unit_data_list.append(unit_data)
            except:
                logging.exception()


        return unit_data_list