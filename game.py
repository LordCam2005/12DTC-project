import arcade

#constants
WIDTH = 1800
HEIGHT = 800
MOVEMENT_SPEED = 7
JUMP_SPEED = 10
Y_VEIWPOINT_MARGIN = 400
X_VEIWPOINT_MARGIN = 900

TITLE = "Blood Hunters"

RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_FRAMES = 8
PLAYER_FRAMES_PER_TEXTURE = 4

BULLET_SPEED = 12
STARTING_AMMO = 10
COOLANT_AMOUNT = 3
POWER_AMOUNT = 0

def load_texture_pair(filename):
    '''loads the animation for sprites'''
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class PlayerCharacter(arcade.Sprite):
    '''class for loading player sprite and its animation'''
    def __init__(self):
        '''starts all of the players functions'''
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
            texture = load_texture_pair(f"./assets/sprites/player/player{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]
        
        self.ammo = STARTING_AMMO
        self.current_coolant = COOLANT_AMOUNT
        self.current_power = POWER_AMOUNT

    def update_animation(self, delta_time:float = 1/60):
        '''updates the frame of player'''
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

class EliteChareter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        self.left_boundary = None
        self.right_boundary = None

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
        self.idle_texture_pair = load_texture_pair("./assets/sprites/elites/elite0.png")

        self.walk_textures = []
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(f"./assets/sprites/elites/elite{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]
        
    def update_animation(self, delta_time:float = 1/60):
        '''updates the frame of enemy'''
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

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Main Menu", WIDTH/2 - 100, HEIGHT/2, arcade.color.RED, font_size=50, anchor_x= "center")
        arcade.draw_text(f"Press Q to play {TITLE}", WIDTH/2 - 100, HEIGHT/2 - 50, arcade.color.RED, font_size=50, anchor_x= "center")
        arcade.draw_text("Press W to view controls", WIDTH/2 - 100, HEIGHT/2 - 100, arcade.color.RED, font_size=50, anchor_x= "center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        if key == arcade.key.W:
            control_view = ControlView()
            self.window.show_view(control_view)

class ControlView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Controls", WIDTH/2 - 100, HEIGHT - 75, arcade.color.RED, font_size=50, anchor_x= "center")
        arcade.draw_text("press ENTER to continue", WIDTH/2 - 100, 75, arcade.color.RED, font_size=50, anchor_x= "center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


class DeadView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = PlayerCharacter()
    
    def setup(self):
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.set_background_color(arcade.color.BLACK)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Game Over", WIDTH/2, HEIGHT/2 + 50, arcade.color.RED, font_size = 50, anchor_x = "center"
        )
        arcade.draw_text(
            "press space to try again", WIDTH/2, HEIGHT/2, arcade.color.RED, font_size = 50, anchor_x = "center"
        )
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = self.window.game
            game_view.setup()
            self.window.show_view(game_view)
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.coolant_list = None
        self.power_list = None
        self.wall_list = None
        self.player_bullet_list = None
        self.player = None
        self.physics_engine = None
        self.level = 1
        self.enemy_list= None
        self.ammo_list = None


    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.coolant_list = arcade.SpriteList()
        self.power_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.player = PlayerCharacter()
        self.ammo_list = arcade.SpriteList()
        self.load_map(f"./assets/maps/level_{self.level}.tmx")
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list, 2
        )
        self.enemy_list = arcade.SpriteList()


        self.player.center_x = 350
        self.player.center_y = 2000

        self.view_left = 0
        self.view_bottom = 0

        #elite enemy setup
        enemy = EliteChareter()
        enemy.center_x = 0
        enemy.center_y = 0
        enemy.left_boundary = 0
        enemy.right_boundary = 0
        self.enemy_list.append(enemy)
        if self.level == 1:
            enemy = EliteChareter()
            enemy.center_x = 2170
            enemy.center_y = 2100
            enemy.change_x = MOVEMENT_SPEED
            enemy.left_boundary = 2100
            enemy.right_boundary = 3690
            self.enemy_list.append(enemy)

            enemy = EliteChareter()
            enemy.center_x = 2506
            enemy.center_y = 2436
            enemy.change_x = MOVEMENT_SPEED
            enemy.left_boundary = 2506
            enemy.right_boundary = 3192
            self.enemy_list.append(enemy)

            enemy = EliteChareter()
            enemy.center_x = 4543
            enemy.center_y = 2532
            enemy.change_x = MOVEMENT_SPEED
            enemy.left_boundary = 4543
            enemy.right_boundary = 5159
            self.enemy_list.append(enemy)

            for i in range(5):
                enemy = EliteChareter()
                enemy.center_x = 6947 + i * 200
                enemy.center_y = 1764
                enemy.change_x = MOVEMENT_SPEED
                enemy.left_boundary = 6947
                enemy.right_boundary = 8459
                self.enemy_list.append(enemy)

    def load_map(self, resource):
        platforms_layer_name = "Tile Layer 1"
        coolant_layer_name = "coolant"
        power_layer_name = "power"


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

        self.power_list = arcade.tilemap.process_layer(
            map_object = my_map,
            layer_name = power_layer_name,
            use_spatial_hash=True
            )



    def on_draw(self):
        arcade.start_render()

        self.wall_list.draw()

        self.player_bullet_list.draw()

        self.player.draw()
        arcade.draw_text(f"Ammo: {self.player.ammo}", self.view_left + 30, self.view_bottom + 30, arcade.color.RED)

        self.coolant_list.draw()
        arcade.draw_text(f"Coolant: {self.player.current_coolant}", self.view_left + 30, self.view_bottom + 45, arcade.color.RED)

        self.power_list.draw()
        arcade.draw_text(f"Power: {self.player.current_power}", self.view_left + 30, self.view_bottom + 60, arcade.color.RED)
        self.enemy_list.draw()

        self.ammo_list.draw()



    def death(self):
        self.window.show_view(self.window.dead)
        self.window.dead.setup()

    def update(self, delta_time):
        self.player.update()
        self.player.update_animation()
        self.player_bullet_list.update()
        self.physics_engine.update()
        self.enemy_list.update()
        self.enemy_list.update_animation()

        for enemy in self.enemy_list:
            if enemy.center_x < enemy.left_boundary or enemy.center_x > enemy.right_boundary:
                enemy.change_x *= -1

        for bullet in self.player_bullet_list:
            enemy_hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            if len(enemy_hit_list) > 0:
                bullet.remove_from_sprite_lists()
                ammo = arcade.Sprite("./assets/sprites/item/ammo/ammo0.png")


            for enemy in enemy_hit_list:
                enemy.remove_from_sprite_lists()
                ammo.center_x =enemy.center_x
                ammo.center_y = enemy.center_y - 40
                self.ammo_list.append(ammo)

        ammo_hit_list = arcade.check_for_collision_with_list(self.player, self.ammo_list)
        for ammo in ammo_hit_list:
            ammo.remove_from_sprite_lists()
            self.player.ammo += STARTING_AMMO


        coolant_hit_list = arcade.check_for_collision_with_list(self.player, self.coolant_list)
        for coolant in coolant_hit_list:
            coolant.remove_from_sprite_lists()
            self.player.current_coolant += 1

        power_hit_list = arcade.check_for_collision_with_list(self.player, self.power_list)
        for power in power_hit_list:
            power.remove_from_sprite_lists()
            self.player.current_power += 1

        self.player_bullet_list.update()
        for bullet in self.player_bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.wall_list)
            for b in touching:
                bullet.kill()

        changed = False

        left_boundary = self.view_left + X_VEIWPOINT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        right_boundary = self.view_left + WIDTH - X_VEIWPOINT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + HEIGHT - Y_VEIWPOINT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + Y_VEIWPOINT_MARGIN
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
            if self.player.current_coolant >= 1:
                self.player.current_coolant -= 1
                self.player.center_y =2000
                self.player.center_x = 350
            elif self.player.current_coolant == 0:
                self.death()
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

class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str):
        super().__init__(width=width, height=height, title=title)
        menu_view = MenuView()

        self.dead = DeadView()
        self.show_view(menu_view)

if __name__ == "__main__":
    window = GameWindow(WIDTH, HEIGHT, TITLE)
    arcade.run()


