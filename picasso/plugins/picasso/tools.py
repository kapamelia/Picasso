from PIL import Image, ImageDraw, ImageFont
import io
import httpx
import asyncio


def create_image_grid_with_text_bytes(image_bytes_list, descriptions, img_size=512, columns=3, padding=10, font_path="simsun.ttc", font_size=24, title="AI绘画竞技场", title_font_path="simhei.ttf", title_font_size=48):
    """
    拼接图片并在每张图片下方添加文字说明，并在大图片上方增加标题，最后返回一个大图片的bytes数组。
    
    :param image_bytes_list: 包含图片的bytes数组列表
    :param descriptions: 包含每张图片对应文字说明的列表
    :param img_size: 每张图片的大小（默认为512x512）
    :param columns: 图片排列的列数（默认为3列）
    :param padding: 图片与图片之间的间距（默认为10）
    :param font_path: 字体文件路径，支持中文显示（默认为宋体'simsun.ttc'）
    :param font_size: 文字大小（默认为24）
    :param title: 标题文字（默认为“AI绘画竞技场”）
    :param title_font_path: 标题字体路径，用于加载粗体字体（默认为'黑体simhei.ttf'）
    :param title_font_size: 标题字体大小（默认为48）
    :return: 最终拼接图片的bytes数组
    """
    # 加载字体
    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(title_font_path, title_font_size)  # 加载粗体字体

    # 计算标题高度
    title_height = title_font_size + 20  # 标题区域高度，包含一点额外的上下间距

    # 计算行数和图片网格总尺寸
    rows = (len(image_bytes_list) + columns - 1) // columns  # 根据图片数量计算行数
    text_height = font_size + 10  # 每个图片下方的文字区域高度
    total_width = columns * img_size + (columns - 1) * padding  # 总宽度
    total_height = rows * (img_size + text_height) + (rows - 1) * padding + title_height  # 总高度，包含标题高度
    
    # 创建白色背景的大图片
    result_img = Image.new("RGB", (total_width, total_height), (255, 255, 255))
    draw = ImageDraw.Draw(result_img)

    # 绘制粉色粗体标题文字在上方居中
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]  # 计算标题的宽度
    title_x = (total_width - title_width) // 2
    title_y = 10  # 标题距离顶部10像素
    pink_color = (255, 20, 147)  # 粉色
    draw.text((title_x, title_y), title, font=title_font, fill=pink_color)  # 绘制粉色粗体标题

    # 遍历图片bytes并绘制到大图上
    for i, (image_bytes, desc) in enumerate(zip(image_bytes_list, descriptions)):
        # 从bytes读取图片，并调整大小为512x512
        img = Image.open(io.BytesIO(image_bytes)).resize((img_size, img_size))  
        row, col = divmod(i, columns)  # 计算图片所在的行列
        
        # 计算每张图片左上角位置
        x = col * (img_size + padding)
        y = row * (img_size + text_height + padding) + title_height  # 注意y要加上标题的高度
        
        # 粘贴图片
        result_img.paste(img, (x, y))
        
        # 绘制文字说明，文字在图片下方居中显示
        bbox = draw.textbbox((x, y), desc, font=font)  # 获取文字的边界框
        text_width = bbox[2] - bbox[0]  # 计算文字的宽度
        text_x = x + (img_size - text_width) // 2
        text_y = y + img_size + 5  # 文字在图片下方稍微留点间距
        
        draw.text((text_x, text_y), desc, font=font, fill=(0, 0, 0))

    # 将最终结果保存到bytes数组中
    output_bytes = io.BytesIO()
    result_img.save(output_bytes, format='JPEG')  # 可以选择其他格式，例如PNG
    output_bytes.seek(0)  # 重置文件指针位置

    return output_bytes.getvalue()  # 返回拼接后的bytes数组

async def download_image(url):
    """
    异步下载图片并保存到本地文件
    :param url: 图片的URL地址
    :param filename: 保存图片的文件名
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)  # 异步发送GET请求获取图片
        response.raise_for_status()  # 检查响应状态码
        return response.content


async def download_images(urls):
    """
    异步下载多张图片并保存到本地文件
    :param urls: 图片的URL地址列表
    :param filenames: 保存图片的文件名列表
    """
    tasks = [download_image(url) for url in urls]  # 创建多个异步任务
    return await asyncio.gather(*tasks)  # 并发执行异步任务
