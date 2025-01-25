# TODO: rewrite in a better language for Steam Input integration and portability
import pygame

from trackpad import Trackpad
from evdev import uinput, ecodes as e


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
                [e.KEY_DOT, e.KEY_F, e.KEY_SLASH],
                [e.KEY_COMMA, e.KEY_I, e.KEY_Z],
            ],
            [
                [None, None, None],
                [None, e.KEY_D, None],
                [None, None, e.KEY_E],
            ],
        ]
    ]

    TRACKPAD_LEFT = Trackpad(KEYMAP, 20)
    TRACKPAD_RIGHT = Trackpad(KEYMAP, -20)

    FPS = 15
    listening = True
    global_cooldown = 0
    clock = pygame.time.Clock()

    mode_switch_cooldown = 100
    mode_typing_active = False

    pygame.joystick.init()
    joysticks = {}

    with uinput.UInput() as user_input:
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
                B_PRESSED = joystick.get_button(3)
                if B_PRESSED:
                    listening = False

                Y_PRESSED = joystick.get_button(5)
                if Y_PRESSED:
                    global_cooldown += clock.get_time()
                    if global_cooldown > mode_switch_cooldown:
                        global_cooldown = 0
                        mode_typing_active = not mode_typing_active

                if not mode_typing_active:
                    continue

                TRACKPAD_LEFT.assign(user_input, e, joystick, 0, 4, 5)
                TRACKPAD_LEFT.process()

                TRACKPAD_RIGHT.assign(user_input, e, joystick, 1, 2, 3)
                TRACKPAD_RIGHT.process()

            clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    main()
