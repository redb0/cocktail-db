"""Модуль вспомогательных функций."""

from io import BytesIO
from pathlib import Path

from fastapi import UploadFile
from PIL import Image

ALLOWED_EXTENSIONS = {"jpg"}
MAX_FILE_SIZE_MB = 5 * 1024 * 1024  # 5 MB
MIN_SIZE_PX = 24
MAX_SIZE_PX = 128


async def validate_file_extensions(file_: UploadFile) -> None:
    """Валидация расширения файла."""
    if (
        file_.filename
        and Path(file_.filename).suffix.lower().lstrip(".") not in ALLOWED_EXTENSIONS
    ):
        extensions = ", ".join(ALLOWED_EXTENSIONS)
        msg = f"Недопустимое расширение файла. Разрешены только - {extensions}"
        raise ValueError(msg)


async def validate_file_size(file_: UploadFile) -> None:
    """Валидация размера файла."""
    file_data = await file_.read()
    await file_.seek(0)
    file_size = len(file_data)
    if file_size > MAX_FILE_SIZE_MB:
        msg = f"Размер файла превышает допустимый предел в {MAX_FILE_SIZE_MB} MB"
        raise ValueError(msg)


async def validate_image_size(file_: UploadFile) -> None:
    """Валидация размера картинки."""
    file_data = await file_.read()
    await file_.seek(0)
    with BytesIO(file_data) as image_file, Image.open(image_file) as image:
        width, height = image.size
        is_not_square = width != height
        is_lt_min_size = width < MIN_SIZE_PX or height < MIN_SIZE_PX
        is_gt_max_size = width > MAX_SIZE_PX or height > MAX_SIZE_PX
        if is_not_square or is_lt_min_size or is_gt_max_size:
            msg = (
                "Неподходящий размер аватара. Он должен быть квадратным "
                f"и в пределах от {MIN_SIZE_PX}х{MIN_SIZE_PX} до {MAX_SIZE_PX}х{MAX_SIZE_PX}"
            )
            raise ValueError(msg)


async def validate_image(file_: UploadFile) -> None:
    """Валидация картинки."""
    validators = [
        validate_file_extensions,
        validate_file_size,
        validate_image_size,
    ]

    for validator in validators:
        await validator(file_)


def convert_to_list_int(string: str) -> list[int]:
    if not string:
        return []
    return list(map(int, string.split(",")))
