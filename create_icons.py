#!/usr/bin/env python3
"""
Script to create app icons for the SHW Reader application.
Creates a simple but professional icon with audio wave symbols.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Create a simple but professional app icon."""
    
    # Create a 1024x1024 image (standard app icon size)
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background gradient (dark blue to lighter blue)
    for y in range(size):
        alpha = 255
        red = int(20 + (y / size) * 40)      # 20 to 60
        green = int(40 + (y / size) * 80)    # 40 to 120  
        blue = int(80 + (y / size) * 120)    # 80 to 200
        color = (red, green, blue, alpha)
        draw.line([(0, y), (size, y)], fill=color)
    
    # Draw rounded rectangle background
    margin = 80
    corner_radius = 120
    rect_coords = [margin, margin, size - margin, size - margin]
    draw.rounded_rectangle(rect_coords, radius=corner_radius, fill=(15, 30, 60, 240))
    
    # Draw audio wave symbols
    center_x, center_y = size // 2, size // 2
    
    # Main waveform lines
    wave_color = (100, 200, 255, 255)  # Light blue
    line_width = 12
    
    # Draw several vertical lines of different heights (audio waveform)
    bar_width = 20
    spacing = 35
    num_bars = 12
    start_x = center_x - (num_bars * spacing) // 2
    
    heights = [0.2, 0.6, 0.9, 0.4, 0.8, 1.0, 0.7, 0.5, 0.9, 0.3, 0.6, 0.2]
    
    for i in range(num_bars):
        x = start_x + i * spacing
        max_height = 300
        bar_height = int(heights[i] * max_height)
        
        # Draw bar
        top_y = center_y - bar_height // 2
        bottom_y = center_y + bar_height // 2
        
        draw.rounded_rectangle(
            [x - bar_width//2, top_y, x + bar_width//2, bottom_y],
            radius=bar_width//4,
            fill=wave_color
        )
    
    # Add wireless signal icons (small circles)
    signal_color = (255, 200, 100, 200)  # Orange
    
    # Top right wireless symbol
    wireless_x = center_x + 280
    wireless_y = center_y - 200
    
    for i in range(3):
        radius = 20 + i * 15
        draw.ellipse(
            [wireless_x - radius, wireless_y - radius, wireless_x + radius, wireless_y + radius],
            outline=signal_color,
            width=8
        )
    
    # Central dot
    draw.ellipse(
        [wireless_x - 8, wireless_y - 8, wireless_x + 8, wireless_y + 8],
        fill=signal_color
    )
    
    # Add "SHW" text at the bottom
    try:
        # Try to use a system font
        font_size = 120
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "SHW"
    text_color = (255, 255, 255, 200)
    
    # Get text dimensions for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = center_x - text_width // 2
    text_y = center_y + 200
    
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    return img

def save_icon_sizes(base_image):
    """Save icon in multiple sizes for macOS app."""
    
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # Standard macOS icon sizes
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # Save PNG version
    base_image.save("assets/icon.png", "PNG")
    print("✓ Created assets/icon.png")
    
    # Create iconset directory for .icns creation
    iconset_dir = "assets/icon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)
    
    # Save all sizes for iconset
    for size in sizes:
        resized = base_image.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f"{iconset_dir}/icon_{size}x{size}.png")
        
        # Also create @2x versions for retina
        if size <= 512:  # Don't create @2x for 1024
            resized.save(f"{iconset_dir}/icon_{size}x{size}@2x.png")
    
    print(f"✓ Created iconset in {iconset_dir}")
    
    # Convert to .icns if iconutil is available (macOS)
    try:
        import subprocess
        result = subprocess.run(
            ["iconutil", "-c", "icns", iconset_dir, "-o", "assets/icon.icns"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Created assets/icon.icns")
            
            # Clean up iconset directory
            import shutil
            shutil.rmtree(iconset_dir)
            print("✓ Cleaned up temporary iconset")
        else:
            print(f"⚠ Could not create .icns file: {result.stderr}")
            
    except Exception as e:
        print(f"⚠ Could not create .icns file: {e}")
        print("  You can manually run: iconutil -c icns assets/icon.iconset -o assets/icon.icns")

if __name__ == "__main__":
    print("Creating SHW Reader app icon...")
    
    try:
        # Create the base icon
        icon = create_app_icon()
        
        # Save in multiple formats and sizes
        save_icon_sizes(icon)
        
        print("\n🎉 App icon created successfully!")
        print("Files created:")
        print("  - assets/icon.png (main PNG icon)")
        print("  - assets/icon.icns (macOS app icon)")
        
    except ImportError:
        print("❌ Error: PIL (Pillow) is required to create icons.")
        print("Install it with: pip3 install Pillow")
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
