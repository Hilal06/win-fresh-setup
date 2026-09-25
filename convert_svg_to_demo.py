import os
import sys
import re
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEMO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")

# Color palette (Catppuccin Mocha / Rich Terminal)
BG_COLOR = (30, 30, 46)          # #1e1e2e
BAR_COLOR = (24, 24, 37)         # #181825
TEXT_COLOR = (205, 214, 244)     # #cdd6f4
GREEN_COLOR = (166, 227, 161)    # #a6e3a1
CYAN_COLOR = (137, 220, 235)     # #89dceb
YELLOW_COLOR = (249, 226, 175)   # #f9e2af
MAGENTA_COLOR = (203, 166, 247)  # #cba6f7
RED_COLOR = (243, 139, 168)      # #f38ba8
DIM_COLOR = (108, 112, 134)      # #6c7086

# Try loading standard Windows Monospace fonts (Consolas / Lucida Console / Courier New)
FONT_PATHS = [
    "C:\\Windows\\Fonts\\consola.ttf",
    "C:\\Windows\\Fonts\\lucon.ttf",
    "C:\\Windows\\Fonts\\cour.ttf"
]
font_path = "arial.ttf"
for p in FONT_PATHS:
    if os.path.exists(p):
        font_path = p
        break

FONT_SIZE = 15
font = ImageFont.truetype(font_path, FONT_SIZE)
font_bold = ImageFont.truetype(font_path, FONT_SIZE)

def parse_svg_texts(svg_filepath):
    """Extract line contents and text elements from Rich generated SVG."""
    with open(svg_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find viewBox or dimensions
    viewbox = re.search(r'viewBox="0 0 (\d+) ([\d.]+)"', content)
    width = int(viewbox.group(1)) if viewbox else 1280
    height = int(float(viewbox.group(2))) if viewbox else 800

    # Extract all text blocks
    # <text class="..." x="..." y="..." textLength="...">TEXT</text>
    # or inside spans
    text_pattern = re.compile(r'<text[^>]*y="([\d.]+)"[^>]*>(.*?)</text>', re.DOTALL)
    
    lines_by_y = {}
    for match in text_pattern.finditer(content):
        y = float(match.group(1))
        inner_html = match.group(2)
        
        # Extract spans or raw text
        spans = re.findall(r'<tspan[^>]*class="([^"]*)"[^>]*>([^<]*)</tspan>|([^<]+)', inner_html)
        line_elements = []
        for s in spans:
            cls = s[0]
            txt = s[1] if s[1] else s[2]
            if txt:
                line_elements.append((cls, txt))
        
        # Group by approx line
        line_key = round(y / 24.0) * 24
        if line_key not in lines_by_y:
            lines_by_y[line_key] = []
        lines_by_y[line_key].extend(line_elements)

    return width, height, lines_by_y

def render_svg_to_png(svg_filepath, png_filepath):
    width, height, lines_by_y = parse_svg_texts(svg_filepath)
    width = max(width, 1200)
    height = max(height, 650)
    
    img = Image.new("RGBA", (width + 60, height + 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded terminal window
    x0, y0, x1, y1 = 20, 20, width + 40, height + 40
    radius = 12
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=BG_COLOR)
    
    # Title bar
    draw.rounded_rectangle([x0, y0, x1, y0 + 38], radius=radius, fill=BAR_COLOR)
    draw.rectangle([x0, y0 + 26, x1, y0 + 38], fill=BAR_COLOR)
    
    # Window controls (macOS / Colorful terminal style)
    draw.ellipse([x0 + 16, y0 + 12, x0 + 28, y0 + 24], fill=(255, 95, 86))
    draw.ellipse([x0 + 36, y0 + 12, x0 + 48, y0 + 24], fill=(255, 189, 46))
    draw.ellipse([x0 + 56, y0 + 12, x0 + 68, y0 + 24], fill=(39, 201, 63))
    
    # Title text
    title_text = os.path.basename(png_filepath).replace(".png", "")
    draw.text((x0 + width // 2 - 60, y0 + 10), title_text, fill=DIM_COLOR, font=font)

    # Render lines from SVG
    start_y = y0 + 55
    sorted_y = sorted(lines_by_y.keys())
    
    for y_val in sorted_y:
        elements = lines_by_y[y_val]
        cur_x = x0 + 25
        cur_y = start_y + (y_val - sorted_y[0] if sorted_y else 0)
        
        for cls, txt in elements:
            # Color mapping based on classes or common tokens
            color = TEXT_COLOR
            if "r1" in cls or "cyan" in cls:
                color = CYAN_COLOR
            elif "r2" in cls or "green" in cls:
                color = GREEN_COLOR
            elif "r3" in cls or "yellow" in cls or "bold" in cls:
                color = YELLOW_COLOR
            elif "r4" in cls or "magenta" in cls:
                color = MAGENTA_COLOR
            elif "r5" in cls or "red" in cls:
                color = RED_COLOR
            elif "dim" in cls or "r6" in cls:
                color = DIM_COLOR
                
            # If text matches common ANSI keywords
            if "[X]" in txt or "PASSED" in txt or "Applied" in txt or "Reverted" in txt:
                color = GREEN_COLOR
            elif "FAILED" in txt or "[!]" in txt:
                color = RED_COLOR
            elif "❯" in txt or "===" in txt:
                color = YELLOW_COLOR

            draw.text((cur_x, cur_y), txt, fill=color, font=font)
            bbox = font.getbbox(txt)
            txt_width = bbox[2] - bbox[0]
            cur_x += txt_width

    img.save(png_filepath, "PNG")
    print(f"[✓] Converted {os.path.basename(svg_filepath)} -> {os.path.basename(png_filepath)}")

# Convert all SVG files
svg_files = [f for f in os.listdir(DEMO_DIR) if f.endswith(".svg")]
png_list = []
for f in sorted(svg_files):
    svg_p = os.path.join(DEMO_DIR, f)
    png_p = os.path.join(DEMO_DIR, f.replace(".svg", ".png"))
    render_svg_to_png(svg_p, png_p)
    png_list.append(png_p)

# Generate animated GIF from the PNG sequence
if png_list:
    gif_frames = []
    # Target uniform size
    target_w, target_h = 1300, 750
    for p in png_list:
        frame = Image.open(p).convert("RGBA")
        # composite over dark background
        bg = Image.new("RGBA", (target_w, target_h), (20, 20, 30, 255))
        frame.thumbnail((target_w - 20, target_h - 20), Image.Resampling.LANCZOS)
        offset = ((target_w - frame.width) // 2, (target_h - frame.height) // 2)
        bg.paste(frame, offset, frame)
        gif_frames.append(bg.convert("RGB"))

    gif_path = os.path.join(DEMO_DIR, "win-fresh-setup-showcase.gif")
    # Save as animated gif with 2 seconds per frame
    gif_frames[0].save(
        gif_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=2200,
        loop=0
    )
    print(f"[✓] Animated GIF showcase successfully generated: {gif_path}")
