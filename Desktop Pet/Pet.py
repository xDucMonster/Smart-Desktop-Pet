import tkinter as tk
import random
import pyautogui
import extralamps

class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Pet")
        
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        
        self.root.config(bg='white')
        self.root.wm_attributes("-transparentcolor", 'white')

        self.canvas = tk.Canvas(root, width=100, height=100, bg='white', highlightthickness=0)
        self.canvas.pack()

        self.frames = []
        i = 0
        try:
            while True:
                frame = tk.PhotoImage(file='path/your_own_pet.gif', format=f'gif -index {i}')
                self.frames.append(frame)
                i += 1
        except tk.TclError:
            pass

        if not self.frames:
            raise ValueError("gif couldn't load")

        self.pet = self.canvas.create_image(50, 50, image=self.frames[0])

        self.x_pos = 0
        self.y_pos = 1300

        self.direction = 1

        self.moving = True

        self.root.geometry(f'+{self.x_pos}+{self.y_pos}')

        self.move_pet()
        self.animate_pet(0)

        self.canvas.bind("<Button-1>", self.on_pet_click)

    def move_pet(self):
        if self.moving:

            screen_width = self.root.winfo_screenwidth()

        self.x_pos += self.direction * 4 #change speed

        if self.x_pos <= 0 or self.x_pos >= screen_width - 100:
            self.direction *= -1

        self.root.geometry(f'+{self.x_pos}+{self.y_pos}')

        self.root.after(100, self.move_pet)


    def animate_pet(self, frame_index):
        if self.moving:
            self.canvas.itemconfig(self.pet, image=self.frames[frame_index])

            frame_index = (frame_index + 1) % len(self.frames)
            self.root.after(100, self.animate_pet, frame_index)

    def on_pet_click(self, event):
        self.moving = False

        self.create_control_window()

    def create_control_window(self):
        control_window = tk.Toplevel(self.root)
        control_window.title("Lampensteuerung")
        control_window.geometry("200x100+300+300")

        def on_close():
            self.moving = True
            control_window.destroy()

        control_window.protocol("WM_DELETE_WINDOW", on_close)

        on_button = tk.Button(control_window, text="An", command=lambda: self.toggle_lights(True))
        on_button.pack(pady=10)

        off_button = tk.Button(control_window, text="Aus", command=lambda: self.toggle_lights(False))
        off_button.pack(pady=10)

    def toggle_lights(self, state):
        extralamps.user_input_ToF = state
        extralamps.update_lights()

if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPet(root)
    root.mainloop()
