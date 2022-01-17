import unittest

from game.common.hitbox import Hitbox
from game.common.map_object import MapObject
from game.common.teleporter import Teleporter
from game.utils.partition_grid import PartitionGrid


class TestPartitionGrid(unittest.TestCase):
    def setUp(self):
        width = 500
        height = 500
        self.grid = PartitionGrid(width, height, 25, 25)
        self.ex_obj = MapObject(hitbox=Hitbox(5, 5, (100, 100)))
        obj_list = [
            self.ex_obj,
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        self.grid.add_object_list(obj_list)

    def test_find_row(self):
        self.assertEqual(5, self.grid.find_row(100))
        self.assertEqual(5, self.grid.find_row(115))
        self.assertEqual(6, self.grid.find_row(125))

    def test_find_column(self):
        self.assertEqual(5, self.grid.find_column(100))
        self.assertEqual(5, self.grid.find_column(115))
        self.assertEqual(6, self.grid.find_column(125))

    def test_find_object_coordinates(self):
        self.assertTrue(self.grid.find_object_coordinates(100, 100))

    def test_find_object_hitbox(self):
        self.assertTrue(self.grid.find_object_hitbox(Hitbox(5, 5, (200, 100))))

    def test_find_object_object(self):
        self.assertTrue(self.grid.find_object_object(self.ex_obj))

    def test_remove_object(self):
        self.grid.remove_object(self.ex_obj)
        self.assertFalse(self.grid.find_object_object(self.ex_obj))

    def test_add_corner(self):
        tel = MapObject(hitbox=Hitbox(10, 10, (490, 486)))
        self.grid.add_object(tel)
        self.assertEqual(self.grid.find_object_coordinates(490, 486), tel)
