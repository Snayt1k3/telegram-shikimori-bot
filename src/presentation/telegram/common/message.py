class Message:
    """
    A class with static methods for formating message
    """

    @staticmethod
    def ensure_user_signout() -> str:
        return "Вы уверены что хотите отключить аккаунт шикимори? это приведет к частичному ограничению возможностей"
