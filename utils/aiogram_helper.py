from typing import Optional, List, Literal

import yadisk
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, InputMediaDocument, InputMediaAnimation, InputMediaVideo

from bot_start import logger
from src.config import Tokens

yandex = yadisk.YaDisk(token=Tokens.yandex)


class SendMessage:
    def __init__(self, event, text, handler_name, state, keyboard: Optional = None):
        """
        :param event: [types.CallbackQuery,types.Message]
        :param text: str, text for sending
        :param handler_name: str, name your handler
        :param state: FSMContext
        :param keyboard: (Optional) function of your keyboard
        :return sending message for user
        """
        self.event = event
        self.text = text
        self.handler_name = handler_name
        self.state = state
        self.keyboard = keyboard

    async def custom_send(self):
        if isinstance(self.event, Message):
            if self.keyboard is not None:
                await self.message_send_message_with_kb()
            else:
                await self.message_send_message_no_kb()
        else:
            if self.keyboard is not None:
                await self.call_send_message_with_kb()
            else:
                await self.call_send_message_no_kb()

    async def message_send_message_no_kb(self):
        data = await self.state.get_data()
        try:
            msg = await data['msg'].edit_text(
                text=self.text
            )
        except (TelegramBadRequest, KeyError) as _ex:
            try:
                await data['msg'].delete()
            except KeyError:
                pass
            logger.error(f'edit msg error -> {self.handler_name} ... {_ex}')
            msg = await self.event.answer(
                text=self.text
            )
        await self.state.update_data(msg=msg)

    async def message_send_message_with_kb(self):
        data = await self.state.get_data()
        try:
            msg = await data['msg'].edit_text(
                text=self.text,
                reply_markup=await self.keyboard(),
                disable_web_page_preview=True
            )
        except (TelegramBadRequest, KeyError) as _ex:
            try:
                await data['msg'].delete()
            except KeyError:
                pass
            logger.error(f'edit msg error -> {self.handler_name} ... {_ex}')
            msg = await self.event.answer(
                text=self.text,
                reply_markup=await self.keyboard(),
                disable_web_page_preview=True
            )
        await self.state.update_data(msg=msg)

    async def call_send_message_no_kb(self):
        data = await self.state.get_data()
        try:
            msg = await data['msg'].edit_text(
                text=self.text,
                disable_web_page_preview=True
            )
        except (TelegramBadRequest, KeyError) as _ex:
            try:
                await data['msg'].delete()
            except KeyError:
                pass
            logger.error(f'edit msg error -> {self.handler_name} ... {_ex}')
            msg = await self.event.message.answer(
                text=self.text,
                disable_web_page_preview=True
            )
        await self.state.update_data(msg=msg)

    async def call_send_message_with_kb(self):
        data = await self.state.get_data()
        try:
            msg = await data['msg'].edit_text(
                text=self.text,
                reply_markup=await self.keyboard(),
                disable_web_page_preview=True
            )
        except (TelegramBadRequest, KeyError) as _ex:
            try:
                await data['msg'].delete()
            except KeyError:
                pass
            logger.error(f'edit msg error -> {self.handler_name} ... {_ex}')
            msg = await self.event.message.answer(
                text=self.text,
                reply_markup=await self.keyboard(),
                disable_web_page_preview=True
            )
        await self.state.update_data(msg=msg)


def input_media(media_type: str, media: str, caption: str):
    match media_type:
        case 'photo':
            return InputMediaPhoto(media=media, caption=caption)
        case 'document':
            return InputMediaDocument(media=media, caption=caption)
        case 'animation':
            return InputMediaAnimation(media=media, caption=caption)
        case 'video':
            return InputMediaVideo(media=media, caption=caption)


def unpack_media_group(messages: List[Message], special_format: Literal['no_caption', 'input_media'] = False):
    media_files = []
    for message in messages:
        if message.document:
            media_files.append(['document', message.document.file_id, message.html_text])
        elif message.photo:
            media_files.append(['photo', message.photo[-1].file_id, message.html_text])
        elif message.audio:
            media_files.append(['audio', message.audio.file_id, message.html_text])
        elif message.animation:
            media_files.append(['animation', message.animation.file_id, message.html_text])
        elif message.video:
            media_files.append(['video', message.video.file_id, message.html_text])
    if special_format:
        if special_format == 'no_caption':
            media_files = [[message[0], message[1]] for message in media_files]
        elif special_format == 'input_media':
            media_files = [input_media(media[0], media[1], media[2]) for media in media_files]
    return media_files


async def upload_file(file_path, yandex_path):
    logger.info(f"Start upload file to drop box")
    with open(file_path, 'rb'):
        yandex.upload(file_path, yandex_path)
    logger.info(f"File {file_path} uploaded to {yandex_path}")


async def create_shared_link(yandex_path):
    url = yandex.get_download_link(yandex_path)
    logger.info(f'link created {url}')
    return url

async def delete_file(yandex_path):
    try:
        yandex.remove(yandex_path)
        logger.info(f"File --> {yandex_path} deleted")
    except Exception as _ex:
        logger.error(f"Error delete file --> {_ex}")

async def upload_image_telegraph(local_file_path, yadisk_name):
    await upload_file(local_file_path, f'/{yadisk_name}')
    link = await create_shared_link(f'/{yadisk_name}')
    return link, f'/{yadisk_name}'
