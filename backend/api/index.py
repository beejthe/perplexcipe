from http.server import BaseHTTPRequestHandler
import json
import os
from main import app
from io import BytesIO
from werkzeug.wrappers import Request

def make_environ(event):
    environ = {
        'REQUEST_METHOD': event.get('method', ''),
        'SCRIPT_NAME': '',
        'PATH_INFO': event.get('path', ''),
        'QUERY_STRING': event.get('query', ''),
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(event.get('body', '').encode('utf-8')),
        'wsgi.errors': BytesIO(),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'HTTP_ACCEPT': '*/*',
        'HTTP_HOST': 'vercel.app',
    }
    return environ

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        environ = make_environ({
            'method': 'GET',
            'path': self.path,
            'query': '',
            'body': ''
        })
        
        with app.request_context(environ):
            response = app.full_dispatch_request()
            self.wfile.write(response.get_data())
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        environ = make_environ({
            'method': 'POST',
            'path': self.path,
            'query': '',
            'body': body.decode('utf-8')
        })
        
        with app.request_context(environ):
            response = app.full_dispatch_request()
            self.wfile.write(response.get_data()) 