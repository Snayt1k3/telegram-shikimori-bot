from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_kb_tf = InlineKeyboardMarkup()
no_btn = InlineKeyboardButton("No ❌", callback_data="reset_user.False")
yes_btn = InlineKeyboardButton("Yes ✔️", callback_data="reset_user.True")
inline_kb_tf.add(yes_btn, no_btn)

watching_keyboard = InlineKeyboardMarkup(row_width=4)
next_1 = InlineKeyboardButton('▶️', callback_data='paginator.anime_watching.next_1')
prev_1 = InlineKeyboardButton('◀️', callback_data='paginator.anime_watching.prev_1')
next_5 = InlineKeyboardButton('⏩', callback_data='paginator.anime_watching.next_5')
prev_5 = InlineKeyboardButton('⏪', callback_data='paginator.anime_watching.prev_5')
edit_btn = InlineKeyboardButton("⚙️ Edit", callback_data="paginator.anime_watching.edit")
watching_keyboard.add(prev_5, prev_1, next_1, next_5).add(edit_btn)

edit_watching_keyboard = InlineKeyboardMarkup()
add_btn = InlineKeyboardButton("+1", callback_data="anime_watch_edit.add")
minus_btn = InlineKeyboardButton("-1", callback_data="anime_watch_edit.minus")
back_btn = InlineKeyboardButton("⬅ Back", callback_data="anime_watch_edit.back")
delete_btn = InlineKeyboardButton("🗑 Delete", callback_data="anime_watch_edit.delete")
complete_btn = InlineKeyboardButton("☑ Mark a Complete", callback_data="anime_watch_edit.complete")
update_score = InlineKeyboardButton("📝 Update Score", callback_data="anime_watch_edit.update_score")
edit_watching_keyboard.add(back_btn, delete_btn).add(minus_btn, add_btn).add(complete_btn).add(update_score)

searching_pagination = InlineKeyboardMarkup()
next_btn1 = InlineKeyboardButton("➡", callback_data="anime_search.next")
add_to_planned_btn = InlineKeyboardButton("☑ Into Planned list", callback_data="anime_search.into_planned")
previous_btn1 = InlineKeyboardButton("⬅", callback_data="anime_search.previous")
searching_pagination.add(previous_btn1, add_to_planned_btn, next_btn1)

planned_keyboard = InlineKeyboardMarkup(row_width=4)
next_1 = InlineKeyboardButton('▶️', callback_data='paginator.anime_planned.next_1')
prev_1 = InlineKeyboardButton('◀️', callback_data='paginator.anime_planned.prev_1')
next_5 = InlineKeyboardButton('⏩', callback_data='paginator.anime_planned.next_5')
prev_5 = InlineKeyboardButton('⏪', callback_data='paginator.anime_planned.prev_5')
edit_btn1 = InlineKeyboardButton('📝 Edit', callback_data='paginator.anime_planned.edit')
planned_keyboard.add(prev_5, prev_1, next_1, next_5).add(edit_btn1)

edit_planned_keyboard = InlineKeyboardMarkup(row_width=4)
add_to_watch = InlineKeyboardButton("🎬 Add to watch", callback_data="anime_planned_edit.watch")
delete = InlineKeyboardButton("🗑 Delete", callback_data="anime_planned_edit.delete")
add_completed = InlineKeyboardButton("☑ Add to Completed", callback_data="anime_planned_edit.completed")
back_btn = InlineKeyboardButton("⬅ Back", callback_data="anime_planned_edit.back")
edit_planned_keyboard.add(back_btn, delete).add(add_to_watch).add(add_completed)

completed_keyboard = InlineKeyboardMarkup(row_width=4)
next_1 = InlineKeyboardButton('▶️', callback_data='paginator.anime_completed.next_1')
prev_1 = InlineKeyboardButton('◀️', callback_data='paginator.anime_completed.prev_1')
next_5 = InlineKeyboardButton('⏩', callback_data='paginator.anime_completed.next_5')
prev_5 = InlineKeyboardButton('⏪', callback_data='paginator.anime_completed.prev_5')
edit_btn1 = InlineKeyboardButton('📝 Edit', callback_data='paginator.anime_completed.edit')
completed_keyboard.add(prev_5, prev_1, next_1, next_5).add(edit_btn1)

edit_completed_keyboard = InlineKeyboardMarkup(row_width=4)
delete = InlineKeyboardButton("🗑 Delete", callback_data="anime_completed_edit.delete")
update_score = InlineKeyboardButton("📝 Update Score", callback_data="anime_completed_edit.completed")
back_btn = InlineKeyboardButton("⬅ Back", callback_data="anime_completed_edit.back")
edit_completed_keyboard.add(back_btn, delete).add(update_score)


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
