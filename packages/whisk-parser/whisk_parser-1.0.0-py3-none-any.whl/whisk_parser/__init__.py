import re

CHARS_MAPPING = {
    "underscore": "_",
    "guion bajo": "_",
    "hashtag": " #", # sometimes hashtags are written as "text#foo" instead of "text #foo"
    'dot': '.'
}

AT_PATTERN = r"\s?(at|arroba)+\s?"
SPECIAL_PATTERN = r"\s?(underscore|guion bajo|hashtag)+\s?"

def parse_email(input_str):
    at_pattern = re.compile(AT_PATTERN)
    special_pattern = re.compile(SPECIAL_PATTERN)

    # Convert at symbol (@)
    at_positions = [match for match in re.finditer(at_pattern, input_str)]

    if at_positions:
        last_at_position = at_positions[-1]

        # Prevent replacing URLs when prefix is "at": https://www.linguee.es/ingles-espanol/traduccion/available+at+www.html
        if not re.match(r"\b(?:www\.)\b(?:https?:\/\/)?(?:[a-zA-Z0-9-]+\.[a-zA-Z]{2,})(?:\/[^\s]*)?", input_str[last_at_position.start() + len(last_at_position.group()):]):
            input_str = input_str[:last_at_position.start()] + "@" + input_str[last_at_position.start() + len(last_at_position.group()):]

    # Convert special chars
    special_positions = [match for match in re.finditer(special_pattern, input_str)]

    if special_positions:
        last_special_position = special_positions[-1]
        input_str = input_str.replace(last_special_position.group(), CHARS_MAPPING[last_special_position.group().strip()])

    return input_str