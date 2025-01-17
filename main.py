import math
import pygame
from pygame.math import clamp


def map_vector_to_key(vec: pygame.Vector2, mappings: list):
    if math.isnan(vec.x):
        vec.x = 0.0
    if math.isnan(vec.y):
        vec.y = 0.0

    x = round(clamp(vec.x, -1.0, 1.0)) + 1
    y = round(clamp(vec.y, -1.0, 1.0)) + 1
    return mappings[y][x]


def main():

    KEYMAP = [
        ["↖", "↑", "↗"],
        ["←", "*", "→"],
        ["↙", "↓", "↘"]
    ]

    listening = True
    pygame.joystick.init()
    joysticks = {}

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

            TRACKPAD_LEFT = {
                "pressed": joystick.get_button(0),
                "x": joystick.get_axis(4),
                "y": joystick.get_axis(5),
            }

            TRACKPAD_RIGHT = {
                "pressed": joystick.get_button(1),
                "x": joystick.get_axis(2),
                "y": joystick.get_axis(3),
            }


if __name__ == "__main__":
    pygame.init()
    main()
