import arcade
import random
from sprites.animated_sprite import AnimatedSprite, load_100x100_textures

ANIMATION_STATE_IDLE_RIGHT = 0
ANIMATION_STATE_WALK_RIGHT = 1
ANIMATION_STATE_ATTACK_1_RIGHT = 2
ANIMATION_STATE_ATTACK_2_RIGHT = 3

ANIMATION_STATE_IDLE_LEFT = 5
ANIMATION_STATE_WALK_LEFT = 6
ANIMATION_STATE_ATTACK_1_LEFT = 7
ANIMATION_STATE_ATTACK_2_LEFT = 8


class OrcSprite(AnimatedSprite):
    _sprite_file = "assets/Characters(100x100)/Orc/Orc.png"

    def __init__(self):
        super().__init__()
        self.is_facing_right = True
        self.attack_animation = 0
        self.texture_clock = random.uniform(0, 1)

        sprite_sheet = arcade.SpriteSheet(self._sprite_file)

        # - Face Right
        # Idle, Walk, attack 1, attack 2
        sprite_count = [6, 8, 6, 6]
        for i in range(len(sprite_count)):
            self.texture_sets.append(
                load_100x100_textures(sprite_sheet, row=i, count=sprite_count[i])
            )

        # - Face Left
        sprite_sheet.flip_left_right()
        for i in range(len(sprite_count)):
            self.texture_sets.append(
                load_100x100_textures(
                    sprite_sheet, row=i, count=sprite_count[i], from_right=True
                )
            )

        self.animation_state = ANIMATION_STATE_IDLE_RIGHT

    def attack_1(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 1
        self.texture_clock = 0
        if self.is_facing_right:
            self.animation_state = ANIMATION_STATE_ATTACK_1_RIGHT
        else:
            self.animation_state = ANIMATION_STATE_ATTACK_1_LEFT

    def attack_2(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 2
        self.texture_clock = 0
        if self.is_facing_right:
            self.animation_state = ANIMATION_STATE_ATTACK_2_RIGHT
        else:
            self.animation_state = ANIMATION_STATE_ATTACK_2_LEFT

    def update(self, delta_time):
        super().update(delta_time)

        if self.attack_animation > 0:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.attack_animation = 0

        elif self.change_x < 0:
            self.is_facing_right = False
            self.animation_state = ANIMATION_STATE_WALK_LEFT

        elif self.change_x > 0:
            self.is_facing_right = True
            self.animation_state = ANIMATION_STATE_WALK_RIGHT

        elif self.change_y != 0:
            if self.is_facing_right:
                self.animation_state = ANIMATION_STATE_WALK_RIGHT
            else:
                self.animation_state = ANIMATION_STATE_WALK_LEFT
        else:
            if self.is_facing_right:
                self.animation_state = ANIMATION_STATE_IDLE_RIGHT
            else:
                self.animation_state = ANIMATION_STATE_IDLE_LEFT
