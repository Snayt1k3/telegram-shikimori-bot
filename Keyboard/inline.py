from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_kb_tf = InlineKeyboardMarkup()
no_btn = InlineKeyboardButton("No ❌", callback_data="reset_user.False")
yes_btn = InlineKeyboardButton("Yes ✔️", callback_data="reset_user.True")
inline_kb_tf.add(yes_btn, no_btn)

searching_pagination = InlineKeyboardMarkup()
next_btn1 = InlineKeyboardButton("➡", callback_data="anime_search.next")
add_to_planned_btn = InlineKeyboardButton("☑ Into Planned list", callback_data="anime_search.into_planned")
previous_btn1 = InlineKeyboardButton("⬅", callback_data="anime_search.previous")
searching_pagination.add(previous_btn1, add_to_planned_btn, next_btn1)


def cr_search_kb(anime_id):
    al_search_kb = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton('⬅ Back', callback_data=f'back.{anime_id}.search_edit_al')
    follow_btn = InlineKeyboardButton('❤️ follow', callback_data=f'follow.{anime_id}.search_edit_al')
    mark_on_shiki = InlineKeyboardButton('📌 Mark on Shikimori', callback_data=f'shikimori.{anime_id}.search_edit_al')
    get_torrent = InlineKeyboardButton('⬇ Get torrent', callback_data=f'torrent.{anime_id}.search_edit_al')
    al_search_kb.add(back, follow_btn).add(mark_on_shiki).add(get_torrent)
    return al_search_kb


def cr_all_follows_kb(anime_id):
    anilibria_all_follows_kb = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton('⬅ Back', callback_data=f'back.{anime_id}.all_follows_edit')
    unfollow = InlineKeyboardButton('💔 UnFollow', callback_data=f'unfollow.{anime_id}.all_follows_edit')
    mark_on_shiki = InlineKeyboardButton('📌 Mark on Shikimori', callback_data=f'shikimori.{anime_id}.all_follows_edit')
    get_torrent = InlineKeyboardButton('⬇ Get torrent', callback_data=f'torrent.{anime_id}.all_follows_edit')
    anilibria_all_follows_kb.add(back, unfollow).add(mark_on_shiki).add(get_torrent)
    return anilibria_all_follows_kb


def cr_kb_by_collection(coll, target_id):
    kb = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⬅ Back', callback_data=f'{coll}.0.back.{coll}_edit')
    update_rating = InlineKeyboardButton('Update Score', callback_data=f'{coll}.{target_id}.update.{coll}_edit')
    delete = InlineKeyboardButton('Delete', callback_data=f'{coll}.{target_id}.delete.anime_edit')

    kb.add(back, update_rating)

    if coll == 'anime_watching':
        kb.add(
            InlineKeyboardButton('+1', callback_data=f'{coll}.{target_id}.plus.anime_edit'),
            InlineKeyboardButton('-1', callback_data=f'{coll}.{target_id}.minus.anime_edit')
        )

        kb.add(
            InlineKeyboardButton("Into Completed", callback_data=f'{coll}.{target_id}.complete.anime_edit'),
            InlineKeyboardButton("Into Dropped", callback_data=f'{coll}.{target_id}.drop.anime_edit')
        )

    elif coll == 'anime_planned':
        kb.add(
            InlineKeyboardButton("Into Completed", callback_data=f'{coll}.{target_id}.complete.anime_edit'),
            InlineKeyboardButton("Into Watching", callback_data=f'{coll}.{target_id}.watch.anime_edit')
        )

    kb.add(delete)
    return kb
