

from random import shuffle

from kivy.app import App
from twisted.internet import reactor

from functools import partial
from datetime import datetime
from datetime import timedelta
from twisted.web.client import ResponseFailed
from twisted.internet.task import deferLater
from ebs.iot.linuxnode.http import swallow_http_error
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
        '045c19c0-93ae-4619-8722-9c1c4708c36d.mp4',
        '0513b4f5-cbda-4983-9f43-6eb20754d3c1.mp4',
        '0f0252e2-ec9c-4992-949d-13d5e7877c3a.mp4',
        '0fce511f-a771-4d45-8d93-140252893675.mp4',
        '15abc6b3-45b2-402d-b41c-2ff9376c78fa.mp4',
        '182529fb-8162-47cd-b56b-b3a42004a415.mp4',
        '18c9a8a8-056e-49c2-9b6c-0a70980c2b25.mp4',
        '21b2bf25-3b6b-45e6-9d11-a585649dc7af.mp4',
        '244495a8-4f5c-44cf-ad7f-2e64c7f9be80.mp4',
        '2aa51517-03b3-4960-9502-36a4b6adf64b.mp4',
        '3d756a79-02b6-49aa-b680-15f374bbd13e.mp4',
        '427873fc-61ac-4da1-a882-f3a7f32a5ad5.mp4',
        '431c1b5c-7613-4c66-a146-6ff81c3909b9.mp4',
        '5037da39-3627-45a0-8eeb-7920f29a5fd3.mp4',
        '55bb7c45-adba-44b3-b54f-ca6ef2ace426.mp4',
        '614ed81c-c94f-4337-baba-e78e45b68858.mp4',
        '69fcd743-0409-4701-a0ce-ebd3f5d76dc7.mp4',
        '6d4ba573-eeaf-48a1-aa24-6a5e8e2487b1.mp4',
        '758a4503-5c20-4b05-9eca-bd49b80f6a5b.mp4',
        '7819b6ff-f3da-4009-b2b9-655cf2742926.mp4',
        '823beae0-bbf7-4653-aee3-92795e95497b.mp4',
        '825dd2ee-fcd5-44a4-99db-8fbb307d3296.mp4',
        '860a427b-7e60-4cfc-891d-1f1d1a38f5c8.mp4',
        '89e3ccfc-4706-4adc-922f-7bdf2c32016d.mp4',
        '8bce1255-5a17-4525-8ad0-730d308d7a92.mp4',
        '8f188a0b-e84e-494c-af3e-e487df51a591.mp4',
        '9ee148b5-2f43-4cf7-92cf-201152263a39.mp4',
        'a20ffc3c-35aa-4cda-b014-e70576c37b59.mp4',
        'a21dc268-e8f9-4356-b296-92c23c93a2a6.mp4',
        'a67963b9-4770-451e-b7f9-988b88b85da7.mp4',
        'aa18a73d-619d-49f5-94f1-575967465927.mp4',
        'ac2e5aed-a2a9-4b95-9da9-1c13bc8e721b.mp4',
        'b5205608-74be-41d7-9365-cc6653039dd1.mp4',
        'b7549578-9a0d-4e11-a180-7ccca73fc9f4.mp4',
        'b952fd66-30af-4e69-8782-f7e62c4437e1.mp4',
        'babdea8e-ba67-4baa-9f10-9228f93bd28b.mp4',
        'ca2cb7ef-4d82-41ca-a22d-088daeb0b1c8.mp4',
        'cb614c0e-790d-4621-b2d1-64ca0eada0e8.mp4',
        'd576d3b5-6dce-46bf-a9f6-6a7925f7f0fa.mp4',
        'd5fb8ad5-8796-4014-8157-45eaaa68f7f2.mp4',
        'd7c7fe8b-eec3-41bc-827c-6fd593da467d.mp4',
        'd8e35181-015d-457d-ac91-e84cd301e86d.mp4',
        'd954fe64-0e84-4b48-9672-2f93fe0ffd73.mp4',
        'e5c953c2-ad51-4a13-b197-371bba9eeb8d.mp4',
        'e882b4e1-4c33-4290-ab3a-3403bf2abbe7.mp4',
        'efe7688f-cf4b-45c8-9100-0159c31f8a13.mp4',
        'f4bed86e-2353-4b1a-a71a-2529cf018e13.mp4',
        'f4c29eec-b3ed-4ce4-82d3-5a8ecd9878e3.mp4',
        'fab6febf-dfec-4fad-aa66-0e66a834a373.mp4',
        'fd667c90-94aa-498c-9dda-a240822ea191.mp4',
        '244495a8-4f5c-44cf-ad7f-2e64c7f9be80_1436616710868.mp4',
        'a21dc268-e8f9-4356-b296-92c23c93a2a6_1442253708908.mp4',
        'd954fe64-0e84-4b48-9672-2f93fe0ffd73_1436616707051.mp4',
        'fd667c90-94aa-498c-9dda-a240822ea191_1442253723366.mp4',
        'DistantHatefulIndochinesetiger.webm',
        'AccomplishedEdibleAnnelid.webm',
        'GloomyAgreeableEarwig.webm',
        'LimitedFlakyBeardeddragon.webm',
        'PhonyLightElk.webm',
        'WealthyChillyAntarcticfurseal.webm',
    ]

    _gallery_resources = [
        '16932275.jpg',
        '17136221.gif',
        '17393195.jpg',
        '20835472.jpg',
        '8809191e149110a6daa9d4a14ce74ce7.jpg',
        '936897552_MMM0383_123_496lo.jpg',
        'af122.jpg',
        'cross-KamSCixK.1398902331.jpg',
        'IMG-20141005-WA0004.jpg',
        'ldkjshfaksjngflag.jpeg',
        'tumblr_ojky77uDxj1vuenqco1_400.jpg',
        'tumblr_ovclw5HxoX1umhkj9o1_500.jpg',
        'tumblr_owgxp087mF1vlp267o1_400.gif',
        'tumblr_owl8i7CvO91vuootio1_250.gif',
        'tumblr_ncdrk7JuMe1tghbqho1_500.gif',
        'tumblr_ncggdfhY5k1rolakdo1_500.jpg',
        'tumblr_nioai6hSWF1u5ncsao1_1280.jpg',
        'tumblr_nz1dbzQQyU1uy1o4lo1_540.jpg',
        'tumblr_o0hv3lRZ001thdxyvo1_500.jpg',
        'tumblr_o2ee0kcPKD1v5suc0o1_500.jpg',
    ]

    def __init__(self, *args, **kwargs):
        kwargs['resource_class'] = ScheduledResourceClass
        super(DemoNode, self).__init__(*args, **kwargs)

    def _demo_busy(self):
        self.busy_set()
        self._reactor.callLater(15, self.busy_clear)

    def _demo_marquee_language(self):
        s = ''
        for lang in self._language_tests:
            s += '{0}: {1}    |    '.format(lang, self._language_tests[lang])
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

    # def _demo_sidebar_left(self, after=11):
    #     def _show_sidebar_left():
    #         print("Showing Left Sidebar")
    #         self.gui_sidebar_left_show()
    #
    #     def _hide_sidebar_left():
    #         print("Hiding Left Sidebar")
    #         self.gui_sidebar_left_hide()
    #
    #     self._reactor.callLater(after, _show_sidebar_left)
    #     self._reactor.callLater(after + 10, _hide_sidebar_left)

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
                url = 'http://scaffold.longclaw/videos/{0}'.format(r)
                self.resource_manager.insert(r, url=url)
                # resource = self.resource_manager.get(r)
                # d = self.resource_manager.prefetch(resource)

            for r in self._gallery_resources:
                url = 'http://scaffold.longclaw/images/{0}'.format(r)
                self.resource_manager.insert(r, url=url)

            # def _play_media(*args, **kwargs):
            #     content = kwargs.pop('content')
            #     return self.media_play(content, duration=60, loop=True)
            # d.addCallback(_play_media, content=resource)
            # return d

        return deferLater(self._reactor, 5, _resource_manager_test)

    def _create_demo_events(self, offset=0):
        runslot = list(range(len(self._test_resources)))
        shuffle(runslot)
        perslot = 110
        n = datetime.now() + timedelta(seconds=offset * perslot)
        for idx in range(len(self._test_resources)):
            eid = 'e{0}'.format(runslot[idx] + offset)
            self.event_manager(WEBRESOURCE).insert(
                eid, etype=WEBRESOURCE, start_time=n,
                resource=self._test_resources[runslot[idx]]
            )
            n = n + timedelta(seconds=perslot)

    def _create_demo_text_events(self, offset=1):
        langs = list(self._language_tests.keys())
        runslot = list(range(len(langs)))
        shuffle(runslot)
        perslot = 60
        n = datetime.now() + timedelta(seconds=offset * perslot)
        for idx in range(len(self._language_tests)):
            eid = 't{0}'.format(runslot[idx] + offset)
            lang = langs[runslot[idx]]
            self.event_manager(TEXT).insert(
                eid, etype=TEXT, start_time=n, duration=50,
                resource='{0}: {1}'.format(lang, self._language_tests[lang])
            )
            n = n + timedelta(seconds=perslot)

    def _demo_event_manager(self):
        print("Starting Event Manager Demo")
        self._create_demo_events()
        self._create_demo_events(offset=len(self._test_resources))
        self.event_manager(WEBRESOURCE).start()
        self._create_demo_text_events(0)
        self.event_manager(TEXT).start()

        # self.event_manager(WEBRESOURCE).prune()
        # self.event_manager(WEBRESOURCE).render()

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
        self._demo_busy()
        # self._demo_overlay()
        # self._demo_sidebar_left()
        # self._demo_sidebar_right()
        # self._demo_http_get()
        # self._demo_http_download()
        self._demo_shell()
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
        print("Constructing node")
        self._node = DemoNodeGui(
            reactor=reactor, application=self,
            # background_color=(0x20/255., 0x5f/255., 0x60/255., 1)
        )
        print("Building GUI")
        return self._node.gui_setup()

    def on_start(self):
        self._node.start()

    def on_stop(self):
        self._node.stop()

    def on_pause(self):
        pass
