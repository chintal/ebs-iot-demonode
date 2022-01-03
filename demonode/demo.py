

from random import shuffle

from kivy.app import App
from twisted.internet import reactor

from functools import partial
from datetime import datetime
from datetime import timedelta
from twisted.web.client import ResponseFailed
from twisted.internet.task import deferLater
from ebs.iot.linuxnode.http import swallow_http_error
from ebs.iot.linuxnode.events import WebResourceEventManager
from ebs.iot.linuxnode.events import TextEventManager
from ebs.iot.linuxnode.events import WEBRESOURCE
from ebs.iot.linuxnode.events import TEXT

from ebs.iot.linuxnode.basenode import BaseIoTNode
from ebs.iot.linuxnode.basenode import BaseIoTNodeGui
from ebs.iot.linuxnode.mediaplayer import MediaPlayerGuiMixin
from ebs.iot.linuxnode.mediaplayer import MediaPlayerMixin
from ebs.iot.linuxnode.events import EventManagerMixin
from ebs.iot.linuxnode.events import ScheduledResourceClass
from ebs.iot.linuxnode.gallery import GalleryMixin
from ebs.iot.linuxnode.gallery import GalleryGuiMixin
from ebs.iot.linuxnode.browser import BrowserMixin
from ebs.iot.linuxnode.browser import BrowserGuiMixin


