from enum import Enum

import arcade

from constants import SPRITE_SCALE


def load_100x100_textures(
    sprite_sheet: arcade.SpriteSheet, row, count, from_right=False
):
    textures = []
    sheet_width = sprite_sheet.image.width
    for i in range(count):
        if from_right:
            # Adjust the x position for left-facing textures
            x = sheet_width - (49 + i * 100)
        else:
            # Adjust the x position for right-facing textures
            x = 49 + i * 100

        y = 100 * row + 49
        texture = sprite_sheet.get_texture(rect=arcade.XYWH(x, y, 100, 100))
        textures.append(texture)
    return textures


class AnimatedSprite(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=SPRITE_SCALE)
        self.center_x = 0
        self.center_y = 0
        self.texture_clock = 0
        self.animation_state = 0
        self.texture_sets = []
        self.frame = 0

    def update_position(self, window_width, window_height):
        # Position the player in the middle of the window
        self.center_x = window_width / 2
        self.center_y = window_height / 2

    def update(self, delta_time):
        # Flip between textures to simulate animation
        self.texture_clock = self.texture_clock + delta_time

        # Ensure the animation state is valid
        # Use the current time to determine which texture to use
        # This is a simple way to animate the player by cycling through textures
        self.frame = int(self.texture_clock * 10) % len(
            self.texture_sets[self.animation_state]
        )
        self.texture = self.texture_sets[self.animation_state][self.frame]
