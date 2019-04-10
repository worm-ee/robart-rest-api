from distutils.core import setup
setup(
  name = 'robart',
  packages = ['robart'], 
  version = '0.1.0',
  description = 'API for the Robart MyVacBot',
  author = 'Mattias Welponer',
  author_email = 'mattias@welponer.net',
  url = 'https://github.com/mxworm/robart-rest-api', 
  download_url = 'https://github.com//mxworm/robart/tarball/0.1.0', 
  keywords = ['robart', 'myvacbot'], 
  classifiers = [],
  install_requires = ["requests", "websocket-client", "future"]
)
