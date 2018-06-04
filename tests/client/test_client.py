import os

from pytest import raises

from bitrise import BitriseClient


TEST_TOKEN = 'TEST_TOKEN'


def test_can_create_new_client_with_token():
    client = BitriseClient(api_token=TEST_TOKEN)

    expected_auth_header = f'token {TEST_TOKEN}'
    assert client.session.headers.get('Authorization') == expected_auth_header


def test_can_create_new_client_with_environment_variable():
    os.environ['BITRISE_TOKEN'] = TEST_TOKEN
    client = BitriseClient()

    expected_auth_header = f'token {TEST_TOKEN}'
    assert client.session.headers.get('Authorization') == expected_auth_header


def test_cannot_create_client_with_no_api_token():
    os.environ['BITRISE_TOKEN'] = ''

    with raises(ValueError) as no_token_exc:
        BitriseClient()
    assert 'Must provide a bitrise token' in str(no_token_exc.value)
