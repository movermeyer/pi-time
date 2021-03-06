"""Hardcoded settings and options."""

# Crossbar node for laptimer, details in .crossbar/config.json
LAPTIMER_NODE = u"pi-time-laptimer-node"
# URI prefix for PUBSUB and RPC
URI_PREFIX = u"pi-time."

PLAYA_BIKE = "BIKE"
PLAYA_DRIVE = "DRIVE"
PLAYA_FLY = "FLY"
PLAYA_MOTORBIKE = "MOTO"
PLAYA_RC = "RC"
PLAYA_RUN = "RUN"
PLAYA_SWIM = "SWIM"
OPTIONS_BIKE = ("Pump Track", "BMX", "Downhill", "Enduro", "Cross Country")
OPTIONS_MOTORBIKE = ("Motocross")
OPTIONS_RC = ("Track")
OPTIONS_RUN = ("Track", "Cross Country")
OPTIONS_SWIM = ("Pool", "Ocean")
OPTIONS_DRIVE = ("Track", "Hillclimb", "Rally")
OPTIONS_FLY = ("Course")
OPTIONS_PLAYA = (
    (PLAYA_BIKE, "Ride", "Rider", OPTIONS_BIKE),
    (PLAYA_DRIVE, "Drive", "Driver", OPTIONS_DRIVE),
    (PLAYA_FLY, "Fly", "Pilot", OPTIONS_FLY),
    (PLAYA_MOTORBIKE, "Ride", "Rider", OPTIONS_MOTORBIKE),
    (PLAYA_RC, "Remote Control", "Driver", OPTIONS_RC),
    (PLAYA_RUN, "Run", "Runner", OPTIONS_RUN),
    (PLAYA_SWIM, "Swim", "Swimmer", OPTIONS_SWIM)
)

# Report speed in km/h|m/s, distance in metres.
METRIC = "METRIC"
# Report speed in m/h|y/s, distance in yards.
IMPERIAL = "IMPERIAL"
OPTIONS_UNIT_OF_MEASUREMENT = (
    (METRIC, "Metric"),
    (IMPERIAL, "Imperial")
)

# TODO: Needed? Also consider i18n
# SENSOR_TYPE_INFRARED_ACTIVE = "AIR"
# SENSOR_TYPE_INFRARED_PASSIVE = "PIR"
# SENSOR_TYPE_RADIO = "RAD"
#SENSOR_TYPE = ( # Defines the hardware used by sensor
#    (SENSOR_TYPE_INFRARED_ACTIVE, "Active Infrared"),
#    (SENSOR_TYPE_INFRARED_PASSIVE, "Passive Infrared"),
#)

# Sensor located at starting line
SENSOR_LOCATION_START = "START"
# Sensor located at finish line
SENSOR_LOCATION_FINISH = "FINISH"
# Sensor located at start/finish line
SENSOR_LOCATION_START_FINISH = "START_FINISH"
# Sensor located at sector position (neither start nor finish)
SENSOR_LOCATION_SECTOR = "SECTOR"
OPTIONS_SENSOR_LOCATION = (
    (SENSOR_LOCATION_START, "Start line"),
    (SENSOR_LOCATION_FINISH, "Finish line"),
    (SENSOR_LOCATION_START_FINISH, "Start and finish line"),
    (SENSOR_LOCATION_SECTOR, "Sector checkpoint (split time)"),
)

# Laptimer pins, tuple of config key, caption, description
PIN_LED_APP = ("pinLedApp", "App Active LED",
               "Pin for LED when application is active")
PIN_LED_LAP = ("pinLedLap", "Lap Active LED",
               "Pin for LED when lap is active")
OPTIONS_PIN_LAPTIMER = (
    PIN_LED_APP,
    PIN_LED_LAP,
)
# Sensor pins, tuple of config key, caption, description
SENSOR_PIN_LED_EVENT = ("pinLedEvent", "Sensor LED",
                        "Pin for LED when sensor triggered")
SENSOR_PIN_EVENT = ("pinEvent", "Sensor Event",
                    "Pin for receiving sensor events")
OPTIONS_PIN_SENSOR = OPTIONS_PIN_LAPTIMER + (
    SENSOR_PIN_LED_EVENT,
    SENSOR_PIN_EVENT
)

# Raspberry Pi pin layouts - http://pi.gadgetoid.com/pinout
# http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/
# Model B - Revision 1.0
RPI_GPIO_REV1 = (
    (3, "3 = GPIO 0"),
    (5, "5 = GPIO 1"),
    (7, "7 = GPIO 4 (GPCLK0)"),
    (8, "8 = GPIO 14 (UART0_TXD)"),
    (10, "10 = GPIO 15 (UART0_RXD)"),
    (11, "11 = GPIO 17"),
    (12, "12 = GPIO 18 (PCMCLK)"),
    (13, "13 = GPIO 27"),
    (15, "14 = GPIO 22"),
    (16, "15 = GPIO 23"),
    (18, "18 = GPIO 24"),
    (19, "19 = GPIO 10 (SPI0_MOSI)"),
    (21, "21 = GPIO 9 (SPI0_MISO "),
    (22, "22 = GPIO 25"),
    (23, "23 = GPIO 11 (SPI0_SCLK)"),
    (24, "24 = GPIO 8 (SPI0_CE0_N)"),
    (26, "26 = GPIO 7 (SPI0_CE1_N)")
)
# Model A/B - Revision 2.0
RPI_GPIO_REV2 = (
    (3, "3 = GPIO 2"),
    (5, "5 = GPIO 3")
) + RPI_GPIO_REV1[2:]  # Same as revision 1 after pin 5
# Model B+
RPI_GPIO_BPLUS = RPI_GPIO_REV2 + (
    (29, "29 = GPIO 5"),
    (31, "31 = GPIO 6"),
    (32, "31 = GPIO 12"),
    (33, "33 = GPIO 13"),
    (35, "35 = GPIO 19"),
    (36, "36 = GPIO 16"),
    (37, "37 = GPIO 26"),
    (38, "38 = GPIO 20"),
    (40, "40 = GPIO 21"),
)

# Laptimer or sensor hardware
HARDWARE_RPI_REV1 = "RPI_REV1"
HARDWARE_RPI_REV2 = "RPI_REV2"
HARDWARE_RPI_BPLUS = "RPI_B+"
HARDWARE_TEST = "TEST"  # Virtual emulation on dev/test box
OPTIONS_HARDWARE = (
    (HARDWARE_RPI_REV1, "Raspberry Pi Model B Revision 1.0", RPI_GPIO_REV1),
    (HARDWARE_RPI_REV2, "Raspberry Pi Model A/B Revision 2.0", RPI_GPIO_REV2),
    (HARDWARE_RPI_BPLUS, "Raspberry Pi Model B+", RPI_GPIO_BPLUS),
    (HARDWARE_TEST, "Virtual (software triggered events)", ()),
)
