from slimpoint.service import Endpoint

from bitrise.services.bitrise_payload import BitrisePayload


class BitriseArtifactDownload(BitrisePayload):
    """Represents a Bitrise artifact download object as depicted via JSON from Bitrise

    Artifact contents:
        artifact_type (str): e.g. file
        expiring_download_url (str): URL to artifact file, expires within 10 minutes
        file_size_bytes (int): Total size of file in file_size_bytes
        is_public_page_enabled (bool): Is the artifact exposed to the public
        slug (str): Unique identifier of artifact
        title (str): Filename of artifact
    """


class BitriseArtifact(BitrisePayload):
    """Represents a Bitrise artifact as depicted via JSON from Bitrise

    Artifact contents:
        artifact_type (str): e.g. file
        file_size_bytes (int): Total size of file in file_size_bytes
        is_public_page_enabled (bool): Is the artifact exposed to the public
        slug (str): Unique identifier of artifact
        title (str): Filename of artifact
    """

    @property
    def download_info(self):
        """Download info associated with a particular artifact"""

        artifact_dl_ep = ArtifactDownloadEndpoint(self.slug_url)
        dl_json = artifact_dl_ep.get(session=self.session).json()
        download_info_ = BitriseArtifactDownload(
            self.session,
            artifact_dl_ep.url,
            dl_json['data']
        )
        return download_info_


class BitriseBuildDetails(BitrisePayload):
    """Represents Bitrise build details as depicted via JSON from Bitrise

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
    """

    @property
    def artifacts(self):
        """Artifacts associated with a particular build"""

        artifacts_ep = ArtifactsEndpoint(self.url_)
        artifacts_json = artifacts_ep.get(session=self.session).json()
        artifacts_ = [
            BitriseArtifact(
                self.session,
                artifacts_ep.url,
                artifact_data
            ) for artifact_data in artifacts_json['data']
        ]
        return artifacts_


class BitriseBuild(BitrisePayload):
    """Represents a Bitrise build as depicted via JSON from Bitrise

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

    @property
    def details(self):
        """Details associated with a particular build"""
        build_details_ep = BuildDetailsEndpoint(self.slug_url)
        build_details_json = build_details_ep.get(session=self.session).json()
        details_ = BitriseBuildDetails(
            self.session,
            build_details_ep.url,
            build_details_json['data']
        )
        return details_


class BuildsEndpoint(Endpoint):
    _path = '/builds'


class BuildDetailsEndpoint(Endpoint):
    _path = ''


class ArtifactsEndpoint(Endpoint):
    _path = '/artifacts'


class ArtifactDownloadEndpoint(Endpoint):
    _path = ''
