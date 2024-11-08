import os
import time

import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from pdf2image import convert_from_path

from bot_start import logger
from utils.aiogram_helper import clear_directory
from utils.gpt import gpt_get_photo
from utils.replicate_api import replicate_func


async def convert_pdf(user_id, pdf_path):
    images = convert_from_path(f'files/{user_id}/{pdf_path}')
    files = []
    for i, image in enumerate(images):
        image.save(f'files/{user_id}/photo_{i}.jpg', 'JPEG')
        replicate_response = await replicate_func(f'files/{user_id}/photo_{i}.jpg')
        response = await gpt_get_photo(f'files/{user_id}/photo_{i}.jpg', replicate_response)
        for resp in response:
            files.append(resp)
        os.remove(f'files/{user_id}/photo_{i}.jpg')
    os.remove(f'files/{user_id}/{pdf_path}')
    return files


async def add_to_sheet(name_file, data):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "root/bot_pdf/praxis-road-437208-v7-403538e0a460.json",
        scope)
    client = gspread.authorize(credentials)
    sheet = client.create(name_file)
    worksheet = sheet.get_worksheet(0)
    sheet.share('', perm_type='anyone', role='writer')
    link = sheet.url
    headers = [
        "Артикул или модель", "Название товара на русском", "Пол",
        "Качественные характеристики (материалы, область применения, СОСТАВ, УПАКОВКА)",
        "код ТНВЭД", "Кол-во, ШТУК", "HAWB", "ОБЩИЙ ВЕС, нетто в кг", "ОБЩИЙ ВЕС, брутто в кг", "кол-во мест",
        "Производитель", "Страна производства", "Торговая марка"
    ]
    worksheet.append_row(headers)
    column_range = 'A1:M1'
    format_cell_range(worksheet, column_range, CellFormat(
        backgroundColor=Color(40, 49, 78),
        textFormat=TextFormat(bold=True),
        horizontalAlignment='CENTER',
        verticalAlignment='MIDDLE',
    ))
    cell_range = 'A2:M100'
    format_cell_range(worksheet, cell_range, CellFormat(
        horizontalAlignment='CENTER',
        verticalAlignment='MIDDLE',
        wrapStrategy='WRAP'
    ))
    worksheet.format('A1:M1', {'wrapStrategy': 'WRAP'})
    set_column_width(worksheet, 'A', 115)
    set_column_width(worksheet, 'B', 205)
    set_column_width(worksheet, 'C', 65)
    set_column_width(worksheet, 'D', 325)
    set_column_width(worksheet, 'E', 125)
    set_column_width(worksheet, 'F', 60)
    set_column_width(worksheet, 'G', 100)
    set_column_width(worksheet, 'H', 60)
    set_column_width(worksheet, 'I', 60)
    set_column_width(worksheet, 'J', 70)
    set_column_width(worksheet, 'K', 150)
    set_column_width(worksheet, 'L', 130)
    set_column_width(worksheet, 'M', 355)
    # Заполнение таблицы данными
    logger.info('add to sheet started')
    print(data)
    for item in data:
        if not item.get('status'):
            row = [
                item.get("Артикул"), item.get("Название товара на русском"), item.get("Пол"),
                item.get("Качественные характеристики"),
                item.get("код ТНВЭД"), item.get("Кол-во, ШТУК"), '',
                '', '', '',
                item.get("Производитель"), item.get("Страна производства"), item.get("Торговая марка")
            ]

            # row = [
            #     item["Артикул"], item["Название товара на русском"], item["Пол"], item["Качественные характеристики"],
            #     item["код ТНВЭД"], item["Кол-во, ШТУК"], '',
            #     '', '', '',
            #     item["Производитель"], item["Страна производства"], item["Торговая марка"]
            # ]
            try:
                worksheet.append_row(row)
            except gspread.exceptions.APIError as e:
                if 'Quota exceeded' in str(e):
                    print("Quota exceeded. Wait 60 seconds...")
                    time.sleep(61)
                else:
                    raise
        else:
            print('Пустой файл')

    logger.info('add to sheet finished')
    return f'{link};{name_file}'


async def convert_to_sheet(user_id, pdf_path, names):
    link_array = []
    for i, pdf in enumerate(pdf_path):
        try:
            json_array = await convert_pdf(user_id, pdf)
        except Exception as _ex:
            logger.error(f'convert error --> {_ex}')
            return None
        try:
            link = await add_to_sheet(names[i], json_array)
        except Exception as _ex:
            logger.error(f'add to sheet error --> {_ex}')
            return None
        link_array.append(link)
    return link_array
