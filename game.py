import arcade

WIDTH = 1800
HEIGHT = 1000
MOVEMENT_SPEED = 10
VEIWPOINT_MARGIN = 500

TITLE = "Blood Hunters"

RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_FRAMES = 8
PLAYER_FRAMES_PER_TEXTURE = 4

BULLET_SPEED = 20

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        # 0 - PLAYER_FRAMES
        self.virtual_frame = 0
        # 0 - 59
        
        self.gun_offset = {
            0: (90, -30),
            1: (95, -20),
            2: (90, -15),
            3: (95, -20),
            4: (90, -30),
            5: (95, -20),
            6: (90, -15),
            7: (95, -20)
        }
        self.idle = False
        
        self.idle_texture_pair = load_texture_pair("./assets/sprites/player/player0.png")

        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"assets\sprites\player\player{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time:float = 1/60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.idle = True
            return

        self.idle = False
        self.virtual_frame += 1
        if self.virtual_frame > PLAYER_FRAMES*PLAYER_FRAMES_PER_TEXTURE -1:
            self.virtual_frame = 0
            self.cur_texture = 0
        if (self.virtual_frame + 1) % PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_frame // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.coin_list = None
        self.wall_list = None
        self.player_bullet_list = None
        self.player = None
        self.physics_engine = None
        self.level = 1


    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.player = PlayerCharacter()
        self.load_map(f"./assets/maps/level_{self.level}.tmx")
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list, 2
        )

        self.player.center_x = 250
        self.player.center_y = 725

        self.view_left = 0
        self.view_bottom = 0

    def load_map(self, resource):
        platforms_layer_name = "Tile Layer 1"


        my_map = arcade.tilemap.read_tmx(resource)

        self.wall_list = arcade.tilemap.process_layer(
            map_object=my_map,
            layer_name=platforms_layer_name,
            use_spatial_hash=True,
            scaling=3,
        )



    def on_draw(self):
        arcade.start_render()

        self.wall_list.draw()
        self.player_bullet_list.draw()

        self.player.draw()

    def update(self, delta_time):
        self.player.update()
        self.player.update_animation()
        self.player_bullet_list.update()
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
        
        if key == arcade.key.SPACE:
            bullet = arcade.Sprite("./assets/sprites/ammo/player_bullet.png")
            current_texture = self.player.cur_texture
            if self.player.idle:
                current_texture = 0
            offset_x = self.player.gun_offset[current_texture][0]
            if self.player.character_face_direction == LEFT_FACING:
                offset_x *= -1
            bullet.center_x = self.player.center_x + offset_x
            bullet.center_y = self.player.center_y + self.player.gun_offset[current_texture][1]
            
            if self.player.character_face_direction == RIGHT_FACING:
                bullet.change_x = BULLET_SPEED
            else:
                bullet.change_x = -BULLET_SPEED
            
            self.player_bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        if key == arcade.key.UP:
            self.player.change_y = 0


game = Game()
game.setup()
arcade.run()