# Importing the pygame library
import pygame
import random


# Initialize pygame
pygame.init()

# Colors in RGB format for pygame
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (91, 123, 249)
blue = (0, 0, 255)

# Game window size
display_width = 1500
display_height = 1500

# Game window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("DataFlair - Snake Game")

# Clock for fps and speed of snake
clock = pygame.time.Clock()

# Snake block size
snake_block = 40

# Snake speed
snake_speed = 40

# Font style and size
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

# Images
snake_head_image = pygame.image.load("head_up.png")
apple_image = pygame.image.load("apple.png")


# Function to pause the game and display message
def pause():
    # Paused variable
    paused = True

    # Message to display
    display_message("Paused", black, -100, size="large")
    display_message("Press C to continue or Q to quit.", black, 25)

    # Updating the display
    pygame.display.update()

    # Loop to pause the game
    # and wait for user input
    while paused:
        for event in pygame.event.get():
            # If user clicks on the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # If user presses C, unpause the game
            # and if presss Q, quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                elif event.key == pygame.K_c:
                    paused = False

        # Game clock
        clock.tick(5)


# Function to display score
def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0, 0])


# Function to generate random apple
def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    randAppleY = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    return randAppleX, randAppleY


# Function to display controls
# on screen when game starts
def game_intro():
    # Variable to start the game
    intro = True

    # Loop to display controls
    while intro:
        # Loop to get all the events
        for event in pygame.event.get():
            # If user clicks on the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # If user presses C, start the game
            # and if presss Q, quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # Background color
        gameDisplay.fill(white)

        # Displaying the message
        display_message("Welcome to Snake", green, -100, "large")
        display_message("The objective of the game is to eat red apples", black, -30)
        display_message("The more apples you eat, the longer you get", black, 10)
        display_message("If you run into yourself, or the edges, you die!", black, 50)
        display_message("Press C to play, P to pause or Q to quit.", black, 180)

        pygame.display.update()
        clock.tick(15)


# Function to display snake on screen
def snake(snake_block, snake_list):
    # Displaying the snake head in the direction
    if direction == "right":
        head = pygame.transform.rotate(snake_head_image, -90)
    if direction == "left":
        head = pygame.transform.rotate(snake_head_image, 90)
    if direction == "up":
        head = snake_head_image
    if direction == "down":
        head = pygame.transform.rotate(snake_head_image, 180)

    gameDisplay.blit(head, (snake_list[-1][0], snake_list[-1][1]))

    # Displaying the snake body
    for XnY in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], snake_block, snake_block])


# Function to display message on screen
# in different sizes
def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


# Function to display message on screen
def display_message(message, color, y_change=0, text_size="small"):
    textSurf, textRect = text_objects(message, color, text_size)
    textRect.center = (display_width / 2), (display_height / 2) + y_change
    gameDisplay.blit(textSurf, textRect)


# Main function of the game
def gameLoop():
    # Variable to keep track of direction of snake
    global direction
    direction = "right"

    # Variable to exit the game
    gameExit = False

    # Variable to end the game
    gameOver = False

    # Variables to keep track of snake position
    lead_x = display_width / 3
    lead_y = display_height * 2 / 3

    # Variables to keep track of snake movement
    lead_x_change = 10
    lead_y_change = 0

    # List to keep track of snake length
    snakeList = []
    snakeLength = 1

    # Generating random apple
    randAppleX, randAppleY = randAppleGen()

    # Loop to run the game until user exits
    while not gameExit:
        # Loop to end the game if user dies
        while gameOver == True:
            # Background color
            gameDisplay.fill(white)

            # Displaying the message that user died
            # and asking user to play again
            display_message("Game over", red, -50, size="large")
            display_message(
                "Press C to play again or Q to quit", black, 50, size="medium"
            )
            pygame.display.update()

            # Loop to get all the events
            for event in pygame.event.get():
                # If user clicks on the close button
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                # If user presses C, start the game
                # and if presss Q, quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Loop to get all the events
        for event in pygame.event.get():
            # If user clicks on the close button
            if event.type == pygame.QUIT:
                gameExit = True

            # If user presses any Arrow key
            # change the direction of snake
            # and pause the game if user presses P
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                    lead_x_change = -snake_block
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                    lead_x_change = snake_block
                    lead_y_change = 0
                elif event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                    lead_y_change = -snake_block
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                    lead_y_change = snake_block
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        # If snake goes out of the screen
        if (
            lead_x >= display_width
            or lead_x < 0
            or lead_y >= display_height
            or lead_y < 0
        ):
            gameOver = True

        # Changing the position of snake
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Background color
        gameDisplay.fill(white)

        # Displaying the apple
        gameDisplay.blit(apple_image, (randAppleX, randAppleY))

        # Storing the snake head in a list
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        # If snake length is greater than 1
        # delete the first element of the list
        # so that the snake length remains constant
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # Loop to check if snake head collides with any segment
        for eachSegment in snakeList[:-1]:
            # If snake head collides with any segment
            if eachSegment == snakeHead:
                # End the game
                gameOver = True

        # Displaying the snake
        snake(snake_block, snakeList)

        # Displaying the score
        score(snakeLength - 1)

        # Updating the display
        pygame.display.update()

        # These conditions check if snake head collides with apple
        # If it does, generate a new apple and increase the snake length
        if lead_x >= randAppleX and lead_x <= randAppleX + snake_block:
            if lead_y >= randAppleY and lead_y <= randAppleY + snake_block:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        elif (
            lead_x + snake_block >= randAppleX
            and lead_x + snake_block <= randAppleX + snake_block
        ):
            if (
                lead_y + snake_block >= randAppleY
                and lead_y + snake_block <= randAppleY + snake_block
            ):
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        # Setting the frame rate
        clock.tick(snake_speed)

    # Quiting the game
    pygame.quit()
    quit()


# Calling the main function
game_intro()
gameLoop()
