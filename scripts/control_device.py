#! python3

# Copyright Tomer Figenblat.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python script for controlling Switcher devices."""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from asyncio import get_event_loop
from datetime import timedelta
from pprint import PrettyPrinter
from typing import Any, Dict, List

from pkg_resources import require

from aioswitcher.api import Command, SwitcherApi
from aioswitcher.schedule import Days

require("aioswitcher>=2.0.0-dev")

printer = PrettyPrinter(indent=4)

_examples = """example usage:

python control_device.py -d ab1c2d -i "111.222.11.22" get_state\n
python control_device.py -d ab1c2d -i "111.222.11.22" turn_on\n
python control_device.py -d ab1c2d -i "111.222.11.22" turn_on -t 15\n
python control_device.py -d ab1c2d -i "111.222.11.22" turn_off\n
python control_device.py -d ab1c2d -i "111.222.11.22" set_name -n "My Boiler"\n
python control_device.py -d ab1c2d -i "111.222.11.22" set_auto_shutdown -r 2 -m 30\n
python control_device.py -d ab1c2d -i "111.222.11.22" get_schedules\n
python control_device.py -d ab1c2d -i "111.222.11.22" delete_schedule -s 3\n
python control_device.py -d ab1c2d -i "111.222.11.22" create_schedule -n "14:00" -f "14:30"\n
python control_device.py -d ab1c2d -i "111.222.11.22" create_schedule -n "17:30" -f "18:30" -w Sunday Monday Friday"""  # noqa E501

# parent parser
parent_parser = ArgumentParser(
    description="Control your Switcher device",
    epilog=_examples,
    formatter_class=RawDescriptionHelpFormatter,
)
parent_parser.add_argument(
    "-v",
    "--verbose",
    default=False,
    action="store_true",
    help="include the raw message",
)
parent_parser.add_argument(
    "-d",
    "--device-id",
    type=str,
    required=True,
    help="the identification of the device",
)
parent_parser.add_argument(
    "-i",
    "--ip-address",
    type=str,
    required=True,
    help="the ip address assigned to the device",
)

subparsers = parent_parser.add_subparsers(
    dest="action", description="supported actions"
)

# get_state parser
subparsers.add_parser("get_state", help="get the current state of a device")

# turn_on parser
turn_on_parser = subparsers.add_parser("turn_on", help="turn on the device")
turn_on_parser.add_argument(
    "-t",
    "--timer",
    type=int,
    nargs="?",
    default=0,
    help="set minutes timer for turn on operation",
)

# turn_off parser
turn_on_parser = subparsers.add_parser("turn_off", help="turn off the device")

# set_name parser
set_name_parser = subparsers.add_parser("set_name", help="set the name of the device")
set_name_parser.add_argument(
    "-n",
    "--name",
    type=str,
    required=True,
    help="new name for the device",
)

# set_auto_shutdown parser
set_auto_shutdown_parser = subparsers.add_parser(
    "set_auto_shutdown", help="set the auto shutdown property (1h-24h)"
)
set_auto_shutdown_parser.add_argument(
    "-r",
    "--hours",
    type=int,
    required=True,
    help="number hours for the auto shutdown",
)
set_auto_shutdown_parser.add_argument(
    "-m",
    "--minutes",
    type=int,
    nargs="?",
    default=0,
    help="number hours for the auto shutdown",
)

# get_schedules parser
subparsers.add_parser("get_schedules", help="retrive a device schedules")

# delete_schedule parser
delete_schedule_parser = subparsers.add_parser(
    "delete_schedule", help="delete a device schedule"
)
delete_schedule_parser.add_argument(
    "-s",
    "--schedule-id",
    type=str,
    required=True,
    help="the id of the schedule for deletion",
)

# create_schedule parser
create_schedule_parser = subparsers.add_parser(
    "create_schedule", help="create a new schedule"
)
create_schedule_parser.add_argument(
    "-n",
    "--start-time",
    type=str,
    required=True,
    help="the on time for the schedule, e.g. 13:00",
)
create_schedule_parser.add_argument(
    "-f",
    "--end-time",
    type=str,
    required=True,
    help="the off time for the schedule, e.g. 13:30",
)
possible_weekdays = [d.value for d in Days]
create_schedule_parser.add_argument(
    "-w",
    "--weekdays",
    choices=possible_weekdays,
    nargs="*",
    required=False,
    help=f"days for recurring schedules, possible values: {possible_weekdays}",
    default=list(),
)


