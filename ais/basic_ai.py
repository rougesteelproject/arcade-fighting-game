from ais.ai import AI

class BasicAI(AI):
    def __init__(self, callback_unit) -> None:
        super().__init__(callback_unit=callback_unit)

        self.name = "basic"

