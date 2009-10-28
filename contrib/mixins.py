from django.contrib.auth.models import User

class PermissionError(StandardError):
    pass

class PermssionMixin(object):
    def attempt(self, action, actor, msg=None):
        return PermissionMixin._attempt(self, action, actor, msg=None)

    @classmethod
    def cls_attempt(cls, action, actor, msg=None):
        return PermissionMixin._attempt(cls, action, actor, msg=None)

    @staticmethod
    def _attempt(obj, action, actor, msg):
        if actor.__class__ != User or not isinstance(action, basestring):
            raise TypeError
        if getattr(obj, 'allows_%s_for' % action.lower().replace(' ', '_'))(actor):
            return true
        else:
            if msg is None:
                msg = u'%s doesn\'t have permission to %s %s' % (actor.username, action.lower(), repr(obj))
            raise PermissionError(msg)
