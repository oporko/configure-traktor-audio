# This code is released under the GPLv3 license, see LICENSE for details.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Script for configuring Traktor Audio 6 channel thru/phono in Linux.
#
# You will need to add a custom udev rule or run this script as sudo, see:
# https://github.com/pyusb/pyusb/blob/master/docs/faq.rst#how-to-practically-deal-with-permission-issues-on-linux
#
# Example usage:
# python3 configure-traktor-audio-6.py --channel a b -t off -p off
#
# Technical details:
#
# This script relies extensively on pyusb, see tutorial for examples:
# https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
#
# Wireshark + USBPcap was used in Windows to sniff the URB_CONTROL out packets sent from the official Native Instruments tool.
# https://desowin.org/usbpcap/tour.html

import argparse
import usb.core
import usb.util

# Traktor Audio 6 constants

VENDOR         = 0x17cc
PRODUCT        = 0x1011 # Product ID may also be 0x1010. I don't have that version and cannot test if this script works with it.

CTRL_SET_THRU  = 1
CTRL_SET_PHONO = 2

TA6_CHANNEL_A  = 3
TA6_CHANNEL_B  = 5

VALUE_OFF      = 0
VALUE_ON       = 1

# Helper functions

def exit_with_error(msg, quiet):
    if quiet is True:
        exit(1)
    else:
        raise RuntimeError(msg)

def get_config_value(str_value):
    if str_value is None:
        return None

    if str_value == 'on':
        return VALUE_ON
    else:
        return VALUE_OFF

def get_channels(str_channels):
    channels = []

    if 'a' in str_channels:
        channels.append(TA6_CHANNEL_A)

    if 'b' in str_channels:
        channels.append(TA6_CHANNEL_B)

    return channels

def set_phono(device, channel, value):
    if value is None:
        return

    device.ctrl_transfer(0x40, CTRL_SET_THRU, value, channel, 0)

def set_thru(device, channel, value):
    if value is None:
        return

    device.ctrl_transfer(0x40, CTRL_SET_PHONO, value, channel, 0)
       
# Parse commandline arguments
parser = argparse.ArgumentParser(description='Script for setting Traktor Audio 6 channel configuration')
parser.add_argument('-c', '--channel', choices=['a', 'b'], nargs='+', required=True, help='Channel(s) to configure, ie. a b')
parser.add_argument('-t', '--thru', choices=['on', 'off'], help='Enable/disable direct thru')
parser.add_argument('-p', '--phono', choices=['on', 'off'], help='Enable/disable phono')
parser.add_argument('-q', '--quiet', action='store_true', help='Prints no output, return code will indicate success')

args = parser.parse_args()

# Convert arguments to Traktor specific commands/data
channels = get_channels(args.channel)
thru     = get_config_value(args.thru)
phono    = get_config_value(args.phono)

if thru is None and phono is None:
    exit_with_error('No configuration options provided, specify --thru or --phono', args.quiet)

# Find Traktor Audio 6
dev = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)

if dev is None:
    exit_with_error('Traktor Audio 6 not found', args.quiet)

# Set configuration if needed
try:
    dev.get_active_configuration()
except usb.core.USBError:
    dev.set_configuration()

# Apply config to channels
for channel in channels:
    set_thru(dev, channel, thru)
    set_phono(dev, channel, phono)