class DemoNode(BrowserMixin, GalleryMixin, EventManagerMixin, MediaPlayerMixin, BaseIoTNode):
    _appname = "demonode"

    _language_tests = {
        'English': 'English Keyboard',
        'Hindi': 'हिंदी कीबोर्ड',
        'Telugu': 'తెలుగులో టైప్',
        'Kannada': 'ಕನ್ನಡ ಕೀಲಿಮಣೆ',
        'Tamil': 'தமிழ் விசைப்பலகை',
        'Marathi': 'मराठी कळफलक',
        'Bengali': 'বাংলা কিবোর্ড',
        'Malyalam': 'മലയാളം കീബോര്‍ഡ്',
        'Punjab': 'ਪੰਜਾਬੀ ਦੇ ਬੋਰਡ',
        'Oriya': 'ଉତ୍କଳଲିପି',
        'Urdu': 'اردوبورڈ',
    }

    _test_resources = [
        'v1.mp4',
        'v2.mp4',
        'v3.mp4',
        'v4.mp4',
    ]

    _test_pdfs = [
        'p1.pdf',
    ]

    _gallery_resources = [
        '1.jpeg',
        '2.jpeg',
        '3.jpeg',
        '4.jpeg',
        '5.jpeg',
        '6.jpeg',
    ]

    def __init__(self, *args, **kwargs):
        kwargs['resource_class'] = ScheduledResourceClass
        super(DemoNode, self).__init__(*args, **kwargs)

    def install(self):
        super(DemoNode, self).install()
        self.event_manager_install(WebResourceEventManager(self, WEBRESOURCE))
        self.event_manager_install(TextEventManager(self, TEXT))

    def _demo_busy(self):
        self.busy_set()
        self._reactor.callLater(15, self.busy_clear)

    def _demo_marquee_language(self):
        s = ''
        for lang in self._language_tests:
            s += '{0}: {1} | '.format(lang, self._language_tests[lang])
        self.reactor.callLater(10, self.marquee_play, s, 1000)

    def _demo_marquee(self):
        self.marquee_play("Lorem Ipsum", 10)
        mt = ', '.join(self._test_resources)
        self._reactor.callLater(13, self.marquee_play, mt, 30)

    def _demo_overlay(self):
        def _enter_overlay():
            self.overlay_mode = True
        self._reactor.callLater(25, _enter_overlay)

        def _exit_overlay():
            self.overlay_mode = False
        self._reactor.callLater(45, _exit_overlay)

    def _demo_sidebar_right(self, after=17):
        def _show_sidebar_right():
            print("Showing Right Sidebar")
            self.gui_sidebar_right_show()

        def _hide_sidebar_right():
            print("Hiding Right Sidebar")
            self.gui_sidebar_right_hide()

        self._reactor.callLater(after, _show_sidebar_right)
        self._reactor.callLater(after + 10, _hide_sidebar_right)

    def _demo_http_get(self):
        def _http_get_callback(response):
            url = response.request.absoluteURI
            self.log.info("Got HTTP GET response from {url}", url=url)
            _ = response.content

        d1 = self.http_get("http://httpstat.us/404")
        d1.addCallbacks(_http_get_callback, swallow_http_error)

        d2 = self.http_get("https://www.google.com")
        d2.addCallbacks(_http_get_callback, swallow_http_error)

    def _demo_http_download(self):
        def _http_download():
            def _http_download_callback(_, url):
                self.log.info(
                    "Done HTTP download for {url}", url=url
                )

            test_url4 = "http://speedtest.ftp.otenet.gr/files/test1M.db"
            d = self.http_download(test_url4, '')
            d.addCallbacks(
                partial(_http_download_callback, url=test_url4),
                swallow_http_error
            )

            test_url3 = "http://speedtest.ftp.otenet.gr/files/test10Mb.db"
            d = self.http_download(test_url3, '')
            d.addCallbacks(
                partial(_http_download_callback, url=test_url3),
                swallow_http_error
            )

            def _retry_hook(failure):
                failure.trap(ResponseFailed)
                print("At Retry Hook")
            d.addErrback(_retry_hook)

        self._reactor.callLater(8, _http_download)

    def _demo_shell(self):
        def _handle_result(result):
            print(result.strip())
        d = self._shell_execute(['iwgetid', '-s'], _handle_result)

    def _demo_resource_manager(self):
        def _resource_manager_test():
            # self.resource_manager.insert(
            #     'testfile', 'http://speedtest.ftp.otenet.gr/files/test10Mb.db'
            # )
            # resource = self.resource_manager.get('testfile')
            # self.resource_manager.prefetch(resource)

            for r in self._test_resources:
                url = 'http://static.chintal.in/starxmedia/demo/{0}'.format(r)
                self.resource_manager.insert(r, url=url)
                # resource = self.resource_manager.get(r)
                # d = self.resource_manager.prefetch(resource)

            for r in self._gallery_resources:
                url = 'http://static.chintal.in/starxmedia/demo/{0}'.format(r)
                self.resource_manager.insert(r, url=url)

            for r in self._test_pdfs:
                url = 'http://static.chintal.in/starxmedia/demo/{0}'.format(r)
                self.resource_manager.insert(r, url=url)

            # def _play_media(*args, **kwargs):
            #     content = kwargs.pop('content')
            #     return self.media_play(content, duration=60, loop=True)
            # d.addCallback(_play_media, content=resource)
            # return d

        return deferLater(self._reactor, 5, _resource_manager_test)

    def _create_demo_events(self, offset=0, resources=None):
        if not resources:
            resources = self._test_resources
        runslot = list(range(len(resources)))
        shuffle(runslot)
        perslot = 120
        n = datetime.now() + timedelta(seconds=offset * perslot)
        n += timedelta(seconds=3)
        for idx in range(len(resources)):
            eid = 'e{0}'.format(runslot[idx] + offset)
            self.event_manager(WEBRESOURCE).insert(
                eid, etype=WEBRESOURCE, start_time=n, duration=100,
                resource=resources[runslot[idx]]
            )
            n = n + timedelta(seconds=perslot)

    def _create_demo_text_events(self, offset=1):
        langs = list(self._language_tests.keys())
        runslot = list(range(len(langs)))
        shuffle(runslot)
        perslot = 30
        n = datetime.now() + timedelta(seconds=offset * perslot)
        for idx in range(len(self._language_tests)):
            eid = 't{0}'.format(runslot[idx] + offset)
            lang = langs[runslot[idx]]
            self.event_manager(TEXT).insert(
                eid, etype=TEXT, start_time=n, duration=20,
                resource='{0}: {1}'.format(lang, self._language_tests[lang])
            )
            n = n + timedelta(seconds=perslot)

    def _demo_event_manager(self):
        print("Starting Event Manager Demo")
        # self._create_demo_events()
        self._create_demo_events(resources=self._test_pdfs + self._test_resources)
        self.event_manager(WEBRESOURCE).start()
        self._create_demo_text_events(0)
        self.event_manager(TEXT).start()

        self.event_manager(WEBRESOURCE).prune()
        self.event_manager(TEXT).prune()
        # self.event_manager(WEBRESOURCE).render()
        # self.event_manager(TEXT).render()

        # Pointers test
        # print("PREV : ", self.event_manager(WEBRESOURCE).previous())
        # print("PREV, FOLLOW : ", self.event_manager(WEBRESOURCE).previous(follow=True))
        #
        # print("NEXT : ", self.event_manager(WEBRESOURCE).next())
        # print("NEXT, FOLLOW : ", self.event_manager(WEBRESOURCE).next(follow=True))
        #
        # print("NEXT PhonyLightElk.webm : ",
        #       self.event_manager(WEBRESOURCE).next(resource='PhonyLightElk.webm'))
        # print("NEXT PhonyLightElk.webm, FOLLOW: ",
        #       self.event_manager(WEBRESOURCE).next(resource='PhonyLightElk.webm', follow=True))

        # next_use test
        # for x in self.resource_manager.cache_files:
        #     print(self.resource_manager.get(x).next_use, x)

    def _populate_demo_gallery(self):
        self.gallery_load([(x, None) for x in self._gallery_resources])

    def _demo_gallery(self):
        print("Starting Gallery Demo")
        self._populate_demo_gallery()
        self.gallery_start()
        self._reactor.callLater(30, self.gallery_stop)
        self._reactor.callLater(61, self.gallery_start)
        self._reactor.callLater(90, self.gallery_stop)
        self._reactor.callLater(110, self.gallery_start)
        self._reactor.callLater(130, self.gallery_stop)
        self._reactor.callLater(150, self.gallery_start)
        self._reactor.callLater(180, self.gallery_stop)
        self._reactor.callLater(210, self.gallery_start)
        self._reactor.callLater(240, self.gallery_stop)
        self._reactor.callLater(270, self.gallery_start)
        self._reactor.callLater(300, self.gallery_stop)
        self._reactor.callLater(350, self.gallery_start)

    def _demo_browser(self):

        def _browser_start():
            print("Starting Browser Demo  (in sidebar)")
            self.browser_start()

        def _browser_target():
            print("Changing browser target")
            self.browser.target = 'http://youtube.com'

        def _browser_stop():
            print("Closing browser")
            self.browser_stop()

        self._reactor.callLater(30, _browser_start)
        self._reactor.callLater(40, _browser_target)
        self._reactor.callLater(60, _browser_stop)
        self._reactor.callLater(90, _browser_start)

    def start(self):
        super(DemoNode, self).start()
        # self._demo_marquee_language()
        # self._demo_marquee()
        # self._demo_busy()
        # self._demo_overlay()
        # self._demo_sidebar_left()
        # self._demo_sidebar_right()
        # self._demo_http_get()
        # self._demo_http_download()
        # self._demo_shell()
        d = self._demo_resource_manager()
        d.addCallback(lambda _: print("Finished Resource Manager Demo"))
        d.addCallback(lambda _: self._demo_event_manager())
        d.addCallback(lambda _: self._demo_gallery())
        # d.addCallback(lambda _: self._demo_browser())

    def stop(self):
        super(DemoNode, self).stop()


class DemoNodeGui(BrowserGuiMixin, GalleryGuiMixin, MediaPlayerGuiMixin,
                  BaseIoTNodeGui, DemoNode):
    _gui_color_1 = (0x6d / 255., 0xc0 / 255., 0x66 / 255., 1)
    _gui_color_2 = (0xff / 255., 0x00 / 255., 0x00 / 255., 1)
    _gui_supports_overlay_mode = True

    def __init__(self, *args, **kwargs):
        super(DemoNodeGui, self).__init__(*args, **kwargs)

    def gui_setup(self):
        super(DemoNodeGui, self).gui_setup()
        return self.gui_root


class DemoApplication(App):
    def __init__(self, config, *args, **kwargs):
        self._config = config
        self._debug = kwargs.pop('debug', False)
        super(DemoApplication, self).__init__(*args, **kwargs)
        self._node = None

    def build(self):
        print("Constructing Node")
        self._node = DemoNodeGui(reactor=reactor, application=self)
        print("Installing Node Resources")
        self._node.install()
        print("Building GUI for node {0}".format(self._node))
        return self._node.gui_setup()

    def on_start(self):
        self._node.start()

    def on_stop(self):
        self._node.stop()

    def on_pause(self):
        pass
