import os
import multiprocessing
import random

from pdf2image import convert_from_path

from utils.gpt import gpt_get_photo


class PDFProcessor:
    def __init__(self, pdf_folder, user_id):
        self.pdf_folder = pdf_folder
        self.user_id = user_id

    def process_pdf(self, pdf_file):
        images = convert_from_path(pdf_file)
        with multiprocessing.Pool(processes=4) as pool:
            results = pool.map(self.process_image, images)

        return results

    def process_image(self, image):
        response_all = []
        name = random.randint(100000,999999)
        image.save(f'files/{self.user_id}/photo_{name}.jpg', 'JPEG')
        responses = gpt_get_photo(f'files/{self.user_id}/photo_{name}.jpg')
        for response in responses:
            response_all.append(response)
        return response_all

    def run(self):
        pdf_files = [f for f in os.listdir(self.pdf_folder) if f.endswith('.pdf')]
        all_results = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.pdf_folder, pdf_file)
            results = self.process_pdf(pdf_path)
            all_results.append(results)

        return all_results

# Пример использования
# pdf_processor = PDFProcessor('/path/to/pdf/folder', 'your_openai_api_key')
# results = pdf_processor.run()
