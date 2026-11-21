import time
from pynput import keyboard, mouse

class input_tracker:
    def __init__(self):
        self.mouse_clicked = False
        self.key_pressed = False
        self.mouse_listener = None
        self.keyboard_listener = None

    def handle_mouse_click(self, x_position, y_position, mouse_button, is_pressed):
        if is_pressed == True:
            self.mouse_clicked = True

    def handle_key_press(self, pressed_key):
        self.key_pressed = True

    def start(self):
        self.mouse_listener = mouse.Listener(on_click=self.handle_mouse_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.handle_key_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def get_data(self):
        current_time = float(time.time())
        input_data = {"timestamp": current_time,"clicked": self.mouse_clicked,"key_pressed": self.key_pressed}
        self.mouse_clicked = False
        self.key_pressed = False
        return input_data

    def stop(self):
        if self.mouse_listener != None:
            self.mouse_listener.stop()
        if self.keyboard_listener != None:
            self.keyboard_listener.stop()