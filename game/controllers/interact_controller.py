from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.common.items.upgrade import Upgrade
from game.common.door import Door
from game.common.items.money import Money
from game.common.moving.shooter import Shooter
from game.common.action import Action
from game.common.game_board import GameBoard
from game.common.enums import *


class InteractController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client, world):
        if client.action._chosen_action is ActionType.interact:

            #placeholder line for now
            object_target = None

            if isinstance(object_target, Upgrade):
                self.interact_upgrade(client, world, object_target)
            elif isinstance(object_target, Door):
                self.interact_door(client, world, object_target)
            elif isinstance(object_target, Money):
                self.interact_money(client, world, object_target)
            else:
                pass

    def interact_upgrade(self, client, world, upgrade):
        if client.shooter.has_empty_slot('upgrades'):
            client.shooter.append_inventory(upgrade)
            world["game_board"].partition.remove_object(upgrade)

    def interact_money(self, client, world, money):
        client.shooter.money = client.shooter.money + money.amount
        world["game_board"].partition.remove_object(money)

    def interact_door(self, client, world, door):
        if door.open_state == False:
            door.open_state = True



