#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Deploy for Humans
	_________________
	
	This recipe will prepare nginx from source for cooking.
	
	:copyright: (c) 2012 by Jair Gaxiola 
	:license: GPLv3
"""

from deploy.recipes.base import Recipe
from deploy.env import globals

class Nginx(Recipe):
	info = {'name':'nginx', 'version':'1.1.14'}
	prefix = "%(path)s"  % globals + "configure/%(name)s/" % info
	sbin_path = prefix
	conf_path = prefix + '%(name)s.conf' % info
	pid_path = '/tmp/nginx'
	pcre_path = '/Applications/MNPP/src/pcre-8.11/'
		
	def prepare(r):
		r.source("http://nginx.org/download/%(name)s-%(version)s.tar.gz", r.info)
		r.configure(options = { \
							'prefix': r.prefix, \
							'sbin-path': r.sbin_path, \
							'conf-path': r.conf_path, \
							'user': 'www', \
							'group': 'www', \
							'pid-path': r.pid_path, \
						},
						with_value = { \
							'pcre': r.pcre_path \
						},
						without_value = { \
							'http_gzip_static_module': 'http_gzip_static_module', \
							'http_ssl_module': 'http_ssl_module', \
							'http_stub_status_module': 'http_stub_status_module' \
						}
						)
	
		r.make()
		r.makeInstall()

if __name__ == "__main__":
	r = Nginx()
	r.prepare()


