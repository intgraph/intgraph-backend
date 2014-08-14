# coding=utf-8
import os
import json
import Config
import gData
from Render import html_render, markdown_render
import MarkdownParser
from Utils import is_markdown, stripext

class BaseView(object):
    def generate(self):
        raise NotImplementedError

class ListView(BaseView):
    def __init__(self, view_name):
        self.view_name = view_name
        self.tags = {}
        self.articlelist = []
        if self.view_name == Config.MAIN_PAGE:
            gData.frames.append({'title':view_name, 'url': 'index.html'})
        else:
            gData.frames.append({'title':view_name, 'url':view_name + '.html'})
        super(ListView, self).__init__()
        
    def generate(self):
        inpath  = os.path.join(gData.indir,  self.view_name)
        outpath = os.path.join(gData.outdir, self.view_name)
        print inpath, outpath
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        else:
            # Log
            pass
        
        for item in os.listdir(inpath):
            av_in_path = os.path.join(inpath, item)
           
            if is_markdown(av_in_path):
                av_out_path = os.path.join(outpath, stripext(item) + '.html')
                av = ArticleView(av_in_path, av_out_path, self.view_name + '/' + stripext(item) + '.html')
                av.generate()
                self.append_info(av.get_stats())
        
        if self.view_name == Config.MAIN_PAGE:
            outlvpath = os.path.join(gData.outdir, 'index.html')
        else:
            outlvpath = os.path.join(gData.outdir, self.view_name + '.html')
        with open(outlvpath, 'w') as outlvfile:
            html = html_render('listpage.html', {'title': self.view_name, 'article_json_list': self.articlelist, 'tags': self.tags})
            outlvfile.write(html)
    
    def append_info(self, stats):
        self.articlelist.append(json.dumps(dict(stats.Metadata.items() + stats.Tags.items())))
        for key, value in stats.Tags.items():
            self.tags[key] = self.tags.get(key, []) + value
    
    
class ArticleView(BaseView):
    HIDE_SESSION = set(['Solution'])
    def __init__(self, infp, outfp, url):
        self.infp = infp
        self.outfp = outfp
        self.stats = None
        self.url = url
        super(ArticleView, self).__init__()

    def render(self, stats):
        for key, value in stats.Metadata.items():
            stats.Metadata[key] = value.strip()
        for key, value in stats.Tags.items():
            stats.Tags[key] = map(lambda x: x.strip(), value.split(','))
        for key, value in stats.Content.items():
            stats.Content[key] = markdown_render('\n'.join(value))
        stats.Metadata['url'] = self.url
        self.stats = stats
        return stats

    def get_stats(self):
        return self.stats
    
    def generate(self):
        with open(self.infp) as infile:
            stats = MarkdownParser.parse(infile.read())
        stats = self.render(stats)
        with open(self.outfp, 'w') as outfile:
            html = html_render('articlepage.html', {'stats': stats, 'hide_session': self.HIDE_SESSION})
            outfile.write(html)
    
class FlatView(BaseView):
    def __init__(self, view_file):
        self.view_name = stripext(view_file)
        self.infp  = os.path.join(gData.indir,  self.view_name + '.md')
        self.outfp = os.path.join(gData.outdir, self.view_name + '.html')
        gData.frames.append({'title':self.view_name, 'url': self.view_name + '.html'})
        super(FlatView, self).__init__()
    
    def generate(self):
        with open(self.infp) as infile:
            stats = infile.read()
        with open(self.outfp, 'w') as outfile:
            stats = markdown_render(stats)
            html = html_render('flatpage.html', {'content': stats})
            outfile.write(html)
        
