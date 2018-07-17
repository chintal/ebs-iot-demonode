

def run_node():
    from .config import DemoNodeConfig
    nodeconfig = DemoNodeConfig()

    from ebs.iot.linuxnode import config
    config.current_config = nodeconfig

    if nodeconfig.fullscreen is True:
        from kivy.config import Config
        Config.set('graphics', 'fullscreen', 'auto')

    from kivy.support import install_twisted_reactor
    install_twisted_reactor()

    from .demo import DemoApplication
    print("Starting Application")
    DemoApplication(config=nodeconfig).run()
