class Message:
    """
    A class with static methods for formating message
    """

    @staticmethod
    def ensure_user_signout() -> str:
        return "Вы уверены что хотите отключить аккаунт шикимори? это приведет к частичному ограничению возможностей"

    @staticmethod
    def start() -> str:
        return (
            f"Привет! Я Твой помощник по Аниме миру с энциклопедией Шикимори\n"
            + f"Если хочешь использовать Полный функционал, "
            f"тебе надо будет привязать свой профиль с Шикимори\n"
            f"Используй комманду - /signin"
        )

    @staticmethod
    def about() -> str:
        return ""  # todo написать описание

    @staticmethod
    def search_query_message() -> str:
        return "Напишите название тайтла, которого хотите найти"

    @staticmethod
    def search_start_message() -> str:
        return "Напишите название тайтла, которого хотите найти"

    @staticmethod
    def torrent_start_msg() -> str:
        return "Напишите название тайтла, которого хотите найти"

    @staticmethod
    def description_torrent_file(size, episodes, quality) -> str:
        return (
            f"Размер: {size}\n"
            f"Качество: {quality}\n"
            f"Кол-во Эпизодов: {episodes}\n"
        )

    @staticmethod
    def torrent_list_msg() -> str:
        return "Выберите из предложенного списка аниме, то аниме, чей торрент файл вы хотите получить"
