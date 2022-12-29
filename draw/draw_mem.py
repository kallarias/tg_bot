# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont, ImageColor


class PostCardMaker:

    def __init__(self, mem, template=None, font_path=None):
        self.mem = mem
        self.template = "C:\\Python\\Projects\\tg_bot\\draw\\yzbg.jpg" if template is None else template
        if font_path is None:
            self.font_path = "C:\\Python\\Projects\\tg_bot\\draw\\ofont.ru_Impact.ttf"
        else:
            self.font_path = font_path

    def make(self, resize=False, out_path=None):
        im = Image.open(self.template)
        if resize:
            w, h = im.size
            im = im.resize((w // 2, h // 2))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(self.font_path, size=46)
        w1, h1 = font.getsize(self.mem)
        y = im.size[1] - h1 - 10
        x = im.size[0] // 2 - (w1 // 2)
        message = self.mem
        draw.multiline_text((x, y), message, font=font)  # , fill=ImageColor.colormap['red'])

        # im.show()
        out_path = out_path if out_path else f'probe.jpg'
        im.save(f'draw//pictures//{out_path}')
        # print(f'Post card saved az {out_path}')
