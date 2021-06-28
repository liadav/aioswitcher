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

"""Switcher unofficial integration TCP socket API packet formats."""

# weekdays sum, start-time timestamp, end-time timestamp
SCHEDULE_CREATE_DATA_FORMAT = "01{}01{}{}"

NO_TIMER_REQUESTED = "00000000"
# format values are local session id, timestamp
REQUEST_FORMAT = "{}340001000000000000000000{}00000000000000000000f0fe"
PAD_74_ZEROS = "0" * 74

# format value just timestamp (initial session id is "00000000")
LOGIN_PACKET = "fef052000232a10000000000" + REQUEST_FORMAT[2:] + "1c" + PAD_74_ZEROS
# format values are local session id, timestamp, device id
GET_STATE_PACKET = "fef0300002320103" + REQUEST_FORMAT + "{}00"
# format values are local session id, timestamp, device id, command, timer
SEND_CONTROL_PACKET = (
    "fef05d0002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "0106000{}00{}"
)
# format values are local session id, timestamp, device id, auto-off seconds
SET_AUTO_OFF_SET_PACKET = (
    "fef05b0002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "040400{}"
)
# format values are local session id, timestamp, device id, name
UPDATE_DEVICE_NAME_PACKET = (
    "fef0740002320202" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "{}"
)
# format values are local session id, timestamp, device id
GET_SCHEDULES_PACKET = (
    "fef0570002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "060000"
)
# format values are local session id, timestamp, device id, schedule id
DELETE_SCHEDULE_PACKET = (
    "fef0580002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "0801000{}"
)
# format values are local session id, timestamp, device id,
# schedule data =
#                   (on_off + week + timstate + start_time + end_time)
CREATE_SCHEDULE_PACKET = (
    "fef0630002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "030c00ff{}"
)
