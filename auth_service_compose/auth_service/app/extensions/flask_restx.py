from typing import Optional

from flask_restx import Namespace, Api

api: Optional[Api] = None

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'oauth2': {
        'type': 'oauth2',
        'flow': 'accessCode',
        'tokenUrl': 'https://somewhere.com/token',
        'authorizationUrl': 'https://somewhere.com/auth',
        'scopes': {
            'read': 'Grant read-only access',
            'write': 'Grant read-write access',
        }
    }
}


class ModifiedNamespace(Namespace):

    @property
    def path(self):
        return ("")
