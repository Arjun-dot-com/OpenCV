import os
import tkinter as tk
from tkinter import Label, Button, Entry
from capture_faces import capture
from train import train
from recognize import recognize

class FaceRecognitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("900x650")
        self.root.configure(bg="#0d0d0d")

        name_frame = tk.Frame(self.root, bg="#0d0d0d")
        name_frame.pack(pady=10)
        Label(name_frame, text="Name:", font=("Arial", 14), fg="white", bg="#0d0d0d").pack(side="left", padx=5)
        self.name_entry = Entry(name_frame, font=("Arial", 14))
        self.name_entry.pack(side="left", padx=5)

        self.info_label = Label(self.root, text="Enter a name and choose an action",
                                font=("Arial", 14),
                                fg="#00aaff", bg="#0d0d0d")
        self.info_label.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#0d0d0d")
        btn_frame.pack(pady=20)

        def create_glow_button(parent, text, command, base_color, hover_color, glow_color, row, col):
            glow = Label(parent, bg=glow_color, width=18, height=2)
            glow.grid(row=row, column=col, padx=10, pady=5)
            glow.grid_propagate(False)
            btn = Button(glow, text=text, command=command,
                         font=("Arial", 14, "bold"),
                         bg=base_color, fg="white",
                         activebackground=hover_color, activeforeground="white",
                         relief="flat", padx=20, pady=10)
            btn.pack(expand=True, fill="both")
            def on_enter(e): btn.config(bg=hover_color, font=("Arial", 15, "bold"))
            def on_leave(e): btn.config(bg=base_color, font=("Arial", 14, "bold"))
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            return btn

        create_glow_button(btn_frame, "📸 Capture Faces", self.gui_capture,
                           "#004d00", "#006600", "#003300", 0, 0)

        create_glow_button(btn_frame, "⚙ Train Model", self.gui_train,
                           "#333300", "#666600", "#4d4d00", 0, 1)

        create_glow_button(btn_frame, "▶ Start Recognition", self.gui_recognize,
                           "#003366", "#005599", "#004080", 1, 0)

    def gui_capture(self):
        name = self.name_entry.get().strip()
        if not name:
            self.info_label.config(text="Please enter a name before capturing")
            return
        capture(name)
        self.info_label.config(text=f"Captured faces for '{name}'")

    def gui_train(self):
        if not os.path.exists("dataset") or not os.listdir("dataset"):
            self.info_label.config(text="No dataset found. Capture faces first.")
            return
        train()
        self.info_label.config(text="Training complete.")

    def gui_recognize(self):
        if not os.path.exists("face_trained.yml"):
            self.info_label.config(text="Model not found. Train model first.")
            return
        self.info_label.config(text="Recognition started. Close window to stop.")
        recognize()

if __name__=="__main__":
    root = tk.Tk()
    app = FaceRecognitionGUI(root)
    root.mainloop()
