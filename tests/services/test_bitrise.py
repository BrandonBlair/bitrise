from responses import RequestsMock, GET

from requests import Session

from bitrise import BitriseClient
from bitrise.services.apps import BitriseApp
from bitrise.services.builds import BitriseBuild


test_token = 'unimportant'
ok_status = 200
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
        get_resp.add(GET, url=client.bitrise.apps.url, status=ok_status, json=apps_json)

        app_list = client.apps
        assert app_list[0].data['slug'] == apps_payload[0]['slug']

    # Builds
    sessn = Session()
    apps_url = client.bitrise.apps.url
    slug_url = f"{apps_url}/{test_app_slug}"
    app = BitriseApp(sessn, apps_url, {'slug': test_app_slug})

    builds_payload = [
        {'slug': 'build1', 'triggered_at': '2018-05-28T09:24:49Z'},
        {'slug': 'build2', 'triggered_at': '2018-04-28T09:24:49Z'},  # Latest build
        {'slug': 'build3', 'triggered_at': '2018-01-28T09:24:49Z'}
    ]

    # Get build by slug
    with RequestsMock() as get_resp:
        builds_url = f"{slug_url}/builds?limit=50"
        get_resp.add(GET, url=builds_url, status=ok_status, json={'data': builds_payload})
        assert app.get_build_by_slug('build2').triggered_at == '2018-04-28T09:24:49Z'

    # Get latest build
    with RequestsMock() as get_resp:
        latest_build_payload = [
            {'slug': 'build1', 'triggered_at': '2018-05-28T09:24:49Z'},
        ]
        builds_url = f"{slug_url}/builds"
        limited_url = f"{builds_url}?limit=1"
        get_resp.add(GET, url=limited_url, status=ok_status, json={'data': latest_build_payload})
        assert app.get_last_build().slug == 'build1'

    # Build Details
    with RequestsMock() as get_resp:
        build_detail_url = f"{apps_url}/{test_app_slug}/builds/{test_build_slug}"
        build_details_payload = {'slug': 'detail1'}
        payld = {'data': build_details_payload}
        get_resp.add(GET, url=build_detail_url, status=ok_status, json=payld)

        build = BitriseBuild(sessn, builds_url, {'slug': test_build_slug})
        details = build.details
        assert details.data == build_details_payload

    # Artifacts
    with RequestsMock() as get_resp:
        artifacts_payload = [
            {'slug': 'artifact1'},
            {'slug': 'artifact2'},
            {'slug': 'artifact3'}
        ]
        artifacts_url = f"{build_detail_url}/artifacts"
        get_resp.add(GET, url=artifacts_url, status=ok_status, json={'data': artifacts_payload})

        artifacts = details.artifacts
        assert artifacts[0].data['slug'] == artifacts_payload[0]['slug']
