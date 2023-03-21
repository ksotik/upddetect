from setuptools import setup
from src.variables import __VERSION__, __DESC__, __URL__, __AUTHOR__

setup(
    name="upddetect",
    packages=["src"],
    entry_points={
        'console_scripts': [
            'upddetect=src.upddetect:main'
        ]
    },
    description=__DESC__,
    version=__VERSION__,
    url=__URL__,
    author=__AUTHOR__,
    author_email="mail@ksotik.com",
    keywords=["upddetect", "packages updates", "outdated list", "security updates", "new versions",
              "security patches list", "updates detection", "search updates"],
    include_package_data=True,
    install_requires=['tqdm', 'safety', 'tabulate']
)
