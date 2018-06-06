from datetime import datetime

from slimpoint.service import Endpoint

from bitrise.exceptions import BitriseException
from bitrise.services.bitrise_payload import BitrisePayload
from bitrise.services.builds import BuildsEndpoint, BitriseBuild


class BitriseApp(BitrisePayload):
    """Represents a Bitrise App as depicted via JSON from Bitrise

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

    @property
    def builds(self):
        """Builds associated with a particular app"""
        builds_ep = BuildsEndpoint(self.slug_url)
        builds_json = builds_ep.get(session=self.session, qs_args={'limit': 50}).json()
        available_builds = [
            BitriseBuild(
                self.session,
                builds_ep.url,
                build_data
            ) for build_data in builds_json['data']
        ]
        return available_builds

    def get_build_by_slug(self, slug):
        current_builds = self.builds  # prevent multiple calls (builds are loaded lazily)
        matching_builds = [build for build in current_builds if build.slug == slug]

        if len(matching_builds) != 1:
            raise BitriseException(f'Expected 1 build with slug {slug}, found: {current_builds}')

        return matching_builds[0]

    @property
    def latest_build(self):
        current_builds = self.builds

        # Sort by build triggered time desc
        sorted_dates = sorted(
            [build for build in current_builds],
            key=lambda x: datetime.strptime(x.triggered_at, r'%Y-%m-%dT%H:%M:%SZ'),
            reverse=True
        )
        if len(sorted_dates) < 1:
            raise BitriseException('No builds found')
        return sorted_dates[0]


class AppsEndpoint(Endpoint):
    _path = '/apps'
