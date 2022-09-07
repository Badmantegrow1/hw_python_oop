from dataclasses import dataclass
from typing import Sequence


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    TIME_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    FIRST_COEFFICIENT: int = 18
    SECOND_COEFFICIENT: int = 20

    def get_spent_calories(self) -> float:
        return ((self.FIRST_COEFFICIENT
                 * self.get_mean_speed()
                 - self.SECOND_COEFFICIENT)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.TIME_IN_MIN)


class SportsWalking(Training):
    FIRST_COEFFICIENT: float = 0.035
    SECOND_COEFFICIENT: float = 0.029
    NUMBER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.FIRST_COEFFICIENT
                * self.weight
                + (self.get_mean_speed()
                   ** self.NUMBER
                   // self.height)
                * self.SECOND_COEFFICIENT
                * self.weight)
                * self.duration
                * self.TIME_IN_MIN)


class Swimming(Training):
    LEN_STEP: float = 1.38
    FIRST_COEFFICIENT: float = 1.1
    SECOND_COEFFICIENT: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_poll = length_pool
        self.count_poll = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_poll
                * self.count_poll
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.FIRST_COEFFICIENT)
                * self.SECOND_COEFFICIENT
                * self.weight)


def read_package(workout_type: str, data: Sequence[int]) -> Training:
    type_of_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in type_of_training:
        return type_of_training[workout_type](*data)
    else:
        raise ValueError('Тренировка не найдена')


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
