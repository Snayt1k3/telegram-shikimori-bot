from logging import getLogger

from aiogram import Router, F, types

from src.application.exceptions.user import FollowsIsEmpty
from src.presentation.telegram.common import constants
from src.presentation.telegram.interactor_factory import InteractorFactory
from src.presentation.telegram.common.keyboards.user import follows
from src.presentation.telegram.common.message import Message

router = Router(name="UserFollows")
logger = getLogger(__name__)


@router.message(F.text.contains(constants.FOLLOW_LIST_CMD))
async def follow_list(msg: types.Message, ioc: InteractorFactory) -> None:
    try:
        async with ioc.all_follows() as usecase:
            res = await usecase(msg.from_user.id)

        kb = follows.follows_keyboard(res, 0)

        await msg.reply_photo(
            caption=Message.follows_msg(len(res.follows), 0),
            reply_markup=kb,
            photo=types.FSInputFile(
                "src/presentation/telegram/assets/img/anime-girl-alone.jpg"
            ),
        )

    except FollowsIsEmpty:
        await msg.answer("Ваш список пуст, чтобы посмотреть, добавьте аниме в подписки")

    except Exception as e:
        logger.error(f"Error occurred while getting follow list - {e}")
        await msg.answer(
            "Упс, произошла ошибка при получение вашего списка, попробуйте еще раз"
        )


@router.callback_query(follows.FollowListPagination.filter())
async def follow_list_pagination(
    call: types.CallbackQuery,
    ioc: InteractorFactory,
    callback_data: follows.FollowListPagination,
) -> None:
    try:
        async with ioc.all_follows() as usecase:
            res = await usecase(call.from_user.id)

        kb = follows.follows_keyboard(res, callback_data.offset)

        await call.message.edit_text(
            text=Message.follows_msg(len(res.follows), callback_data.offset),
            reply_markup=kb,
        )

    except Exception as e:
        logger.error(f"Error occurred while getting follow list - {e}")
        await call.message.answer(
            "Упс, произошла ошибка при получение вашего списка, попробуйте еще раз"
        )


@router.callback_query(follows.FollowItem.filter())
async def follow_item(
    call: types.CallbackQuery, ioc: InteractorFactory, callback_data: follows.FollowItem
) -> None:

    async with ioc.get_anilibria_title() as usecase:
        res = await usecase(callback_data.id)

    msg = Message.follow_item(res)
    kb = follows.follow_item_keyboard(callback_data.id, callback_data.offset)

    await call.message.edit_media(media=types.InputMediaPhoto(media=res.img))
    await call.message.edit_caption(
        caption=msg,
        reply_markup=kb,
    )


@router.callback_query(follows.Follow.filter())
async def follow(
    call: types.CallbackQuery, ioc: InteractorFactory, callback_data: follows.Follow
) -> None:
    try:

        async with ioc.add_follow() as usecase:
            await usecase(call.from_user.id, callback_data.id)
        await call.answer("Успех")

    except Exception as e:
        logger.error(f"Error occurred while add anime to list - {e}")
        await call.message.answer(
            "Упс, произошла ошибка при добавление в список, попробуйте еще раз"
        )


@router.callback_query(follows.UnFollow.filter())
async def unfollow(
    call: types.CallbackQuery, ioc: InteractorFactory, callback_data: follows.UnFollow
) -> None:
    try:
        async with ioc.remove_follow() as usecase:
            await usecase(call.from_user.id, callback_data.id)
        await call.answer("Успех")
    except Exception as e:
        logger.error(f"Error occurred while add anime to list - {e}")
        await call.message.answer(
            "Упс, произошла ошибка при удаления из списка, попробуйте еще раз"
        )
