import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

setup(
  name = 'whisk_parser',
  packages = ['whisk_parser'],  # this must be the same as the name above
  version = '1.0.0',
  license=open('LICENSE.txt').read(),
  description = 'Parse emails from Vosk API and Whisper.',
  author = 'Neuri',
  author_email = 'support@neuri.ai',
  url = 'https://github.com/Neuri-ai/whisk-parser',  # use the URL to the github repo
  keywords = ['parse', 'emails', 'vosk', 'whisper', 'english' 'spanish'],  # arbitrary keywords
  classifiers = [
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
  ],
  long_description=open_file('README.rst').read(),
  long_description_content_type="text/markdown",
)