__author__ = 'yang.hua'
import httplib
from utils import NamedDict


kdt360_host = NamedDict({"host": "www.kdt360.com",
                         "api_url": "/userxml.action"})


def post_xml(request_xml, config):
    """HTTP XML Post request"""
    webservice = httplib.HTTP(config.host)
    webservice.putrequest("POST", config.api_url)
    webservice.putheader("Host", config.host)
    webservice.putheader("User-Agent", "Python post")
    webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
    webservice.putheader("Content-length", "%d" % len(request_xml))
    webservice.endheaders()
    webservice.send(request_xml)
    webservice.getreply()
    return webservice.getfile().read()


def fetch_kdt360(request_xml, config=kdt360_host):
    return post_xml(request_xml, config)