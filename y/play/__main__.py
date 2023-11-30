#!/usr/bin/env python


from pyglet import app
from pyglet.window import Window
from pyglet.shapes import BorderedRectangle


command_window = Window(style=Window.WINDOW_STYLE_DEFAULT, resizable=True)



class PreviewFrame(BorderedRectangle):

    def __init__(self, parent: Window):
        self.parent = parent
        

        width, height = self.calculate_size()

        super().__init__(parent.width/10, parent.height/10,width, height/10*3, border=2)

    def calculate_size(self):
        base_height = self.parent.height/10*3
        base_width = self.parent.width/10*3

        if base_width > 16 * base_height / 9:
            base_width = 16 * base_height / 9
        if base_height > 9 * base_width / 16:
            base_height = 9 * base_width / 16
        
        return base_width, base_height

    def draw(self):
        self.width, self.height = self.calculate_size()
        super().draw()

preview = PreviewFrame(parent=command_window)

@command_window.event
def on_draw():
    command_window.clear()
    preview.draw()

@command_window.event
def on_mouse_press(x, y, button, mod):

    if preview.x < x < (preview.x + preview.width) and preview.y < y < (preview.y + preview.height):
        print("click")




if __name__ == "__main__":

    app.run()

