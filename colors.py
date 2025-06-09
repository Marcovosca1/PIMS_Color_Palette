import colorsys

# ===== Color Utility Functions =====

def get_text_color(bg_hex):
    bg_hex = bg_hex.lstrip('#')
    r, g, b = int(bg_hex[0:2], 16), int(bg_hex[2:4], 16), int(bg_hex[4:6], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "black" if brightness > 128 else "white"

# ===== Color Conversion Functions =====

def hex_to_hsl(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h*360, s*100, l*100

def hsl_to_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0)
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

# ===== Color Palette Generation Functions =====

def generate_monochromatic_palette(base_hex, num_colors=5):
    h, s, l = hex_to_hsl(base_hex)
    palette = []
    step = 100 / (num_colors - 1)
    for i in range(num_colors):
        new_l = max(0, min(100, l + (i - (num_colors // 2)) * step))
        palette.append(hsl_to_hex(h, s, new_l))
    return palette

def generate_analog_palette(base_hex, num_colors=5, step=30):
    h, s, l = hex_to_hsl(base_hex)
    palette = []
    offset = step * (num_colors // 2)
    for i in range(num_colors):
        new_hue = (h - offset + i * step) % 360
        palette.append(hsl_to_hex(new_hue, s, l))
    return palette

def generate_complementary_palette(base_hex):
    h, s, l = hex_to_hsl(base_hex)
    new_hue = (h + 180) % 360
    return [base_hex, hsl_to_hex(new_hue, s, l)]

def generate_split_complementary_palette(base_hex):
    h, s, l = hex_to_hsl(base_hex)
    new_hue1 = (h + 150) % 360
    new_hue2 = (h + 210) % 360
    return [base_hex, hsl_to_hex(new_hue1, s, l), hsl_to_hex(new_hue2, s, l)]

def generate_triadic_palette(base_hex):
    h, s, l = hex_to_hsl(base_hex)
    new_hue1 = (h + 120) % 360
    new_hue2 = (h + 240) % 360
    return [base_hex, hsl_to_hex(new_hue1, s, l), hsl_to_hex(new_hue2, s, l)]

def generate_tetradic_palette(base_hex):
    h, s, l = hex_to_hsl(base_hex)
    new_hue1 = (h + 90) % 360
    new_hue2 = (h + 180) % 360
    new_hue3 = (h + 270) % 360
    return [base_hex, hsl_to_hex(new_hue1, s, l), hsl_to_hex(new_hue2, s, l), hsl_to_hex(new_hue3, s, l)]