def asdict(dc: object, verbose: bool = False) -> Dict[str, Any]:
    """Use as custom implementation of the asdict utility method."""
    return {
        k: v
        for k, v in dc.__dict__.items()
        if not (not verbose and k == "unparsed_response")
    }


async def get_state(device_id: str, device_ip: str, verbose: bool) -> None:
    """Use to launch a get_state request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.get_state(), verbose))


async def turn_on(device_id: str, device_ip: str, timer: int, verbose: bool) -> None:
    """Use to launch a turn_on request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.control_device(Command.ON, timer), verbose))


async def turn_off(device_id: str, device_ip: str, verbose: bool) -> None:
    """Use to launch a turn_off request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.control_device(Command.OFF), verbose))


async def set_name(device_id: str, device_ip: str, name: str, verbose: bool):
    """Use to launch a set_name request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.set_device_name(name), verbose))


async def set_auto_shutdown(
    device_id: str, device_ip: str, hours: int, minutes: int, verbose: bool
):
    """Use to launch a set_auto_shutdown request."""
    td_val = timedelta(hours=hours, minutes=minutes)
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.set_auto_shutdown(td_val), verbose))


async def get_schedules(device_id: str, device_ip: str, verbose: bool) -> None:
    """Use to launch a get_schedules request."""
    async with SwitcherApi(device_ip, device_id) as api:
        response = await api.get_schedules()
        if verbose:
            printer.pprint({"unparsed_response": response.unparsed_response})
            print()
        for schedule in response.schedules:
            printer.pprint(asdict(schedule))
            print()


async def delete_schedule(
    device_id: str, device_ip: str, schedule_id: str, verbose: bool
) -> None:
    """Use to launch a delete_schedule request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.delete_schedule(schedule_id), verbose))


async def create_schedule(
    device_id: str,
    device_ip: str,
    start_time: str,
    end_time: str,
    weekdays: List[str],
    verbose: bool,
):
    """Use to launch a create_schedule request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(
            asdict(
                await api.create_schedule(
                    start_time,
                    end_time,
                    set([Days(w) for w in weekdays]),  # type: ignore
                ),
                verbose,
            )
        )


if __name__ == "__main__":
    try:
        args = parent_parser.parse_args()

        if args.action == "get_state":
            get_event_loop().run_until_complete(
                get_state(args.device_id, args.ip_address, args.verbose)
            )
        elif args.action == "turn_on":
            get_event_loop().run_until_complete(
                turn_on(args.device_id, args.ip_address, args.timer, args.verbose)
            )
        elif args.action == "turn_off":
            get_event_loop().run_until_complete(
                turn_off(args.device_id, args.ip_address, args.verbose)
            )
        elif args.action == "set_name":
            get_event_loop().run_until_complete(
                set_name(args.device_id, args.ip_address, args.name, args.verbose)
            )
        elif args.action == "set_auto_shutdown":
            get_event_loop().run_until_complete(
                set_auto_shutdown(
                    args.device_id,
                    args.ip_address,
                    args.hours,
                    args.minutes,
                    args.verbose,
                )
            )
        elif args.action == "get_schedules":
            get_event_loop().run_until_complete(
                get_schedules(args.device_id, args.ip_address, args.verbose)
            )
        elif args.action == "delete_schedule":
            get_event_loop().run_until_complete(
                delete_schedule(
                    args.device_id, args.ip_address, args.schedule_id, args.verbose
                )
            )
        elif args.action == "create_schedule":
            get_event_loop().run_until_complete(
                create_schedule(
                    args.device_id,
                    args.ip_address,
                    args.start_time,
                    args.end_time,
                    args.weekdays,
                    args.verbose,
                )
            )
    except KeyboardInterrupt:
        exit()