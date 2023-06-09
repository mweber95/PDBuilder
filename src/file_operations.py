def get_content_from_input(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        file_content = file.readlines()
    return file_content


def write_content_to_output(filename: str, content: list[str]) -> None:
    with open(filename, 'w') as file:
        for line in content:
            file.write(f'{line}')
