
import os


def run_node():
    from .config import DemoNodeConfig
    nodeconfig = DemoNodeConfig()

    from ebs.iot.linuxnode import config
    config.current_config = nodeconfig

    os.environ['KIVY_TEXT'] = 'pango'

    if nodeconfig.platform == 'rpi':
        os.environ['KIVY_BCM_DISPMANX_LAYER'] = str(nodeconfig.app_dispmanx_layer)
        os.environ['KIVY_WINDOW'] = 'egl_rpi'
        print("Using app_dispmanx_layer {0}".format(nodeconfig.app_dispmanx_layer))
        
    if nodeconfig.fullscreen is True:
        from kivy.config import Config
        Config.set('graphics', 'fullscreen', 'auto')

    from kivy.support import install_twisted_reactor
    install_twisted_reactor()

    from .demo import DemoApplication
    print("Starting Application")
    DemoApplication(config=nodeconfig).run()
