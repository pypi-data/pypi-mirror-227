from pidevguru.piwebapi.pi_web_api_client import PIWebApiClient
from pidevguru.piwebapi.models import PWAPoint, PWAAttribute, PWAElement
from pidevguru.piwebapi.web_id.web_id_generator import WebIdGenerator
from piwebapiml.pml_stream import PMLStream
from piwebapiml.pml_stream_set import PMLStreamSet


class PMLWebApiClient(object):
    piwebapi = None

    def __init__(self, base_url, verify_ssl=True):
        self.piwebapi = PIWebApiClient(base_url, verify_ssl)

    def set_basic_auth(self, username, password):
        self.piwebapi.set_basic_auth(username, password)

    def set_kerberos_auth(self, mode=0):
        self.piwebapi.set_kerberos_auth(mode)

    def get_pi_point(self, path):
        web_id_generator = WebIdGenerator()  
        web_id = web_id_generator.generate_web_id_by_path(path, type(PWAPoint()))
        return PMLStream(self.piwebapi, web_id, path)

    def get_af_attribute(self, path):
        web_id_generator = WebIdGenerator()        
        web_id = web_id_generator.generate_web_id_by_path(path, type(PWAAttribute()), type(PWAElement()))
        return PMLStream(self.piwebapi, web_id, path)

    def get_pi_points(self, paths):
        streams = []
        for path in paths:
            stream = self.get_pi_point(path)
            streams.append(stream)
        return PMLStreamSet(self.piwebapi, streams)

    def get_af_attributes(self, paths):
        streams = []
        for path in paths:
            stream = self.get_pi_point(path)
            streams.append(stream)
        return PMLStreamSet(self.piwebapi, streams)
