import os
import sys
import cv2
import pygame
import numpy as np

from eyeGestures.utils import VideoCapture
from eyeGestures import EyeGestures_v2

pygame.init()
pygame.font.init()

# Get the display dimensions
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("EyeGestures v2 example")
font_size = 48
bold_font = pygame.font.Font(None, font_size)
bold_font.set_bold(True)  # Set the font to bold

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{dir_path}/..')

gestures = EyeGestures_v2()
cap = VideoCapture(0)

# x = np.arange(0, 1.1, 0.5)
# y = np.arange(0, 1.1, 0.5)

test_points = [(round(x, 2), round(y, 2)) 
               for x in np.linspace(0.1, 0.9, 7) 
               for y in np.linspace(0.1, 0.9, 7)]
gestures.uploadCalibrationMap(test_points)


# test_points = np.column_stack([xx.ravel(), yy.ravel()])
print(test_points)
n_points = len(test_points)
gestures.setClassicalImpact(3)  # weight it more
# np.random.shuffle(test_points)\
gestures.setClassicalImpact(2)
gestures.setFixation(1.0)
# Initialize Pygame
# Set up colors
RED = (255, 0, 100)
BLUE = (100, 0, 255)
GREEN = (0, 255, 0)
BLANK = (0,0,0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

# Main game loop
running = True
iterator = 0
prev_x = 0
prev_y = 0
while running:
    # Event handling
    cursor_x, cursor_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                running = False


    # Generate new random position for the cursor
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    calibrate = (iterator <= n_points) # calibrate 25 points

    event, calibration = gestures.step(frame, calibrate, screen_width, screen_height, context="my_context")
    
    screen.fill((0, 0, 0))
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.scale(frame, (400, 400))

    if event is not None or calibration is not None:
        # Display frame on Pygame screen
        screen.blit(frame, (0, 0))
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f'{event.fixation}', False, (0, 0, 0))
        screen.blit(text_surface, (0,0))
        if calibrate:

            pygame.draw.circle(screen, GREEN, (cursor_x, cursor_y), 8)  # Actual cursor (feedback)

            # Optional: Log or use this data for adaptive calibration
            if event is not None:
                predicted_x, predicted_y = event.point
                print(f"Gaze: ({predicted_x}, {predicted_y}) | Cursor: ({cursor_x}, {cursor_y})")


            if calibration.point[0] != prev_x or calibration.point[1] != prev_y:
                iterator += 1
                prev_x = calibration.point[0]
                prev_y = calibration.point[1]
            # pygame.draw.circle(screen, GREEN, fit_point, calibration_radius)
            pygame.draw.circle(screen, BLUE, calibration.point, calibration.acceptance_radius/4)
            text_surface = bold_font.render(f"{iterator}/{n_points}", True, WHITE)
            text_square = text_surface.get_rect(center=calibration.point)
            screen.blit(text_surface, text_square)
        else:
            pass
        if gestures.whichAlgorithm(context="my_context") == "Ridge":
            pygame.draw.circle(screen, RED, event.point, 5)
        if gestures.whichAlgorithm(context="my_context") == "LassoCV":
            pygame.draw.circle(screen, BLUE, event.point, 5)
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f'{gestures.whichAlgorithm(context="my_context")}', False, (0, 0, 0))
        screen.blit(text_surface, event.point)
        
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

