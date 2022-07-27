import traceback

class Menu():
    def __init__(self, menu_name, prompt, number_of_options) -> None:
        self._name = menu_name
        self._prompt = prompt
        self._number_of_options = number_of_options
        #Options should be a list of functions

    def get_selection(self):
        print(self._name)

        selection_invalid = True

        while selection_invalid:
            try:
                print(f'select a number from 0 to {self._number_of_options - 1}')
                selection_index = int(input(f'{self._prompt}'))


                if selection_index in range(0, self._number_of_options - 1):
                    selection_invalid = False
                    return selection_index

            except:
                traceback.print_exception()
                selection_invalid = True

