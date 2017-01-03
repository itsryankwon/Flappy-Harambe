import pygame
import time
from random import randint

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 40)


pygame.init() #initialize pygame
clock = pygame.time.Clock() #intialize clock

width = 800 #set width to 800
height = 400 #set height to 400
surface = pygame.display.set_mode((width, height)) #set surface to 800 x 400 px
pygame.display.set_caption("PY-O-NEERS FLAPPY HARAMBE") #set caption

img = pygame.image.load('harambesprite.png') # load harambe image
bgIMG = pygame.image.load('bg.png') #load background image

imageHeight = 108 #set our image's height
imageWidth = 96 #set our image's width

#method blocks() to draw our blocks
def blocks(x_block, y_block, block_width, block_height, gap):
    pygame.draw.rect(surface, black, [x_block, y_block, block_width, block_height])
    pygame.draw.rect(surface, black, [x_block, y_block+block_height+gap, block_width, height-block_height])

#method gameOver() to handle what our game does after collision detection
def gameOver():

    smallText = pygame.font.Font("impact.ttf", 20) #load font for small text
    largeText = pygame.font.Font("impact.ttf", 70) #load font for large text

    titleTextSurf, titleTextRect = makeTextObjs("U LOST!!!", largeText) 
    titleTextRect.center = width/2, height/2
    surface.blit(titleTextSurf, titleTextRect)

    typTextSurf, typTextRect = makeTextObjs("Press any key to continue", smallText)
    typTextRect.center = width/2, ((height/2)+100)
    surface.blit(typTextSurf, typTextRect)
    pygame.display.update()
    time.sleep(3)

    while replay_or_quit() == None:
        clock.tick()
    main()

def makeTextObjs(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            continue
        return event.key
    return None
    
#zoobg method for drawing zoo background image
def zoobg(image):
    surface.blit(bgIMG, (0,0))
    

#harambe method which will draw harambe onto surface
def harambe(x, y, image):
    surface.blit(img, (x,y))

def score(count):
    font = pygame.font.Font("impact.ttf", 15) #set font of our score to be impact and size of 15
    text = font.render("Score: " + str(count), True, green) #render this text with green color
    surface.blit(text, [0,0]) #blit our text onto surface at position 0, 0

def main():
    #initial x,y coordinates for harambe
    x = 100
    y = 100

    #set y_move to 0 for no movement initially
    y_move = 0

    x_block = width #set x_block to value of width
    y_block = 0 #set y_block to value of 0
    block_width = 75 #set block_width to 75
    block_height = randint(50, 200) #generate a random height from 50 to 200 for blocks
    gap = imageHeight + 50 #gap will be our imageHeight + 50
    block_move = 0 #set block_move to 0

    current_score = 0 #set our current score

    game_status = True #set initial game_status to True

    #game loop
    while game_status == True:
        for event in pygame.event.get(): #pygame.event.get() will get all events
            if event.type == pygame.QUIT: #if quit event 
                game_status = False #set game_status to false
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 3
                    block_move = 4

        y += y_move #y will continuously be updated as y_move changes with the presses of the up arrow key

        if (y > height-imageHeight or y < -4): #if harambe touches top or bottom of window
            gameOver() #run gameOver method
        
        surface.fill(red) #change bg color to red
        zoobg(bgIMG) #draw background image
        harambe(x, y, img) #draw harambe

        blocks(x_block, y_block, block_width, block_height, gap) #call blocks() method
        score(current_score) #call score() method
        
        x_block -= block_move

        if x_block < (-1*block_width):
            x_block = width
            block_height = randint(50, 200)

        if (x + imageWidth > x_block):
            if (x < x_block + block_width):
                #print('possibly within the boundaries of x upper')
                if (y < block_height):
                    #print('Y crossover upper')
                    if (x - imageWidth < block_width + x_block):
                        #print('game over hit upper')
                        gameOver()

        if (x + imageWidth > x_block):
            #print('x crossover')
            if (y + imageHeight > block_height+gap):
                #print('Y crossover lower')
                if (x < block_width + x_block):
                    #print('game over Lower')
                    gameOver()
                    
        #print("x_block", x_block)
        if (x_block == 16):
            current_score += 1

        pygame.display.update() #update display
        clock.tick(30) #set fps to 30

main()
pygame.quit()
quit()
