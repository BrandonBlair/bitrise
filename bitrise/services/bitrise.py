from slimpoint.service import Endpoint

from .apps import AppsEndpoint


class Bitrise(Endpoint):
    _base_url = 'https://api.bitrise.io/v0.1'

    @property
    def apps(self):
        return AppsEndpoint(base_url=self.url)
