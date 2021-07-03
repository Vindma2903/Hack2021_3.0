# -*- coding: utf-8 -*-
import datetime, pyramid, sys
import urllib.parse
from json import dumps, loads
from argparse import ArgumentParser, RawTextHelpFormatter
from os import getcwd
from os.path import normpath, join
from traceback import format_exc
from time import strftime, gmtime, sleep
from wsgiref.simple_server import make_server, ServerHandler
from http.server import BaseHTTPRequestHandler
from pyramid.config import Configurator
from pyramid.renderers import render, render_to_response
from pyramid.response import Response, FileResponse
from pyramid.view import view_config, view_defaults
from mako.template import Template
from collections import OrderedDict


class RHandler(BaseHTTPRequestHandler):

    server_version = "0.1"

    def get_environ(self):
        env = self.server.base_environ.copy()
        env['SERVER_PROTOCOL'] = self.request_version
        env['SERVER_SOFTWARE'] = self.server_version
        env['REQUEST_METHOD'] = self.command
        if '?' in self.path:
            path,query = self.path.split('?',1)
        else:
            path,query = self.path,''

        if 'X-Real-IP' in self.headers:
            self.client_address = (self.headers['X-Real-IP'], self.client_address[1])
        if 'X-Forwarded-For' in self.headers:
            self.client_address = (self.headers['X-Forwarded-For'], self.client_address[1])
        if 'Cf-Connecting-Ip' in self.headers:
            self.client_address = (self.headers['Cf-Connecting-Ip'], self.client_address[1])

        env['PATH_INFO'] = urllib.parse.unquote(path, 'iso-8859-1')
        env['QUERY_STRING'] = query

        host = self.address_string()
        if host != self.client_address[0]:
            env['REMOTE_HOST'] = host
        env['REMOTE_ADDR'] = self.client_address[0]

        if self.headers.get('content-type') is None:
            env['CONTENT_TYPE'] = self.headers.get_content_type()
        else:
            env['CONTENT_TYPE'] = self.headers['content-type']

        length = self.headers.get('content-length')
        if length:
            env['CONTENT_LENGTH'] = length

        for k, v in self.headers.items():
            k=k.replace('-','_').upper(); v=v.strip()
            if k in env:
                continue                    # skip content length, type,etc.
            if 'HTTP_'+k in env:
                env['HTTP_'+k] += ','+v     # comma-separate multiple headers
            else:
                env['HTTP_'+k] = v
        return env

    def get_stderr(self):
        return sys.stderr

    def handle(self):
        """Handle a single HTTP request"""

        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return

        if not self.parse_request(): # An error code has been sent, just exit
            return

        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())


def log(logpath, msg):
    time_format = '%A, %d-%B-%Y, %H:%M:%S %Z %z'
    time_log = strftime(time_format, gmtime())
    with open(logpath, "a") as f:
        try:
            f.write("[{}] {}\n\n\n".format(time_log, msg))
        except Exception as e:
            f.write(e)

def ip_grab(request):
    if "X-Real-Ip" in request.headers and request.remote_addr == "127.0.0.1":
        return request.headers["X-Real-Ip"]
    else:
        return request.remote_addr


