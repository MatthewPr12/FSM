"""
Possible day in my life simulated with FSM
"""
# pylint:disable=method-hidden
# pylint:disable=invalid-name
# pylint:disable=too-many-instance-attributes
from time import sleep
import random


def prime(fn):
    """
    launch generator beforehand
    :param fn:
    :return:
    """
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v

    return wrapper


class FSM:
    """
    Finite State Machine class
    """
    def __init__(self):
        """
        constructor
        """
        self.start = self.start()
        self.sleep = self.sleep()
        self.learn = self.learn()
        self.eat = self.eat()
        self.play = self.play()
        self.air_alarm = self.air_alarm()
        self.die = self.die()
        self.night_awake = False

        self.cur_state = self.start
        self.dead = False

    def clock(self, hour):
        """
        manage all generators
        :param hour:
        :return:
        """
        try:
            self.cur_state.send(hour)
        except StopIteration:
            self.dead = True

    def survived_this_day(self):
        """
        check whether still alive
        :return:
        """
        return not self.dead

    @prime
    def air_alarm(self):
        """
        Повітряна тривога! Повітряна тривога!
        :return:
        """
        while True:
            hour = yield
            self.night_awake = True
            print(f"Беремо по канапці і в сховище {hour}:00")
            if random.randint(0, 5) == 3:
                # if by some chance the rocket reaches its aim - you can die
                # if you're not in bomb shelter
                print("Не нехтуйте сигналом повітряної тривоги!")
                self.cur_state = self.die
            elif hour == 8:
                print(f"Канапки скінчились {hour}:00")
                self.cur_state = self.eat
            else:
                print("Вібій повітряної тривоги!")
                print(f"Можете повертатись до нормального життя {hour}:00")
                self.cur_state = self.sleep

    @prime
    def start(self):
        """
        starter state
        :return:
        """
        while True:
            hour = yield
            print("Starting...")
            if hour == 0:
                self.cur_state = self.sleep
            else:
                break

    @prime
    def sleep(self):
        """
        sleeping state
        :return:
        """
        while True:
            hour = yield
            print(f"sleeping---------- {hour}:00")
            bledina = random.randint(0, 5)
            if bledina == 3:  # if the rocket is launched it causes air raid alarm
                print("Here we go again... русня не люди")
                self.cur_state = self.air_alarm
            elif hour == 8:
                self.cur_state = self.eat
            elif hour in {9, 11, 13}:
                self.cur_state = self.learn

    @prime
    def eat(self):
        """
        eating state
        :return:
        """
        while True:
            hour = yield
            print(f"eating------------ {hour}:00")
            if hour == 23:
                self.cur_state = self.sleep
            elif hour == 15:
                self.cur_state = self.learn
            elif hour == 9:
                self.cur_state = self.learn

    @prime
    def play(self):
        """
        playing state
        :return:
        """
        while True:
            hour = yield
            print(f"playing----------- {hour}:00")
            if hour == 21:
                self.cur_state = self.learn

    @prime
    def learn(self):
        """
        learning state
        :return:
        """
        while True:
            hour = yield
            print(f"learning---------- {hour}:00")
            period = ['session', 'normal studying', 'holiday']
            if hour == 14:
                self.cur_state = self.eat
            elif hour == 19 and not self.night_awake:
                self.cur_state = self.play
            elif hour == 19 and self.night_awake:
                # if you did not sleep enough due to air alarm
                # you will fall asleep without playing
                self.cur_state = self.sleep
            elif hour == 23 and random.choice(period) == 'session':
                print("It's session, fella...")
                self.cur_state = self.die

    @prime
    def die(self):
        """
        final state -> DEATH
        :return:
        """
        while True:
            hour = yield
            print(f"I'm dead... {hour}:00")
            self.dead = True


def main():
    """
    main wrapper
    :return:
    """
    day = FSM()
    for hour in range(25):
        sleep(1)
        day.clock(hour)
        if not day.survived_this_day():
            break
    print("THE END")


if __name__ == "__main__":
    main()
