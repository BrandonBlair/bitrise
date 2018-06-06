class BitrisePayload(object):
    def __init__(self, session, url, payload_data):
        """Represents a Bitrise payload as depicted via JSON from Bitrise API

        Each payload should contain a slug - a unique identifier for that object
        """

        for attr in payload_data:
            setattr(self, attr, payload_data[attr])

        self.session = session
        self.url_ = url  # Use this name to decrease likelihood of clashing with url attrs
        self.data = payload_data
        self.slug_url = f"{self.url_}/{self.slug}"

    @property
    def json(self):
        return self.data
