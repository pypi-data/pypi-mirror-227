from setuptools import setup, find_packages
import os

# requirments = os.open("/var/labsstorage/home/jevaa_kharthik/.local/bin/pipreqs media_jk --print").read().splitlines()

with open('/home/jevaa_kharthik/pythoncli/mediaquery_pkg/mediaquery/requirements.txt', 'r') as f:
    requirments = f.read().splitlines()

with open("README.md", 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(

    name='media_jk',
    version='0.3.6',
    packages=find_packages(),
    author='Jevaa Kharthik N',
    author_email='jevaasureka@gmail.com',
    description='Media_jk is a Wrapper of Mediainfo',
    url= 'https://git.selfmade.ninja/jevaa_kharthik/media_jk',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
            requirments
    ],
    entry_points={
        'console_scripts': [
            'media_jk = media_jk.media_jk:main'
        ],
    },
    
)
    