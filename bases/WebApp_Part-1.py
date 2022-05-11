from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server

class HelloWorld(TGController):
	@expose()
	def index(self):
		return("Matheus become Chimpanzé")

if(__name__ == '__main__'):
	config = AppConfig(minimal=True, root_controller=HelloWorld())
	application = config.make_wsgi_app()
	httpd = make_server('',8080, application)
	httpd.serve_forever()