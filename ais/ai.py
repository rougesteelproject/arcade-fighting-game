from random import choice


class AI():
    def __init__(self) -> None:

        self.name = "ai_class"

    def _update_target_list(self, targets):
        self._target_list = targets
    
    def _select_target(self):
        target = choice(self._target_list)
        return target

    def _attack(self, use_variance):
        damage = self._callback_unit.attack_roll(use_variance)
        target = self._select_target()

        return damage, target

    def _decide_to_attack(self, use_variance):
        if True:
            damage, target = self._attack(use_variance)
            
        else:
            damage = None
            target = None

        return damage, target


    def do_game_tick(self, calling_unit, targets, use_variance):
        self._callback_unit = calling_unit

        self._update_target_list(targets)
        damage, target = self._decide_to_attack(use_variance)

        return damage, target
