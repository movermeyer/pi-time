# Code based on Crossbar.io checkconfig.py (with thanks!:)
import json
import logging
import os

import pytz
import six

from autobahn.websocket.protocol import parseWsUrl

from twisted.python import log

from pi_time import settings


def check_name(config, section, required=False):
    if 'name' in config:
        name = config['name']
        if type(name) != six.text_type:
            raise TypeError("'name' in {} configuration must be str, "
                            "but got {}".format(section, type(name).__name__))
    else:
        if required:
            raise ValueError("'name' required in {} configuration"
                             .format(section))


def check_url(config, section):
    if 'url' in config:
        url = config['url']
        if type(url) != six.text_type:
            raise TypeError("'url' in {} configuration must be str, "
                            "but got {}".format(section, type(url).__name__))
        try:
            parseWsUrl(url)
        except Exception as e:
            raise ValueError("Invalid 'url' in {} configuration: {}".format(
                section, e))
    else:
        raise ValueError("'url' required in {} configuration"
                         .format(section))


def check_hardware(config, section):
    if 'hardware' in config:
        hardware = config['hardware']
        hw = zip(*settings.OPTIONS_HARDWARE)[0]
        if hardware not in hw:
            raise ValueError("'hardware' in {} configuration must be {}, "
                             "but got {}".format(section, hw, hardware))


def check_unit_of_measurement(laptimer):
    if 'unitOfMeasurement' in laptimer:
        unit = laptimer['unitOfMeasurement']
        units = zip(*settings.OPTIONS_UNIT_OF_MEASUREMENT)[0]
        if unit not in units:
            raise ValueError("'unitOfMeasurement' in laptimer configuration "
                             "must be {}, but got {}".format(units, unit))


def check_timezone(laptimer):
    if 'timezone' in laptimer:
        timezone = laptimer['timezone']
        if timezone not in pytz.common_timezones:
            raise ValueError("'timezone' in laptimer configuration must be "
                             "valid timezone, but got {}".format(timezone))


def check_pin(config, pin_name):
    if pin_name not in config:
        return
    pin = config[pin_name]
    if type(pin) not in six.integer_types:
        raise TypeError("'{}' in sensor configuration must be "
                        "integer, but got {}".format(pin, type(pin).__name__))
    if 'hardware' in config:
        # Safe to assume hardware has already been checked
        hardware = config['hardware']
        # Ignore test hardware as it has no pins and any existing pin
        # configuration should remain to avoid re-entry
        if hardware == settings.HARDWARE_TEST:
            return
        for n, hw in enumerate(settings.OPTIONS_HARDWARE):
            if hw[0] == hardware:
                pins = zip(*hw[2])[0]
                if pin not in pins:
                    raise ValueError("'{}' in sensor configuration invalid for "
                                     "'{}' hardware, must be {}, but got {}"
                                     .format(pin_name, hardware, pins, pin))
    else:
        raise ValueError("'hardware' in sensor configuration must be "
                         "specified if setting pin")


def check_sensor_location(sensor):
    if 'location' in sensor:
        location = sensor['location']
        locations = zip(*settings.OPTIONS_SENSOR_LOCATION)[0]
        if location not in locations:
            raise ValueError("'location' in sensor configuration must be {}, "
                             "but got {}".format(locations, location))


def check_sensor_position(sensor):
    if 'position' in sensor:
        position = sensor['position']
        if type(position) not in six.integer_types:
            raise TypeError("'position' in sensor configuration must be "
                            "integer, but got {}"
                            .format(type(position).__name__))
        if position <= 0:
            raise ValueError("'position' in sensor configuration must be "
                             "greater than zero".format(position))


def check_laptimer(laptimer):
    """
    Check a laptimer configuration item.

    :param laptimer: The laptimer configuration to check.
    :type laptimer: dict
    :returns: Laptimer configuration in dictionary format.
    :rtype: dict
    """
    for key in laptimer:
        if key not in ['name', 'url', 'hardware', 'unitOfMeasurement',
                       'timezone']:
            raise ValueError("Unknown attribute '{}' in laptimer "
                             "configuration".format(key))

    check_name(laptimer, 'laptimer')
    check_url(laptimer, 'laptimer')
    check_hardware(laptimer, 'laptimer')
    check_unit_of_measurement(laptimer)
    check_timezone(laptimer)
    check_pin(laptimer, settings.PIN_LED_APP[0])
    check_pin(laptimer, settings.PIN_LED_LAP[0])

    return laptimer


def check_sensor(sensor):
    """
    Check a sensor configuration item.

    :param sensor: The sensor configuration to check.
    :type sensor: dict
    :returns: Sensor configuration in dictionary format.
    :rtype: dict
    """
    if type(sensor) != dict:
        raise TypeError("Sensor items must be dictionaries, but got {}"
                        .format(type(sensor)))

    for key in sensor:
        if key not in ['name', 'url', 'hardware', 'location',
                       settings.PIN_LED_APP[0], settings.PIN_LED_LAP[0],
                       settings.SENSOR_PIN_LED_EVENT[0], settings.SENSOR_PIN_EVENT[0]]:
            raise ValueError("Unknown attribute '{}' in sensor configuration"
                             .format(key))

    check_name(sensor, 'sensor', True)
    check_url(sensor, 'sensor')
    check_hardware(sensor, 'sensor')
    check_sensor_location(sensor)
    check_sensor_position(sensor)
    check_pin(sensor, settings.PIN_LED_APP[0])
    check_pin(sensor, settings.PIN_LED_LAP[0])
    check_pin(sensor, settings.SENSOR_PIN_LED_EVENT[0])
    check_pin(sensor, settings.SENSOR_PIN_EVENT[0])

    return sensor


def check_config(config):
    """
    Check a pi-time top-level configuration.

    :param config: The configuration to check.
    :type config: dict
    """

    if type(config) != dict:
        raise TypeError(
            "Top-level configuration item must be a dictionary, but got {}"
            .format(type(config)))

    for key in config:
        if key not in ['laptimer', 'sensors']:
            raise ValueError("Unknown attribute '{}' in top level "
                             "configuration".format(key))

    # check laptimer config
    if 'laptimer' in config:
        check_laptimer(config['laptimer'])
        log.msg('Configuration ok for laptimer', logLevel=logging.DEBUG)

    # check sensors config
    sensors = config.get('sensors', [])

    if type(sensors) != list:
        raise TypeError("'sensors' attribute in top-level configuration "
                        "must be a list, but got {}".format(type(sensors)))

    for sensor in sensors:
        check_sensor(sensor)
        log.msg("Configuration ok for sensor '{}'".format(sensor['name']),
                logLevel=logging.DEBUG)


def check_config_file(config_file):
    """
    Check a pi-time configuration file.

    :param config_file: Name of configuration file to check.
    :type config_file: str
    :returns: Configuration in dictionary format.
    :rtype: dict
    """
    log.msg("Checking configuration '{}'".format(config_file),
            logLevel=logging.DEBUG)

    config_file = os.path.abspath(config_file)
    config = {}

    with open(config_file, 'rb') as infile:
        try:
            config = json.load(infile)
        except ValueError as e:
            raise Exception("Configuration file '{}' does not seem to be "
                            "proper JSON ({})".format(config_file, e))

    check_config(config)

    return config
