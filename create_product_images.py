"""
Create simple product images for the e-commerce bot
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory
os.makedirs("bot/images", exist_ok=True)

products = [
    {"id": "PROD001", "name": "Laptop", "color": (52, 73, 94), "emoji": "💻"},
    {"id": "PROD002", "name": "Smartphone", "color": (41, 128, 185), "emoji": "📱"},
    {"id": "PROD003", "name": "Headphones", "color": (155, 89, 182), "emoji": "🎧"},
    {"id": "PROD004", "name": "Tablet", "color": (26, 188, 156), "emoji": "📱"},
    {"id": "PROD005", "name": "Smartwatch", "color": (230, 126, 34), "emoji": "⌚"},
]

for product in products:
    # Create image
    img = Image.new('RGB', (400, 300), color=product["color"])
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic font if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        emoji_font = ImageFont.truetype("arial.ttf", 100)
    except:
        title_font = ImageFont.load_default()
        emoji_font = ImageFont.load_default()
    
    # Draw emoji
    draw.text((150, 50), product["emoji"], fill=(255, 255, 255), font=emoji_font)
    
    # Draw product name
    draw.text((50, 180), product["name"], fill=(255, 255, 255), font=title_font)
    
    # Save image
    img.save(f"bot/images/{product['id']}.png")
    print(f"Created {product['id']}.png")

print("\n✅ All product images created successfully!")
print("Images saved in bot/images/")
