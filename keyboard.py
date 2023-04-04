import time

from pynput import keyboard

KEY_PRESSED = None


def get_key_pressed():
    global KEY_PRESSED
    key = KEY_PRESSED
    KEY_PRESSED = None
    return key


def wait_for_key():
    key = None
    while key is None:
        key = get_key_pressed()
        time.sleep(0.1)
    return key


def on_press(key):
    global KEY_PRESSED
    KEY_PRESSED = key


def listen_for_keys():
    global KEY_PRESSED
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
