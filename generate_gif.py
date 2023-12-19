import imageio
import os
from PIL import Image
import numpy as np

width, height = 1000, 1000

def resize_image(image_path, target_size=(width, height)):
    img = Image.open(image_path).resize(target_size[:2], Image.ANTIALIAS)
    return np.array(img)

def create_gif(image_directory, output_path, file_prefix, start_index, end_index):
    image_files = sorted([f for f in os.listdir(image_directory) if f.startswith(file_prefix) and f.endswith('.png')])

    selected_images = [os.path.join(image_directory, f) for f in image_files if start_index <= int(f[len(file_prefix):-4]) <= end_index]

    images = []

    target_size = resize_image(selected_images[0]).shape

    for image_path in selected_images:
        resized_image = resize_image(image_path, target_size)
        images.append(resized_image)

    imageio.mimsave(output_path, images, duration=3)

    print(f'GIF saved at: {output_path}')

image_directory = 'heatmaps'

output_path_win = 'win.gif'
output_path_loss = 'loss.gif'

create_gif(image_directory, output_path_win, 'win', 2, 8)

create_gif(image_directory, output_path_loss, 'loss', 2, 8)

