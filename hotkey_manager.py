from pynput import keyboard

class HotkeyManager:
    def __init__(self, app):
        self.app = app
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+r': self.app.toggle_recording,
        })

    def start(self):
        self.listener.start()
