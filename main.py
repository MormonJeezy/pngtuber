import pygame
import json
import time
import random
from audio import AudioHandler
from image_handler import ImageHandler

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PNG Tuber")

# Main function
def main(config):
    mic_name = config["mic_name"]
    image_folder = config["image_folder"]
    background_color = tuple(config["background_color"])  # Convert list to tuple for Pygame
    image_files = config["images"]

    # Initialize AudioHandler
    try:
        audio_handler = AudioHandler(mic_name)
    except ValueError as e:
        print(e)
        return

    # Initialize ImageHandler
    try:
        image_handler = ImageHandler(image_folder, background_color, image_files)
    except (ValueError, FileNotFoundError) as e:
        print(e)
        return

    # Main loop
    running = True
    last_talking = False  # Track the previous state of talking
    threshold = config["mic_threshold"]  # Adjust this value based on your microphone sensitivity

    # Blinking logic
    next_blink_time = time.time() + random.uniform(config["blink_min"], config["blink_max"])
    eyes_open = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check microphone input
        volume = audio_handler.get_microphone_input(duration=0.05)  # Short duration for more frequent updates
        # For debugging purposes
        #print("Volume:", volume)  

        is_talking = volume > threshold

        # Handle blinking
        current_time = time.time()
        if current_time >= next_blink_time:
            eyes_open = not eyes_open
            next_blink_time = current_time + random.uniform(0.1, 0.2) if not eyes_open else current_time + random.uniform(5, 15)

        # Display the current image based on volume and blink state
        image_handler.display_image(screen, eyes_open, is_talking)

        # If we stopped talking, ensure the closed mouth is displayed immediately
        if not is_talking and last_talking:
            image_handler.display_image(screen, eyes_open, False)

        last_talking = is_talking

        # Sleep to control the loop frequency
        time.sleep(config["loop_interval"])

    pygame.quit()

if __name__ == "__main__":
    # Load configuration
    with open("config.json", "r") as file:
        config = json.load(file)

    # Run the main function with configuration
    main(config)





