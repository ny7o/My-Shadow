import pygame


class World:
    def __init__(self, background_path):
        self.game_objects = []
        self.background_image = pygame.image.load(background_path)

    def add(self, game_object):
        self.game_objects.append(game_object)


class Camera:
    def __init__(self, screen, target_game_object):
        self.screen = screen
        self.target_game_object = target_game_object

    def update(self):
        self.screen.blit(self.target_game_object.world.background_image, (0, 0))

        target_pos = self.target_game_object.rectangle.move(
            -self.screen.get_width() // 2 + self.target_game_object.rectangle.width // 2,
            -self.screen.get_height() // 1.5 + self.target_game_object.rectangle.height // 1.5
        )

        for game_object in self.target_game_object.world.game_objects:
            self.screen.blit(
                game_object.surface,
                game_object.rectangle.move(-target_pos.x, -target_pos.y)
            )


class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size_x, size_y, world, allow_transparency=False):
        super().__init__()
        self.world = world
        self.world.add(self)
        self.allow_transparency = allow_transparency
        if self.allow_transparency:
            self.surface = pygame.Surface((size_x, size_y), pygame.SRCALPHA)
        else:
            self.surface = pygame.Surface((size_x, size_y))
        self.rectangle = self.surface.get_rect()
        self.rectangle.x = pos_x
        self.rectangle.y = pos_y
        self.has_collision = True


class Entity(GameObject):
    def __init__(self, pos_x, pos_y, size_x, size_y, world, allow_transparency=False):
        super().__init__(pos_x, pos_y, size_x, size_y, world, allow_transparency)
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

        if pressed_keys[pygame.K_a]:
            x_move = -self.speed
        if pressed_keys[pygame.K_d]:
            x_move = self.speed

        if pressed_keys[pygame.K_SPACE] and not self.is_jumping:
            self.vertical_speed = -self.jump_strength
            self.is_jumping = True

        self.vertical_speed += self.gravity
        y_move = self.vertical_speed

        new_rect_x = self.rectangle.move(x_move, 0)
        new_rect_y = self.rectangle.move(0, y_move)

        for game_object in self.world.game_objects:
            if game_object is not self:
                if new_rect_x.colliderect(game_object.rectangle) and game_object.has_collision:
                    x_move = 0
                if new_rect_y.colliderect(game_object.rectangle) and game_object.has_collision:
                    if self.rectangle.top < game_object.rectangle.bottom and self.vertical_speed > 0:
                        self.vertical_speed = 0
                        self.is_jumping = False
                    y_move = 0

        self.rectangle.move_ip(x_move, y_move)


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
    pygame.display.set_caption("My Shadow")

    world = World("res/BG.jpg")
    player = Player(100, -192, 60, 120, world)
    player.surface.blit(pygame.image.load("res/Ground.png"), (0, 0))
    camera = Camera(screen, player)

    entity = Entity(-80, 80, 6000, 350, world)
    entity.surface.blit(pygame.transform.scale(pygame.image.load("res/Ground.png"), (0, 0)), (384, 384))
    new_entity_2 = Entity(-40, -100, 60, 60, world, allow_transparency=True)
    new_entity_2.surface.fill((0, 0, 0, 0))
    new_entity_2.has_collision = False

    cam_switch = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()
        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            if cam_switch:
                cam_switch = False
                new_entity_2.rectangle = player.rectangle.__copy__()
                camera.target_game_object = new_entity_2
            else:
                cam_switch = True
                camera.target_game_object = player

        camera.update()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
