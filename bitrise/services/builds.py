from slimpoint.service import Endpoint

from bitrise.services.bitrise_payload import BitrisePayload


class BitriseBuildDetails(BitrisePayload):
    def __init__(self, session, build_url, build_detail_data):
        """Represents Bitrise build details as depicted via JSON from Bitrise

        Args:
            build_detail_data (dict): App data as received from Bitrise

        Build data contents:
            abort_reason (str): Reason build was aborted
            branch (str): Git branch name
            build_number (int): numerical id of build
            commit_hash (str): Git commit hash
            commit_message (str): Git commit message
            commit_view_url (str): URL to commit
            environment_prepare_finished_at (str): e.g. 2017-05-30T15:47:17Z
            finished_at (str): e.g. 2017-05-30T15:47:32Z
            is_on_hold (bool): If build is currently on hold
            original_build_params (dict): {
                branch (str): Git branch name
                commit_message (str): Git commit message
            }
            pull_request_id (int): Defaults to 0
            pull_request_target_branch (str): Name of PR target branch
            pull_request_view_url (str): URL to PR view
            slug (str): Build detail slug
            stack_config_type (str): Refer to https://devcenter.bitrise.io/api/v0.1
            stack_identifier (str): Refer to https://devcenter.bitrise.io/api/v0.1
            started_on_worker_at (str): e.g. 2017-05-30T15:47:17Z
            status (int): Build status, e.g. 3
            status_text (str): e.g. "aborted"
            tag (str): Build tag
            triggered_at (str): e.g. 2017-05-30T15:47:17Z
            triggered_by (str): User who triggered build (if provided)
            triggered_workflow (str): e.g. "primary"
        }
        """

        super().__init__(build_detail_data)
        self.session = session
        self.build_url = build_url


class BitriseBuild(BitrisePayload):
    def __init__(self, session, build_url, build_data):
        """Represents a Bitrise build as depicted via JSON from Bitrise

        Args:
            build_data (dict): App data as received from Bitrise

        Build data contents:
            status (int): Filter by build status
            branch (str): Retrieve builds from a certain branch
            trigger_event_type (str): push or pull-request
            pull_request_id (int): PR ID (trigger_event_type must be pull-request)
            after (int): Builds triggered after a certain time (UNIX timestamp)
            before (int): Builds triggered before a certain time (UNIX timestamp)
            workflow (str): Builds triggered with a specific workflow
            commit_message (str): Builds containing commit message (partial-matches too)
            build_number (str): Builds with specific build number
        """

        super().__init__(build_data)
        self.session = session
        self.build_url = build_url

    @property
    def details(self):
        """Details associated with a particular build"""
        slug_url = f"{self.build_url}/{self.slug}"
        build_details_ep = BuildDetailsEndpoint(slug_url)

        build_details_json = build_details_ep.get(session=self.session).json()
        available_details = [
            BitriseBuildDetails(
                self.session,
                build_details_ep.url,
                build_data
            ) for build_data in build_details_json['data']
        ]
        return available_details


class BuildsEndpoint(Endpoint):
    _path = '/builds'


class BuildDetailsEndpoint(Endpoint):
    _path = ''
