import pygame
import random

# Making The Enemy's Brain
class Enemy():
    # Enemy Constructer Function
    def __init__(self, x, y, speed, size):
        # Make The Enemy's Variables
        self.x = x
        self.y = y
        self.pic = pygame.image.load("assets/Fish04_A.png")
        self.pic2 = pygame.image.load("assets/Fish04_B.png")
        self.speed = speed
        self.size = size
        self.hitbox = pygame.Rect(self.x, self.y, int(self.size*1.25), self.size)
        self.animationTimerMax = 14
        self.animationTimer = self.animationTimerMax
        self.animationFrame = 0

        # Shrink The Enemy Pic
        self.pic = pygame.transform.scale(self.pic, (int(self.size*1.250), self.size))
        self.pic2 = pygame.transform.scale(self.pic2, (int(self.size*1.250), self.size))

        # Flip the pic if the enemy is moving left
        if self.speed < 0:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.pic2 = pygame.transform.flip(self.pic2, True, False)

    # Enemy update function
    def update(self, screen):
        self.animationTimer -= 1
        if self.animationTimer <= 0:
            self.animationTimer = self.animationTimerMax
            self.animationFrame += 1
            if self.animationFrame > 1:
                self.animationFrame = 0
        self.x += self.speed
        self.hitbox.x += self.speed
        # pygame.draw.rect(screen, (0,0,0), self.hitbox)
        if self.animationFrame == 0:
            screen.blit(self.pic, (self.x, self.y))
        else:
            screen.blit(self.pic2, (self.x, self.y))
    
# End of Enemy class

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

# Load all the images for the game
backgroundImg = pygame.image.load("assets/Scene_A.png")
backgroundImg2 = pygame.image.load("assets/Scene_B.png")
playerPic = pygame.image.load("assets/sid.png")
playerEatingPic = pygame.image.load("assets/sid3open.png")
playerPic2 = pygame.image.load("assets/sid2.png")

# Make some variables for the background animation
bgAnimationTimerMax = 25
bgAnimationTimer = bgAnimationTimerMax
bgAnimationFrame = 0

# Direction of the fish
playerFacingLeft = False

# Speed of the player
playerSpeed = 8

# Size of the player
playerStartingSize = 30
playerSize = playerStartingSize

# Make some variables for the position of our player
playerStartingX = 480
playerStartingY = 310
player_x = playerStartingX
player_y = playerStartingY

# Make some variables for the player animation
playerEatingTimerMax = 9
playerEatingTimer= 0
playerSwimmingTimerMax = 14
playerSwimmingTimer = playerSwimmingTimerMax
playerSwimmingFrame = 0

# Player hitbox
playerHitbox = pygame.Rect(player_x, player_y, int(playerSize*1.25), playerSize)
playerAlive = False

# Make some variables for the HUD (heads-up display)
score = -1
scoreFont = pygame.font.SysFont("myriadhebrewopentype", 30)
scoreText = scoreFont.render("Score: "+str(score), 1, (255, 255, 255))
playButtonPic = pygame.image.load("assets/BtnPlayIcon.png")
playButtonX = game_width/2 - playButtonPic.get_width()/2
playButtonY = game_height/2 - playButtonPic.get_height()/2 + 40
titlePic = pygame.image.load("assets/title.png")
titleX = game_width/2 - titlePic.get_width()/2
titleY = playButtonY - 150
 
# Variables for the spawn rate (timer) of enemies
enemyTimerMax = 40
enemyTimer = enemyTimerMax

# Make the enemy's array
enemies = []
enemiesToRemove = []


# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Check to see what keys the player is pressing
    keys = pygame.key.get_pressed()
    
    # Move Right
    if keys[pygame.K_d]:
        playerFacingLeft = False
        player_x += playerSpeed
    # Move Left
    if keys[pygame.K_a]:
        playerFacingLeft = True
        player_x -= playerSpeed
    # Move Down
    if keys[pygame.K_s]:
        player_y += playerSpeed
    # Move Up
    if keys[pygame.K_w]:
        player_y -= playerSpeed
    # Get Bigger
    if keys[pygame.K_SPACE]:
        playerSize += 2

    # Stop the player from leaving the screen
    if player_x < 0:
        player_x = 0
    if player_x > game_width - playerSize*1.25:
        player_x = game_width - playerSize*1.25
    if player_y < 0:
        player_y = 0
    if player_y > game_height - playerSize:
        player_y = game_height - playerSize
    
    # do the background animation timer
    bgAnimationTimer -= 1
    if bgAnimationTimer <= 0:
        bgAnimationFrame += 1
        if bgAnimationFrame > 1:
            bgAnimationFrame = 0
        bgAnimationTimer = bgAnimationTimerMax

    if bgAnimationFrame == 0:
        screen.blit(backgroundImg, (0, 0))
    else:
        screen.blit(backgroundImg2, (0, 0))

    # Spawn a new enemy whenever enemyTimer hits 0
    enemyTimer -= 1
    if enemyTimer <= 0:
        newEnemyY = random.randint(0, game_height)
        newEnemySpeed = random.randint(1, 5)
        newEnemySize = random.randint(playerSize/2, playerSize*2)
        if random.randint(0, 1) == 0:
            enemies.append(Enemy(-newEnemySize*2, newEnemyY, newEnemySpeed, newEnemySize))
        else:
            enemies.append(Enemy(game_width, newEnemyY, -newEnemySpeed, newEnemySize))
        enemyTimer = enemyTimerMax

    for enemy in enemiesToRemove:
        enemies.remove(enemy)
    enemiesToRemove = []

    # Update all enemies
    for enemy in enemies:
        enemy.update(screen)
        if enemy.x < -1000 or enemy.x > game_width + 1000:
            enemiesToRemove.append(enemy)
        
    if playerAlive:
        # Update the player hitbox
        playerHitbox.x = player_x
        playerHitbox.y = player_y
        playerHitbox.width = int(playerSize*1.25)
        playerHitbox.height = playerSize
        # pygame.draw.rect(screen, (255, 255, 255), playerHitbox)
    
        # Check to see when the player hits an Enemy
        for enemy in enemies:
            if playerHitbox.colliderect(enemy.hitbox):
                if playerSize >= enemy.size:
                    score += enemy.size
                    playerSize += 2
                    enemies.remove(enemy)
                    playerEatingTimer = playerEatingTimerMax
                else:
                    playerAlive = False

        # Do the player swimming animation timer
        playerSwimmingTimer -= 1
        if playerSwimmingTimer <= 0:
            playerSwimmingTimer = playerSwimmingTimerMax
            playerSwimmingFrame += 1
            if playerSwimmingFrame > 1:
                playerSwimmingFrame = 0
    
        # Draw the player pic
        if playerEatingTimer > 0:
            playerPicSmall = pygame.transform.scale(playerEatingPic, (int(playerSize*1.25), playerSize))
            playerEatingTimer -= 1
        else:
            if playerSwimmingFrame == 0:
                playerPicSmall = pygame.transform.scale(playerPic, (int(playerSize*1.25), playerSize))
            else:
                playerPicSmall = pygame.transform.scale(playerPic2, (int(playerSize*1.25), playerSize))
        if playerFacingLeft:
            playerPicSmall = pygame.transform.flip(playerPicSmall, True, False)
        screen.blit(playerPicSmall, (player_x, player_y))

    # Draw the score text
    if playerAlive:
        scoreText = scoreFont.render("Score: "+str(score), 1, (255, 255, 255))
    else:
        scoreText = scoreFont.render("Final Score: "+str(score), 1, (255, 255, 255))

    if score >= 0:
        screen.blit(scoreText, (30, 30))

    # Draw the menu (when the player is not alive
    if not playerAlive:
        screen.blit(playButtonPic, (playButtonX, playButtonY))
        screen.blit(titlePic, (titleX, titleY))
        mouseX, mouseY = pygame.mouse.get_pos()
        # Check to see if the player clicks the play button
        if pygame.mouse.get_pressed()[0]:
            if mouseX > playButtonX and mouseX < playButtonX+playButtonPic.get_width():
                if mouseY > playButtonY and mouseY < playButtonY+playButtonPic.get_height():
                    # Restart the game
                    playerAlive = True
                    score = 0
                    player_x = playerStartingX
                    player_y = playerStartingY
                    playerSize = playerStartingSize
                    for enemy in enemies:
                        enemiesToRemove.append(enemy)
        

    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
