from slimpoint.service import Endpoint


class BitriseApp(object):
    def __init__(self, app_data):
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

        self.data = app_data

        for attr in app_data:
            setattr(self, attr, app_data[attr])

    @property
    def json(self):
        return self.data


class AppsEndpoint(Endpoint):
    _path = '/apps'
