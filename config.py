TOKEN = 'vk1.a.El5OgrYlMPQrrFUIdR5EdvbaU8vBDXZNz7j73k0usi' \
                 '-BGZZNIkl4gfMGEGOIv5QNT9V1ZmbSA3eCbAOniq6xEZWhwFLjvDzf1Yz' \
                 '-1w72AdXoNNwPIQCUdDSKhSQPrIENKBo0Ty_ashR62IijoFygWIXKpeYHEtRk1em2Z6Ow-_YpDHDadEPvY5CPidWkXly9' \
                 '-C91kvJLp9eRPD67zOdwPg'

START_MESSAGE = 'Привет, я бот. Могу подсказать тебе расписание твоей группы на любой день' \
                ', прогноз погоды и расписание необходимого преподавателя. Если хотите помощи, напишите "помощь". Но' \
                ' для начала напишите свою группу, чтобы не приходилось каждый раз указывать ее'

HELP_MESSAGE = 'Список команд:\n\nНачать - Запуск бота\nБот - Показ клавиатуры для выбора периода расписания\n' \
            'Бот <номер группы> - Запоминает группу и показывает клавиатуру\n' \
            'Бот <день недели> - Показывает расписание на чётный и нечётный день\n' \
            'Бот <день недели> <номер группы> - Сохраняет группу и показывает расписание за выбранный день\n\n' \
            'Найти <фамилия преподавателя> [И.О.] - Получить расписание преподавателя за определённый период\n\n' \
            'Погода - Показывает погоду в Москве'

SCHEDULE_URL: str = 'https://www.mirea.ru/schedule/'

# CMD_START = 'начать'
# CMD_SCHEDULE = 'бот'
# CMD_FIND_TEACHER = 'найти'
# CMD_WEATHER = 'погода'
#
# SPLIT_PAIR_SEPARATOR = ' / '
# WINDOW_SIGNATURE = '--'
# VOID_SIGNATURE = '_'
# ONE_PAIR_PATTERN = '{}) {}, {}, {}, {}\n'  # Номер, Предмет, Тип, Преподаватель, Аудитория
# ONE_PAIR_SHORT_PATTERN = '{}) {}\n'
# ONE_DAY_HEADER_PATTERN = '\nРасписание на {}:\n'  #
# ONE_DAY_TEACHER_HEADER_PATTERN = '\nРасписание преподавателя {} на {}:\n'  #
#
# ODD_DAY_PATTERN = 'Расписание на {}, нечётной недели\n'
# EVEN_DAY_PATTERN = 'Расписание на {} чётной недели\n'
#
# MONTHS_SLUGS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
#                 'ноября', 'декабря']
# WEEK_DAYS_SLUGS = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье']
# WEEK_DAYS_INFINITIVE_SLUGS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
#
# INVALID_GROUP_TEXT = 'Неверный формат или группа не найдена!\n\nФормат: \'АБВГ-12-34\''
# SET_GROUP_TEXT = 'Я запомнил, что ты учишься в группе {}'
# CURRENT_GROUP_TEXT = 'Я показываю расписание группы {}'
# CURRENT_GROUP_ERROR_TEXT = 'Группа не выбрана, для выбора группы, напишите \n\'{}\' и номер группы'
# CURRENT_WEEK_TEXT = 'Идёт {} неделя'
# SCHEDULE_SELECT_TEXT = 'Показать расписание ...'
# TEACHER_SELECT_TEXT = 'Выберите преподавателя'
# TEACHER_SELECT_PERIOD_TEXT = 'Показать расписание преподавателя {} ...'
# TEACHER_SELECT_ERROR_TEXT = 'Преподаватель не найден'
#
# INVALID_COMMAND_TEXT = 'Неизвестная команда\nЧто бы получить список команд напиши \'{}\''
#
# BTN_SCHEDULE_TODAY = 'на сегодня'
# BTN_SCHEDULE_TOMORROW = 'на завтра'
# BTN_SCHEDULE_WEEK = 'на эту неделю'
# BTN_SCHEDULE_NEXT_WEEK = 'на следующую неделю'
# BTN_WHAT_WEEK = 'неделя?'
# BTN_WHAT_GROUP = 'группа?'
# BTN_SETTINGS = 'настройки'
# BTN_HELP = 'помощь'
