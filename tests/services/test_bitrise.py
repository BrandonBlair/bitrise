from responses import RequestsMock, GET

from requests import Session

from bitrise import BitriseClient
from bitrise.services.apps import BitriseApp
from bitrise.services.builds import BitriseBuild


test_token = 'unimportant'
success_status = 200
test_app_slug = 'appslug'
test_build_slug = 'buildslug'
test_build_details_slug = 'buiolddetailsslug'


def test_bitrise_services():
    client = BitriseClient(api_token=test_token)

    # Apps
    apps_payload = [
        {'slug': 'app1'},
        {'slug': 'app2'},
        {'slug': 'app3'}
    ]

    apps_json = {
        'data': apps_payload
    }
    with RequestsMock() as get_resp:
        get_resp.add(GET, url=client.bitrise.apps.url, status=success_status, json=apps_json)

        app_list = client.apps
        assert app_list[0].data['slug'] == apps_payload[0]['slug']

    # Builds
    sessn = Session()
    apps_url = client.bitrise.apps.url
    slug_url = f"{apps_url}/{test_app_slug}"
    app = BitriseApp(sessn, apps_url, {'slug': test_app_slug})

    builds_payload = [
        {'slug': 'build1', 'triggered_at': '2018-03-28T09:24:49Z'},
        {'slug': 'build2', 'triggered_at': '2018-04-28T09:24:49Z'},  # Latest build
        {'slug': 'build3', 'triggered_at': '2018-01-28T09:24:49Z'}
    ]

    builds_json = {
        'data': builds_payload
    }
    with RequestsMock() as get_resp:
        builds_url = f"{slug_url}/builds?limit=10"
        get_resp.add(GET, url=builds_url, status=success_status, json=builds_json)

        builds = app.builds

        # Get build by slug
        assert app.get_build_by_slug('build1').triggered_at == '2018-03-28T09:24:49Z'

        # Get latest build
        assert app.latest_build.slug == 'build2'

        # Validate build contents
        assert builds[0].data['slug'] == builds_payload[0]['slug']

    # Build Details
    builds_url = f"{apps_url}/{test_app_slug}/builds"
    build = BitriseBuild(sessn, builds_url, {'slug': test_build_slug})

    build_details_payload = {'slug': 'detail1'}

    build_details_json = {
        'data': build_details_payload
    }
    with RequestsMock() as get_resp:
        get_resp.add(
            GET,
            url=f"{builds_url}/{test_build_slug}",
            status=success_status,
            json=build_details_json
        )

        details = build.details

        assert details.data == build_details_payload

    # Artifacts
    artifacts_url = f"{builds_url}/{test_build_slug}/artifacts"

    artifacts_payload = [
        {'slug': 'artifact1'},
        {'slug': 'artifact2'},
        {'slug': 'artifact3'}
    ]

    artifacts_json = {
        'data': artifacts_payload
    }

    with RequestsMock() as get_resp:
        get_resp.add(GET, url=artifacts_url, status=success_status, json=artifacts_json)

        artifacts = details.artifacts

        assert artifacts[0].data['slug'] == artifacts_payload[0]['slug']
