import pygame
import os
import math
import sys

#from pygame.sprite import _Group

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1016
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join('assets','map.png'))
WALLS = pygame.image.load(os.path.join('assets','walls.png'))

font = pygame.font.SysFont("Arial", 30)


class Car(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        self.original_image = pygame.image.load(os.path.join('assets','car.png'))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(364,929))
        self.start_pos = (364,929)
        self.drive_state = False
        self.vel_vector = pygame.math.Vector2(1,0)
        self.rotation_vel = 5
        self.direction = 0
        self.speed = 5
        self.angle = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.drive()
        self.reverse()
        self.rotate()

    def drive(self):
        if self.drive_state == 'f':
            self.rect.center -= self.vel_vector * self.speed

    def reverse(self):
        if self.drive_state == 'r':
            self.rect.center += self.vel_vector * self.speed
    

    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)

        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.original_image,self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)  # Update mask after rotation
        
    def reset(self):
        self.rect.center = self.start_pos
        self.angle = 0
        self.vel_vector = pygame.math.Vector2(1, 0)  # Reset to initial direction
        self.direction = 0
        self.drive_state = False
        self.image = pygame.transform.rotozoom(self.original_image, 0, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def boost(self):
        #for the lolz
        self.speed = 20
    
    def normal_speed(self):
        self.speed = 5

car = pygame.sprite.GroupSingle(Car())

def eval_genomes():
    lap_start_time = pygame.time.get_ticks()
    last_lap_time = 0  # Store the last lap time
    last_checkpoint_crossed = False  # Track if the checkpoint has been crossed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        SCREEN.blit(TRACK, (0,0))
        SCREEN.blit(WALLS, (0, 0))
        
        user_input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            car.sprite.drive_state = False
            car.sprite.direction = 0

        # drive
        if user_input[pygame.K_UP]:
            car.sprite.drive_state = 'f'

        # reverse
        if user_input[pygame.K_DOWN]:
            car.sprite.drive_state = 'r'

        # steer
        if user_input[pygame.K_RIGHT]:
            car.sprite.direction = 1
        if user_input[pygame.K_LEFT]:
            car.sprite.direction = -1
        
        if user_input[pygame.K_SPACE]:
            car.sprite.boost()
        
        if not user_input[pygame.K_SPACE]:
            car.sprite.normal_speed()

        # Check for collisions using masks
        car_mask = car.sprite.mask
        walls_mask = pygame.mask.from_surface(WALLS)
        offset = (int(car.sprite.rect.left), int(car.sprite.rect.top))
        collision_point = walls_mask.overlap(car_mask, offset)
        if collision_point:
            print("Car crashed!")
            car.sprite.drive_state = False
            car.sprite.direction = 0
            car.sprite.angle = 0
            car.sprite.reset()

        if 330 <= car.sprite.rect.centerx <= 370 and 900 <= car.sprite.rect.centery <= 950:
            if not last_checkpoint_crossed:
                current_time = pygame.time.get_ticks()
                last_lap_time = (current_time - lap_start_time) / 1000  # Lap time in seconds
                lap_start_time = current_time  # Reset lap start time
                last_checkpoint_crossed = True  # Set checkpoint crossed to True
        else:
            last_checkpoint_crossed = False  # Reset checkpoint crossing flag

        # Display lap time
        if last_lap_time is not None:
            lap_time_text = font.render(f"Lap Time: {last_lap_time:.2f} s", True, (255, 255, 255))
            SCREEN.blit(lap_time_text, (50, 50))

        car.draw(SCREEN)
        car.update()
        pygame.display.update()
        clock.tick(60)

eval_genomes()