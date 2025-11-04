from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler
)
from datetime import date
from config import BOT_TOKEN, schedule_yana, schedule_ksenia, schedule_alina

CHOOSE_PERSON, CHOOSE_DAY = range(2)


def get_week_type():
    start_date = date(2025, 9, 1)
    today = date.today()
    week_number = ((today - start_date).days // 7) + 1
    return "первая" if week_number % 2 != 0 else "вторая"


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
    person = context.user_data.get("person")
    day = q.data
    week = get_week_type()

    if person == "yana":
        table = schedule_yana
    elif person == "ksenia":
        table = schedule_ksenia
    else:
        table = schedule_alina

    lessons = table.get(day, {}).get(week, [])

    if not lessons:
        text = f"🚫 Нет данных для выбранного дня.\nТекущая неделя: {week.capitalize()}"
    else:
        text = f"📆 Неделя: {week.capitalize()}\n\n" + "\n\n———\n\n".join(
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
        },
        fallbacks=[],
        per_user=True,
        per_chat=True,
    )

    app.add_handler(conv)
    app.run_polling()