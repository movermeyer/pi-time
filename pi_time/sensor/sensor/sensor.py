import pi_time

from os import path

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError

from twisted.internet.defer import inlineCallbacks
from twisted.python import log

from pi_time import settings
from pi_time.api import Api
from pi_time.models.api import ApiRequest


class SensorAppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        config_dir = path.dirname(path.dirname(path.realpath(__file__)))
        config_file = path.join(config_dir, 'config.json')
        api = Api(session=self, config_file=config_file)
        prefix = settings.URI_PREFIX

        reg_options = yield self.register(api.get_sensor_options,
            prefix + 'get_sensor_options')
        reg_config = yield self.register(api.get_sensor_config,
            prefix + 'get_sensor_config')

        log.msg('Pi-time sensor v{} ready'.format(pi_time.VERSION))
