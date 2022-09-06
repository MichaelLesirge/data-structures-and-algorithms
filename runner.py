from collections.abc import Callable
from doctest import OutputChecker
from typing import Any

EXIT_KEYWORDS= ("exit", "ex", "leave", "quit")

def welcome(welcome_message: str) -> None:
    print(f"Welcome to the {welcome_message}.")
    print()

def run(function: Callable, *inputs: tuple[str, tuple[Callable, str|None]|None], welcome_message: str|None = None, error_message: str | None = None, output_label: str|None = None, after_input_blank_line: bool = False) -> None:
    """
    function should return answer.
    inputs: tuple[string, tuple[callable, str | None] | None]
    inputs ex: ("Enter a number", (int, "input most be a number"))

    what inputs do ("input message" + ": ", (converter_funtion, "Error message if converter fails" or None to use normal error message) or None to just leave as str)
    """
    if welcome_message is not None:
        welcome(welcome_message)
    while True:
        vals = []
        for input_text, converter in inputs:
            user_input = get_input(input_text)
            if user_input in EXIT_KEYWORDS:
                print("Goodbye.")
                return

            new_input = valid_input(user_input, converter)
                

            vals.append(new_input)

        try:
            output = function(*vals)
        except Exception as exs:
            if error_message is None:
                print_error(exs)
            else:
                print_error(error_message)
        else:
            if after_input_blank_line:
                print()
            if output_label is not None:
                print(f"{output_label}: ")
            print(output)
        print()

def print_error(*args, **kwargs):
    print("Error:", *args, **kwargs)

def print_input_error(*args, **kwargs):
    print("Invalid Input:", *args, **kwargs)

def get_input(prompt):
    return input(prompt + ": ")

def get_valid_input(input_text, converter):
    user_input = get_input(input_text)
    return valid_input(user_input, converter)

def valid_input(user_input, converter):
    need_input = True
    while need_input:
        if converter is None:
            new_input = user_input
            need_input = False
        else:
            converter_func, error_message = converter
            try:
                new_input = converter_func(user_input)
            except Exception as exs:
                if error_message is None:
                    print_input_error(exs)
                else:
                    print_input_error(error_message)
            else:
                need_input = False
    return new_input