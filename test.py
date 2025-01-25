import unittest
from pygame import Vector2
from trackpad import Trackpad


class TestTrackpad(unittest.TestCase):

    KEYMAP = [
        [
            [
                ['s', None, None],
                [None, 'w', None],
                [None, None, None],
            ],
            [
                [None, 'r', None],
                [None, 'g', None],
                [None, None, None],
            ],
            [
                [None, None, 'o'],
                [None, 'u', None],
                [None, None, None],
            ],
        ],
        [
            [
                [None, None, None],
                ['n', 'm', None],
                [None, None, None],
            ],
            [
                ['j', 'q', 'b'],
                ['k', 'h', 'p'],
                ['v', 'x', 'y'],
            ],
            [
                [None, '\n', None],
                [None, 'l', 'a'],
                [None, None, ' '],
            ],
        ],
        [
            [
                [None, None, None],
                [None, 'c', None],
                ['t', None, None],
            ],
            [
                [None, None, None],
                ['.', 'f', '/'],
                [',', 'i', 'z'],
            ],
            [
                [None, None, None],
                [None, 'd', None],
                [None, None, 'e'],
            ],
        ]
    ]

    def test_map_edge_case_vectors_to_keys(self):
        expected_edge = ""

        # edge_cases = [
        #     [Vector2(float('-inf'), float('inf')), Vector2(float('inf'), float('inf'))],
        #     [Vector2(float('inf'), float('-inf')), Vector2(float('inf'), float('inf'))],
        #     [Vector2(float('inf'), float('inf')), Vector2(float('-inf'), float('inf'))],
        #     [Vector2(float('inf'), float('inf')), Vector2(float('inf'), float('-inf'))],
        #     [Vector2(float('nan'), float('nan')), Vector2(float('nan'), float('nan'))],
        # ]
        # for source, target in edge_cases:
        #     print(trackpad._Trackpad__map_vector_to_key(self.KEYMAP, target, source))

    def test_map_vectors_from_steam_controller_to_keys(self):
        expected1 = 'hello, world.'
        expected2 = "Instead of pouring in more\nbetter stop while you can."

        trackpad = Trackpad(self.KEYMAP, 20)
        trackpad._Trackpad__grid_ratio = 1.33  # keep test indiependant from the implementation

        test_cases = [
            [Vector2(-0.00454712, 0.0545044), Vector2(-0.0106201, 0.0626526)],  # h
            [Vector2(0.37265, 0.829315), Vector2(0.389923, 0.814331)],          # e
            [Vector2(0.827087, 0.338318), Vector2(0.612, 0.322418)],            # l
            [Vector2(0.792908, 0.332275), Vector2(0.0250854, 0.0972595)],       # l
            [Vector2(0.684631, -0.420349), Vector2(0.703857, -0.419342)],       # o
            [Vector2(-0.155792, 0.976013), Vector2(-0.571869, 0.814331)],       # ,
            [Vector2(0.862274, 0.315826), Vector2(0.551758, 0.889221)],         # _
            [Vector2(-0.430878, -0.799774), Vector2(-0.298492, -0.583832)],     # w
            [Vector2(0.83139, -0.357788), Vector2(0.845215, -0.326691)],        # o
            [Vector2(0.310547, -0.752991), Vector2(0.315979, -0.753265)],       # r
            [Vector2(0.889404, 0.299377), Vector2(0.455261, 0.141418)],         # l
            [Vector2(0.270325, 0.916138), Vector2(0.202454, 0.565857)],         # d
        ]

        for source, target in test_cases:
            print(trackpad._Trackpad__map_vector_to_key(self.KEYMAP, target, source))

if __name__ == '__main__':
    unittest.main()
