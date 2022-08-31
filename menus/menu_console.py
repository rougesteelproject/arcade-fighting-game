import logging

class MenuConsole():
    def __init__(self, menu_name, prompt, number_of_options, start_at_one = False) -> None:
        self._name = menu_name
        self._prompt = prompt
        self._number_of_options = number_of_options
        self._start_at_one = start_at_one
        #Options should be a list of functions

    def get_selection(self):
        print(self._name)

        selection_invalid = True

        while selection_invalid:
            try:

                if self._start_at_one == False:

                    print(f'select a number from 0 to {self._number_of_options - 1}')
                    selection_index = int(input(f'{self._prompt}'))

                    if selection_index in range(self._number_of_options):
                        selection_invalid = False
                        return selection_index

                else:
                    print(f'select a number from 1 to {self._number_of_options}')
                    selection_index = int(input(f'{self._prompt}'))

                    if selection_index in range(1, self._number_of_options):
                        selection_invalid = False
                        return selection_index

            except ValueError:
                logging.exception("Tried to input a non-integer as a selection")
                selection_invalid = True

