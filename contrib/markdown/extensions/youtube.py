import markdown
from markdown import etree
import re

class YouTubePattern(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        if m.group(2).strip():
            #Create an youtube player instance.
            obj = etree.Element('object')
            obj.set('width', '425')
            obj.set('height', '344')
            param = etree.SubElement(obj, 'param')
            param.set('name', 'movie')
            param.set('value', 'http://www.youtube.com/v/%s&hl=en&fs=1&' % m.group(2))
            param2 = etree.SubElement(obj, 'param')
            param2.set('name', 'allowFullScreen')
            param2.set('value', 'true')
            param3 = etree.SubElement(obj, 'param')
            param3.set('name', 'allowscriptaccess')
            param3.set('value', 'always')
            embed = etree.SubElement(obj, 'embed')
            embed.set('src', 'http://www.youtube.com/v/%s&hl=en&fs=1&' % m.group(2))
            embed.set('type', 'application/x-shockwave-flash')
            embed.set('allowscriptaccess', 'always')
            embed.set('allowfullscreen', 'true')
            embed.set('width', '425')
            embed.set('height', '344')
        else:
            obj = ''
        return obj

class YouTubeExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        self.md = md

        REGEXP = ':http://www\.youtube\.com/watch\?v=([a-zA-Z0-9\-_]+)[\w&=\-]*:'
        youtubePattern = YouTubePattern(REGEXP)
        youtubePattern.md = md
        md.inlinePatterns.add('youtubepattern', youtubePattern, '<not_strong')

