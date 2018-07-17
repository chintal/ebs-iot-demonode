import setuptools

_requires = [
    'ebs-iot-linuxnode>=0.9.3',
    'setuptools-scm'
]

setuptools.setup(
    name='demonode',
    url='',

    author='Chintalagiri Shashank',
    author_email='shashank.chintalagiri@gmail.com',

    description='',
    long_description='',

    packages=setuptools.find_packages(),
    package_data={'demonode': ['default/config.ini',
                               'fonts/FreeSans.ttf',
                               'fonts/ARIALUNI.TTF',
                               'images/background.png']},

    install_requires=_requires,

    setup_requires=['setuptools_scm'],
    use_scm_version=True,

    dependency_links=[
        'git+https://github.com/kivy/kivy.git@master#egg=kivy-1.11.0'
    ],

    entry_points={
          'console_scripts': [
              'demonode = demonode.runnode:run_node'
          ]
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
    ],
)
