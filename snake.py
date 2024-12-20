from random import randint
import pygame
from settings import *
from audio_util import *


# https://www.beepbox.co/#9n62s6k0l00e05t3ea7g0Fj1zr1i0o432333T0v0u10f0qg01d04w2h0E0T0v0u10f0qg01d04w2h0E0T1v0u17f0q00d03A1F0B0Q200ePb793E3617628637T0v0u13f10o5q00d03w5h1E0T1v1ue7f10p7q0331d08A0F5B3Q0140Pea77E361b627638T1v1u40f0qww10r51d08A4F2B6Q0068Pf624E2b676T2v0u15f10w4qw02d03w0E0T4v1uf0f0q00z6666ji8k8k3jSBKSJJAArriiiiii07JCABrzrrrrrrr00YrkqHrsrrrrjr005zrAqzrjzrrqr1jRjrqGGrrzsrsA099ijrABJJJIAzrrtirqrqjqixzsrAjrqjiqaqqysttAJqjikikrizrHtBJJAzArzrIsRCITKSS099ijrAJS____Qg99habbCAYrDzh00E0b0ww8c240000000000000000000000000000000000000000000ww88200000000000000000000000000000000000000000000ww88200000000000000000000000000000000000000000000wgg443000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ww88220000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000p24PFH-zd7wwAtcAtl4tcAqrzZ2CLWkOddu0YECR-XWsHiGjhZ4th7khFKfp0000000000000000FKfN2CO_7F0yIQvl2ISLPddN_hdHUms0000000000000000iZCRYeGAGXbVuPnYEBZcBZcBZcw0000000000000005dWfOFJvi9H-p62jsvRjuzI00000000000000000000000000000000000000000000000001jhByddutAAujAAujAAujjai5E5OtAzOsAzOsAzOg000000000000000000000000000000000

# total fade: 40

# snakes body:
    # # # 
    #

# snakes body len: 4

# one_fade_index = total_fade / sum(range(1, 11))

# sum(range(1, 4 + 1)) = 1 + 2 + 3 + 4 = 10

# one_fade_index = 40 / 10 = 4

# next one_fade_index = (4 * 4) / 5

# next one_fade_index = 3.2

# 4 * 4 = 3.2 * 5




default_keybinds = {
    'Up': pygame.K_w,
    'Down': pygame.K_s,
    'Left': pygame.K_a,
    'Right': pygame.K_d
}

class Snake:
    
    def __init__(self, game, pos, color, direction, keybinds=None, fade=None):
        # important setup
        self.screen = game.screen
        self.snakes = game.snakes

        # color
        self.color = color
        self.transparency = None

        # powerup
        self.rainbow_pallete = None
        self.powerup_rainbow = False
        self.powerup_score_entity = None

        # keybinds
        if keybinds is None:
            self.keybinds = default_keybinds
        else:
            self.keybinds = keybinds

        # movement
        self.rect = pygame.rect.Rect(
            pos[0], pos[1], TILE_SIZE, TILE_SIZE
        )
        self.direction = pygame.math.Vector2(direction[0], direction[1])
        self.last_move = pygame.time.get_ticks()
        self.speed = SNAKE_SPEED

        # body
        self.body = []
        self.bodyparts = 4

        # fade
        self.fade = False
        if fade is not None:
            self.fade = True
            self.one_fade_index = fade / sum(range(1, self.bodyparts + 1))
        self.surf = pygame.Surface((TILE_SIZE - 1, TILE_SIZE - 1))
        self.surf.fill(self.color)

    def die(self):
        pass

    def check_collision(self):
        # collision with snakes:
        for snake in self.snakes:
            if self.rect.topleft in snake.body:
                self.snakes.remove(self)
                play_sound_effect('audio/snakeDie.wav')
            elif snake is not self and self.rect.topleft == snake.rect.topleft:
                self.snakes.remove(self)
                self.snakes.remove(snake)
                play_sound_effect('audio/snakeDie.wav')
        
        # collision with walls:
        if ((self.rect.x < 0 or self.rect.x >= SCREEN_WIDTH) or
            (self.rect.y < 0 or self.rect.y >= SCREEN_HEIGHT)):
            self.snakes.remove(self)
            play_sound_effect('audio/snakeDie.wav')

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[self.keybinds['Up']] and self.direction.xy != (0, TILE_SIZE):
            self.direction.xy = (0, -TILE_SIZE)

        elif keys[self.keybinds['Down']] and self.direction.xy != (0, -TILE_SIZE):
            self.direction.xy = (0, TILE_SIZE)

        elif keys[self.keybinds['Left']] and self.direction.xy != (TILE_SIZE, 0):
            self.direction.xy = (-TILE_SIZE, 0)

        elif keys[self.keybinds['Right']] and self.direction.xy != (-TILE_SIZE, 0):
            self.direction.xy = (TILE_SIZE, 0)

    def move(self):
        if pygame.time.get_ticks() - self.last_move >= self.speed:
            self.body.append(self.rect.topleft)
            if len(self.body) == self.bodyparts + 1:
                self.body.pop(0)
            self.rect.topleft += self.direction.xy
            self.last_move = pygame.time.get_ticks()
    
    def draw(self):
        # draw head
        self.surf.set_alpha(self.transparency)
        if self.powerup_rainbow:
            self.surf.fill(self.rainbow_pallete[0])
        else:
            self.surf.fill(self.color)
        self.screen.blit(self.surf, (self.rect.x + .5, self.rect.y + .5))


        # draw body when fade:
        if self.fade:
            for i, b in enumerate(reversed(self.body)):
                surf = pygame.Surface((
                    TILE_SIZE - (i + 1) * (self.one_fade_index * 2), 
                    TILE_SIZE - (i + 1) * (self.one_fade_index * 2)
                ))
                if self.powerup_rainbow:
                    surf.fill(self.rainbow_pallete[i + 1])
                else:
                    surf.fill(self.color)
                surf.set_alpha(self.transparency)
                self.screen.blit(
                    surf,
                    (b[0] + (i + 1) * self.one_fade_index,
                    b[1] + (i + 1) * self.one_fade_index)
                )
                
        # draw body when not fade
        else:
            for bx, by in self.body:
                self.screen.blit(self.surf, (bx + .5, by + .5))

    def update(self):
        self.get_input()
        self.move()
        self.check_collision()
        self.draw()

