import pygame
import cv2
import mediapipe as mp
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pose Estimation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
LIGHT_RED = (255, 182, 193)

# Fonts
font = pygame.font.Font(None, 36)

# Mediapipe pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Load images from the images folder
image_folder = 'images'
images = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    draw_text(text, x + 10, y + 10, WHITE)

def main_menu():
    screen.fill(LIGHT_BLUE)
    draw_text("Pose Estimation", WIDTH // 2 - 100, HEIGHT // 4, BLUE)
    draw_button("Use Image", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, BLUE, LIGHT_BLUE, lambda: set_mode('image_selection'))
    draw_button("Use Camera", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GREEN, LIGHT_GREEN, lambda: set_mode('camera_selection'))
    draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, RED, LIGHT_RED, quit_app)
    pygame.display.flip()

def image_selection():
    screen.fill(LIGHT_BLUE)
    draw_text("Select an Image", WIDTH // 2 - 100, HEIGHT // 4, BLUE)
    margin = 20
    image_size = 100
    columns = 5
    x_offset = (WIDTH - (columns * (image_size + margin))) // 2
    y_offset = HEIGHT // 4 + 50
    for i, img in enumerate(images):
        image = pygame.image.load(os.path.join(image_folder, img))
        image = pygame.transform.scale(image, (image_size, image_size))
        x = x_offset + (i % columns) * (image_size + margin)
        y = y_offset + (i // columns) * (image_size + margin)
        screen.blit(image, (x, y))
        draw_button("Select", x, y + image_size + 5, image_size, 30, BLUE, LIGHT_BLUE, lambda img=img: set_mode('pose_image', img))
    draw_button("Back", 10, 10, 100, 30, RED, LIGHT_RED, lambda: set_mode('menu'))
    pygame.display.flip()

def pose_estimation_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    annotated_image = image.copy()
    mp.solutions.drawing_utils.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    annotated_image = scale_and_center_image(annotated_image)
    screen.fill(WHITE)
    screen.blit(annotated_image, (WIDTH // 2 - annotated_image.get_width() // 2, HEIGHT // 2 - annotated_image.get_height() // 2))
    draw_button("Back", 10, 10, 100, 30, RED, LIGHT_RED, lambda: set_mode('menu'))
    pygame.display.flip()

def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

def pose_estimation_camera(camera_index):
    cap = cv2.VideoCapture(camera_index)
    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        annotated_frame = frame.copy()
        mp.solutions.drawing_utils.draw_landmarks(annotated_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        annotated_frame = scale_and_center_image(annotated_frame)
        screen.fill(WHITE)
        screen.blit(annotated_frame, (WIDTH // 2 - annotated_frame.get_width() // 2, HEIGHT // 2 - annotated_frame.get_height() // 2))
        draw_button("Back", 10, 10, 100, 30, RED, LIGHT_RED, lambda: stop_camera(cap))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    cap.release()

def scale_and_center_image(image):
    image_surface = pygame.surfarray.make_surface(image)
    image_surface = pygame.transform.rotate(image_surface, -90)
    image_surface = pygame.transform.scale(image_surface, (WIDTH, HEIGHT))
    return image_surface

def stop_camera(cap):
    cap.release()
    set_mode('menu')

def camera_selection():
    screen.fill(LIGHT_BLUE)
    draw_text("Select a Camera", WIDTH // 2 - 100, HEIGHT // 4, BLUE)
    y_offset = HEIGHT // 2 - 50
    cameras = list_cameras()
    for i, cam in enumerate(cameras):
        draw_button(f"Camera {cam}", WIDTH // 2 - 100, y_offset + i * 50, 200, 50, GREEN, LIGHT_GREEN, lambda cam=cam: set_mode('pose_camera', cam))
    draw_button("Back", 10, 10, 100, 30, RED, LIGHT_RED, lambda: set_mode('menu'))
    pygame.display.flip()

def set_mode(new_mode, param=None):
    global mode, selected_image, camera_index
    mode = new_mode
    if new_mode == 'pose_image':
        selected_image = param
    elif new_mode == 'pose_camera':
        camera_index = param

def quit_app():
    global running
    running = False

def main():
    global mode, selected_image, camera_index, running
    mode = 'menu'
    selected_image = None
    camera_index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if mode == 'menu':
            main_menu()
        elif mode == 'image_selection':
            image_selection()
        elif mode == 'pose_image':
            pose_estimation_image(os.path.join(image_folder, selected_image))
        elif mode == 'camera_selection':
            camera_selection()
        elif mode == 'pose_camera':
            pose_estimation_camera(camera_index)

    pygame.quit()

if __name__ == "__main__":
    main()
