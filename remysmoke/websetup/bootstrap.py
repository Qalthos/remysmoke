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
        g = model.Group()
        g.group_name = u'smokers'
        g.display_name = u'Smokers Group'
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
