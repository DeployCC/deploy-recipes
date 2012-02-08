#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Deploy for Humans
    _________________
    
    This recipe will prepare percona from source for cooking.
    
    :copyright: (c) 2012 by Jair Gaxiola 
    :license: GPLv3
"""

from deploy.recipes.base import Recipe
from deploy.env import globals

class Percona(Recipe):
    
    info = {'name':'Percona-Server', 'version':'5.5.19-rel24.0'}
    prefix = "%(prefix)s"  % globals + "/%(name)s/" % info
    socket_path = prefix + '/mysql.sock'
    
    def prepare(r):
        r.source('http://www.percona.com/redir/downloads/Percona-Server-5.5/Percona-Server-5.5.19-24.0/source/%(name)s-%(version)s.tar.gz', r.info)
        r.preCompile('BUILD/autorun.sh; ')
        r.configure( \
                    flags = 'CFLAGS="-arch x86_64 -Wall -Wextra -Wunused -Wwrite-strings -mtune=native -m64 -DUNIV_MUST_NOT_INLINE -DEXTRA_DEBUG -DFORCE_INIT_OF_VARS  -DSAFE_MUTEX -O1 -g3 -gdwarf-2 CXXFLAGS="-arch x86_64 -Wall -Wextra -Wunused -Wwrite-strings -Wno-unused-parameter -Wnon-virtual-dtor -felide-constructors -fno-exceptions -fno-rtti -mtune=native -m64 -DUNIV_MUST_NOT_INLINE -DEXTRA_DEBUG -DFORCE_INIT_OF_VARS  -DSAFE_MUTEX -O2 -g3 -gdwarf-2; ' % r.info, \
                    options = { \
                        'prefix': r.prefix
                        }, \
                    with_value = { \
                        'extra-charsets': 'complex',
                        'unix-socket-path': r.socket_path,
                        'charset':'latin1',
                        'collation': 'latin1_general_ci',
                        'mysqld-user': '_mysql',
                        'plugins': 'max',
                        }, \
                    without_value = { \
                        'big-tables': 'big-tables',
                        'ssl': 'ssl',
                        'readline': 'readline',
                        'debug': 'debug'
                        }, \
                    enable = { \
                    	'thread-safe-client': 'thread-safe-client',
            			'local-infile': 'local-infile',
            			'shared': 'shared',
            			'assembler': 'assembler'}, \
                    disable = { \
                        'dependency-tracking': 'dependency-tracking',
            			'mysql-maintainer-mode': 'mysql-maintainer-mode'
            			}
                    )
        r.make()
        r.makeInstall()
        
        after = 'cd %(path)s' % globals + '%(name)s-%(version)s; cp support-files/my-small.cnf ' % r.info + r.prefix + 'my.cnf;'
    	after += 'cd ' + r.prefix + ';scripts/mysql_install_db'

        r.postCompile(after)

if __name__ == "__main__":
    r = Percona()
    r.prepare()