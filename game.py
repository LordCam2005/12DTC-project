import arcade

WIDTH = 1800
HEIGHT = 1000
MOVEMENT_SPEED = 7
JUMP_SPEED = 10
VEIWPOINT_MARGIN = 500

TITLE = "Blood Hunters"

RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_FRAMES = 8
PLAYER_FRAMES_PER_TEXTURE = 4

BULLET_SPEED = 12
STARTING_AMMO = 10
COOLANT_AMOUNT = 0

def load_texture_pair(filename):
    '''loads the animation for sprites'''
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class PlayerCharacter(arcade.Sprite):
    '''class for loading player sprite and its animation'''
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
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(f"assets\sprites\player\player{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]
        self.ammo = STARTING_AMMO
        self.current_coolant = COOLANT_AMOUNT

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

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.coolant_list = None
        self.wall_list = None
        self.player_bullet_list = None
        self.player = None
        self.physics_engine = None
        self.level = 1


    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.coolant_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.player = PlayerCharacter()
        self.load_map(f"./assets/maps/level_{self.level}.tmx")
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list, 2
        )

        self.player.center_x = 350
        self.player.center_y = 2000

        self.view_left = 0
        self.view_bottom = 0

    def load_map(self, resource):
        platforms_layer_name = "Tile Layer 1"
        coolant_layer_name = "coolant"


        my_map = arcade.tilemap.read_tmx(resource)

        self.wall_list = arcade.tilemap.process_layer(
            map_object=my_map,
            layer_name=platforms_layer_name,
            use_spatial_hash=True,
            scaling=1,
        )

        self.coolant_list = arcade.tilemap.process_layer(
            map_object = my_map,
            layer_name = coolant_layer_name,
            use_spatial_hash=True
            )



    def on_draw(self):
        arcade.start_render()

        self.wall_list.draw()

        self.player_bullet_list.draw()

        self.player.draw()
        arcade.draw_text(f"Ammo: {self.player.ammo}", self.view_left + 30, self.view_bottom + 30, arcade.color.RED)

        self.coolant_list.draw()
        arcade.draw_text(f"Coolant: {self.player.current_coolant}", self.view_left + 30, self.view_bottom + 15, arcade.color.RED)

    def update(self, delta_time):        
        self.player.update()
        self.player.update_animation()
        self.player_bullet_list.update()
        self.physics_engine.update()

        coolant_hit_list = arcade.check_for_collision_with_list(self.player, self.coolant_list)
        for coolant in coolant_hit_list:
            coolant.remove_from_sprite_lists()
            self.player.current_coolant += 1

        self.player_bullet_list.update()
        for bullet in self.player_bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.wall_list)
            for b in touching:
                bullet.kill()

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

        if self.view_left <= 0:
            self.view_left = 0

        if changed:
            arcade.set_viewport(self.view_left, WIDTH + self.view_left, self.view_bottom, HEIGHT + self.view_bottom)

        if self.player.center_y <=1000:
            self.player.center_y =2000
            self.player.center_x = 350
            self.player.ammo = STARTING_AMMO

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP and self.physics_engine.can_jump(y_distance=5):
            self.player.change_y = 3 * JUMP_SPEED

        
        if key == arcade.key.SPACE and self.player.ammo > 0:
            self.player.ammo -= 1
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

window = arcade.Window(width= WIDTH, height= HEIGHT, title= TITLE)
game = GameView()
game.setup()
window.show_view(game)
arcade.run()