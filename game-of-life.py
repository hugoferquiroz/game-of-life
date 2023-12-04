# -*- coding: utf-8 -*-

# Import libraries 
import pygame
import numpy as np
import time, os

# Center the pop up windows
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Start the simulation
pygame.init()

# Define the screen settings
    ## Size of the screen
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
    ## Background color
bg = 25, 25, 25
screen.fill(bg)

# Define the grid settings
    ## Number of cells in the grid
nxC, nyC = 60, 60   
    ## Size of the grid
dimCW = width / nxC
dimCH = height / nyC

# Define the initial conditions
    # Status of the cells: Alive = 1, Death = 0

gameState = np.zeros((nxC, nyC))

# Autómata palo:
# 0 1 0
# 0 1 0
# 0 1 0
#gameState[5, 3] = 1
#gameState[5, 4] = 1
#gameState[5, 5] = 1

# Another pattern
posInitX = int((nxC / 2) - 3)
posInitY = int((nyC / 2) - 5)
gameState[posInitX, posInitY] = 1
gameState[posInitX + 1, posInitY] = 1
gameState[posInitX + 2, posInitY] = 1
gameState[posInitX + 3, posInitY] = 1

gameState[posInitX + 3, posInitY + 1] = 1
gameState[posInitX + 3, posInitY + 2] = 1

gameState[posInitX, posInitY + 3] = 1
gameState[posInitX + 3, posInitY + 3] = 1

gameState[posInitX, posInitY + 4] = 1
gameState[posInitX + 1, posInitY + 4] = 1
gameState[posInitX + 2, posInitY + 4] = 1
gameState[posInitX + 3, posInitY + 4] = 1

pauseExec = False # True: Start with the simulation paused, False: Start with the simulation running
Endgame = False

iteration = 0
clock = pygame.time.Clock()

# Main loop
while not Endgame:

    newGameState = np.copy(gameState)
    screen.fill(bg)
    
    # Add pause to no stress the cpu
    time.sleep(0.1)

    # Save the actions of keyboard and mouse
    ev = pygame.event.get()

    # Count the population
    population = 0

    for event in ev:

        # If the user press the X button, close the window
        if event.type == pygame.QUIT:
            Endgame = True
            break

        # Add interactive actions
        if event.type == pygame.KEYDOWN:

            # Space bar: pause the simulation
            if event.key == pygame.K_SPACE:
                pauseExec = not pauseExec

            # R key: reset the simulation
            if event.key == pygame.K_r:
                gameState = np.zeros((nxC, nyC))
                newGameState = np.zeros((nxC, nyC))
                pauseExec = True
            else:
                # Another key: pause or resume the simulation
                pauseExec = not pauseExec
        
        # Detect the click of the mouse
        mouseClick = pygame.mouse.get_pressed()
        # Clic -> 1 -> Cell alive 
        if sum(mouseClick) > 0:

            # Click del medio pausa / reanuda el juego
            if mouseClick[1]:
                
                # Obtengo las coordenadas del cursor del mouse en pixeles
                posX, posY, = pygame.mouse.get_pos()

                # Convierto de coordenadas en pixeles a celda clickeada en la grilla
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

                # Click izquierdo y derecho permutan entre vida y muerte
                newGameState[celX, celY] = not gameState[celX, celY]

    if not pauseExec:
        # Add a new generation
        iteration += 1

    # Pass through each cell of the grid
        for y in range(0, nxC):
           for x in range(0, nyC):
                if not pauseExec:
                    # Calculate the number of neighbors
                    n_neigh = (
                        gameState[(x - 1) % nxC, (y - 1) % nyC]
                        + gameState[x % nxC, (y - 1) % nyC]
                        + gameState[(x + 1) % nxC, (y - 1) % nyC]
                        + gameState[(x - 1) % nxC, y % nyC]
                        + gameState[(x + 1) % nxC, y % nyC]
                        + gameState[(x - 1) % nxC, (y + 1) % nyC]
                        + gameState[x % nxC, (y + 1) % nyC]
                        + gameState[(x + 1) % nxC, (y + 1) % nyC]
                    )
                    # The cell dead rebirth if has 3 cell alive around
                    if gameState[x, y] == 0 and n_neigh == 3:
                        newGameState[x, y] = 1

                    # The cell live when has between 2 or 3 cell alive around no more
                    elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        newGameState[x, y] = 0

                # Add population:
                if gameState[x, y] == 1:
                    population += 1

                # Draw the simulation
                poly = [
                    (int(x * dimCW), int(y * dimCH)),
                    (int((x + 1) * dimCW), int(y * dimCH)),
                    (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                    (int(x * dimCW), int((y + 1) * dimCH)),
                ]

                if newGameState[x, y] == 0:
                    # (128, 128, 128) -> Color Grey
                    # (255, 255, 255) -> Color Black
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                    # Constrast when the game is paused
                else:
                    if pauseExec:
                        pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                    else:
                        pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    title = f"The game of life - Population: {population} - Generation: {iteration}"
    if pauseExec:
        title += " - [Paused]"
    pygame.display.set_caption(title)
    print(title)

    # Update gameState
    gameState = np.copy(newGameState)

    # Muestro y actualizo los fotogramas en cada iteración del bucle principal
    pygame.display.flip()

    # Use max 60 fps
    clock.tick(60)

print("The game is over")
