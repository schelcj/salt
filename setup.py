#!/usr/bin/python2
'''
The setup script for salt
'''

import os
import sys
from glob import glob
from distutils.core import setup, Extension
from distutils.command.sdist import sdist
from distutils import log
from distutils.cmd import Command
from distutils.core import setup
from distutils.sysconfig import get_python_lib, PREFIX

from salt import __version__

try:
    from Cython.Distutils import build_ext
    import Cython.Compiler.Main as cython_compiler
    have_cython = True
except ImportError:
    from distutils.command.build_ext import build_ext
    have_cython = False


NAME = 'salt'
VER = __version__
DESC = ('Portable, distributed, remote execution and '
        'configuration management system')
mod_path = os.path.join(get_python_lib(), 'salt/modules')
doc_path = os.path.join(PREFIX, 'share/doc', NAME + '-' + VER)
example_path = os.path.join(doc_path, 'examples')
template_path = os.path.join(example_path, 'templates')

if 'SYSCONFDIR' in os.environ:
    etc_path = os.environ['SYSCONFDIR']
else:
    etc_path = os.path.join(os.path.dirname(PREFIX), 'etc')

# take care of extension modules.
if have_cython:
    sources = ['salt/msgpack/_msgpack.pyx']

    class Sdist(sdist):
        def __init__(self, *args, **kwargs):
            for src in glob('salt/msgpack/*.pyx'):
                cython_compiler.compile(glob('msgpack/*.pyx'),
                                        cython_compiler.default_options)
            sdist.__init__(self, *args, **kwargs)
else:
    sources = ['salt/msgpack/_msgpack.c']

    Sdist = sdist

libraries = ['ws2_32'] if sys.platform == 'win32' else []

msgpack_mod = Extension('salt.msgpack._msgpack',
                        sources=sources,
                        libraries=libraries,
                        )

setup(
      name=NAME,
      version=VER,
      description=DESC,
      author='Thomas S Hatch',
      author_email='thatch45@gmail.com',
      url='http://saltstack.org',
      cmdclass={'build_ext': build_ext, 'sdist': Sdist},
      ext_modules=[msgpack_mod],
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Cython',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Clustering',
          'Topic :: System :: Distributed Computing',
          ],
      packages=['salt',
                'salt.cli',
                'salt.ext',
                'salt.grains',
                'salt.modules',
                'salt.renderers',
                'salt.returners',
                'salt.runners',
                'salt.states',
                'salt.utils',
                'salt.msgpack',
                ],
      scripts=['scripts/salt-master',
               'scripts/salt-minion',
               'scripts/salt-syndic',
               'scripts/salt-key',
               'scripts/salt-cp',
               'scripts/salt-call',
               'scripts/salt-run',
               'scripts/salt'],
      data_files=[(os.path.join(etc_path, 'salt'),
                    ['conf/master',
                     'conf/minion',
                    ]),
                ('share/man/man1',
                    ['doc/man/salt-master.1',
                     'doc/man/salt-key.1',
                     'doc/man/salt.1',
                     'doc/man/salt-cp.1',
                     'doc/man/salt-call.1',
                     'doc/man/salt-syndic.1',
                     'doc/man/salt-run.1',
                     'doc/man/salt-minion.1',
                    ]),
                ('share/man/man7',
                    ['doc/man/salt.7',
                    ]),
                (mod_path,
                    ['salt/modules/cytest.pyx',
                    ]),
                (doc_path,
                    ['LICENSE'
                    ]),
                 ],
     )
