#!/usr/bin/env python3
#
# Building the messageboard server:
##################################
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

comments = []
html_string = ''' 
  <!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST" action="http://localhost:8000/">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
  <h2>Comments</h2>'''
  
# add comments to html
def add_comments(html_string):
    if not comments:
        html_string += '<p>There are no comments.</p>'
    else:
        for comment in comments:
            html_string += '<p>{}</p>'.format(comment)
    return html_string


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. How long was the message? (Use the Content-Length header.)
        length = int(self.headers.get('content-length',0))

        # 2. Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()

        # 3. Extract the "message" field from the request data.
        messages = parse_qs(data).get('message') # it returns a list or None

        if messages:
            comments.append(messages[0])

        # Send the "message" field back as the response.
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()
        
    def do_GET(self):
        self.send_response(200);
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(add_comments(html_string).encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
