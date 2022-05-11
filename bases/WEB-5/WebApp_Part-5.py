from tg import AppConfig, expose, TGController
from wsgiref.simple_server import make_server

class StaticDemo(TGController):
	@expose('WebApp_Template-index.xhtml')
	def index(self):
		return dict(message = 'Welcome to the static demo webapp!')

if __name__ == '__main__':
	config = AppConfig(minimal = True, root_controller= StaticDemo())
	config.renderers.append('kajiki')
	config.serve_static = True
	config.paths['static_files'] = 'static'
	application = config.make_wsgi_app()
	httpd = make_server('',8080, application)
	httpd.serve_forever()