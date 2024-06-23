import os
from PIL import Image

# 폴더 내 모든 이미지 파일을 순회
for root, dirs, files in os.walk('D:\\project\\study-crolling\\data\\참외 사진'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext.lower() in ['.jpg', '.png', '.gif']:
            # 이미지 파일 열기
            im = Image.open(os.path.join(root, file)).convert('RGB')
            
            # 이미지 크기 구하기
            width, height = im.size

            # 중앙을 기준으로 100x100 크기로 자를 좌표 계산
            left = (width - 100) // 2
            top = (height - 100) // 2
            right = left + 100
            bottom = top + 100

            # 이미지 자르기
            crop_image = im.crop((left, top, right, bottom))
            
            # 자른 이미지 저장
            output_path = os.path.join('D:\\project\\study-crolling\\data\\images\\chamwea', 'cropped_Img' + str(idx) + '.jpg')
            crop_image.save(output_path)

print("이미지 자르기가 완료되었습니다.")
