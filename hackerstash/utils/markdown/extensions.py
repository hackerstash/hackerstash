import re
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor


class StrikethroughExtension(Extension):
    def extendMarkdown(self, md):
        postprocessor = StrikethroughPostprocessor(md)
        md.postprocessors.add('strikethrough', postprocessor, '>raw_html')


class StrikethroughPostprocessor(Postprocessor):
    pattern = re.compile(r'~~(((?!~~).)+)~~')

    def run(self, html):
        return re.sub(self.pattern, self.convert, html)

    def convert(self, match):
        return '<s>' + match.group(1) + '</s>'
