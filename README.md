# redmine2confluence

이 코드는 blue-yonder/redmine2confluence에서 fork 해서 수정한 것입니다.

redmine2confluence는 redmine의 wiki를 confluence로 migration을 할 때 사용하는 툴입니다.

장점
* Page 계층 구조가 보존된다.
* 첨부파일도 migration이 된다.
* URL에 link macro 추가.
* redmine 내 Link를 Confluence 내의 Link로 변경해준다.

제약사항
* Page ownership는 settings.py의 confluence 계정으로 migration 됨
* 완벽하게 migration 되진 않음. (테스트버전 - confluence : 5.10.2, redmine : 2.6.10.stable)

굳이 필요 없는 기능(?)
* redmine 이슈(e.g. `#12345`)를 JIRA 이슈로 변경해서 링크 시켜줌.

주의 사항
해당 script를 실행 전에 *반드시* backup을 한 후, 진행!!!

## Step

* 레파지토리를 checkout 하세요.
* `requirements.txt` 파일 안의 package들을 설치하세요.  - pip install -r requirements.txt
* `settings.py` 파일을 해당 서버 정보에 맞게 수정하세요.

````
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
````

* `./redmine2confluence.py`를 실행하세요.
