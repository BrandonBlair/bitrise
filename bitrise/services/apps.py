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

    def get_builds(self, limit=50, **kwargs):
        """Builds associated with a particular app

        NOTE: Bitrise API returns builds ordered from newest to oldest

        Available filters:
            limit (int): Limit result set
            status (int): Filter by build status
                0: Not finished yet.
                    If is_on_hold = true: the build did not start yet (status_text=on-hold)
                    If is_on_hold = false: the build is running (status_text=in-progress).
                1: Build finished, with success (status_text=success).
                2: Build finished, with error (status_text=error).
                3: Build was aborted
            branch (str): Retrieve only builds from the given branch
            trigger_event_type (str): Filter by trigger event
                push: Builds triggered by a commit push
                pull-request: Builds triggered by a PR
            pull_request_id (int): Filter by PR ID (trigger event type must be pull-request)
            pull_request_id (int): PR ID (trigger_event_type must be pull-request)
            after (int): Builds triggered after a certain time (UNIX timestamp)
            before (int): Builds triggered before a certain time (UNIX timestamp)
            workflow_id (str): Builds triggered with a specific workflow
            commit_message (str): Builds containing commit message (partial-matches too)
            build_number (str): Builds with specific build number
        """

        # Add filters
        qs_args = {k: v for k, v in kwargs.items() if v is not None}
        qs_args['limit'] = limit

        builds_ep = BuildsEndpoint(self.slug_url)
        builds_json = builds_ep.get(session=self.session, qs_args=qs_args).json()
        available_builds = [
            BitriseBuild(
                self.session,
                builds_ep.url,
                build_data
            ) for build_data in builds_json['data']
        ]
        return available_builds

    @property
    def completed_builds(self):
        completed = self.get_builds(status=1)
        return completed

    def get_build_by_slug(self, slug):
        current_builds = self.get_builds()  # prevent multiple calls (builds are loaded lazily)
        matching_builds = [build for build in current_builds if build.slug == slug]

        if len(matching_builds) != 1:
            raise BitriseException(f'Expected 1 build with slug {slug}, found: {current_builds}')

        return matching_builds[0]

    def get_last_build(self, status=None):
        """Retrieves last build from Bitrise

        Args:
            status (int): Retrieves the last build matching a specific status
        """

        if status:
            builds = self.get_builds(limit=1, status=status)
        else:
            builds = self.get_builds(limit=1)

        if len(builds) < 1:
            raise BitriseException('No builds found')
        return builds[0]

    def get_builds_by_workflow(self, workflow):
        """Retrieves all builds matching a specific workflow

        Returns:
            matching_builds (list): All builds matching the provided workflow
        """

        workflow = workflow.lower()
        builds_by_workflow = self.get_builds(workflow=workflow)

        if not builds_by_workflow:
            raise BitriseException(f'No builds found with workflow {workflow}')

        return builds_by_workflow


class AppsEndpoint(Endpoint):
    _path = '/apps'
