import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from src.presentation.telegram.common import Message
from src.presentation.telegram.common.constants import (
    MAX_SEARCH_RESPONSE_SIZE,
    TORRENT_CMD,
)
from src.presentation.telegram.common.keyboards import TorrentCallback, torrent_keyboard
from src.presentation.telegram.common.states import TorrentState
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="AnilibriaTorrentRouter")
logger = logging.getLogger(__name__)


@router.message(F.text.contains(TORRENT_CMD))
async def start_torrent(
    msg: types.Message, state: FSMContext, messages: Message
) -> None:
    await state.set_state(TorrentState.query)
    await msg.answer(messages.search_message)


@router.message(TorrentState.query)
async def torrent_list_display(
    msg: types.Message, state: FSMContext, ioc: InteractorFactory, messages: Message
) -> None:

    await state.clear()

    async with ioc.anilibria_search() as usecase:
        res = await usecase(msg.text)

    if len(res.results) > MAX_SEARCH_RESPONSE_SIZE:
        await msg.answer("Некоторые аниме не поместились, напишите поточнее")

    kb = torrent_keyboard(res.results[:MAX_SEARCH_RESPONSE_SIZE])

    await msg.answer(text=messages.torrent_list_msg, reply_markup=kb)


@router.callback_query(TorrentCallback.filter())
async def torrent_send_file(
    call: types.CallbackQuery,
    ioc: InteractorFactory,
    callback_data: TorrentCallback,
    messages: Message,
) -> None:
    try:
        async with ioc.anilibria_get_torrent() as usecase:
            res = await usecase(callback_data.id)

            for file in res:
                await call.message.reply_document(
                    document=types.URLInputFile(
                        file.url, filename=f"{file.name} {file.episodes}.torrent"
                    ),
                    caption=messages.description_torrent_file(
                        file.size, file.episodes, file.quality
                    ),
                )
    except Exception as e:
        logger.error(f"Error when getting torrent file - {e}")
        await call.message.answer(
            "Упс, произошла ошибка при получение торрент файла, попробуйте еще раз"
        )
