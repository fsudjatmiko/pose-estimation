import pygame
from ui import main_menu, image_selection, camera_selection, quit_app
from pose_estimation import pose_estimation_image
from camera import pose_estimation_camera, list_cameras

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pose Estimation")

mode = 'menu'
selected_image = None
camera_index = 0
running = True

def set_mode(new_mode, param=None):
    global mode, selected_image, camera_index
    mode = new_mode
    if new_mode == 'pose_image':
        selected_image = param
    elif new_mode == 'pose_camera':
        camera_index = param

def main():
    global mode, selected_image, camera_index, running

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if mode == 'menu':
            main_menu(set_mode)
        elif mode == 'image_selection':
            image_selection(set_mode)
        elif mode == 'pose_image':
            pose_estimation_image(set_mode, selected_image)
        elif mode == 'camera_selection':
            camera_selection(set_mode)
        elif mode == 'pose_camera':
            pose_estimation_camera(set_mode, camera_index)

    pygame.quit()

if __name__ == "__main__":
    main()
