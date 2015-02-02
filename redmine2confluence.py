import codecs

import logbook
from redmine import Redmine
import requests
import pypandoc

from confluence import Confluence, InvalidXML
from convert import urls_to_confluence
from settings import REDMINE, CONFLUENCE, PROJECTS

log = logbook.Logger('redmine2confluence')


def process(redmine, wiki_page):
    """Processes a wiki page, getting all metadata and reformatting body"""
    # Get again, to get attachments:
    wiki_page = wiki_page.refresh(include='attachments')
    # process title
    title = wiki_page.title.replace('_', ' ')
    # process body
    body = urls_to_confluence(wiki_page.text) # translate links
    if body.startswith('h1. %s' % title):
        # strip extra repeated title from within body text
        body = body[len('h1. %s' % title):]
    body = pypandoc.convert(body, 'html', format='textile') # convert textile
    ##### build tree object of all wiki pages
    return {
        'title': title,
        'body': body,
        'space': space,
        'username': wiki_page.author.refresh().login,
        'display_name': wiki_page.author.name,
        'attachments': [attachment for attachment in wiki_page.attachments]
    }


if __name__ == '__main__':
    redmine = Redmine(REDMINE['url'], key=REDMINE['key'])
    confluence = Confluence(
        CONFLUENCE['url'], CONFLUENCE['username'], CONFLUENCE['password'])
    for proj_name, space in PROJECTS.iteritems():
        log.info(u"Creating space {0}".format(space))
        project = redmine.project.get(proj_name)
        confluence.create_space(space, project.name, project.description)
        for wiki_page in project.wiki_pages:
            log.info(u"Importing: {0}".format(wiki_page.title))
            processed = process(redmine, wiki_page)
            try:
                page = confluence.create_page(
                    processed['title'], processed['body'], processed['space'],
                    processed['username'], processed['display_name'])
            except InvalidXML:
                log.error(u'Invalid XML: {0}. Aborting.'.format(wiki_page.title))
                continue
            for attachment in processed['attachments']:
                data = requests.get(
                    u'{0}?key={1}'.format(attachment.content_url, REDMINE['key']),
                    stream=True)
                confluence.add_attachment(
                    page['id'], attachment.filename, data.raw, attachment.description)
