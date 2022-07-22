from PIL import Image, ImageDraw
import os


# REF: https://blog.csdn.net/yupu56/article/details/122300218
def circle_corner(img, radii):
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 黑色方形内切白色圆形

    img = img.convert("RGBA")
    w, h = img.size

    #创建一个alpha层，存放四个圆角，使用透明度切除圆角外的图片
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)),
                (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)),
                (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)),
                (0, h - radii))  # 左下角
    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见

    # # 添加圆角边框
    # draw = ImageDraw.Draw(img)
    # draw.rounded_rectangle(img.getbbox(), outline="black", width=3, radius=radii)
    return img


if __name__ == '__main__':
    radii = 25  # 圆角大小
    src = 'logo.JPG'
    des = 'test1.png'
    print(src)
    img = Image.open(src)
    img = circle_corner(img, radii)
    img.save(des, 'png', quality=100)
