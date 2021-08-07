from game.common.enums import ActionType
from game.controllers.controller import Controller

class ReloadController(Controller):
    @staticmethod
    def handle_actions(client):
        if client.action._chosen_action is ActionType.reload:
            client.shooter.primary_gun.reload()
