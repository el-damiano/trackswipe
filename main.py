import math
import pygame
from pygame.math import Vector2


def map_vector_to_key(mappings: list, target: pygame.Vector2, source = Vector2(0.0, 0.0)):
    def nan_to_zero(vec: Vector2):
        if math.isnan(vec.x):
            vec.x = 0.0
        if math.isnan(vec.y):
            vec.y = 0.0

    nan_to_zero(source)
    nan_to_zero(target)

    def part(x):
        return (x > 0.43) + (x >= -0.33)

    target_x = part(target.x)
    target_y = part(target.y)
    source_x = part(source.x)
    source_y = part(source.y)

    relative_target = mappings[source_y][source_x][target_y][target_x]
    return relative_target


def main():

    # TODO: make more intuitive?
    KEYMAP = [
        [
            [
                ["s", "", ""],
                ["", "w", ""],
                ["", "", ""],
            ],
            [
                ["", "r", ""],
                ["", "g", ""],
                ["", "", ""],
            ],
            [
                ["", "", "o"],
                ["", "u", ""],
                [" ", "", ""],
            ],
        ],
        [
            [
                ["", "", ""],
                ["n", "m", ""],
                ["", "", ""],
            ],
            [
                ["j", "q", "b"],
                ["k", "h", "p"],
                ["v", "x", "y"],
            ],
            [
                ["", "", " "],
                ["", "l", "a"],
                ["", " ", "\n"],
            ],
        ],
        [
            [
                ["", "", " "],
                ["", "c", ""],
                ["t", "", ""],
            ],
            [
                ["", "", ""],
                ["", "f", ""],
                [",", "i", "z"],
            ],
            [
                ["", "", ""],
                ["", "d", ""],
                ["", "", "e"],
            ],
        ]
    ]

    listening = True
    pygame.joystick.init()
    joysticks = {}
    clock = pygame.time.Clock()
    first_selection = None
    final_selection = None

    while listening:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                listening = False

            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]

        for joystick in joysticks.values():
            B = joystick.get_button(3)
            if B:
                listening = False

            # TRACKPAD_LEFT = {
            #     "pressed": joystick.get_button(0),
            #     "x": joystick.get_axis(4),
            #     "y": joystick.get_axis(5),
            # }

            TRACKPAD_RIGHT = {
                "pressed": joystick.get_button(1),
                "x": joystick.get_axis(2),
                "y": joystick.get_axis(3),
            }

            trackpad_pressed = TRACKPAD_RIGHT["pressed"]
            key_was_selected = (
                not trackpad_pressed and
                first_selection is not None and
                final_selection is not None
            )

            if trackpad_pressed:
                target = pygame.Vector2(TRACKPAD_RIGHT["x"], TRACKPAD_RIGHT["y"])
                final_selection = target

                if first_selection is None:
                    first_selection = target

            elif key_was_selected:
                print(map_vector_to_key(KEYMAP, final_selection, first_selection))
                first_selection = None

        clock.tick(15)


if __name__ == "__main__":
    pygame.init()
    main()
