from PIL import Image

def apply_palette(image_path, palette):
    with Image.open(image_path).convert('RGBA') as image:
        palette = [tuple(color) + (255,) for color in palette]
        new_data = []
        for pixel in image.getdata():
            if pixel[3] == 0:
                new_data.append(pixel)
            else:
                new_data.append(closest_color(palette, pixel))
        new_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
        new_image.putdata(new_data)
        new_image.save('icon2.png')

def closest_color(palette, color):
    return min(palette, key=lambda p: sum((c1 - c2) ** 2 for c1, c2 in zip(p, color)))

palette = [(142,142,142),(192,197,201), (43,43,43),(152,50,50),(208,81,81),(198,132,100),(223,152,118),(122,169,75),(124,164,56),(105,142,88),(69,99,90),(100,126,118),(132,156,148),(152,171,165),(224,228,231),(80,165,201),(108,133,195)]
apply_palette('icon.png', palette)
