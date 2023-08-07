from image_generator import ImageGenerator


def get_user_menu_choice():
    choices = "nhocx"
    while choice := input(
        "\tMenu:\n"
        "\t(n) Generate new image from prompt\n"
        "\t(h) display saved prompt history\n"
        "\t(o) display the image with assigned id (in history)\n"
        "\t(c) clear history\n"
        "\t(x) exit\n"
        "\t: "
    ):
        if choice in choices:
            return choice
        print("Invalid choice. Try again...")


def validate_prompt(text: str):
    """
    prompt should be non empty and should contain less than 1000 characters
    """
    if 1 <= len(text) <= 1000:
        return text


def get_prompt():
    while (prompt := validate_prompt(input("input prompt: ").strip())) is None:
        print(
            "prompt should be non empty and should contain less than 1000 characters. Try again..."
        )
    return prompt


def validate_prompt_id(prompt_id):
    """prompt_id should be integer"""
    try:
        prompt_id = int(prompt_id)
        return prompt_id
    except Exception:
        return


def get_prompt_id():
    while (
        prompt_id := validate_prompt_id(
            input("input prompt id (listed in history): ").strip()
        )
    ) is None:
        print("prompt id should be integer. Try again...")
    return prompt_id


def display_prompt_history(image_generator: ImageGenerator):
    prompt_history = image_generator.get_prompt_history()
    print(f"\nPrompt History:\n{prompt_history}\n")


def main():
    image_generator = ImageGenerator()
    while (choice := get_user_menu_choice()) != "x":
        if choice == "n":
            prompt = get_prompt()
            print("generating, please wait...")
            image_generator.generate_image(prompt=prompt)
        elif choice == "h":
            display_prompt_history(image_generator)
        elif choice == "c":
            image_generator.clear_history()
        elif choice == "o":
            prompt_id = get_prompt_id()
            image_generator.display_image_with_prompt_id(prompt_id)


if __name__ == "__main__":
    main()
