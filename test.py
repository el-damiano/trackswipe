import unittest

from pygame import Vector2
from main import map_vector_to_key


class TestVector(unittest.TestCase):

    def test_map_vector_to_key(self):
        COMPASS = [
            ["NW", "N", "NE"],
            ["W",  "0",  "E"],
            ["SW", "S", "SE"],
        ]

        center = Vector2(0, 0)
        center_still = Vector2(0.5, 0.5)
        center_adjacent = Vector2(0.6, 0.6)

        north = Vector2(0, -1)
        north_east = Vector2(1, -1)
        east = Vector2(1, 0)
        south_east = Vector2(1, 1)
        south = Vector2(0, 1)
        south_west = Vector2(-1, 1)
        west = Vector2(-1, 0)
        north_west = Vector2(-1, -1)

        negative_zero = Vector2(-0.0, -0.0)
        subnormal = Vector2(1e-320, 1e-320)
        infinity = Vector2(float('-inf'), float('inf'))
        nan = Vector2(float('nan'), float('nan'))

        test_cases = [
            (center, "0"),
            (center_still, "0"),
            (center_adjacent, "SE"),
            (north, "N"),
            (north_east, "NE"),
            (east, "E"),
            (south_east, "SE"),
            (south, "S"),
            (south_west, "SW"),
            (west, "W"),
            (north_west, "NW"),
            (negative_zero, "0"),
            (subnormal, "0"),
            (infinity, "SW"),
            (nan, "0"),
        ]

        for vector, expected in test_cases:
            self.assertEqual(expected, map_vector_to_key(vector, COMPASS))


if __name__ == '__main__':
    unittest.main()
