from PIL import Image

import random

lists = [
    r"./images/1.png",
    r"./images/2.png",
    r"./images/3.png",
    r"./images/4.png",
    r"./images/5.png",
    r"./images/6.png",
    r"./images/7.png",
    r"./images/8.png",
    r"./images/9.png",
    r"./images/10.png",
]

random_img = random.choices(lists, weights=(90, 10, 10, 10, 10, 10, 10, 10, 10, 10))[0]

selected_img = Image.open(random_img)

selected_img.save('nft.png')

# final = Image.save(selected_img)

# final.save('nft.png')

# img1 = Image.open(r"./images/3.png")
# print(img1)
