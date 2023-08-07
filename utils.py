import os
import random
import string


def generate_random_image_name(length=10, extension=".png"):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string + extension


def remove_files_from_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


# Example usage
if __name__ == "__main__":
    random_image_name = generate_random_image_name()
    print(random_image_name)
