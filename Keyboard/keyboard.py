from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

keyboard_status = ReplyKeyboardMarkup()
keyboard_status.add("completed", "watching").add("planned").add("rewatching", "dropped")


default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add("/AnimeSearch", "/AnimeMark").add("/MyProfile", '/ResetProfile').add('/MyWatchList',
                                                                                          "/MyPlannedList")


keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add('/cancel')


inline_kb_tf = InlineKeyboardMarkup()
no_btn = InlineKeyboardButton("No", callback_data="reset_user.False")
yes_btn = InlineKeyboardButton("Yes", callback_data="reset_user.True")
inline_kb_tf.add(yes_btn, no_btn)


watching_pagination = InlineKeyboardMarkup()
next_btn = InlineKeyboardButton(">>", callback_data="anime_watch.next")
edit_btn = InlineKeyboardButton("Edit", callback_data="anime_watch.edit")
previous_btn = InlineKeyboardButton("<<", callback_data="anime_watch.previous")
watching_pagination.add(previous_btn, edit_btn, next_btn)


edit_keyboard = InlineKeyboardMarkup()
add_btn = InlineKeyboardButton("+1", callback_data="anime_watch_one.add")
minus_btn = InlineKeyboardButton("-1", callback_data="anime_watch_one.minus")
back_btn = InlineKeyboardButton("Back", callback_data="anime_watch_one.back")
delete_btn = InlineKeyboardButton("Delete", callback_data="anime_watch_one.delete")
complete_btn = InlineKeyboardButton("Mark a Complete", callback_data="anime_watch_one.complete")

edit_keyboard.add(back_btn, delete_btn).add(minus_btn, add_btn).add(complete_btn)

searching_pagination = InlineKeyboardMarkup()
next_btn1 = InlineKeyboardButton(">>", callback_data="anime_search.next")
add_to_planned_btn = InlineKeyboardButton("Add Into Planned", callback_data="anime_search.into_planned")
previous_btn1 = InlineKeyboardButton("<<", callback_data="anime_search.previous")
searching_pagination.add(previous_btn1, add_to_planned_btn, next_btn1)

planned_keyboard = InlineKeyboardMarkup(row_width=4)
next_1 = InlineKeyboardButton('>', callback_data='anime_planned.next_1')
prev_1 = InlineKeyboardButton('<', callback_data='anime_planned.prev_1')
next_5 = InlineKeyboardButton('>>', callback_data='anime_planned.next_5')
prev_5 = InlineKeyboardButton('<<', callback_data='anime_planned.prev_5')
edit_btn1 = InlineKeyboardButton('Edit', callback_data='anime_planned.edit')
planned_keyboard.add(prev_5, prev_1, next_1, next_5).add(edit_btn1)

edit_planned_keyboard = InlineKeyboardMarkup(row_width=4)
add_to_watch = InlineKeyboardButton("🎬 Add to watch", callback_data="anime_planned_edit.watch")
delete = InlineKeyboardButton("❌ Delete", callback_data="anime_planned_edit.delete")
add_completed = InlineKeyboardButton("☑️ Add to Completed", callback_data="anime_planned_edit.completed")
back_btn = InlineKeyboardButton("⬅️ Back", callback_data="anime_planned_edit.back")
edit_planned_keyboard.add(back_btn, delete).add(add_to_watch).add(add_completed)
