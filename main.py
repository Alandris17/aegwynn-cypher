import os
import string

def get_poem_path(title, author):
    return f"{title.title()} - {author.title()}.txt"

def check_poem_exists(poem_path):
    return os.path.exists(poem_path)

def read_poem(poem_path):
    with open(poem_path, "r", encoding="utf-8") as file:
        return file.readlines()

def split_into_stanzas(poem_lines):
    """Return a list of stanzas, where each stanza is a list of non-empty lines."""
    stanzas = []
    current_stanza = []
    for poem_line in poem_lines:
        stripped_line = poem_line.strip()
        if stripped_line:
            current_stanza.append(stripped_line)
        elif current_stanza:
            stanzas.append(current_stanza)
            current_stanza = []
    if current_stanza:
        stanzas.append(current_stanza)
    if not stanzas:
        raise ValueError("The poem contains no stanzas.")
    return stanzas

def clean_word(word):
    """Keep only alphabetic characters from a poem word."""
    cleaned = "".join(char for char in word if char.isalpha())
    if not cleaned:
        raise ValueError(f"The selected poem word {word!r} contains no letters.")
    return cleaned

def get_starting_word(poem_lines, stanza, line, word):
    stanzas = split_into_stanzas(poem_lines)
    stanza_index = (stanza - 1) % len(stanzas)
    stanza_lines = stanzas[stanza_index]
    line_index = (line - 1) % len(stanza_lines)
    line_words = stanza_lines[line_index].split()
    if not line_words:
        raise ValueError("The selected line contains no words.")
    word_index = (word - 1) % len(line_words)
    return clean_word(line_words[word_index])

def get_shift_from_key_word(key_word, key_letter_index):
    alphabet = string.ascii_lowercase
    key_letter = key_word[key_letter_index % len(key_word)].lower()
    return alphabet.index(key_letter)

def shift_character(char, shift):
    if char.islower():
        alphabet = string.ascii_lowercase
        return alphabet[(alphabet.index(char) + shift) % 26]
    if char.isupper():
        alphabet = string.ascii_uppercase
        return alphabet[(alphabet.index(char) + shift) % 26]
    return char

def unshift_character(char, shift):
    if char.islower():
        alphabet = string.ascii_lowercase
        return alphabet[(alphabet.index(char) - shift) % 26]
    if char.isupper():
        alphabet = string.ascii_uppercase
        return alphabet[(alphabet.index(char) - shift) % 26]
    return char

def convert_number_to_words(number_text):
    """Convert an integer string from 0 to 999999 into English words."""
    number = int(number_text)
    ones = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen"
    ]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    def under_thousand(n):
        parts = []
        if n >= 100:
            parts.append(ones[n // 100])
            parts.append("hundred")
            n %= 100
        if n >= 20:
            parts.append(tens[n // 10])
            n %= 10
        if 0 < n < 20:
            parts.append(ones[n])
        return parts
    if number == 0:
        return "zero"
    if number > 999999:
        raise ValueError("Numbers larger than 999999 are not supported by this simple converter.")
    words = []
    if number >= 1000:
        words.extend(under_thousand(number // 1000))
        words.append("thousand")
        number %= 1000
    words.extend(under_thousand(number))
    return " ".join(words)

def write_numbers_as_words(message):
    """Replace digit sequences with English words before encoding."""
    result = []
    i = 0
    while i < len(message):
        if message[i].isdigit():
            start = i
            while i < len(message) and message[i].isdigit():
                i += 1
            result.append(convert_number_to_words(message[start:i]))
        else:
            result.append(message[i])
            i += 1
    return "".join(result)

def encode_message(poem_lines, stanza, line, word, message):
    key_word = get_starting_word(poem_lines, stanza, line, word)
    key_letter_index = 0
    current_shift = get_shift_from_key_word(key_word, key_letter_index)
    message = write_numbers_as_words(message)
    coded_message = []
    for char in message:
        if char.isalpha():
            coded_message.append(shift_character(char, current_shift))
        elif char in string.punctuation:
            coded_message.append(char)
            key_letter_index += 1
            current_shift = get_shift_from_key_word(key_word, key_letter_index)
        else:
            coded_message.append(char)
    return "".join(coded_message)

def decode_message(poem_lines, stanza, line, word, coded_message):
    key_word = get_starting_word(poem_lines, stanza, line, word)
    key_letter_index = 0
    current_shift = get_shift_from_key_word(key_word, key_letter_index)
    decoded_message = []
    for char in coded_message:
        if char.isalpha():
            decoded_message.append(unshift_character(char, current_shift))
        elif char in string.punctuation:
            decoded_message.append(char)
            key_letter_index += 1
            current_shift = get_shift_from_key_word(key_word, key_letter_index)
        else:
            decoded_message.append(char)
    return "".join(decoded_message)

def parse_reference(reference):
    """
    Parse the letter reference as stanza.line.word.
    Example: 2.4.7 means stanza 2, line 4, word 7.
    """
    try:
        stanza, line, word = reference.split(".")
        return int(stanza), int(line), int(word)
    except ValueError as exc:
        raise ValueError("Invalid reference format. Use stanza.line.word, for example 2.4.7.") from exc

def main():
    title = input("Enter the poem title: ").strip().title()
    author = input("Enter the author: ").strip().title()
    poem_path = get_poem_path(title, author)
    if not check_poem_exists(poem_path):
        print(f"The poem '{title}' by '{author}' does not exist in the directory.")
        return
    reference = input("Enter the letter reference as stanza.line.word, e.g. 2.4.7: ").strip()
    poem_lines = read_poem(poem_path)
    stanza, line, word = parse_reference(reference)
    action = input("Do you want to encode or decode a message? (encode/decode): ").strip().lower()
    if action == "encode":
        message = input("Enter the message to encode: ")
        encoded_message = encode_message(poem_lines, stanza, line, word, message)
        print(f"Encoded Message: {encoded_message}")
    elif action == "decode":
        coded_message = input("Enter the coded message to decode: ")
        decoded_message = decode_message(poem_lines, stanza, line, word, coded_message)
        print(f"Decoded Message: {decoded_message}")
    else:
        print("Invalid action. Please enter 'encode' or 'decode'.")

if __name__ == "__main__":
    main()
