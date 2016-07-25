REDMINE = {
    'url': 'http://my_redmine_server/redmine', # No trailing slash
    'key': 'my admin user api key'
}

CONFLUENCE = {
    'url': 'http://my_confluence_server:8090', # No trailing slash
    'username': 'root',
    'password': 'root'
}

JIRA_URL = 'http://my_jira_server:8080'

VERIFY_SSL = True   # Set to False if you want to ignore an invalid ssl cert

PROJECTS = {
    "pets" : "PTS", # in the form: "REDMINE_PROJECT_ID": "CONFLUENCE_SPACE_ID (short)"
}
