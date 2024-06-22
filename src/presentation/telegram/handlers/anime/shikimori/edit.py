from aiogram import types, Router

router = Router(name="shikimori_edit")


@router.callback_query()
async def edit_episode(call: types.CallbackQuery):
    pass


@router.callback_query()
async def pagination_episode(call: types.CallbackQuery):
    pass


@router.callback_query()
async def edit_status(call: types.CallbackQuery):
    pass


@router.callback_query()
async def delete_title(call: types.CallbackQuery):
    pass
