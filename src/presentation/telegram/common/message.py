from src.application.dto import UserRateDTO, SearchResultDTO, TitleDTO


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
            f"Если хочешь использовать Полный функционал, "
            f"тебе надо будет привязать свой профиль с Шикимори\n"
            f"Используй комманду - /signin"
        )

    @staticmethod
    def about() -> str:
        return ""  # todo написать описание

    @staticmethod
    def search_response_message(query) -> str:
        return f"Ниже представлены аниме найденные по данному запросу - '{query}'"

    @staticmethod
    def search_message() -> str:
        return "Напишите название тайтла, которого хотите найти."

    @staticmethod
    def description_torrent_file(size, episodes, quality) -> str:
        return (
            f"Размер: {round(size / (1024 ** 3), 2)}GB\n"
            f"Качество: {quality}\n"
            f"Кол-во Эпизодов: {episodes}\n"
        )

    @staticmethod
    def torrent_list_msg() -> str:
        return "Выберите из предложенного списка аниме, то аниме, чей торрент файл вы хотите получить"

    @staticmethod
    def all_lists_msg():
        return "Вот ваши списки, выберите список, который хотите изучить."

    @staticmethod
    def list_info_msg(length: int, page: int):
        pages = length // 8
        total_pages = pages + 1 if length % 8 else pages
        return f"Вы просматриваете страницу {page // 8} из {total_pages} в выбранном вами списке."

    @staticmethod
    def user_rate_info_msg(rate: UserRateDTO) -> str:
        return (
            f"{rate.title.title_ru} | {rate.title.title_en} \n\n"
            f"Статус: {rate.status}\n"
            f"Эпизоды: {rate.episodes} | {rate.title.episodes_aired} \n"
            f"Ваша Оценка: {rate.score if rate.score != 0 else 'Вы не поставили оценку'} \n"
        )

    @staticmethod
    def anilibria_title_msg(anime: SearchResultDTO) -> str:
        return (
            f"{anime.ru} | {anime.en} \n\n"
            f"Статус: {anime.status} \n"
            f"Войсеры: {''.join(anime.additional_data['voicers'])}"
        )

    @staticmethod
    def shikimori_title_msg(title: TitleDTO) -> str:
        return (
            f"{title.title_ru} | {title.title_en} \n\n"
            f"Эпизодов Вышло: {title.episodes_aired} из {title.episodes} \n"
            f"Статус: {title.status} \n"
        )
