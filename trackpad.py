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

        self.__grid_ratio = 0.33
        self.user_input = 0
        self.event_codes = 0
        self.joystick = 0
        self.pressed_idx = 0
        self.x_idx = 0
        self.y_idx = 0

        self.__pressed = 0
        self.__x = 0.0
        self.__y = 0.0
        self.__first_selection = None
        self.__final_selection = None

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

        def vector_part(vec):
            vec.x = (vec.x > self.__grid_ratio) + (vec.x >= -self.__grid_ratio)
            vec.y = (vec.y > self.__grid_ratio) + (vec.y >= -self.__grid_ratio)
            return vec

        # rotating because Steam Controller trackpads are at an angle
        target_rotated = target.rotate(self.rotation_angle)
        source_rotated = source.rotate(self.rotation_angle)

        target_new = vector_part(target_rotated)
        source_new = vector_part(source_rotated)

        # unpacking them because Vector2 stores float values
        target_x, target_y = int(target_new.x), int(target_new.y)
        source_x, source_y = int(source_new.x), int(source_new.y)

        # right now I'm simply accessing absolute positions in the matrix
        # this feels stiff
        # TODO: improve by using a relative vector
        mapping_target = mappings[source_y][source_x][target_y][target_x]
        return mapping_target

    def process(self) -> None:
        """Meant to be called each tick.
        Detects trackpad presses and positions.
        Inject input events into the Linux input subsystem.
        """
        if self.user_input == 0 or self.event_codes == 0:
            return

        self.__x = self.joystick.get_axis(self.x_idx)
        self.__y = self.joystick.get_axis(self.y_idx)
        self.__pressed = abs(self.__x) != 0.0 and abs(self.__y) != 0.0

        key_was_selected = (
            not self.__pressed and
            self.__first_selection is not None and
            self.__final_selection is not None
        )

        if self.__pressed:
            target = pygame.Vector2(self.__x, self.__y)
            self.__final_selection = target

            if self.__first_selection is None:
                self.__first_selection = target

        elif key_was_selected:
            key = self.__map_vector_to_key(self.keymap, self.__final_selection, self.__first_selection)
            self.__first_selection = None
            if key is None:
                return

            self.user_input.write(self.event_codes.EV_KEY, key, 1)
            self.user_input.syn()
            self.user_input.write(self.event_codes.EV_KEY, key, 0)
            self.user_input.syn()
