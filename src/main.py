import arcade
from arcade import PhysicsEngineSimple

from sprites.animated_sprite import load_100x100_textures
from constants import CAMERA_BOUNDARY, CAMERA_SPEED, DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH, SPRITE_SCALE
from sprites.player import PlayerSprite
from sprites.orc import OrcSprite


class AdventureGameWindow(arcade.Window):
    """
    Main game window for the Rogue-Like adventure game.
    Handles rendering, input, and game logic.
    """

    def __init__(self, width, height, title):
        """
        Initialize the game window.

        Args:
            width (int): Width of the window.
            height (int): Height of the window.
            title (str): Title of the window.
        """

        # Set up the window
        super().__init__(width, height, title, resizable=True)
        arcade.set_background_color(arcade.color.SLATE_GRAY)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set up the player sprite
        self.player_list = arcade.SpriteList()
        self.player_sprite = PlayerSprite()
        self.player_sprite.position = (100, 950)
        self.player_list.append(self.player_sprite)
        self.player_speed = 5  # Speed of the player

        # Set up the characters
        self.character_list = arcade.SpriteList()
        orc_sprite = OrcSprite()
        orc_sprite.position = (160, 950)
        self.character_list.append(orc_sprite)

        self.tile_map = arcade.load_tilemap(
            "tiled/adventure.tmj",
            scaling=SPRITE_SCALE,
            layer_options={
                "Floor": {"use_spatial_hash": True},
                "Walls": {"use_spatial_hash": True},
            },
        )
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Physics engine
        self.physics_engine = PhysicsEngineSimple(player_sprite=self.player_sprite, walls=self.scene["Walls"])

        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

    def on_draw(self):
        """
        Render the game scene, including the player, characters, and tilemap.
        """
        self.clear()

         # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()
        self.scene.draw(pixelated=True)
        self.character_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

    def update_player_speed(self):
        """
        Update the player's speed based on the keys pressed.
        """
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = self.player_speed
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -self.player_speed
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -self.player_speed
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = self.player_speed

    def on_key_press(self, key, modifiers):
        """
        Handle key press events to move the player.

        Args:
            key (int): The key that was pressed.
            modifiers (int): Modifier keys pressed (e.g., Shift, Ctrl).
        """
        if key == arcade.key.W:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.A:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """
        Handle key release events to stop the player's movement.

        Args:
            key (int): The key that was released.
            modifiers (int): Modifier keys pressed (e.g., Shift, Ctrl).
        """
        if key == arcade.key.W:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()

    def on_update(self, delta_time):
        """
        Update the game state, including player and character positions.

        Args:
            delta_time (float): Time since the last update.
        """
        self.player_sprite.update(delta_time)
        self.character_list.update(delta_time)
        self.physics_engine.update()

        # Scroll the screen to the player
        self.scroll_to_player()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handle mouse press events to trigger player attacks.

        Args:
            x (float): X-coordinate of the mouse click.
            y (float): Y-coordinate of the mouse click.
            button (int): Mouse button pressed.
            modifiers (int): Modifier keys pressed (e.g., Shift, Ctrl).
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.attack_1()
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.attack_2()
        elif button == arcade.MOUSE_BUTTON_MIDDLE:
            self.player_sprite.attack_3()

    def scroll_to_player(self):
        """
        Scroll the camera to keep the player in view.
        """
        """
        Scroll the window to the player.
        This method will attempt to keep the player at least VIEWPORT_MARGIN
        pixels away from the edge.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        # --- Manage Scrolling ---
        new_position = arcade.camera.grips.constrain_boundary_xy(
            self.camera_sprites.view_data, CAMERA_BOUNDARY, self.player_sprite.position
        )

        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position, (new_position[0], new_position[1]), CAMERA_SPEED
        )


    def on_resize(self, width: int, height: int):
        """
        Handle window resize events.

        Args:
            width (int): New width of the window.
            height (int): New height of the window.
        """

        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window(position=True)

def main():
    """
    Entry point for the game. Initializes and runs the game window.
    """
    window = AdventureGameWindow(
        DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, "Adventure Game"
    )
    arcade.run()


if __name__ == "__main__":
    main()
