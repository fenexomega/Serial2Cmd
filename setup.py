from setuptools import setup

setup(name="serial2cmd",
        version='0.1.0',
        author='Jordy Ferreira',
        license='GPLv3',
        url='https://github.com/fenexomega/serial2cmd',
        keywords='serial python shell commands',
        packages=['serial2cmd'],
        entry_points={
        'gui_scripts':[
            'serial2cmd = serial2cmd.ui:main'
            ]
        },
#        install_requires=['pyqt5','pyserial'],
        data_files=[
            ('share/icons/hicolor/scalable/apps', ['serial2cmd.svg']),
            ('share/applications/',['serial2cmd.desktop']),
            ('share/serial2cmd/',['config.json']),
            ('share/serial2cmd/icons/', ['icons/icon128.png','icons/icon32.png'])
            ],
        classifiers=[
         # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Users',
        'Topic :: Serial Comunication ',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GPLv3 License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ])
