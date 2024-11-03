import pygame
import cv2
import mediapipe as mp

# Dimensi layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Warna
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_RED = (255, 182, 193)

# Font
font = pygame.font.Font(None, 36)

# Mediapipe pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Fungsi untuk menggambar tombol
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

# Fungsi untuk menggambar teks
def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Fungsi untuk melakukan pose estimation pada gambar
def pose_estimation_image(set_mode, image_path):
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

# Fungsi untuk menskalakan dan memusatkan gambar
def scale_and_center_image(image):
    image_surface = pygame.surfarray.make_surface(image)
    image_surface = pygame.transform.scale(image_surface, (WIDTH, HEIGHT))
    return image_surface
