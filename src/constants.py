import arcade

DEFAULT_WINDOW_WIDTH = 1600
DEFAULT_WINDOW_HEIGHT = 1200

SPRITE_SCALE = 4

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 400

HORIZONTAL_BOUNDARY = DEFAULT_WINDOW_WIDTH / 2.0 - VIEWPORT_MARGIN
VERTICAL_BOUNDARY = DEFAULT_WINDOW_HEIGHT / 2.0 - VIEWPORT_MARGIN

# If the player moves further than this boundary away from the camera we use a
# constraint to move the camera
CAMERA_BOUNDARY = arcade.LRBT(
    -HORIZONTAL_BOUNDARY,
      HORIZONTAL_BOUNDARY,
      -VERTICAL_BOUNDARY,
      VERTICAL_BOUNDARY,
)