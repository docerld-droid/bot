"""Simple GUI-configurable bot that controls the real mouse and keyboard.

The script allows the user to specify a sequence of actions in a
multiline field. Each line should contain a command and optional
arguments, for example::

    move 100 200
    click
    type Hello, world!
    press enter

Supported commands:

``move X Y``
    Move the cursor to coordinates ``X`` and ``Y``.

``click``
    Click the left mouse button at the current cursor position.

``doubleclick``
    Perform a double left click.

``type TEXT``
    Type the given ``TEXT`` via the keyboard.

``press KEY``
    Press a single key, e.g. ``press enter``.

``sleep SECONDS``
    Pause execution for the specified number of seconds.

The bot relies on :mod:`pyautogui` to interact with the actual mouse and
keyboard, so it will move the user's real cursor and send keypresses.
Use with caution and make sure automating your target application does
not violate its terms of service.
"""

from __future__ import annotations

import time
import webbrowser

import PySimpleGUI as sg
import pyautogui


def run_bot(url: str, steps: list[str]) -> None:
    """Execute the user provided steps.

    Parameters
    ----------
    url:
        Optional URL to open in the default web browser before executing
        the steps. If empty, no page is opened.
    steps:
        Sequence of textual commands (see module documentation).
    """

    if url:
        webbrowser.open(url)
        time.sleep(2)  # give the browser a moment to open

    for step in steps:
        parts = step.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        try:
            if cmd == "move":
                x_str, y_str = arg.split()
                pyautogui.moveTo(int(x_str), int(y_str))
            elif cmd == "click":
                pyautogui.click()
            elif cmd == "doubleclick":
                pyautogui.doubleClick()
            elif cmd == "type":
                pyautogui.write(arg)
            elif cmd == "press":
                pyautogui.press(arg)
            elif cmd == "sleep":
                time.sleep(float(arg))
            else:
                sg.popup_error(f"Unknown command: {cmd}")
                break
        except Exception as exc:  # pylint: disable=broad-except
            sg.popup_error(f"Ошибка выполнения шага '{step}': {exc}")
            break


layout = [
    [sg.Text("URL сайта (опционально)"), sg.Input(key="-URL-")],
    [sg.Text("Шаги (по одному на строку):")],
    [
        sg.Multiline(
            key="-STEPS-",
            size=(60, 15),
            default_text=(
                "move 100 200\n"
                "click\n"
                "type Привет\n"
                "press enter\n"
            ),
        )
    ],
    [sg.Button("Запустить"), sg.Button("Выход")],
]

window = sg.Window("Mouse/Keyboard Bot", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Выход"):
        break
    if event == "Запустить":
        url_value = values["-URL-"].strip()
        raw_steps = [s for s in values["-STEPS-"].strip().splitlines() if s]
        run_bot(url_value, raw_steps)

window.close()

