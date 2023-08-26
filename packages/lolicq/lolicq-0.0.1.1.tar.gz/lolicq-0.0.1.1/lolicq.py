from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
from threading import Thread

posturl = ('127.0.0.1',5700)#Cqhttp监听地址
listurl = ('127.0.0.1',5701)#Lolicq监听地址
def launch():
    _listen(listurl)
def sendgm(gid,text):
    gid = str(gid)
    url = ('http://'+str(posturl[0])+':'+str(posturl[1])+'/send_group_msg?')
    data = url + 'group_id='+gid+'&message='+text
    requests.get(url=data)
def sendpm(uid,text):
    uid = str(uid)
    url = ('http://'+str(posturl[0])+':'+str(posturl[1])+'/send_private_msg?')
    data = url + 'user_id='+uid+'&message='+text
    requests.get(url=data)
def pmsg(uid,text,sender):
    pass
def gmsg(gid,uid,text,sender):
    pass

class _Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write()

    def do_POST(self):
        datas = self.rfile.read(int(self.headers['content-length']))
        msg = json.loads(datas)
        if msg['post_type'] == 'message':
            _hasmsg(msg)
        self.send_response_only(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(''.encode())
    
def _listen(host):
    server = HTTPServer(host, _Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
def _hasmsg(msg):
    if msg['message_type'] == 'private':
        pmsg(msg['user_id'],msg['message'],msg['sender'])
    else:
        gmsg(msg['group_id'],msg['user_id'],msg['message'],msg['sender'])

def _sendpost(point,tex):
    url = point
    data = json.dumps(tex)
    return requests.post(url=url,data=data)