from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_kb_tf = InlineKeyboardMarkup()
no_btn = InlineKeyboardButton("❌", callback_data="False.reset_user")
yes_btn = InlineKeyboardButton("✔️", callback_data="True.reset_user")
inline_kb_tf.add(yes_btn, no_btn)


def cr_search_kb(anime_id):
    al_search_kb = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton('⬅', callback_data=f'back.{anime_id}.search_edit_al')
    follow_btn = InlineKeyboardButton('❤️ Подписаться', callback_data=f'follow.{anime_id}.search_edit_al')
    mark_on_shiki = InlineKeyboardButton('📌 Шикимори', callback_data=f'shikimori.{anime_id}.search_edit_al')
    get_torrent = InlineKeyboardButton('⬇ torrent', callback_data=f'torrent.{anime_id}.search_edit_al')
    al_search_kb.add(back, follow_btn).add(mark_on_shiki).add(get_torrent)
    return al_search_kb


def cr_all_follows_kb(anime_id):
    anilibria_all_follows_kb = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton('⬅', callback_data=f'back.{anime_id}.all_follows_edit')
    unfollow = InlineKeyboardButton('💔', callback_data=f'unfollow.{anime_id}.all_follows_edit')
    mark_on_shiki = InlineKeyboardButton('📌 Шикимори', callback_data=f'shikimori.{anime_id}.all_follows_edit')
    get_torrent = InlineKeyboardButton('⬇ torrent', callback_data=f'torrent.{anime_id}.all_follows_edit')
    anilibria_all_follows_kb.add(back, unfollow).add(mark_on_shiki, get_torrent)
    return anilibria_all_follows_kb


def cr_kb_by_collection(coll, target_id, page):
    kb = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⬅', callback_data=f'{coll}.{target_id}.{page}.back.anime_edit')
    update_rating = InlineKeyboardButton('✏️ Оценка', callback_data=f'{coll}.{target_id}.{page}.update.anime_edit')
    delete = InlineKeyboardButton('🗑 Удалить', callback_data=f'{coll}.{target_id}.{page}.delete.anime_edit')

    kb.add(back, update_rating)

    if coll == 'anime_watching':
        kb.add(
            InlineKeyboardButton('-1 эпизод', callback_data=f'{coll}.{target_id}.{page}.minus.anime_edit'),
            InlineKeyboardButton('+1 эпизод', callback_data=f'{coll}.{target_id}.{page}.plus.anime_edit')
        )

        kb.add(
            InlineKeyboardButton("✔️ Просмотрено", callback_data=f'{coll}.{target_id}.{page}.complete.anime_edit'),
            InlineKeyboardButton("🗑 Брошено", callback_data=f'{coll}.{target_id}.{page}.drop.anime_edit')
        )

    elif coll == 'anime_planned':
        kb.add(
            InlineKeyboardButton("✔️ Просмотрено", callback_data=f'{coll}.{target_id}.{page}.complete.anime_edit'),
            InlineKeyboardButton("🎥 Смотрю", callback_data=f'{coll}.{target_id}.{page}.watch.anime_edit')
        )

    kb.add(delete)
    return kb


def AnimeMarkEdit_Kb(anime_id):
    kb = InlineKeyboardMarkup()

    back = InlineKeyboardButton(
        '⬅',
        callback_data=f'back.{anime_id}.anime_mark_edit'
    )
    completed = InlineKeyboardButton(
        '✔️ Просмотрено',
        callback_data=f'completed.{anime_id}.anime_mark_edit'
    )
    watching = InlineKeyboardButton(
        '🎥 Смотрю',
        callback_data=f'watching.{anime_id}.anime_mark_edit'
    )
    dropped = InlineKeyboardButton(
        '🗑 Брошено',
        callback_data=f'dropped.{anime_id}.anime_mark_edit'
    )
    planned = InlineKeyboardButton(
        '📝 Запланированное',
        callback_data=f'planned.{anime_id}.anime_mark_edit'
    )
    score = InlineKeyboardButton(
        '✏️ Оценка',
        callback_data=f'score.{anime_id}.anime_mark_edit'
    )
    delete = InlineKeyboardButton(
        '🗑 Удалить',
        callback_data=f'delete.{anime_id}.anime_mark_edit'
    )

    kb.add(back, planned).add(completed, watching).add(dropped, score).add(delete)
    return kb
