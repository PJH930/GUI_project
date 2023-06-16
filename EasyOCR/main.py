
import easyocr
from PIL import Image, ImageDraw, ImageFont

if __name__ == '__main__':

    # easyocr.download("en")
    # easyocr.download(["ko", "ja"])

    # 이미지문자인식
    reader = easyocr.Reader(['ko', 'en'])
    result = reader.readtext('*.png')
    for res in result:
        print(res[0:2])

    # # 텍스트문자인식
    # reader = easyocr.Reader(['en'])
    # result = reader.readtext('')
    # for res in result:
    #     print(res[1])














    # # 이미지 파일 경로
    # image_path = 'img_0.png'
    #
    # # EasyOCR 인식
    # reader = easyocr.Reader(['en'])
    # result = reader.readtext(image_path)
    #
    # # 이미지 불러오기
    # image = Image.open(image_path)
    #
    # # 그림 그리기 준비
    # draw = ImageDraw.Draw(image)
    #
    # # 결과를 이용하여 그림 그리기
    # for detection in result:
    #     bbox = detection[0]  # 인식된 영역의 바운딩 박스 좌표
    #     text = detection[1]  # 인식된 텍스트
    #     draw.rectangle(bbox[0:], outline='red', width=2)
    #     draw.text((bbox[0], bbox[1] - 20), text, fill='red')
    #
    # # 그림 파일 저장
    # output_image_path = 'output.jpg'
    # image.save(output_image_path)
