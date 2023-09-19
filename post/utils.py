import uuid


# 파일명이 중복되는 경우를 방지
def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return f'images/{new_filename}'
