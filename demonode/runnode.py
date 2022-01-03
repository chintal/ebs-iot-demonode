

import faulthandler

import os
from raspi_system import hwinfo


def run_node():
    from .config import DemoNodeConfig
    nodeconfig = DemoNodeConfig()

    from ebs.iot.linuxnode import config
    config.current_config = nodeconfig

    os.environ['KIVY_TEXT'] = 'pango'

    if nodeconfig.platform == 'rpi':
        if hwinfo.is_pi4():
            os.environ['KIVY_WINDOW'] = 'sdl2'
        else:
            os.environ['KIVY_WINDOW'] = 'egl_rpi'
        os.environ['KIVY_BCM_DISPMANX_LAYER'] = str(nodeconfig.app_dispmanx_layer)
        print("Using app_dispmanx_layer {0}".format(nodeconfig.app_dispmanx_layer))

    from kivy.config import Config
    if nodeconfig.fullscreen is True:
        Config.set('graphics', 'fullscreen', 'auto')

    if nodeconfig.orientation:
        Config.set('graphics', 'rotation', nodeconfig.orientation)

    from kivy.support import install_twisted_reactor
    install_twisted_reactor()

    from .demo import DemoApplication
    print("Starting Application")
    DemoApplication(config=nodeconfig, debug=True).run()


if __name__ == '__main__':
    print("Starting faulthandler")
    faulthandler.enable()
    run_node()
