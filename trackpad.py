import os
import math
import pygame
from pygame.math import Vector2

class Trackpad():
    """
    Module for interacting with a Steam Controller Trackpad.

    Arguments:
    keymap - assumed to be a 3x3 matrix of 3x3 matrices with ``evdev`` eventcodes | None
    rotation_angle - used to rotate the trackpad angle
    """

    def __init__(self, keymap, rotation_angle) -> None:
        self.keymap = keymap
        self.rotation_angle = rotation_angle  # used to rotate the trackpad angle

        self.__grid_ratio = 1.33
        self.user_input = 0
        self.event_codes = 0
        self.joystick = 0
        self.pressed_idx = 0
        self.x_idx = 0
        self.y_idx = 0

        self.__pressed = 0
        self.__x = 0.0
        self.__y = 0.0
        self.__selection_first = None
        self.__selection_last = None

    def assign(self, user_input, event_codes, joystick, pressed_idx, x_idx, y_idx) -> None:
        """Meant to be called each tick.
        Assigns arguments to the ``Trackpad`` module.

        Args:
        user_input - a userland input device that can inject input events into the Linux input subsystem.
        event_codes - ``evdev`` event codes
        joystick - ``pygame.Joystick`` module
        *_idx - indices of inputs from `joystick`
        """
        self.user_input = user_input
        self.event_codes = event_codes
        self.joystick = joystick
        self.pressed_idx = pressed_idx
        self.x_idx = x_idx
        self.y_idx = y_idx

    def __map_vector_to_key(self, mappings: list, target: pygame.Vector2, source = Vector2(0.0, 0.0)):
        def nan_to_zero(vec: Vector2):
            if math.isnan(vec.x):
                vec.x = 0.0
            if math.isnan(vec.y):
                vec.y = 0.0

        nan_to_zero(source)
        nan_to_zero(target)

        def remap_vector(vec):
            rotated = vec.rotate(self.rotation_angle)
            return rotated + Vector2(1, 1)

        def vector_snap(vec):
            vec.x = (vec.x > self.__grid_ratio) + (vec.x >= -self.__grid_ratio)
            vec.y = (vec.y > self.__grid_ratio) + (vec.y >= -self.__grid_ratio)
            return vec

        def get_extension(source, target):
            difference = source - target
            # print(f"diff: {difference}")
            return Vector2(0, 0)

        # # rotating because Steam Controller trackpads are at an angle
        # source_rotated = source.rotate(self.rotation_angle)
        # target_rotated = target.rotate(self.rotation_angle)
        # extension = get_extension(source_rotated, target_rotated)

        source_remapped = remap_vector(source)
        target_remapped = remap_vector(target)

        print(f"source before: {source}")
        print(f"target before: {target}")
        #
        # print(f"source remapped: {source_remapped}")
        # print(f"target remapped: {target_remapped}")
        #
        # print(f"source snapped: {vector_snap(source_remapped)}")
        # print(f"target snapped: {vector_snap(target_remapped)}")

        print(f"length between: {target_remapped - source_remapped}")

        return None

    def process(self) -> None:
        """Meant to be called each tick.
        Detects trackpad presses and positions.
        Inject input events into the Linux input subsystem.
        """
        if self.user_input == 0 or self.event_codes == 0:
            return

        self.__pressed = self.joystick.get_button(self.pressed_idx)
        self.__x = self.joystick.get_axis(self.x_idx)
        self.__y = self.joystick.get_axis(self.y_idx)

        key_was_selected = (
            not self.__pressed and
            self.__selection_first is not None and
            self.__selection_last is not None
        )

        if self.__pressed:
            target = pygame.Vector2(self.__x, self.__y)
            self.__selection_last = target

            if self.__selection_first is None:
                self.__selection_first = target

        elif key_was_selected:
            key = self.__map_vector_to_key(self.keymap, self.__selection_last, self.__selection_first)
            self.__selection_first = None
            if key is None:
                return

            self.user_input.write(self.event_codes.EV_KEY, key, 1)
            self.user_input.syn()
            self.user_input.write(self.event_codes.EV_KEY, key, 0)
            self.user_input.syn()
