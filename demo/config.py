

import os
import shutil
from appdirs import user_config_dir
from ebs.iot.linuxnode.config import IoTNodeConfig


class DemoNodeConfig(IoTNodeConfig):
    _config_file = os.path.join(user_config_dir('demonode'), 'config.ini')

    @property
    def text_font_name(self):
        font_name = super(DemoNodeConfig, self).text_font_name
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        if os.path.exists(os.path.join(_ROOT, font_name)):
            return os.path.join(_ROOT, font_name)
        return font_name

    @property
    def background(self):
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        return self._config.get(
            'display', 'background',
            fallback=os.path.join(_ROOT, 'images/background.jpg')
        )

    def __init__(self):
        if not os.path.exists(os.path.dirname(self._config_file)):
            os.makedirs(os.path.dirname(self._config_file), exist_ok=True)
        if not os.path.exists(self._config_file):
            _ROOT = os.path.abspath(os.path.dirname(__file__))
            shutil.copy(os.path.join(_ROOT, 'default/config.ini'), self._config_file)
        super(DemoNodeConfig, self).__init__()
