from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler
)
from config import BOT_TOKEN, schedule_yana, schedule_ksenia, schedule_alina

CHOOSE_PERSON, CHOOSE_DAY, CHOOSE_WEEK = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Яна", callback_data="yana"),
         InlineKeyboardButton("Ксения", callback_data="ksenia"),
         InlineKeyboardButton("Алина", callback_data="alina")]
    ]
    if update.message:
        await update.message.reply_text("👋 Привет, кто ты?",
                                        reply_markup=InlineKeyboardMarkup(buttons))
    else:
        q = update.callback_query
        await q.answer()
        await q.edit_message_text("👋 Привет, кто ты?",
                                  reply_markup=InlineKeyboardMarkup(buttons))
    return CHOOSE_PERSON


async def choose_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["person"] = q.data
    buttons = [[InlineKeyboardButton(day, callback_data=day.lower())
                for day in ["ПН", "ВТ", "СР"]],
               [InlineKeyboardButton(day, callback_data=day.lower())
                for day in ["ЧТ", "ПТ", "СБ"]]]
    await q.edit_message_text("📅 Выбери день недели:",
                              reply_markup=InlineKeyboardMarkup(buttons))
    return CHOOSE_DAY


async def choose_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["day"] = q.data
    buttons = [[InlineKeyboardButton("Первая", callback_data="первая"),
                InlineKeyboardButton("Вторая", callback_data="вторая")]]
    await q.edit_message_text("📅 Выбери учебную неделю:",
                              reply_markup=InlineKeyboardMarkup(buttons))
    return CHOOSE_WEEK


async def choose_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    person = context.user_data.get("person")
    day = context.user_data.get("day")
    week = q.data

    if(person == "yana"):
        table = schedule_yana
    elif(person == "ksenia"):
        table = schedule_ksenia
    else:
        table = schedule_alina
    

    lessons = table.get(day, {}).get(week, [])

    if not lessons:
        text = "🚫 Нет данных для выбранного дня."
    else:
        text = "\n\n———\n\n".join(
            f"🕒 {l['time']}\n📚 {l['subject']} — {l['type']}\n🏫 {l['room']}\n👨‍🏫 {l['teacher']}"
            for l in lessons
        )

    btn = [[InlineKeyboardButton("🔄 Ещё раз?", callback_data="start")]]
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(btn))
    return CHOOSE_PERSON


if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_PERSON: [
                CallbackQueryHandler(choose_person, pattern="^(yana|ksenia|alina)$"),
                CallbackQueryHandler(start, pattern="^start$")
            ],
            CHOOSE_DAY: [
                CallbackQueryHandler(choose_day, pattern="^(пн|вт|ср|чт|пт|сб)$")
            ],
            CHOOSE_WEEK: [
                CallbackQueryHandler(choose_week, pattern="^(первая|вторая)$")
            ],
        },
        fallbacks=[],
        per_user=True,
        per_chat=True,
    )

    app.add_handler(conv)
    app.run_polling()