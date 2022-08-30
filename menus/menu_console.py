import logging

class MenuConsole():
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

                if selection_index in range(self._number_of_options):
                    selection_invalid = False
                    return selection_index

            except ValueError:
                print("Tried to input a non-integer as a selection")
                selection_invalid = True

