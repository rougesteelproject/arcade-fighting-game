from random import randint


class AI():
    def __init__(self, callback_unit) -> None:
        self._callback_unit = callback_unit

    def _update_target_list(self, targets):
        self._target_list = targets
    
    def _select_target(self):
        target = self._target_list[randint(0, len(self._target_list))]
        return target

    def _attack(self):
        damage = self._callback_unit.attack_roll()
        target = self._select_target()

        return damage, target

    def _decide_to_attack(self):
        if True:
            damage, target = self._attack()
            
        else:
            damage = None
            target = None

        return damage, target


    def do_game_tick(self, targets):
        self._update_target_list(targets)
        damage, target = self._decide_to_attack()

        return damage, target
