from setuptools import setup, find_packages
from variables import __VERSION__, __DESC__, __URL__, __AUTHOR__

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="upddetect",
    packages=find_packages("upddetect"),
    description=__DESC__,
    version=__VERSION__,
    url=__URL__,
    author=__AUTHOR__,
    author_email="mail@ksotik.com",
    keywords=["upddetect", "packages updates", "outdated list", "security updates", "new versions",
              "security patches list", "updates detection", "search updates"],
    include_package_data=True,
    install_requires=required
)
