import os

import arcade

WIDTH = 800
HEIGHT = 600
MOVEMENT_SPEED = 5

TITLE = "tmx tings"

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.coin_list = None
        self.wall_list = None
        self.player = None
        self.physics_engine = None
        self.level = 1

    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player = arcade.Sprite(
            "\\DataServer2\CCampbell$\dev\game project\game\player.png"
        )
        self.load_map(f"./maps/level{self.level}.tmx")
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list, 1
        )

        self.player.center_x = 100
        self.player.center_y = 125

        self.view_left = 0
        self.view_bottom = 0

    def load_map(self, resource):
        platforms_layer_name = "Platforms"
        coins_layer_name = "Coins"
        foreground_layer_name = "Detail"
        dont_touch_layer_name = "Death"

        my_map = arcade.tilemap.read_tmx(resource)

        self.wall_list = arcade.tilemap.process_layer(
            map_object=my_map,
            layer_name=platforms_layer_name,
            use_spatial_hash=True,
            scaling=0.5,
        )

        self.coin_list = arcade.tilemap.process_layer(
            map_object=my_map, layer_name=coins_layer_name, scaling=0.5
        )

        self.foreground_list = arcade.tilemap.process_layer(
            map_object=my_map, layer_name=foreground_layer_name, scaling=0.5
        )

        self.dont_touch_list = arcade.tilemap.process_layer(
            map_object=my_map, layer_name=dont_touch_layer_name, scaling=0.5
        )

    def on_draw(self):
        arcade.start_render()
        self.coin_list.draw()
        self.wall_list.draw()
        self.dont_touch_list.draw()
        self.foreground_list.draw()
        self.player.draw()

    def update(self, delta_time):
        self.player.update()
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP:
            self.player.change_y = 3 * MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        if key == arcade.key.UP:
            self.player.change_y = 0


game = Game()
game.setup()
arcade.run()
