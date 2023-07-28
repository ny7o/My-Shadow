import pygame


class World:
    def __init__(self):
        self.game_objects = []

    def add(self, game_object):
        self.game_objects.append(game_object)


class Camera:
    def __init__(self, screen, target_game_object):
        self.screen = screen
        self.target_game_object = target_game_object

    def update(self):
        target_pos = self.target_game_object.rectangel.move(
            -self.screen.get_width() // 2 + self.target_game_object.rectangel.width // 2,
            -self.screen.get_height() // 2 + self.target_game_object.rectangel.height // 2
        )
        
        for game_object in self.target_game_object.world.game_objects:
            self.screen.blit(
                game_object.surface,
                game_object.rectangel.move(-target_pos.x, -target_pos.y)
            )


class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size_x, size_y, world):
        super().__init__()
        self.world = world
        self.world.add(self)
        self.surface = pygame.Surface((size_x, size_y))
        self.rectangel = self.surface.get_rect()
        self.rectangel.x = pos_x
        self.rectangel.y = pos_y


class Entity(GameObject):
    def __init__(self, pos_x, pos_y, size_x, size_y, world):
        super().__init__(pos_x, pos_y, size_x, size_y, world)
        self.speed = 10


class Player(Entity):
    def __init__(self, pos_x, pos_y, size_x, size_y, world):
        super().__init__(pos_x, pos_y, size_x, size_y, world)
        self.vertical_speed = 0
        self.jump_strength = 20
        self.gravity = 1
        self.is_jumping = False

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        x_move, y_move = 0, 0

        if pressed_keys[pygame.K_LEFT]:
            x_move = -self.speed
        if pressed_keys[pygame.K_RIGHT]:
            x_move = self.speed

        if pressed_keys[pygame.K_SPACE] and not self.is_jumping:
            self.vertical_speed = -self.jump_strength
            self.is_jumping = True

        self.vertical_speed += self.gravity
        y_move = self.vertical_speed

        new_rect_x = self.rectangel.move(x_move, 0)
        new_rect_y = self.rectangel.move(0, y_move)

        for game_object in self.world.game_objects:
            if game_object is not self:
                if new_rect_x.colliderect(game_object.rectangel):
                    x_move = 0
                if new_rect_y.colliderect(game_object.rectangel):
                    if self.rectangel.top < game_object.rectangel.bottom and self.vertical_speed > 0:
                        self.vertical_speed = 0
                        self.is_jumping = False
                    y_move = 0

        self.rectangel.move_ip(x_move, y_move)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

    world = World()
    player = Player(0, 0, 50, 50, world)
    player.surface.fill((255, 0, 0))
    camera = Camera(screen, player)
    
    entity = Entity(-80, 80, 1000, 60, world)
    entity.surface.fill((0, 255, 0))
    new_entity = Entity(-60, 20, 60, 60, world)
    new_entity.surface.fill((0, 255, 0))
    new_entity_2 = Entity(-40, -100, 60, 60, world)
    new_entity_2.surface.fill((0, 255, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()
        screen.fill((0, 0, 0))
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_1]:
            camera.target_game_object = new_entity_2
        if pressed_keys[pygame.K_2]:
            camera.target_game_object = player
        
        camera.update()
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
