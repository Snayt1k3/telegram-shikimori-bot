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
        pass  # todo написать описание

    @staticmethod
    def search_start_message() -> str:
        pass  # todo написать описание

    @staticmethod
    def torrent_start_msg() -> str:
        pass  # todo написать текст

    @staticmethod
    def description_torrent_file(size, episodes, quality) -> str:
        pass  # todo написать текст
