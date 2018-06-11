from slimpoint.service import Endpoint

from bitrise.services.bitrise_payload import BitrisePayload
from bitrise.exceptions import BitriseException


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

    @property
    def download_url(self):
        return self.download_info.expiring_download_url


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
        triggered_at (str): Timestamp when build was triggered, e.g. 2018-06-11T11:00:45Z
        started_on_worker_at (str): When build started on worker
        environment_prepare_finished_at (str): When build environment completed preparation
        finished_at (str): When build finished
        slug (str): Unique identifier for build, e.g. c1969235a56e1c17
        status (int): Current status of build
            0: Not finished yet
                If is_on_hold = true: the build did not start yet (status_text=on-hold)
                If is_on_hold = false: the build is running (status_text=in-progress)
            1: Build finished, with success (status_text=success)
            2: Build finished, with error (status_text=error)
            3: Build was aborted
        status_text: Additional details regarding status, e.g. 'error'
        abort_reason (str): Reason build was aborted, if applicable
        is_on_hold (bool): Whether build is on hold
        branch (str): Git branch, e.g. publisher/develop
        build_number (int): Bitrise build number
        commit_hash (str): Git commit hash
        commit_message (str): Git commit message
        tag (str): Git tag
        triggered_workflow (str): Workflow under which build was triggered
        triggered_by (str): User/process that triggered build
        stack_config_type (str): Configuration type for build stack, e.g. 'standard1'
        stack_identifier (str): ID of build stack, e.g. 'osx-xcode-9.1.x'
        original_build_params (dict): e.g. {
            branch: publisher/develop
            workflow_id: test
        }
        pull_request_id (int): PR request ID if provided
        pull_request_target_branch (str): PR target branch
        pull_request_view_url (str): URL to PR
        commit_view_url: URL to commit
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

    @property
    def artifacts(self):
        """Convenience function to expose artifacts at the build level"""

        return self.details.artifacts

    def get_artifact_by_name(self, name):
        """Retrieve a specific artifact by filename"""

        name = name.lower()
        matching_artifacts = [artifact for artifact in self.artifacts if artifact.title == name]

        if len(matching_artifacts) != 1:
            raise BitriseException(f'Expected 1 artifact named {name}, found {matching_artifacts}')

        return matching_artifacts[0]


class BuildsEndpoint(Endpoint):
    _path = '/builds'


class BuildDetailsEndpoint(Endpoint):
    _path = ''


class ArtifactsEndpoint(Endpoint):
    _path = '/artifacts'


class ArtifactDownloadEndpoint(Endpoint):
    _path = ''
