from dataclasses import dataclass, asdict
from typing import List, Dict, Type


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {}; '
                    'Длительность: {:.3f} ч.; '
                    'Дистанция: {:.3f} км; '
                    'Ср. скорость: {:.3f} км/ч; '
                    'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(*asdict(self).values())


class Training:
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    COEFF_CALORY_1: float = 18
    COEFF_CALORY_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORY_1
                 * self.get_mean_speed()
                 - self.COEFF_CALORY_2)
                * self.weight
                / self.M_IN_KM
                * self.duration_h
                * self.MIN_IN_H)


class SportsWalking(Training):
    COEFF_CALORY_1: float = 0.035
    COEFF_CALORY_2: float = 0.029
    COEFF_CALORY_3: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORY_1
                * self.weight
                + (self.get_mean_speed()
                   ** self.COEFF_CALORY_3
                   // self.height)
                * self.COEFF_CALORY_2
                * self.weight)
                * self.duration_h
                * self.MIN_IN_H)


class Swimming(Training):
    LEN_STEP: float = 1.38
    COEFF_CALORY_1: float = 1.1
    COEFF_CALORY_2: float = 2

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
                / self.duration_h)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.COEFF_CALORY_1)
                * self.COEFF_CALORY_2
                * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    type_of_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in type_of_training:
        raise ValueError(f'Тренировка {workout_type} не найдена')
    return type_of_training[workout_type](*data)


def main(training_1: Training) -> None:
    info = training_1.show_training_info()
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
