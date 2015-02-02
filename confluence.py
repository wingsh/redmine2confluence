import json
import xmlrpclib

import requests


class InvalidXML(Exception):
    pass


class Confluence(object):
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.headers = {'Content-type': 'application/json'}

    def _post(self, url, data, files=None, headers=None, jsonify=True):
        if headers is None:
            headers = self.headers
        if jsonify:
            data = json.dumps(data)
        res = requests.post(url, auth=(self.username, self.password), data=data,
                            headers=headers, files=files)
        if not 200 <= res.status_code < 300:
            error = json.loads(res.text)
            if error['message'] == 'Error parsing xhtml':
                raise InvalidXML()
            import pudb;pudb.set_trace()
            raise RuntimeError(res.text)
        return res.json()

    def create_space(self, key, name, description):
        data = {
            'key': key, 'name': name,
            'description': {
                'plain': {
                    'value': description,
                    'representation': 'plain'
                }
            }
        }
        return self._post('{0}/space'.format(self.base_url), data)

    def create_page(self, title, body, space, username, display_name, parent_id=None):
        data = {
            "type": "page",
            "title": title,
            "space": {"key": space},
            "version": {
                "by": {
                    "type": "known",
                    "username": username,
                    "displayName": display_name
                }
            },
            "body": {
                "storage": {
                    "value": body,
                    "representation": "storage"
                }
            }
        }
        if parent_id is not None:
            data["ancestors"] = [{"type": "page", "id": parent_id}]
        return self._post('{0}/content'.format(self.base_url), data)

    def add_attachment(self, confluence_id, filename, data, description):
        url = '{0}/content/{1}/child/attachment'.format(
            self.base_url, confluence_id)
        return self._post(url, {'comment': description},
                          files={'file': (filename, data)},
                          headers={'X-Atlassian-Token': 'nocheck'},
                          jsonify=False)

    def move_page(self, page_id, target_page_id):
        server = xmlrpclib.ServerProxy('http://localhost:8090/rpc/xmlrpc')
        token = server.confluence2.login(self.username, self.password)
        server.confluence2.movePage(
            token, str(page_id), str(target_page_id), 'append')
