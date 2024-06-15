import pygame
import json
import time
import random
import logging
from audio import AudioHandler
from image_handler import ImageHandler

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PNG Tuber")

def setup_logging(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    logging.basicConfig(filename='png_tuber.log', level=numeric_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')

# Main function
def main(config):
    mic_name = config["mic_name"]
    image_folder = config["image_folder"]
    background_color = tuple(config["background_color"])  # Convert list to tuple for Pygame
    image_files = config["images"]
    logging_level = config["logging_level"]

    # Set up logging
    setup_logging(logging_level)
    logging.info("Application started")

    # Initialize AudioHandler
    try:
        audio_handler = AudioHandler(mic_name)
        logging.info(f"Microphone '{mic_name}' initialized successfully")
    except ValueError as e:
        logging.error(e)
        print(e)
        return

    # Initialize ImageHandler
    try:
        image_handler = ImageHandler(image_folder, background_color, image_files)
        logging.info("Images loaded successfully")
    except (ValueError, FileNotFoundError) as e:
        logging.error(e)
        print(e)
        return

    # Main loop
    running = True
    last_talking = False  # Track the previous state of talking
    threshold = 0.02  # Adjust this value based on your microphone sensitivity

    # Blinking logic
    next_blink_time = time.time() + random.uniform(5, 15)
    eyes_open = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                logging.info("Application terminated by user")

        # Check microphone input
        volume = audio_handler.get_microphone_input(duration=0.05)  # Short duration for more frequent updates
        logging.debug(f"Microphone volume: {volume}")

        is_talking = volume > threshold

        # Handle blinking
        current_time = time.time()
        if current_time >= next_blink_time:
            eyes_open = not eyes_open
            next_blink_time = current_time + random.uniform(0.1, 0.2) if not eyes_open else current_time + random.uniform(5, 15)
            logging.debug(f"Blink state changed: {'eyes open' if eyes_open else 'eyes closed'}")

        # Display the current image based on volume and blink state
        image_handler.display_image(screen, eyes_open, is_talking)

        # If we stopped talking, ensure the closed mouth is displayed immediately
        if not is_talking and last_talking:
            image_handler.display_image(screen, eyes_open, False)

        last_talking = is_talking

        # Sleep to control the loop frequency
        time.sleep(0.05)

    pygame.quit()
    logging.info("Application terminated")

if __name__ == "__main__":
    # Load configuration
    with open("config.json", "r") as file:
        config = json.load(file)

    # Run the main function with configuration
    main(config)






