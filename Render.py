# coding=utf-8
import os
import sys
import jinja2
import gData
import Config
import misaka
import pygments.lexers
import pygments.formatters
import cgi

reload(sys)
sys.setdefaultencoding('utf-8')


class BleepRenderer(misaka.HtmlRenderer, misaka.SmartyPants):
    def block_code(self, text, lang):
        print self, text, lang
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % cgi.escape(text.strip())
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
        formatter = pygments.formatters.HtmlFormatter()
        return pygments.highlight(text, lexer, formatter)


def markdown_render(content):
    renderer = BleepRenderer()
    print renderer
    misaka_md = misaka.Markdown(renderer,
        extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS)
    return misaka_md.render(content)

def html_render(tmpl, infodict):
    infodict['config'] = Config
    infodict['frames'] = gData.frames
    print infodict['frames']
    env = jinja2.Environment(loader = jinja2.FileSystemLoader(Config.THEME_PATH), autoescape=True)
    tmpl = env.get_template(tmpl)
    return tmpl.render(infodict)

