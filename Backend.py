import json
import openai
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
class DemoRequestHandler(BaseHTTPRequestHandler):
    def query_helper(query):
        key =  "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"
        openai.api_key = key
        template = ""
        prompt = f"Response in the form of a json object in a single line (Here's the template: {template}). Extract the useful information that can be used on a calendar. Here's the given information:{query}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.1,
        )
        return response
    def do_GET(self):
        parsedUrl = urlparse(self.path)
        parsedQs= parse_qs(parsedUrl.query)
        query=parsedQs.get('query',[''])[0]
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'response' : DemoRequestHandler.query_helper(query)}
        print(response)
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'This is a demo JSON response to a POST request.'}
        self.wfile.write(json.dumps(response).encode())




def run():
    print('Starting httpd on port 8888...')
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, DemoRequestHandler)
    print('httpd running...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()

