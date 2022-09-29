import simplejson as json
import logging
from os import listdir
import fnmatch

from unit import Unit

class JSONDB():
    def __init__(self) -> None:
        self._create_db_if_not_exists()

    def _create_db_if_not_exists(self):
        pass

    def _create_file_if_not_exists(self, file_name):
        pass

    def save_unit(self, unit):
        
        unit_dict = unit.to_dict()

        try:
            pack_name = f'./unit_data/{unit_dict["name"]}.json'
            #each unit gets it's own json file

            with open(pack_name, 'w+') as pack:
                #'w+' means 'Create if not exists, then write'
        
                json.dump(unit_dict, pack)
        except:
            logging.exception()

    def get_unit_list_by_name(self, unit_name, game_version:int):
        #a way to search the file names, then load each file

        json_list = []

        for file in listdir('unit_data'):
            if fnmatch.fnmatch(file, f'*{unit_name}*.json'):
                json_list.append(file)

        unit_data_list = []
        #This is tied to the class so that the loop can use it when buying units

        for json_file in json_list:
            try:
                with open(f'./unit_data/{json_file}') as unit_json:
                    unit_data = json.load(unit_json)
                    if int(unit_data['game_version']) >= game_version:
                        unit_data_list.append(unit_data)
            except:
                logging.exception(f"No unit named {unit_name}")

        self.unit_list = [Unit.from_dict() for unit in unit_data_list]
        return self.unit_list