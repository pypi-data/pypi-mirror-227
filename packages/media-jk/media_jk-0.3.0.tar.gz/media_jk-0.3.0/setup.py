from setuptools import setup, find_packages

with open('/home/jevaa_kharthik/pythoncli/mediaquery_pkg/mediaquery/requirements.txt', 'r') as f:
    requirments = f.read().splitlines()

setup(

    name='media_jk',
    version='0.3.0',
    packages=find_packages(),
    author='Jevaa Kharthik N',
    author_email='jevaasureka@gmail.com',
    description='Media_jk is a Wrapper of Mediainfo',
    url= 'https://git.selfmade.ninja/jevaa_kharthik/media_jk',
    install_requires=[
            requirments
    ],
    entry_points={
        'console_scripts': [
            'media_jk = media_jk.media_jk:main'
        ],
    },
    
)
    