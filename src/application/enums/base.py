import enum


class Enum(enum.Enum):
    def __str__(self):
        return self.value
