class BitrisePayload(object):
    def __init__(self, payload_data):
        """Represents a Bitrise payload as depicted via JSON from Bitrise API"""

        self.data = payload_data

        for attr in payload_data:
            setattr(self, attr, payload_data[attr])

    @property
    def json(self):
        return self.data
