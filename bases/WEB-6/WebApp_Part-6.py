from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, DateTime, String

from datetime import datetime

from tg import expose, AppConfig, TGController
from tg.util import Bunch
from wsgiref.simple_server import make_server

DeclarativeBase = declarative_base()
DBSession = scoped_session(sessionmaker(autoflush = True, autocommit = False))

class Log(DeclarativeBase):
	__tablename__ = 'logs'

	uid = Column(Integer, primary_key = True)
	timestamp = Column(DateTime, nullable = False, default = datetime.now)
	person = Column(String(50), nullable = False)

def init_model(engine):
	DBSession.configure(bind = engine)
	DeclarativeBase.metadata.create_all(engine)

class DBDemo(TGController):
	@expose(content_type = 'text/plain')
	def index(self):
		logs = DBSession.query(Log).order_by(Log.timestamp.desc()).all()
		return 'Past Greetings: \n' + '\n'.join(['%s - %s' % (l.timestamp, l.person) for l in logs])

	@expose('WebApp_Template-3.xhtml')
	def hello(self, person='Default'):
		DBSession.add(Log(person = person))
		DBSession.commit()
		return dict(person = person)

if __name__ == '__main__':
	config = AppConfig(minimal = True, root_controller = DBDemo())
	config.renderers.append('kajiki')
	config['use_sqlalchemy'] = True
	config['sqlalchemy.url'] = 'sqlite:///D:/TurboGears2-Project/tgenv/Scripts/Code/WEB-6/WebApp_DB-register.db'
	config['model'] = Bunch(DBSession=DBSession, init_model = init_model)
	application = config.make_wsgi_app()
	httpd = make_server('',8080, application)
	httpd.serve_forever()