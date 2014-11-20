try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='helloworld',
    version='0.3',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "Pylons>=1.0",
        "Genshi>=0.4",
        "Babel",
        "nose>=1.1",
        "SQLAlchemy>=0.6",
        "requests",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'helloworld': ['i18n/*/LC_MESSAGES/*.mo']},
    message_extractors={'helloworld': [
            ('lib/inspire_vocabulary.py', 'helloworld_vocabularies', None),
            ('**.py', 'python', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)]
    },
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    
    [babel.extractors]

    helloworld_vocabularies = helloworld.lib.babel_extractors:extract_vocabularies

    [nose.plugins]

    pylons = pylons.test:PylonsPlugin
    
    [paste.app_factory]

    main = helloworld.config.middleware:make_app

    [paste.app_install]

    main = pylons.util:PylonsInstaller

    [paste.paster_command]

    hello-echo  = helloworld.commands:Echo
    hello-hello = helloworld.commands:Hello
    hello-init  = helloworld.commands:InitDb
    """,
)
