from slimpoint.service import Endpoint


class BitriseApp(object):
    def __init__(self, **kwargs):
        """Represents a Bitrise App as depicted via JSON from Bitrise

        Args:
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
            owner_account_type (str): organization, etc
            owner_name (str): Name of app owner
            owner_slug (str): Unique ID of owner
        """

        self.slug = kwargs.get('slug')
        self.title = kwargs.get('title')
        self.project_type = kwargs.get('project_type')
        self.provider = kwargs.get('provider')
        self.repo_owner = kwargs.get('repo_owner')
        self.repo_url = kwargs.get('repo_url')
        self.repo_slug = kwargs.get('repo_slug')
        self.is_disabled = kwargs.get('is_disabled')
        self.status = kwargs.get('status')
        self.is_public = kwargs.get('is_public')
        self.owner_account_type = kwargs.get('owner_account_type')
        self.owner_name = kwargs.get('owner_name')
        self.owner_slug = kwargs.get('owner_slug')


class AppsEndpoint(Endpoint):
    _path = '/apps'
