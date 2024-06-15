from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.presentation.telegram.common import Message
from src.presentation.telegram.common.keyboards.torrent import TorrentCallback
from src.presentation.telegram.common.states import TorrentState
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="torrent")


@router.message(F.text.lower() == "торрент", Command("torrent"))
async def start_torrent(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(TorrentState.query)
    await msg.answer(Message.torrent_start_msg())


@router.message(TorrentState.query)
async def torrent_list_display(msg: types.Message, state: FSMContext, ioc: InteractorFactory) -> None:

    await state.clear()

    async with ioc.anilibria_search() as usecase:
        res = await usecase(msg.text)

    # todo добавить отрисовку

@router.callback_query(TorrentCallback.filter())
async def torrent_send_file(call: types.CallbackQuery, ioc: InteractorFactory, callback_data: TorrentCallback) -> None:
    async with ioc.anilibria_get_torrent() as usecase:
        res = await usecase(callback_data.id)

    for file in res:
        await call.message.reply_document(
            document=file.url,
            caption=Message.description_torrent_file(file.size, file.episodes, file.quality)
        )

