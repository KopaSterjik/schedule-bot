from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler, MessageHandler, filters
)

CHOOSE_DAY, CHOOSE_WEEK = range(2)

schedule = {
    'пн': {
        'первая': [
            {'subject': 'Внешнеэкономическая деятельность и таможенные системы', 'time': '13:55-15:30', 'room': 'Ауд. 1108 К.8', 'teacher': ' Седюкевич В.Н.', 'type': 'Лекция'},
            {'subject': 'Внешнеэкономическая деятельность и таможенные системы', 'time': '15:40-17:15', 'room': 'Ауд. 1108 К.8', 'teacher': ' Седюкевич В.Н.', 'type': 'Лекция'},
            {'subject': 'Внешнеэкономическая деятельность и таможенные системы', 'time': '17:45-19:20', 'room': 'Ауд. 1108 К.8', 'teacher': ' Седюкевич В.Н.', 'type': 'Лабораторное занятие'},
        ],
        'вторая': [
             {'subject': 'Внешнеэкономическая деятельность и таможенные системы', 'time': '13:55-15:30', 'room': 'Ауд. 1108 К.8', 'teacher': ' Седюкевич В.Н.', 'type': 'Лекция'},
            {'subject': 'Внешнеэкономическая деятельность и таможенные системы', 'time': '15:40-17:15', 'room': 'Ауд. 1108 К.8', 'teacher': ' Седюкевич В.Н.', 'type': 'Лекция'},
        ]
    },
    'вт': {
        'первая': [
            {'subject': 'Основы эколого-энергетической устойчивости производства', 'time': '15:40-17:15', 'room': 'Ауд. 3п К.17', 'teacher': 'Рекс А.Г.', 'type': 'Лекция'},
            {'subject': 'Основы эколого-энергетической устойчивости производства', 'time': '17:45-19:20', 'room': 'Ауд. 428 К.18', 'teacher': 'Мартынюк С.С.', 'type': 'Лабораторное занятие'},
        ],
        'вторая': [
            {'subject': 'Охрана труда', 'time': '13:55-15:30', 'room': 'Ауд. 381 К.1', 'teacher': 'Абметко О.В.', 'type': 'Лабораторное занятие'},
            {'subject': 'Основы эколого-энергетической устойчивости производства', 'time': '15:40-17:15', 'room': 'Ауд. 3п К.17', 'teacher': 'Мартынюк С.С.', 'type': 'Лекция'},
        ]
    },
    'ср': {
        'первая': [
            {'subject': 'Международные перевозки опасных грузов', 'time': '13:55-15:30', 'room': 'Ауд. 1103 К.8', 'teacher': 'Ходоскин Д.П.', 'type': 'Лекция'},
            {'subject': 'Международные перевозки опасных грузов', 'time': '15:40-17:15', 'room': 'Ауд. 1103 К.8', 'teacher': 'Ходоскин Д.П.', 'type': 'Лекция'},
            {'subject': 'Международные автоперевозки грузов и ТЭД ', 'time': '17:45-19:20', 'room': 'Ауд. 802 К.8', 'teacher': 'Кустенко А.А.', 'type': 'Курсовое проектирование'},
        ],
        'вторая': [
           {'subject': 'Международные перевозки опасных грузов', 'time': '13:55-15:30', 'room': 'Ауд. 1103 К.8', 'teacher': 'Ходоскин Д.П.', 'type': 'Лекция'},
            {'subject': 'Международные перевозки опасных грузов', 'time': '15:40-17:15', 'room': 'Ауд. 1103 К.8', 'teacher': 'Ходоскин Д.П.', 'type': 'Практика'},
            {'subject': 'Испанский язык', 'time': '19.30-21.05', 'room': 'Ауд. ?', 'teacher': '?', 'type': 'Практика'},
        ]
    },
    'чт': {
        'первая': [
            {'subject': 'Международные автоперевозки грузов и ТЭД', 'time': '13:55-15:30', 'room': 'Ауд. 1106 К.8', 'teacher': 'Кустенко А.А.', 'type': 'Лабораторное занятие'},
            {'subject': 'Международные автоперевозки грузов и ТЭД', 'time': '15:40-17:15', 'room': 'Ауд. 1106 К.8', 'teacher': 'Кустенко А.А.', 'type': 'Лекция'},
            {'subject': 'Охрана труда', 'time': '17:45-19:20', 'room': 'Ауд. 453 К.1', 'teacher': 'Абметко О.В.', 'type': 'Лекция'},
            {'subject': 'Испанский язык', 'time': '19.30-21.05', 'room': 'Ауд. ?', 'teacher': '?', 'type': 'Практика'},
            
            

        ],
        'вторая': [
            {'subject': 'Международные автоперевозки грузов и ТЭД', 'time': '15:40-17:15', 'room': 'Ауд. 1106 К.8', 'teacher': 'Кустенко А.А.', 'type': 'Лекция'},
            {'subject': 'Охрана труда', 'time': '17:45-19:20', 'room': 'Ауд. 453 К.1', 'teacher': 'Абметко О.В.', 'type': 'Лекция'},
            {'subject': 'Испанский язык', 'time': '19.30-21.05', 'room': 'Ауд. ?', 'teacher': '?', 'type': 'Практика'},
            ]
    },
    'пт': {
        'первая': [
            {'subject': 'Международные автоперевозки грузов и ТЭД', 'time': '13:55-15:30', 'room': 'Ауд. 1103 К.8', 'teacher': 'Кустенко А.А.', 'type': 'Лекция'},
            {'subject': 'Бухгалтеский учет. Биржевое и банковское дело', 'time': '15:40-17:15', 'room': 'Ауд. 608 К.8', 'teacher': 'Мойсак О.И.', 'type': 'Лекция'},
            {'subject': 'Бухгалтеский учет. Биржевое и банковское дело', 'time': '17:45-19:20', 'room': 'Ауд. 321 К.8', 'teacher': 'Мойсак О.И.', 'type': 'Практика'},

        ],
        'вторая': [
            {'subject': 'Международные автоперевозки грузов и ТЭД', 'time': '13:55-15:30', 'room': 'Ауд. 1103 К.8', 'teacher': 'Кустенко А.А.', 'type': 'Лекция'},
            {'subject': 'Бухгалтеский учет. Биржевое и банковское дело', 'time': '15:40-17:15', 'room': 'Ауд. 608 К.8', 'teacher': 'Мойсак О.И.', 'type': 'Лекция'},
            {'subject': 'Международные автоперевозки грузов и ТЭД', 'time': '17:45-19:20', 'room': 'Ауд. 1103 К.8', 'teacher': 'Кустенко А.А.', 'type': 'Практика'},
        ]
    },
    'сб': {
        'первая': [
            {'subject': 'Транспортные тарифы', 'time': '9:55-11:30', 'room': 'Ауд. 804 К.8', 'teacher': 'Семченков С.С.', 'type': 'Лекция'},
            {'subject': 'Транспортные тарифы', 'time': '12:00-13:35', 'room': 'Ауд. 804 К.8', 'teacher': 'Семченков С.С.', 'type': 'Практика'},

        ],
        'вторая': [
            {'subject': 'Транспортные тарифы', 'time': '9:55-11:30', 'room': 'Ауд. 804 К.8', 'teacher': 'Семченков С.С.', 'type': 'Лекция'},
]
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start -> показывает большую reply-кнопку "Начать"
    (используйте встроенную кнопку Telegram 'Start' — не обязательно печатать /start)
    """
    kb = ReplyKeyboardMarkup([['Начать']], resize_keyboard=True, one_time_keyboard=True)
    # обычно /start приходит как message
    if update.message:
        await update.message.reply_text('👋 Привет! Нажми кнопку, чтобы начать:', reply_markup=kb)
    return CHOOSE_DAY

async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает нажатие reply-кнопки 'Начать' (приходит как message)
    или callback 'start_process' (при нажатии 'Ещё раз?' после результата).
    Показывает inline-кнопки с днями.
    """
    buttons = [[InlineKeyboardButton(day, callback_data=day.lower()) for day in ['ПН','ВТ','СР']],
               [InlineKeyboardButton(day, callback_data=day.lower()) for day in ['ЧТ','ПТ','СБ']]]
    if update.callback_query:
        q = update.callback_query
        await q.answer()
        await q.edit_message_text('📅 Выбери день недели:', reply_markup=InlineKeyboardMarkup(buttons))
    else:
        # пришло как text message "Начать"
        await update.message.reply_text('📅 Выбери день недели:', reply_markup=InlineKeyboardMarkup(buttons))
    return CHOOSE_DAY

async def choose_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data['day'] = q.data  # 'пн', 'вт', ...
    buttons = [[InlineKeyboardButton('Первая', callback_data='первая'),
                InlineKeyboardButton('Вторая', callback_data='вторая')]]
    await q.edit_message_text('📅 Выбери учебную неделю:', reply_markup=InlineKeyboardMarkup(buttons))
    return CHOOSE_WEEK

async def choose_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    day = context.user_data.get('day')
    week = q.data  # 'первая' или 'вторая'
    lessons = schedule.get(day, {}).get(week, [])
    if not lessons:
        text = '🚫 Нет данных для выбранного дня.'
    else:
        blocks = []
        for l in lessons:
            block = f"🕒 {l['time']}\n📚 {l['subject']} — {l['type']}\n🏫 {l['room']}\n👨‍🏫 {l['teacher']}"
            blocks.append(block)
        text = '\n\n———\n\n'.join(blocks)

    # кнопка "Ещё раз?" чтобы начать заново (возвращает в CHOOSE_DAY)
    buttons = [[InlineKeyboardButton("🔄 Ещё раз?", callback_data="start_process")]]
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    return CHOOSE_DAY

if __name__ == "__main__":
    app = Application.builder().token("8311147492:AAFK2E8wlwOGYr4mJViyqbcMccJwsX_yJAQ").build()

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_DAY: [
                # нажатие reply-кнопки "Начать" приходит как message с текстом -> ловим внутри CHOOSE_DAY
                MessageHandler(filters.Regex('^(Начать|начать)$'), start_process),
                # если пользователь нажал "Ещё раз?" (callback с start_process)
                CallbackQueryHandler(start_process, pattern="^start_process$"),
                # выбор дня (callback)
                CallbackQueryHandler(choose_day, pattern="^(пн|вт|ср|чт|пт|сб)$"),
            ],
            CHOOSE_WEEK: [
                CallbackQueryHandler(choose_week, pattern="^(первая|вторая)$"),
            ],
        },
        fallbacks=[],
        per_user=True,
        per_chat=True
    )

    app.add_handler(conv)
    app.run_polling()



