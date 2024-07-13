from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.adapters.enums import SearchEngineEnum
from src.application.enums import ShikimoriEntryType
from src.presentation.telegram.common import keyboards, Message
from src.presentation.telegram.common.states import SearchState
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="search")


@router.message(lambda msg: "поиск" in msg.text.lower(), Command("Search"))
async def start_search(msg: types.Message):
    """
    Requesting from user about platform he wants to search anime
    """
    text = Message.search_message()
    kb = keyboards.search_keyboard()
    await msg.answer(text=text, reply_markup=kb)


@router.callback_query(keyboards.SearchCallback.filter())
async def search_set_query(
    call: types.CallbackQuery,
    state: FSMContext,
    callback_data: keyboards.SearchCallback,
):
    """
    Starting getting data for query
    """
    await state.set_state(SearchState.query)
    await state.update_data(engine=str(callback_data.engine))
    await call.message.answer(Message.search_message())


@router.message(SearchState.query)
async def search(msg: types.Message, state: FSMContext, ioc: InteractorFactory):
    await state.clear()

    data = await state.get_data()
    engine = data.get("engine")

    if engine == SearchEngineEnum.shikimori:
        res = await search_on_shikimori(msg.text, ioc)
        kb = keyboards.shikimori_response_kb(res)

    else:
        res = await search_on_anilibria(msg.text, ioc)
        kb = keyboards.anilibria_response_kb(res)

    text = Message.search_response_message(res.query)
    await msg.reply_photo(
        photo=types.InputFile(
            "src/presentation/telegram/assets/img/anime-girl-cityscape.jpg"
        ),
        caption=text,
        reply_markup=kb,
    )


async def search_on_shikimori(query: str, ioc: InteractorFactory):

    async with ioc.shikimori_search() as usecase:
        res = await usecase(query, ShikimoriEntryType.ANIME)

    return res


async def search_on_anilibria(query: str, ioc: InteractorFactory):

    async with ioc.anilibria_search() as usecase:
        res = await usecase(query)

    return res
