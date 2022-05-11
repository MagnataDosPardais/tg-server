from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server
import webhelpers2.text

class TruncateDemo(TGController):
	@expose('WebApp_Template-2.xhtml')
	def index(self, tobetruncated='This is going to be truncated!'):
		return dict(tobetruncated=tobetruncated)

if __name__ == '__main__':
	config = AppConfig(minimal = True, root_controller = TruncateDemo())
	config.renderers.append('kajiki')
	config['helpers'] =  webhelpers2
	application = config.make_wsgi_app()
	httpd = make_server('',8080, application)
	httpd.serve_forever()