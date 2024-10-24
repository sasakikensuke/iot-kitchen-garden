from time import sleep
from gpiozero import OutputDevice
import argparse
import schedule

DEFAULT_CHANNEL = 7
DEFAULT_WAIT_TIME = 3
DEFAULT_INTERVAL_TIME = 10


class Scheduler(object):
    def __init__(self, channel, interval):
        self._relay = OutputDevice(channel)
        self._interval = interval

    def power_on_and_off(self):
        self._relay.on()
        sleep(self._interval)
        self._relay.off()
        sleep(self._interval)

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
        help="set power on wait seconds (default {} seconds)".format(DEFAULT_WAIT_TIME),
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_TIME,
        help="set script interval seconds (default {} seconds)".format(DEFAULT_INTERVAL_TIME),
    )
    args = parser.parse_args()

    scheduler = Scheduler(args.channel, args.wait_time)
    schedule.every(args.interval).seconds.do(scheduler.power_on_and_off)
    
    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()