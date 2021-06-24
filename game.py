import arcade

WIDTH = 1800
HEIGHT = 1000
MOVEMENT_SPEED = 10
VEIWPOINT_MARGIN = 500

TITLE = "Blood Hunters"
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
            "./assets/sprites/player.png"
        )
        #self.load_map(f"./maps/level{self.level}.tmx")
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
        #self.dont_touch_list.draw()
        #self.foreground_list.draw()
        self.player.draw()

    def update(self, delta_time):
        self.player.update()
        self.physics_engine.update()

        changed = False

        left_boundary = self.view_left + VEIWPOINT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        right_boundary = self.view_left + WIDTH - VEIWPOINT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + HEIGHT - VEIWPOINT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + VEIWPOINT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        if changed:
            arcade.set_viewport(self.view_left, WIDTH + self.view_left, self.view_bottom, HEIGHT + self.view_bottom)

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
