from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server

#http://localhost:8080/

class MultiPages(TGController):
	@expose()
	def index(self):
		return('Welcome to the multi page webapp!')

	#O site abre, pois não há parâmetros sem valor;
	@expose()
	def add(self, a=0, b=0):
		a = int(a)
		b = int(b)
		return(f"{a} + {b} = {a+b}")

	#O site não abre, pois não há valores para 'a' e 'b';
	@expose()
	def multiply(self, a, b):
		a = int(a)
		b = int(b)
		return(f"{a} * {b} = {a*b}")

if(__name__ == '__main__'):
	config = AppConfig(minimal=True, root_controller=MultiPages())
	application = config.make_wsgi_app()
	httpd = make_server('',8080, application)
	httpd.serve_forever()