
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
        
        unit_dict = {"name": unit.name, "base_health": unit._base_health,"min_attack": unit._min_attack ,"ai_types" : unit._ai_types, "game_version": unit._game_version, "raw_power_v1": unit.get_raw_power(1), "attack_verb": unit.attack_verb}

        unit_game_version = unit_dict['game_version']

        if  unit_game_version >= 2:
            unit_dict['min_initiative'] = unit._min_initiative
            unit_dict["raw_power_v2"] = unit.get_raw_power(2)

            if unit_game_version >= 3:
                unit_dict['max_initiative'] = unit.get_max_initiative()
                unit_dict['max_attack'] = unit._max_attack
                unit_dict["raw_power_v3"] = unit.get_raw_power(3)

        try:
            pack_name = f'./unit_data/{unit.name.lower()}.json'
            #each unit gets it's own json file

            with open(pack_name, 'w+') as pack:
                #'w+' means 'Create if not exists, then write'
        
                json.dump(unit_dict, pack)
        except:
            logging.exception()

    def get_unit_data_by_name(self, unit_name, game_version):
        
        #load form a pack with that name

        try:
            with open(f'{unit_name.lower()}.json') as unit_json:
                unit_data = json.load(unit_json)

                if unit_data['game_version'] >= game_version:
                    return unit_data

                else:
                    return None
                    
        except:
            logging.exception()

    def get_unit_list_by_name(self, unit_name, game_version):
        #a way to search the file names, then load each file

        game_version = int(game_version)

        json_list = []

        for file in os.listdir('unit_data'):
            if fnmatch.fnmatch(file, f'*{unit_name}*.json'):
                json_list.append(file)

        self.unit_data_list = []

        for json_file in json_list:
            try:
                with open(f'./unit_data/{json_file}') as unit_json:
                    unit_data = json.load(unit_json)
                    if int(unit_data['game_version']) >= game_version:
                        self.unit_data_list.append(unit_data)
            except:
                logging.exception(f"No unit named {unit_name}")


        return self.unit_data_list

    def search_units_by_name(self, unit_name, game_version):
        search_bar_units_data = self.get_unit_list_by_name(unit_name, game_version)

        unit_prompts = []
        
        if len(search_bar_units_data) != 0:
            for index, unit_data in enumerate(search_bar_units_data):

                unit_power = unit_data[f'raw_power_v{game_version}']
                #diferent power for diferent game versions

                unit_prompts.append(f'{index}: {unit_data["name"]}: {unit_power} \n')


            return unit_prompts