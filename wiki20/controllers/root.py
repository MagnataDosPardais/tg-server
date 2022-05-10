# -*- coding: utf-8 -*-
"""Main Controller"""
import random

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from wiki20 import model
from wiki20.controllers.secure import SecureController
from wiki20.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from wiki20.lib.base import BaseController
from wiki20.controllers.error import ErrorController
from wiki20.model.page import Page
import sqlalchemy

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the wiki20 application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "wiki20"

    @expose('wiki20.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict()
    @expose('wiki20.templates.contents')
    def main(self):
        dto = DBSession.query(Page)
        dtdesc = sqlalchemy.sql.expression.desc(Page.id)
        dt = dto.order_by(dtdesc)
        
        dtc = []
        for c in dt:
            dtc.append(c.comm)
        for i in range(0,len(dtc)):
            try:
                dtc[i] = dtc[i].split('§')
            except: pass

        return dict(pgData=dt,pgCom=dtc)

    @expose('wiki20.templates.page')
    def _default(self, pagename="FrontPage"):
        """Handle the front-page."""
        page = DBSession.query(Page).filter_by(pagename=pagename).one()
        return dict(wikipage=page)

    @expose(template="wiki20.templates.edit")
    def edit(self, pagename):
        page = DBSession.query(Page).filter_by(pagename=pagename).one()
        return dict(wikipage=page)

    @expose()
    def save(self, pageuser, pagename, data, submit):
        #############################################
        #### GET NAME OF THE EDITOR OF THE PAGE #####
        #############################################
        print(f"PAGE {pagename} EDITED BY {pageuser}")
        page = DBSession.query(Page).filter_by(pagename=pagename).one()
        page.data = data
        page.user = pageuser
        redirect("/" + pagename)



    @expose('wiki20.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('wiki20.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('wiki20.templates.data')
    @expose('json')
    def data(self, **kw):
        """
        This method showcases how you can use the same controller
        for a data page and a display page.
        """
        return dict(page='data', params=kw)
    @expose('wiki20.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('wiki20.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('wiki20.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('Usuário não encontrado'), 'error')
            elif failure == 'invalid-password':
                flash(_('Senha invalida'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Credenciais incorretas'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Salve, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('Até mais!'))
        return HTTPFound(location=came_from)
