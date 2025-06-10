from colors import *
from tkinter import filedialog
import customtkinter as ctk
import random
import json
import csv

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ColorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.bind("<F11>", lambda e: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.title("Palette Generator")
        self.geometry("1280x720")
        self.configure(padx=20, pady=20)

        # Setări culoare de bază
        self.base_color = "#FFDFA9"
        self.num_colors = 5
        self.num_palettes = 5

        # Main Color
        self.color_display = ctk.CTkLabel(self, text=self.base_color, width=100, height=100, fg_color=self.base_color, text_color=get_text_color(self.base_color), corner_radius=12)
        self.color_display.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.color_display.bind("<Button-1>", lambda e: self.open_color_picker())

        # Număr culori
        self.color_count_label = ctk.CTkLabel(self, text="Number of colors")
        self.color_count_label.grid(row=0, column=1)
        self.color_count = ctk.CTkLabel(self, text=str(self.num_colors))
        self.color_count.grid(row=0, column=2)

        self.less_colors = ctk.CTkButton(self, text="<", width=20, command=self.decrease_colors)
        self.more_colors = ctk.CTkButton(self, text=">", width=20, command=self.increase_colors)
        self.less_colors.grid(row=0, column=3)
        self.more_colors.grid(row=0, column=4)

        # Butoane
        self.generate_btn = ctk.CTkButton(self, text="Generate palette", command=self.generate_palette)
        self.generate_btn.grid(row=0, column=6, padx=10)
        self.random_btn = ctk.CTkButton(self, text="Generate random", command=self.random_color)
        self.random_btn.grid(row=1, column=6, padx=10)

        # Preview paletă
        self.palette_frame = ctk.CTkFrame(self, corner_radius=20)
        self.palette_frame.grid(row=2, column=0, columnspan=7, pady=20, sticky="ew")

        self.generate_palette()

        # Export buton
        self.export_btn = ctk.CTkButton(self, text="Export Palettes", command=self.export_palettes)
        self.export_btn.grid(row=1, column=0, columnspan=2, pady=10) 

    def open_color_picker(self, event=None):
        pick_color = AskColor()
        color = pick_color.get()
        if color:
            self.base_color = color
            self.color_display.configure(text=self.base_color, fg_color=self.base_color)
            self.generate_palette()

    def increase_colors(self):
        if self.num_colors < 8:
            self.num_colors += 1
            self.color_count.configure(text=str(self.num_colors))

    def decrease_colors(self):
        if self.num_colors > 2:
            self.num_colors -= 1
            self.color_count.configure(text=str(self.num_colors))

    def random_color(self):
        self.base_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.color_display.configure(text=self.base_color, fg_color=self.base_color)
        self.generate_palette()

    def copy_to_clipboard(self, text, widget):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # Unele sisteme necesită actualizarea clipboard-ului

        # "Copied!" visual label
        copied_label = ctk.CTkLabel(
            master=self,
            text="Copied!",
            fg_color="transparent",
            text_color="green",
            font=("Arial", 14, "bold")
        )

        # Sa il pun sa fie vizibil la colt de widget
        x = widget.winfo_rootx() - self.winfo_rootx()
        y = widget.winfo_rooty() - self.winfo_rooty() - 25

        copied_label.place(x=x, y=y)

        # Auto-destroy after 1.5 seconds
        copied_label.after(1500, copied_label.destroy)

    def generate_palette(self):
        for widget in self.palette_frame.winfo_children():
            widget.destroy()

        # Tipuri de palete și funcțiile lor
        palette_funcs = [
            ("Analog", generate_analog_palette),
            ("Complementary", generate_complementary_palette),
            ("Split Complementary", generate_split_complementary_palette),
            ("Triadic", generate_triadic_palette),
            ("Tetradic", generate_tetradic_palette),
        ]

        for row_idx, (label, func) in enumerate(palette_funcs):
            # Afișează titlul paletei
            title_label = ctk.CTkLabel(
                self.palette_frame,
                text=label,
                anchor="w",
                font=ctk.CTkFont(weight="bold", size=16)
            )
            title_label.grid(row=row_idx, column=0, padx=(10, 20), pady=5, sticky="w")

            # Generează culorile
            colors = func(self.base_color, self.num_colors) if label == "Analog" else func(self.base_color)

            for col_idx, color in enumerate(colors):
                swatch = ctk.CTkLabel(
                    self.palette_frame,
                    text=color,
                    fg_color=color,
                    text_color=get_text_color(color),
                    height=80,
                    corner_radius=12
                )
                swatch.grid(row=row_idx, column=col_idx + 1, padx=5, pady=5, sticky="nsew")  # +1 pt. a lăsa loc titlului
                swatch.bind("<Button-1>", lambda e, c=color, w=swatch: self.copy_to_clipboard(c, w))

            # Flexibilitate la scalare
            for i in range(len(colors) + 1):
                self.palette_frame.columnconfigure(i, weight=1)
   
    def export_palettes(self):
        palettes = {
            "Analog": generate_analog_palette(self.base_color, self.num_colors),
            "Complementary": generate_complementary_palette(self.base_color),
            "Split Complementary": generate_split_complementary_palette(self.base_color),
            "Triadic": generate_triadic_palette(self.base_color),
            "Tetradic": generate_tetradic_palette(self.base_color),
        }

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("JSON Files", "*.json"), ("CSV Files", "*.csv")],
            title="Save Palette"
        )

        if not file_path:
            return

        if file_path.endswith(".txt"):
            with open(file_path, "w") as file:
                for name, colors in palettes.items():
                    file.write(f"{name} Palette:\n")
                    for color in colors:
                        file.write(f"{color}\n")
                    file.write("\n")
        elif file_path.endswith(".json"):
            with open(file_path, "w") as file:
                json.dump(palettes, file, indent=4)
        elif file_path.endswith(".csv"):
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                for name, colors in palettes.items():
                    writer.writerow([name])
                    for color in colors:
                        writer.writerow([color])
                    writer.writerow([])

if __name__ == "__main__":
    app = ColorApp()
    app.mainloop()
