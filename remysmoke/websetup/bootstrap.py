# -*- coding: utf-8 -*-
"""Setup the remysmoke application"""

import logging
from tg import config
from remysmoke import model
import transaction

def bootstrap(command, conf, vars):
    """Place any commands to setup remysmoke here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = u'manager'
        u.display_name = u'Example manager'
        u.email_address = u'manager@somedomain.com'
        u.password = u'managepass'

        model.DBSession.add(u)

        g = model.Group()
        g.group_name = u'managers'
        g.display_name = u'Managers Group'

        g.users.append(u)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = u'manage'
        p.description = u'This permission give an administrative right to the bearer'
        p.groups.append(g)

        model.DBSession.add(p)

        u1 = model.User()
        u1.user_name = u'editor'
        u1.display_name = u'Example editor'
        u1.email_address = u'editor@somedomain.com'
        u1.password = u'editpass'

        model.DBSession.add(u1)

        g = model.Group()
        g.group_name = u'smokers'
        g.display_name = u'Smokers Group'

        g.users.append(u1)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = u'smoke'
        p.description = u'This permission gives rights to add smoking data'
        p.groups.append(g)

        model.DBSession.add(p)

        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'

    # <websetup.bootstrap.after.auth>
