from time import sleep
import RPi.GPIO as GPIO
import argparse
import schedule

DEFAULT_CHANNEL = 7
DEFAULT_WAIT_TIME = 3
DEFAULT_INTERVAL_TIME = 10


class Scheduler(object):
    def __init__(self, channel, interval):
        self._channel = channel
        self._interval = interval

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._channel, GPIO.OUT)

    def power_on_and_off(self):
        self.setup()
        GPIO.output(self._channel, 0)
        sleep(self._interval)
        self.cleanup()
        sleep(self._interval)

    def power_off(self):
        GPIO.output(self._channel, 1)

    @staticmethod
    def cleanup():
        GPIO.cleanup()


def main():
    parser = argparse.ArgumentParser(description="Relay Module Script")
    parser.add_argument(
        "-c",
        "--channel",
        type=int,
        default=DEFAULT_CHANNEL,
        help="set channel (default {} channel)".format(DEFAULT_CHANNEL),
    )
    parser.add_argument(
        "-w",
        "--wait-time",
        type=int,
        default=DEFAULT_WAIT_TIME,
        help="set power on wait seconds (default {} seconds)".format(
            DEFAULT_WAIT_TIME),
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_TIME,
        help="set script interval seconds (default {} seconds)".format(
            DEFAULT_INTERVAL_TIME
        ),
    )
    args = parser.parse_args()

    scheduler = Scheduler(args.channel, args.wait_time)
    schedule.every(args.interval).seconds.do(scheduler.power_on_and_off)

    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        scheduler.cleanup()
        pass


if __name__ == "__main__":
    main()
