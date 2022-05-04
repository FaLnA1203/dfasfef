import pygame

pygame.init()
win = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("game")

walkRight = [pygame.image.load('right_1.png'),
pygame.image.load('right_2.png'), pygame.image.load('right_3.png'),
pygame.image.load('right_4.png')]

walkLeft = [pygame.image.load('left_1.png'),
pygame.image.load('left_2.png'), pygame.image.load('left_3.png'),
pygame.image.load('left_4.png')]

jumpLeft = [pygame.image.load('jumpleft_1.png'),
pygame.image.load('jumpleft_2.png'), pygame.image.load('jumpleft_3.png'),
pygame.image.load('jumpleft_4.png'), pygame.image.load('jumpleft_5.png'),
pygame.image.load('jumpleft_6.png')]

jumpRight = [pygame.image.load('jumpright_1.png'),
pygame.image.load('jumpright_2.png'), pygame.image.load('jumpright_3.png'),
pygame.image.load('jumpright_4.png'), pygame.image.load('jumpright_5.png'),
pygame.image.load('jumpright_6.png')]

platform_1 = pygame.image.load('platform.png')
menu = pygame.image.load('menu.png')
bg = pygame.image.load('bg.png')
playerStand_1 = pygame.image.load('idle_right.png')
playerStand_2 = pygame.image.load('idle_left.png')

def map_sprites(*surfaces):
    def yeilder():
        for surface in surfaces:
            sprite = pygame.sprite.Sprite()
            sprite.image = surface
            sprite.rect = surface.get_rect()
            yield sprite

    return list(yeilder())

def map_single_sprite(surface): return map_sprites(surface)[0]

walkRight_sprite = map_sprites(*walkRight)
walkLeft_sprite = map_sprites(*walkLeft)
jumpLeft_sprite = map_sprites(*jumpLeft)
jumpRight_sprite = map_sprites(*jumpRight)
platform_1_sprite = map_single_sprite(platform_1)
menu_sprite = map_single_sprite(menu)
bg_sprite = map_single_sprite(bg)
playerStand_1_sprite = map_single_sprite(playerStand_1)
playerStand_2_sprite = map_single_sprite(playerStand_2)

clock = pygame.time.Clock()

x = 500
y = 500
width = 60
height = 71
PLATFORM_WIDTH = 52
PLATFORM_HEIGHT = 45
PLATFORM_COLOR = "#FF6262"
speed = 5
jump = False
jumpcount = 10

left = False
right = False
idle_1 = True
idle_2 = False
run_1 = True
run_2 = False
animcount = 0
bullets = []
entities = pygame.sprite.Group()
platforms = []
level = [
       "-------------------------",
       "-                       -",
       "-                       -",
       "-                       -",
       "-            --         -",
       "-                       -",
       "--                      -",
       "-                       -",
       "-                   --- -",
       "-                       -",
       "-                       -",
       "-      ---              -",
       "-                       -",
       "-   -----------        --",
       "-                       -",
       "-------------------------"]

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class silk(pygame.sprite.Sprite):
    def __init__(self, x, y, width_1, height_1, color, facing):
        self.x = x
        self.y = y
        self.width_1 = width_1
        self.height_1 = height_1
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width_1, self.height_1))



def drawwin():
    global animcount
    if run_1:
        win.blit(menu, (0, 0))
    if run_2:
        win.blit(bg, (0, 0))
        win.blit(pf,(x,y))
        entities.draw(win)
        if animcount + 1 >= 30:
            animcount = 0
        if idle_2 and jump:
            win.blit(jumpLeft[animcount // 5], (x, y))
            entities.add(jumpLeft_sprite)
            animcount += 1
        elif idle_1 and jump:
            win.blit(jumpRight[animcount // 5], (x, y))
            entities.add(jumpRight_sprite)
            animcount += 1
        elif left:
            win.blit(walkLeft[animcount // 8], (x, y))
            entities.add(walkLeft_sprite)
            animcount += 1
        elif right:
            win.blit(walkRight[animcount // 8], (x, y))
            entities.add(walkRight_sprite)
            animcount += 1
        else:
            if idle_2:
                win.blit(playerStand_2, (x, y))
                entities.add(playerStand_2_sprite)
            elif idle_1:
                win.blit(playerStand_1, (x, y))
                entities.add(playerStand_1_sprite)
            else:
                win.blit(playerStand_1, (x, y))
                entities.add(playerStand_1_sprite)
        x_1=y_1=0
        for row in level:
            for col in row:
                if col == "-":
                    pf = Platform(x,y)
                    entities.add(pf)
                    platforms.append(pf)
                x_1 += PLATFORM_WIDTH
            y_1 += PLATFORM_HEIGHT
            x_1 = 0
        for bullet in bullets:
            bullet.draw(win)

    pygame.display.update()

while run_1:
    for game in pygame.event.get():
        if game.type == pygame.QUIT:
            run_1 = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        run_1 = False
        run_2 = True

    drawwin()

while run_2:
    clock.tick(30)

    for game in pygame.event.get():
        if game.type == pygame.QUIT:
            run_2 = False

    for bullet in bullets:
        if bullet.x < 1280 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        if idle_1:
            facing = 1
        else:
            facing = -1

        if len(bullets) < 10:
            bullets.append(silk(round(x + width // 2), round(y + height // 2), 40, 2, (255, 255, 255), facing))

    # откуда что и где
    """
    for p in platforms:
        if sprite.collide_rect(self, p):

            if xvel > 0:
                self.rect.right = p.rect.left

            if xvel < 0:
                self.rect.left = p.rect.right

            if yvel > 0:
                self.rect.bottom = p.rect.top
                self.onGround = True

            if yvel < 0:
                self.rect.top = p.rect.bottom
                self.yvel = 0
    """

    if keys[pygame.K_a] and x > 5:
        x -= speed
        left = True
        right = False
        idle_2 = True
        idle_1 = False
    elif keys[pygame.K_d] and x < 720 - width - 5:
        x += speed
        left = False
        right = True
        idle_2 = False
        idle_1 = True
    else:
        left = False
        right = False
        animcount = 0
    if not(jump):
        if keys[pygame.K_SPACE]:
            jump = True
    else:
        if jumpcount >= -10:
            if jumpcount < 0:
                y += (jumpcount ** 2) / 2
            else:
                y -= (jumpcount ** 2) / 2
            jumpcount -= 1
        else:
            jump = False
            jumpcount = 10

    drawwin()
