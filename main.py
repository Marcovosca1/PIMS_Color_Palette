import customtkinter as ctk
from CTkColorPicker import *
import random
from colors import *
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ColorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Palette Generator")
        self.geometry("1920x1080")
        self.configure(padx=20, pady=20)

        # Setări culoare de bază
        self.base_color = "#FFDFA9"
        self.num_colors = 5
        self.num_palettes = 5

        # UI Elemente
        self.color_display = ctk.CTkLabel(self, text=self.base_color, width=100, height=100, fg_color=self.base_color, text_color=get_text_color(self.base_color), corner_radius=12)
        self.color_display.grid(row=0, column=0, padx=20, pady=10, sticky="w")

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

            # Flexibilitate la scalare
            for i in range(len(colors) + 1):
                self.palette_frame.columnconfigure(i, weight=1)
   


if __name__ == "__main__":
    app = ColorApp()
    app.mainloop()
