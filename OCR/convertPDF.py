import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np


class PDFToTextConverter:
    def __init__(self, pdf_path, output_file):
        """
        Инициализация объекта конвертера PDF в текст.

        Args:
            pdf_path (str): Путь к PDF-файлу.
            output_file (str): Имя файла, в который будет сохранен текст.
        """
        self.pdf_path = pdf_path
        self.output_file = output_file

    def convert_to_text(self):
        """
        Извлечение текста из PDF-файла и сохранение его в текстовом файле.

        Returns:
            None
        """
        pages = convert_from_path(self.pdf_path, poppler_path='./poppler-23.08.0/Library/bin')
        with open(self.output_file, 'w', encoding='utf-8') as output:
            for page in pages:
                imgcv = cv2.cvtColor(np.asarray(page), cv2.COLOR_BGR2RGB)
                text = pytesseract.image_to_string(imgcv, lang='rus')
                output.write(text)
                output.write('\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('output_file', help='Name of the output text file')
    args = parser.parse_args()

    converter = PDFToTextConverter(args.pdf_path, args.output_file)
    converter.convert_to_text()
