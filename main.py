import math
import pygame
from pygame.math import Vector2
from evdev import uinput, ecodes as e


def map_vector_to_key(mappings: list, target: pygame.Vector2, source = Vector2(0.0, 0.0)):
    def nan_to_zero(vec: Vector2):
        if math.isnan(vec.x):
            vec.x = 0.0
        if math.isnan(vec.y):
            vec.y = 0.0

    nan_to_zero(source)
    nan_to_zero(target)

    # TODO: figure out how to properly divide it
    def part(x):
        return (x > 0.33) + (x >= -0.33)

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
                [e.KEY_S, None, None],
                [None, e.KEY_W, None],
                [None, None, None],
            ],
            [
                [None, e.KEY_R, None],
                [None, e.KEY_G, None],
                [None, None, None],
            ],
            [
                [None, None, e.KEY_O],
                [None, e.KEY_U, None],
                [None, None, None],
            ],
        ],
        [
            [
                [None, None, None],
                [e.KEY_N, e.KEY_M, None],
                [None, None, None],
            ],
            [
                [e.KEY_J, e.KEY_Q, e.KEY_B],
                [e.KEY_K, e.KEY_H, e.KEY_P],
                [e.KEY_V, e.KEY_X, e.KEY_Y],
            ],
            [
                [None, e.KEY_ENTER, None],
                [None, e.KEY_L, e.KEY_A],
                [e.KEY_BACKSPACE, e.KEY_BACKSPACE, e.KEY_SPACE],
            ],
        ],
        [
            [
                [None, None, None],
                [None, e.KEY_C, None],
                [e.KEY_T, None, None],
            ],
            [
                [None, None, None],
                [None, e.KEY_F, None],
                [None, e.KEY_I, e.KEY_Z],
            ],
            [
                [None, None, None],
                [None, e.KEY_D, None],
                [None, None, e.KEY_E],
            ],
        ]
    ]

    listening = True
    pygame.joystick.init()
    joysticks = {}
    clock = pygame.time.Clock()
    first_selection = None
    final_selection = None

    with uinput.UInput() as ui:
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
                    key = map_vector_to_key(KEYMAP, final_selection, first_selection)
                    first_selection = None
                    if key is None:
                        continue

                    ui.write(e.EV_KEY, key, 1)
                    ui.syn()
                    ui.write(e.EV_KEY, key, 0)
                    ui.syn()

            clock.tick(15)


if __name__ == "__main__":
    pygame.init()
    main()
