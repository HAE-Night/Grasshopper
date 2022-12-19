from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import re


# 判断字符串是否含中文，有为True
def check_u(contents):
    zhmodel = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
    # zhmodel = re.compile(u'[^\u4e00-\u9fa5]')   #检查非中文
    match = zhmodel.search(contents)
    if match:
        return True
    else:
        return False


# 找到文字区域，修改背景颜色，然后填写英文
def change_photo(all_lists):
    # 拼接图片目录
    # 打开图片
    img = Image.open("F:\京东视频\翻译图片\001.jpg")
    img = img.convert("RGB")  # 把图片强制转成RGB
    # 图片宽度
    width = img.size[0]
    # 图片高度
    height = img.size[1]
    """对每个坐标区域颜色修改-背景色"""
    for i in all_lists:
        key, = i
        value, = i.values()
        lists = value
        """
        判断识别的内容是否在对照表，若无，判断是否包含中文，
        识别的纯数字符号不做处理
        """
        if check_u(key):
            words = connect_translate(key)
        else:
            continue

        """右边边界向右平移1/5高度，若识别区域右边界为图片右边界则不作平移"""
        if lists[2] != width and lists[4] != width:
            add_right_size = int((lists[7] - lists[1]) * 1 / 5)
            lists[2] += add_right_size
            lists[4] += add_right_size
        """上边界向下平移1/6高度,若识别区域上边界为图片上边界则不作平移"""
        if lists[0] != 0 and lists[3] != 0:
            down_right_size = int((lists[7] - lists[1]) * 1 / 6)
            lists[1] += down_right_size
            lists[3] += down_right_size
        """下边界向上平移1/8高度"""
        # up_right_size = int((lists[7] - lists[1]) * 1 / 10)
        # lists[5] -= up_right_size
        # lists[7] -= up_right_size
        """计算背景颜色"""
        RGB_1 = []
        RGB_2 = []
        RGB_3 = []
        for x in range(0, width):
            for y in range(0, height):
                if (x == lists[0] and lists[1] < y < lists[7]) or (y == lists[1] and lists[0] < x < lists[2]) or (
                        x == lists[2] and lists[3] < y < lists[5]) or (y == lists[5] and lists[6] < x < lists[4]):
                    # RGB_data2=(0,255,255)
                    # img.putpixel((x, y), RGB_data2)
                    """获取边框上的全部点的颜色"""
                    data = (img.getpixel((x, y)))
                    # 获取坐标颜色R值
                    RGB_1.append(data[0])
                    # 获取坐标颜色g值
                    RGB_2.append(data[1])
                    # 获取坐标颜色b值
                    RGB_3.append(data[2])
        # 按从小到大排序
        RGB_1.sort()
        RGB_2.sort()
        RGB_3.sort()
        # 取出颜色中间值
        RGB_1 = RGB_1[int(len(RGB_1) / 2)]
        RGB_2 = RGB_2[int(len(RGB_2) / 2)]
        RGB_3 = RGB_3[int(len(RGB_3) / 2)]
        # 组成最可能的背景色
        RGB_data = (RGB_1, RGB_2, RGB_3)
        """根据背景色选择文字颜色"""
        if (RGB_1 * 0.299 + RGB_2 * 0.578 + RGB_3 * 0.114) >= 192:  # 浅色
            words_colour = (0, 0, 0)  # 设置文字颜色为黑色
        else:
            words_colour = (255, 255, 255)  # 设置文字颜色为白色
        """填充颜色"""
        for x in range(0, width):
            for y in range(0, height):
                if (x >= lists[0] and y >= lists[1]) and (x <= lists[2] and y >= lists[3]) and (
                        x <= lists[4] and y <= lists[5]) and (x >= lists[6] and y <= lists[7]):
                    # pass
                    # 将该区域颜色改成背景色
                    img.putpixel((x, y), RGB_data)

        """填充文字"""
        """写字位置下调五分之一高度"""
        add_low_size = int((lists[7] - lists[1]) * 1 / 5)
        # font_size=get_font_size(lists[7] - lists[1])
        font_size = int(lists[7] - lists[1])
        """字体采用himalaya"""
        font = ImageFont.truetype("C:\Windows\Fonts\himalaya.ttf", font_size)
        # 画图
        draw = ImageDraw.Draw(img)
        draw.text((lists[0], lists[1] + add_low_size), words, words_colour, font=font)  # 设置文字位置/内容/颜色/字体
        draw = ImageDraw.Draw(img)
        # 另存图片
    img.save("F:\京东视频\翻译图片\001.jpg")  # 保存图片
    print("图片保存完成")