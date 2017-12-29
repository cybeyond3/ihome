# encoding: utf-08

import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os
import torndb
import redis
import config

from handlers import Passport
from urls import urls
from tornado.options import options, define
from tornado.web import RequestHandler, Application


define('port', default=8000, type=int, help='Run server on the given port.')


class Application(Application):

	def __init__(self, *args, **kwargs):
		super(Application, self).__init__(*args, **kwargs)
		self.db = torndb.Connection(**config.mysql_options)
		self.redis = redis.StrictRedis(**config.redis_options)


def main():
	options.log_file_profix = config.log_path
	options.logging = config.log_level
	tornado.options.parse_command_line()
	app = Application(
		urls,
		**config.settings,
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()
