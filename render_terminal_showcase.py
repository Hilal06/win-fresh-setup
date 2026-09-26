import os
import sys
from html2image import Html2Image
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEMO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")
hti = Html2Image(output_path=DEMO_DIR)

# Prefer Edge or Chrome
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

if os.path.exists(edge_path):
    hti.browser.executable = edge_path
elif os.path.exists(chrome_path):
    hti.browser.executable = chrome_path

# Custom flags to allow headless local file and SVG rendering
hti.browser.flags = [
    "--no-sandbox",
    "--disable-gpu",
    "--hide-scrollbars",
    "--force-device-scale-factor=1",
    "--default-background-color=00000000"
]

svg_files = [f for f in os.listdir(DEMO_DIR) if f.endswith(".svg")]
png_list = []

for svg_name in sorted(svg_files):
    svg_path = os.path.join(DEMO_DIR, svg_name)
    png_name = svg_name.replace(".svg", ".png")
    png_path = os.path.join(DEMO_DIR, png_name)
    
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 24px;
    background: #181825;
    display: flex;
    justify-content: center;
    align-items: center;
  }}
  svg {{
    max-width: 100%;
    height: auto;
    filter: drop-shadow(0 15px 30px rgba(0,0,0,0.5));
  }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    
    hti.screenshot(html_str=html, save_as=png_name, size=(1540, 860))
    if os.path.exists(png_path):
        print(f"[✓] Rendered high-res terminal screenshot: {png_name} ({os.path.getsize(png_path)} bytes)")
        png_list.append(png_path)

# Generate GIF animation from rendered pixel-perfect screenshots
if png_list:
    frames = []
    for p in png_list:
        im = Image.open(p).convert("RGB")
        frames.append(im)

    gif_path = os.path.join(DEMO_DIR, "win-fresh-setup-showcase.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=2200,
        loop=0
    )
    print(f"[✓] High-res Animated Showcase GIF created: {gif_path} ({os.path.getsize(gif_path)} bytes)")
