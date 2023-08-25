import sys
import threading
import time
from typing import Generator, Tuple

from prompt_toolkit import HTML, PromptSession, print_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import Style


from pai.console import (
    Console,
    ConsoleInput,
    LLMCodeInput,
    LLMErrorInput,
    LLMMessageInput,
    UserInput,
)
from pai.llms.llm import LLMError, LLMResponseCode, LLMResponseMessage


def spinner_generator() -> Generator[str, None, None]:
    """Generate spinner frames."""
    while True:
        yield "| Generating response..."
        yield "/ Generating response..."
        yield "- Generating response..."
        yield "\\ Generating response..."


def spinner_animation(event: threading.Event):
    """Spinner animation function to be run in a separate thread."""
    spinner = spinner_generator()
    while not event.is_set():
        print(next(spinner), end="\r", flush=True)
        time.sleep(0.1)
    print(" " * 2, end="\r", flush=True)  # Clear the spinner


class Animation:
    """Context manager for spinner animation."""

    def __enter__(self):
        self.stop_event = threading.Event()
        self.spinner_thread = threading.Thread(
            target=spinner_animation, args=(self.stop_event,)
        )
        self.spinner_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_event.set()
        self.spinner_thread.join()


# Create a session object
key_bindings = KeyBindings()


@key_bindings.add(Keys.Tab)
def _(event):
    "Insert four spaces for tab key."
    event.cli.current_buffer.insert_text("    ")


@key_bindings.add("escape", "enter")
@key_bindings.add("c-o")
def _(event):
    "Bind meta+enter or esc+enter to insert a newline."
    event.current_buffer.insert_text("\n")


@key_bindings.add("enter")
def _(event):
    event.current_buffer.validate_and_handle()


prompt_style = Style.from_dict(
    {
        "inp": "bold",
        "gen": "bold",
        "multi": "bold",
        "out": "bold",
    }
)


class REPL:
    console: Console
    session: PromptSession
    multiline: bool
    buffered_lines: list[str]

    def __init__(self, console: Console):
        self.console = console
        self.session = PromptSession(key_bindings=key_bindings)
        self.multiline = False
        self.buffered_lines = []

    def go(self):
        while True:
            try:
                current_index = self.console.history_tree.current_position().depth

                inp_prompt = HTML(f"<inp>Inp [{current_index}]> </inp>")
                gen_prompt = HTML(f"<gen>Gen [{current_index}]> </gen>")

                ellipsis = "." * (2 + len(str(current_index)))
                multi_prompt = HTML(f"<multi>    {ellipsis}> </multi>")

                # get the next line from the user
                prompt = (
                    multi_prompt if self.console.more_input_required else inp_prompt
                )
                line: str = self.session.prompt(
                    prompt, prompt_continuation=multi_prompt, style=prompt_style
                )

                line_input = UserInput(line)
                # handle the please command
                if line.startswith("ai:"):
                    line = line[3:]  # remove the "please " prefix

                    with Animation():
                        resp = self.console.gen_code(line)

                    if isinstance(resp, LLMResponseCode):
                        # print the message of the response
                        if resp.message:
                            print(resp.message)

                        # prompt the user to edit the generated code code
                        edited = self.session.prompt(
                            gen_prompt,
                            default=resp.code,
                        )
                        line_input = LLMCodeInput(
                            message=resp.message,
                            prompt=resp.prompt,
                            code=edited,
                            raw_resp=resp.raw,
                        )
                    elif isinstance(resp, LLMResponseMessage):
                        line_input = LLMMessageInput(
                            prompt=resp.prompt, message=resp.message, raw_resp=resp.raw
                        )
                    elif isinstance(resp, LLMError):
                        line_input = LLMErrorInput(
                            prompt=resp.prompt, error=resp.error, raw_resp=resp.raw
                        )
                # handle the history command
                if line.startswith("history"):
                    nodes = self.console.history_tree.lineage()
                    for node in nodes:
                        print(f"[{node.depth}]: {node.data}")
                    continue

                resp = self.console.handle_line(line_input)
                if resp:
                    out = HTML(f"<out>Out [{current_index}]></out> ")
                    print_formatted_text(out, style=prompt_style, end="")
                    print(resp, end="")

            except KeyboardInterrupt as e:
                # Handle Ctrl+C and reset the lines
                self.multiline = False
                string_error = str(e)
                if string_error:
                    print(string_error)
                continue
            except EOFError:
                # Handle Ctrl+D (exit)
                print("\nGoodbye!")
                break
