#!/bin/bash

# MUST HAVE:
# sudo apt install pulseaudio-utils
# alsa_output.pci-0000_01_00.1.hdmi-stereo
# pactl list short sinks


# Define your sinks
SPEAKERS="alsa_output.pci-0000_01_00.1.hdmi-stereo"
HEADPHONES="alsa_output.usb-Corsair_CORSAIR_VOID_ELITE_Wireless_Gaming_Dongle-00.iec958-stereo"

# Get the current default sink
CURRENT_SINK=$(pactl get-default-sink)

# Toggle if argument is "toggle"
if [ "$1" == "toggle" ]; then
    if [ "$CURRENT_SINK" == "$SPEAKERS" ]; then
        pactl set-default-sink "$HEADPHONES"
    else
        pactl set-default-sink "$SPEAKERS"
    fi

    # Optional: move all current playing streams to the new default sink
    for STREAM in $(pactl list short sink-inputs | cut -f1); do
        pactl move-sink-input "$STREAM" "$(pactl get-default-sink)"
    done

    # Send a Polybar message to refresh the module
    polybar-msg hook audio_output 1
    exit 0

fi

# Get the updated default sink
UPDATED_SINK=$(pactl get-default-sink)

# Output the current sink name
if [ "$UPDATED_SINK" == "$SPEAKERS" ]; then
    echo "Speakers"
elif [ "$UPDATED_SINK" == "$HEADPHONES" ]; then
    # Check battery status of headphones
    BATTERY_INFO=$(headsetcontrol -b 2>/dev/null)
    BATTERY_STATUS=$(echo "$BATTERY_INFO" | grep "Status" | awk -F ': ' '{print $2}')
    BATTERY_LEVEL=$(echo "$BATTERY_INFO" | grep "Level" | awk -F ': ' '{print $2}')

	if [[ "$BATTERY_STATUS" == "BATTERY_AVAILABLE" ]]; then
        echo "Headphones ($BATTERY_LEVEL)";
    else
        echo "Headphones (OFF)"
	fi
else
    echo "Unknown"
fi
