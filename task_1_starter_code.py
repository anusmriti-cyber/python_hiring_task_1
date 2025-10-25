!pip install pillow reportlab
import os
import random
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

SHAPES = ["rectangle", "ellipse", "triangle", "line"]

def draw_one_shape(draw, width, height):
    shape_type = random.choice(SHAPES)
    pad_w, pad_h = int(width*0.1), int(height*0.1)

    x1 = random.randint(pad_w, int(width*0.3))
    y1 = random.randint(pad_h, int(height*0.3))
    x2 = random.randint(int(width*0.7), width - pad_w)
    y2 = random.randint(int(height*0.7), height - pad_h)

    fill_color = tuple(random.randint(60,220) for _ in range(3)) + (180,)
    outline_color = tuple(random.randint(0,120) for _ in range(3)) + (255,)
    outline_width = max(2, int(min(width,height)*0.02))

    if shape_type == "rectangle":
        draw.rectangle([x1, y1, x2, y2], fill=fill_color, outline=outline_color, width=outline_width)
    elif shape_type == "ellipse":
        draw.ellipse([x1, y1, x2, y2], fill=fill_color, outline=outline_color, width=outline_width)
    elif shape_type == "triangle":
        points = [(random.randint(x1, x2), y1), (x1, y2), (x2, y2)]
        draw.polygon(points, fill=fill_color, outline=outline_color)
    elif shape_type == "line":
        draw.line([(x1, y1),(x2,y2)], fill=outline_color, width=outline_width*2)

def generate_transparent_images(output_dir="input_images", count=50, min_w=200, max_w=800, min_h=200, max_h=1000):
    os.makedirs(output_dir, exist_ok=True)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    for i in range(1, count+1):
        width = random.randint(min_w, max_w)
        height = random.randint(min_h, max_h)

        img = Image.new("RGBA", (width, height), (0,0,0,0))
        draw = ImageDraw.Draw(img, "RGBA")
        draw_one_shape(draw, width, height)

        fname = os.path.join(output_dir, f"img_{i:02d}.png")
        img.save(fname, "PNG")
    print(f"✅ Generated {count} images in '{output_dir}'.")
    
def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGBA")
    bg = Image.new("RGBA", img.size, (255,255,255,255))
    img = Image.alpha_composite(bg, img)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img.convert("RGB")

def generate_pdf(input_dir="input_images", output_pdf="output.pdf", page_size=A4, cols=3, rows=4, margin=10):
    c = canvas.Canvas(output_pdf, pagesize=page_size)
    page_width, page_height = page_size

    cell_w = (page_width - (cols+1)*margin)/cols
    cell_h = (page_height - (rows+1)*margin)/rows

    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png','.jpg','.jpeg'))]
    image_files.sort()  # optional, to keep order

    idx = 0
    total = len(image_files)

    while idx < total:
        for r in range(rows):
            for c_idx in range(cols):
                if idx >= total:
                    break
                img_path = os.path.join(input_dir, image_files[idx])
                img = preprocess_image(img_path)
                w, h = img.size

                scale = min(cell_w/w, cell_h/h)
                w_scaled, h_scaled = int(w*scale), int(h*scale)
                
                x = margin + c_idx*(cell_w + margin) + (cell_w - w_scaled)/2
                y = margin + r*(cell_h + margin) + (cell_h - h_scaled)/2

             
                c.drawImage(img_path, x, page_height - y - h_scaled, width=w_scaled, height=h_scaled)
                idx += 1
        c.showPage()  # next page
    c.save()
    print(f"✅ PDF generated: {output_pdf}")

generate_transparent_images(count=50)
generate_pdf()
generate_pdf(input_dir="input_images", output_pdf="output.pdf", page_size=A4, cols=3, rows=4, margin=10)
from google.colab import files
files.download("output.pdf")

