import markdown
import random
from markdown import etree
import re

class MP3PlayerPattern(markdown.inlinepatterns.Pattern):
    '''
    MP3 Player plugin for py-markdown (http://www.freewisdom.org/projects/python-markdown/).
    
    Converts :http://urltomp3/song.mp3: to an inline flash mp3 player which plays
    song.mp3.

    Basic Usage:
        >>> import markdown
        >>> import location of mp3 player extension.
        >>> text = ':http://example.com/song.mp3:'
        >>> mp3 = MP3PlayerExtension()
        >>> html = markdown.markdown(text, extensions=[mp3])

    Requirements:
        * markdown
        * wordpress audio player (http://wpaudioplayer.com/)
          or any other audioplayer capable of playing mp3 from
          remote sites.
        * the site displaying the player must include the audio-player.js file.
    Paths:
        By default the path of the audioplayer is
        /media/audio-player/player.swf
    '''

    def handleMatch(self,m):
        if m.group(2).strip():
            #Create a mp3 player instance.
            id = abs(hash(m.group(2)))
            url = m.group(2)
            player_url = '/media/audio-player/player.swf'
            obj = etree.Element('object')
            obj.set('type', 'application/x-shockwave-flash')
            obj.set('data', player_url)
            obj.set('id', 'audioplayer_%s' % id)
            obj.set('height', '24')
            obj.set('width', '290')
            param = etree.SubElement(obj, 'param')
            param.set('name', 'movie')
            param.set('value', player_url)
            param2 = etree.SubElement(obj, 'param')
            param2.set('name', 'FlashVars')
            param2.set('value', 'playerID=audioplayer_%s&soundFile=%s' % (id,url))
            param3 = etree.SubElement(obj, 'param')
            param3.set('name', 'quality')
            param3.set('value', 'high')
            param4 = etree.SubElement(obj, 'param')
            param4.set('name', 'menu')
            param4.set('value', 'false')
            param5 = etree.SubElement(obj, 'param')
            param5.set('name', 'wmode')
            param5.set('value', 'transparent')
        else:
            obj = ''
        return obj


class MP3PlayerExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        #TODO: Add config for player path
        self.md = md

        REGEXP = ':(https?://([-\w\.]+)+(:\d+)?(/([\w/_]*(\?\S+)?)?)?\.mp3):'
        mp3pattern = MP3PlayerPattern(REGEXP)
        mp3pattern.md = md
        md.inlinePatterns.add('mp3pattern', mp3pattern, '<not_strong')
