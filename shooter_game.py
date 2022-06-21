from pygame import *
from random import *
up = 600
wid = 1000
window = display.set_mode((wid, up))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (wid, up))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.05)
mixer.music.play()
kick = mixer.Sound('fire.ogg')
kick.set_volume(0.1)
class GameSprite(sprite.Sprite):
    def __init__(self, x, y, file_name, speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(file_name), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < wid - 100:
            self.rect.x += self.speed
    def update(self):
        global lost
        if self.rect.y > up:
            self.rect.y = 0
            self.rect.x = randint(50, wid - 100)
            lost += 1
            if lost != 0 and lost%5 == 0:
                ast = Ast(randint(50, wid - 100), 0, 'asteroid.png', randint(1, 3), 75, 75)
                asteroid.add(ast)
        self.rect.y += self.speed
    def fire(self):
        bullet1 = Bullet(self.rect.centerx, self.rect.top, 'bullet.png', 6, 16, 32)
        bullet.add(bullet1)
class Bullet(GameSprite):
    def update(self):
        if self.rect.y <= 0:
            self.kill()
        self.rect.y -= self.speed
class Ast(GameSprite):
    def update(self):
        if self.rect.y > up:
            self.kill()
        self.rect.y += self.speed
bullet = sprite.Group()
rocket = Player(int(wid/2), up - 120, 'rocket.png', 7, 80, 100)
enemy1 = Player(randint(50, wid - 100), 0, 'ufo.png', randint(1, 3), 120, 75)
enemy2 = Player(randint(50, wid - 100), 0, 'ufo.png', randint(1, 3), 120, 75)
enemy3 = Player(randint(50, wid - 100), 0, 'ufo.png', randint(1, 3), 120, 75)
enemy4 = Player(randint(50, wid - 100), 0, 'ufo.png', randint(1, 3), 120, 75)
enemy5 = Player(randint(50, wid - 100), 0, 'ufo.png', randint(1, 3), 120, 75)
asteroid = sprite.Group()
ufo = sprite.Group()
ufo.add(enemy1)
ufo.add(enemy2)
ufo.add(enemy3)
ufo.add(enemy4)
ufo.add(enemy5)
font.init()
score = 0
lost = 0
n1 = font.SysFont('Verdana', 45).render('Счет:', True, (255, 255, 255))
n2 = font.SysFont('Verdana', 45).render('Пропущено:', True, (255, 255, 255))
clock = time.Clock()
game = True
finish = False 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        # if e.type == KEYDOWN:
        #     if e.key == K_SPACE:
        #         rocket.fire()
        #         kick.play()
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                rocket.fire()
                kick.play()    
    window.blit(background, (0, 0))
    rocket.draw()
    ufo.draw(window)
    bullet.draw(window)
    asteroid.draw(window)
    n3 = font.SysFont('Verdana', 45).render(str(score), True, (255, 255, 255))
    n4 = font.SysFont('Verdana', 45).render(str(lost), True, (255, 255, 255))
    window.blit(n1, (2, 10))
    window.blit(n2, (2, 55))
    window.blit(n3, (145, 10))
    window.blit(n4, (300, 55))
    if finish == False:
        # if sprite.collide_rect(rocket):
        #     kick.play()
        #     finish = True
        # if sprite.collide_rect(rocket):
        #     money.play()
        #     finish = True
        #     win = font.SysFont('Verdana', 100).render('YOU WIN!!!', True, (6, 246, 167))
        rocket.move()
        ufo.update()
        bullet.update()
        asteroid.update()
        if sprite.groupcollide(ufo, bullet, True, True):
            enemy4 = Player(randint(50, wid - 100), 0, 'ufo.png', randint(1, 3), 120, 75)
            ufo.add(enemy4)
            score += 1
        if sprite.spritecollide(rocket, ufo, False) or lost > 25 or sprite.spritecollide(rocket, asteroid, False):
           finish = True    
           win = font.SysFont('Verdana', 100).render('YOU LOSE!!!', True, (255, 0, 0))
        if score > 50:
           finish = True
           win = font.SysFont('Verdana', 100).render('YOU WIN!!!', True, (6, 246, 167))
    else:
        window.blit(win, (int(wid/2-150), int(up/2-100)))
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            finish = False
            score = 0
            lost= 0
            rocket = Player(int(wid/2), up - 120, 'rocket.png', 7, 80, 100)
            ufo = sprite.Group()
            bullet = sprite.Group()
            asteroid = sprite.Group()
            for i in range(5):
                enemy4 = Player(randint(50, wid - 100), 0, 'ufo.png', randint(1, 3), 120, 75)
                ufo.add(enemy4)
    display.update()
    clock.tick(120)