from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory
os.makedirs('static/images', exist_ok=True)

# Colors
colors = {
    'blue': (26, 77, 140),      # SBI Blue
    'light-blue': (42, 110, 176),
    'gold': (253, 185, 19),
    'dark': (51, 51, 51),
    'gray': (245, 245, 245)
}

# Create hero banner images
def create_banner(filename, color, text, width=1200, height=400):
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw text
    text_width = draw.textlength(text, font=font)
    draw.text(((width - text_width) / 2, height/2 - 30), text, fill='white', font=font)
    draw.text((width/2 - 100, height/2 + 20), "State Bank of India", fill='white', font=font_small)
    
    # Save
    img.save(f'static/images/{filename}')
    print(f"Created {filename}")

# Create product icons
def create_icon(filename, color, icon_text, size=100):
    img = Image.new('RGB', (size, size), color=color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    # Draw icon representation
    draw.text((size/3, size/3), icon_text, fill='white', font=font)
    
    img.save(f'static/images/{filename}')
    print(f"Created {filename}")

# Install PIL if not available
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Installing Pillow...")
    os.system('pip install Pillow')
    from PIL import Image, ImageDraw, ImageFont

# Create all images
print("Creating images...")

# Banner images
create_banner('home_loan_banner.jpg', colors['blue'], 'Home Loans at 8.50%*')
create_banner('car_loan_banner.jpg', colors['light-blue'], 'Car Loans at 8.75%*')
create_banner('fixed_deposit_banner.jpg', colors['gold'], 'Fixed Deposits - 7.25%*')

# Logo (simple version)
logo_img = Image.new('RGB', (200, 80), color=colors['blue'])
draw = ImageDraw.Draw(logo_img)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    draw.text((20, 25), "SBI", fill='white', font=font)
except:
    draw.text((20, 25), "SBI", fill='white')
logo_img.save('static/images/sbi-logo.png')

# Icons
create_icon('savings-icon.png', colors['blue'], '💰')
create_icon('loan-icon.png', colors['light-blue'], '🏠')
create_icon('card-icon.png', colors['gold'], '💳')
create_icon('investment-icon.png', colors['dark'], '📈')

# Chat icons
chat_img = Image.new('RGB', (50, 50), color=colors['blue'])
chat_img.save('static/images/chat-icon.png')

print("\n✅ All images created in static/images/")
