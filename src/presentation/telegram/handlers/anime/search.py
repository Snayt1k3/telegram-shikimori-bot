import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from src.application.enums import ShikimoriEntryType, SearchEngineEnum
from src.presentation.telegram.common import keyboards, Message, constants

from src.presentation.telegram.common.states import SearchState
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="search")
logger = logging.getLogger(__name__)


@router.message(F.text.contains(constants.SEARCH_CMD))
async def start_search(msg: types.Message, messages: Message):
    """
    Requesting from user about platform he wants to search anime
    """
    text = messages.search_message
    kb = keyboards.search_keyboard()
    await msg.answer(text=text, reply_markup=kb)


@router.callback_query(keyboards.SearchCallback.filter())
async def search_set_query(
    call: types.CallbackQuery,
    state: FSMContext,
    callback_data: keyboards.SearchCallback,
    messages: Message,
):
    """
    Starting getting data for query
    """
    await state.set_state(SearchState.query)
    await state.set_data({"engine": str(callback_data.engine)})
    await call.message.answer(messages.search_message)


@router.message(SearchState.query)
async def search(
    msg: types.Message, state: FSMContext, ioc: InteractorFactory, messages: Message
):

    try:
        data = await state.get_data()
        engine = data.get("engine")

        if engine == str(SearchEngineEnum.shikimori):
            res = await search_on_shikimori(msg.text, ioc)
            kb = keyboards.shikimori_response_kb(res)

        else:
            res = await search_on_anilibria(msg.text, ioc)
            kb = keyboards.anilibria_response_kb(res)

        text = messages.search_response_message(res.query)
        await state.clear()
        await msg.reply_photo(
            photo=types.FSInputFile(
                "src/presentation/telegram/assets/img/anime-girl-cityscape.jpg"
            ),
            caption=text,
            reply_markup=kb,
        )
    except Exception as e:
        await msg.reply("Упс, Что-то пошло не так, попробуйте еще раз.")
        logger.error(f"Error during searching titles - {e}")


async def search_on_shikimori(query: str, ioc: InteractorFactory):

    async with ioc.shikimori_search() as usecase:
        res = await usecase(query, ShikimoriEntryType.ANIME)

    return res


async def search_on_anilibria(query: str, ioc: InteractorFactory):

    async with ioc.anilibria_search() as usecase:
        res = await usecase(query)

    return res
