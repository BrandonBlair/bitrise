from slimpoint.service import Endpoint

from bitrise.services.bitrise_payload import BitrisePayload
from bitrise.services.builds import BuildsEndpoint, BitriseBuild


class BitriseApp(BitrisePayload):
    def __init__(self, session, apps_url, app_data):
        """Represents a Bitrise App as depicted via JSON from Bitrise

        Args:
            app_data (dict): App data as received from Bitrise

        App data contents:
            slug (str): Unique identifier for app
            title (str): App title
            project_type (str): ios, etc
            provider (str): github, etc
            repo_owner (str): Name of repo owner
            repo_url (str): URL to code repository
            repo_slug (str): Repo name
            is_disabled (bool): Is the app currently disabled?
            status (int): Status of app in Bitrise
            is_public (bool): Whether or not app is public
            owner (dict):
                account_type (str): organization, etc
                name (str): Name of app owner
                slug (str): Unique ID of owner
        """

        super().__init__(app_data)
        self.apps_url = apps_url
        self.session = session

    @property
    def builds(self):
        """Builds associated with a particular app"""
        slug_url = f"{self.apps_url}/{self.slug}"
        builds_ep = BuildsEndpoint(slug_url)

        builds_json = builds_ep.get(session=self.session, qs_args={'limit': 10}).json()
        available_builds = [
            BitriseBuild(
                self.session,
                builds_ep.url,
                build_data
            ) for build_data in builds_json['data']
        ]
        return available_builds


class AppsEndpoint(Endpoint):
    _path = '/apps'
