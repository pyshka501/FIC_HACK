from PIL import Image
import numpy as np
import base64
from io import BytesIO
import cv2


def is_black_and_white_or_gray(image: Image, threshold=10) -> bool:
    """
    Пример использования функции с объектом PIL

        image_path = 'path_to_your_image.jpg'
    image = Image.open(image_path)

    if is_black_and_white_or_gray(image):
        print("Фотография черно-белая или серая")
    else:
        print("Фотография цветная")

    :param image:
    :param threshold:
    :return: bool:
    """
    # Переводим изображение в формат RGB, если оно не в этом формате
    rgb_image = image.convert('RGB')

    # Преобразуем изображение в numpy массив
    np_image = np.array(rgb_image)

    # Вычисляем разницу между каналами
    r_g_diff = np.abs(np_image[:, :, 0] - np_image[:, :, 1])
    r_b_diff = np.abs(np_image[:, :, 0] - np_image[:, :, 2])
    g_b_diff = np.abs(np_image[:, :, 1] - np_image[:, :, 2])

    # Считаем пиксели, которые не отличаются значительно по каналам RGB
    is_gray = (r_g_diff < threshold) & (r_b_diff < threshold) & (g_b_diff < threshold)

    # Если большая часть пикселей серые или черно-белые, возвращаем True
    return np.mean(is_gray) > 0.99


def pil_to_base64(image: Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


def base64_to_pil(base64_str: str) -> Image:
    img_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(img_data))
    return image


def pil_to_cv2(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def cv2_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

