import os
import cv2
import tqdm
from PIL import ImageFont, ImageDraw, Image
import numpy as np

IMAGES_FOLDER = 'bereals 2023'
YEAR = 2023


def add_text(frame):
    font = ImageFont.truetype('Genera Grotesk Heavy.ttf', 300)
    colour = (255, 255, 255, 255)
    frame_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(frame_pil)
    draw.text(
        (frame_pil.width / 2, frame_pil.height / 2),
        f'{YEAR}\nRECAP',
        font=font,
        fill=colour,
        align='center',
        anchor='mm',
    )
    return np.array(frame_pil)


images = sorted([img for img in os.listdir(IMAGES_FOLDER)])
frame = cv2.imread(os.path.join(IMAGES_FOLDER, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(
    f'BeReal Recap {YEAR}.mp4',
    cv2.VideoWriter_fourcc(*'mp4v'),
    60,
    (width, height),
)

print('Fast recap:')
# First fast recap with text overlay
for i, image in tqdm.tqdm(enumerate(images[::5]), total=len(images) / 5):
    video.write(add_text(cv2.imread(os.path.join(IMAGES_FOLDER, image))))

print('Black Frames')
# add 30 black frames with text
black_frame = add_text(np.zeros_like(np.array(frame)))
for _ in tqdm.tqdm(range(30)):
    video.write(black_frame)

print('Start Frames')
# add first 20 frames, where each one gets faster
for i, image in tqdm.tqdm(enumerate(images[:30]), total=30):
    frame = cv2.imread(os.path.join(IMAGES_FOLDER, image))
    for _ in range(35 - i):
        video.write(frame)

print('Main Frames')
# add the rest up to the last 30
for image in tqdm.tqdm(images[30:-30]):
    frame = cv2.imread(os.path.join(IMAGES_FOLDER, image))
    for _ in range(5):
        video.write(frame)

print('End Frames')
# add the final 30, where each one gets slower
for i, image in tqdm.tqdm(enumerate(images[-30:]), total=30):
    frame = cv2.imread(os.path.join(IMAGES_FOLDER, image))
    for _ in range(5 + i):
        video.write(frame)

video.write(black_frame)

cv2.destroyAllWindows()
video.release()
