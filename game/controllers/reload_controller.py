from game.common.enums import ActionType
from controller import Controller


class ReloadController(Controller):
    @staticmethod
    def handle_actions(client):
        if client.action.chosen_action is ActionType.reload:
            client.shooter.primary_gun.reload()
