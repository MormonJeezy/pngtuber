import pygame
import os

class ImageHandler:
    def __init__(self, image_folder, background_color, image_files):
        self.image_folder = image_folder
        self.background_color = background_color
        self.image_files = image_files
        self.image_states = self.load_images(image_folder, image_files)

    def load_images(self, folder, image_files):
        images = {}
        for state, file_name in image_files.items():
            image_path = os.path.join(folder, file_name)
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Required image file '{file_name}' not found in folder '{folder}'.")
            images[state] = pygame.image.load(image_path)
        return images

    def display_image(self, screen, eyes_open, mouth_open):
        screen.fill(self.background_color)
        if eyes_open and mouth_open:
            screen.blit(self.image_states["eyes_open_mouth_open"], (0, 0))
        elif eyes_open and not mouth_open:
            screen.blit(self.image_states["eyes_open_mouth_closed"], (0, 0))
        elif not eyes_open and mouth_open:
            screen.blit(self.image_states["eyes_closed_mouth_open"], (0, 0))
        else:
            screen.blit(self.image_states["eyes_closed_mouth_closed"], (0, 0))
        pygame.display.flip()