@view_defaults(route_name="main")
class Server():
    def __init__(self, request):
        self.request = request
        self.view_name = "Qerver"
        self.rserver = "Hypach"

    @view_config(route_name="root")
    def root(self):
        log("main.log", "Requested root page from {}\n{}".format(ip_grab(self.request), str(self.request)))
        kwargs = {}
        template = Template(filename='temp/root.mako')
        result = template.render(**kwargs)
        resp = Response(result)
        resp.server = self.rserver
        return resp

    @view_config(route_name="index")
    def index(self):
        log("main.log", "Requested index page from {}\n{}".format(ip_grab(self.request), str(self.request)))
        kwargs = {"name": "test", "value": 1}
        template = Template(filename='temp/index.mako')
        result = template.render(**kwargs)
        resp = Response(result)
        resp.server = self.rserver
        return resp

    @view_config(route_name="dev")
    def dev(self):
        log("main.log", "Requested dev page from {}\n{}".format(ip_grab(self.request), str(self.request)))
        kwargs = {}
        template = Template(filename='temp/dev.mako')
        result = template.render(**kwargs)
        resp = Response(result)
        resp.server = self.rserver
        return resp

    @view_config(route_name="collect")
    def collect(self):
        if self.request.method == 'POST':
            log("collect.log", "Collect from {}\n{}".format(ip_grab(self.request), str(self.request)))
            resp = Response("")
            resp.server = self.rserver
        else:
            log("main.log", "Unexpected from {}\n{}".format(ip_grab(self.request), str(self.request)))
            kwargs = {}
            template = Template(filename='temp/matrix.mako')
            result = template.render(**kwargs)
            resp = Response(result)
            resp.server = '\xde\xad'
        return resp

    @view_config(route_name="trap")
    def trap(self):
        resp = Response(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0f\x00\x00\x00\x0f\x08\x02\x00\x00\x00\xb4\xb4\x02\x1d\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x03viTXtXML:com.adobe.xmp\x00\x00\x00\x00\x00<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?> <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.6-c142 79.160924, 2017/07/13-01:06:39        "> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stRef="http://ns.adobe.com/xap/1.0/sType/ResourceRef#" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmpMM:OriginalDocumentID="xmp.did:c1ae92d0-a061-a04b-abac-3220029f9d68" xmpMM:DocumentID="xmp.did:A77CE6A65A9D11E895CABF782D9CED6E" xmpMM:InstanceID="xmp.iid:A77CE6A55A9D11E895CABF782D9CED6E" xmp:CreatorTool="Adobe Photoshop CC 2018 (Windows)"> <xmpMM:DerivedFrom stRef:instanceID="xmp.iid:bc43d349-bf98-884c-b939-ea47a155d3c4" stRef:documentID="xmp.did:c1ae92d0-a061-a04b-abac-3220029f9d68"/> </rdf:Description> </rdf:RDF> </x:xmpmeta> <?xpacket end="r"?>\xbd\xd6\x16A\x00\x00\x01\xa8IDATx\xda\x94\x92M/\x03Q\x14\x86\xe7\xceWg\xc6\xb4\xda\xce\x14\xcd\x14\t\xa9\x86\xaa\x88\x95h\xea\x07\xd8\x89\xad\xa4\xb1\xf6\x17\xec\xd8\x89\x85\xb5\xad\x8d? !\x16"V\xc4\x02A\xbb\xa0\xd14)ZU\x1f\x9di;\xd3{\x9c\xd2\x90\xf8H8\x8b\xc9\xb9\x99w\xde\xfb\xbco\x86\x00\x00\xf3\xe7a\x99\xff\x0c\xff\xb1m\\\x94\xeeL;_\xb1\xe7bz\x9f\xd7\xc5\x11\xf2]M>H\xf2/vr\xf3*\xaa\xcb\xe3Au+\xf38\x13\xf1\xddV\xec:\x85\xb8\xa1\xc6\x02\xcaW\xef\xa0*t\xb5\tQMN\x97\xacn\x8f\xb8\x9b}\x169b9tP\x93\x7f\xe6\xee\xf1\x88\xba\xc2S`L\x9br\x841\x1d\xfaPu\xc8o)\xe3\x86\x1bI\xa6\xfa\xbd(M\xc6\xf4!M\x1e\xf0K\x11\xbf\xf4\x95\xfb\xb2\\;/Z<Kd\x9e\x15X\xe2\x004(\xe0\xce\x12\xa6\xd6\x00\xc3-\xf6{]-\xee\xf5\xb3\xfb\xe5\x83\xfct\xd8\x875\xac\x1d\x17\x1c\n\x1d\x8a\xe0\x97\xb9\xd4}\xf5\xdd\x12?[L\x84f\xa3ZS\xbdr\x98/\x9aNo\xbbhS@\x12\xf4\x1b\t(\x89\x90{\xf5\xe8F\x97\x05\x81#\xdb\x99G\xd4\xb4\xd45\x07\x1a\x00\xe8\x84\xe1&\x0c\xd5PE\x9e#\x15\x9b\xce\x8fu\xfa\xa5\xa6`?\xf7\x8c\xafZ))\x03\xef\xd7\xc9\x02\x82\x12|\x8a,)\xd7\x1c\x0c\x80\r\xeef\x9f\x90\xed\xb3\xef\x1e\x8f\xab\\5S%\xcb\xb2\xc1+q\x01\x85?\xb93\x87ue\xe7\xfaI\x93x\x8c^o@\xd8\'\xb6:9-X\x0b{\xb9\xf4\x83\x85gl\x08\x8d\xb0cL\x8c\x0b\xfb\xd6v\xd8\'-M\x86F;\x14\xf2\xaf\x7f\xf0U\x80\x01\x00\xd2\xc7\xb19\xeb\x0b2\x94\x00\x00\x00\x00IEND\xaeB`\x82')
        resp.content_type = "image/png"
        if self.request.method == 'GET':
            log("trap.log", "Trap from {}\n{}".format(ip_grab(self.request), str(self.request)))
            resp.server = self.rserver
        else:
            log("main.log", "Unexpected from {}\n{}".format(ip_grab(self.request), str(self.request)))
            kwargs = {}
            template = Template(filename='temp/matrix.mako')
            result = template.render(**kwargs)
            resp = Response(result)
            resp.server = '\xde\xad'
        return resp


def error_page(request):
    log("main.log", "Other request from {}\n{}".format(ip_grab(request), str(request)))
    kwargs = {}
    template = Template(filename='temp/matrix.mako')
    result = template.render(**kwargs)
    resp = Response(result)
    resp.server = '\xde\xad'
    return resp

def app():
    with Configurator() as config:
        config.add_route("root", "/")
        config.add_route("collect", "/collect")
        config.add_route("index", "/index")
        config.add_route("dev", "/dev")
        config.add_route("trap", "/EF4F109CFI411/yt.png")
        config.add_notfound_view(error_page, append_slash=True)
        config.add_static_view(name='/', path='stat')
        config.scan()
        app = config.make_wsgi_app()
        return app


if __name__ == '__main__':
    version = 0.11
    parser = ArgumentParser(description="", formatter_class=RawTextHelpFormatter, epilog="")

    parser.add_argument("-l",'--hostname', dest='host', type=str, default="127.0.0.1", help="hostname")
    parser.add_argument("-p",'--port', dest='port', type=int, default=7777, help="port")
    parser.add_argument("-v",'--verb', dest='verb', action='store_true', help="verbose")

    args = parser.parse_args()

    server = make_server(args.host, args.port, app(), handler_class=RHandler)
    server.serve_forever()
