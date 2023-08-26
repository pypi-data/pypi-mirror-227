from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'A package allowing you to use multiple AI Modals for free!'

# Setting up
setup(
    name="freechat",
    version=VERSION,
    author="Cannonball Chris",
    author_email="cannonballchris8@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="A package allowing you to use multiple AI Modals for free! It's still in development and official release will be soon! Join our discord server: https://discord.gg/sj2c7gzPzE for more information!",
    packages=find_packages(),
    install_requires=['aiohttp'],
    keywords=["freegpt", "gpt", "ai", "free", "freetech"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

