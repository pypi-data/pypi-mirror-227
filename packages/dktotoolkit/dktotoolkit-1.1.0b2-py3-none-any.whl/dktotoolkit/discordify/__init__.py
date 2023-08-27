# -*- coding: utf-8 -*-

from textwrap import wrap
import itertools
import markdownify as md
# https://github.com/matthewwithanm/python-markdownify/blob/develop/markdownify/__init__.py


RETURN = "return"

class DiscordMarkdownConverter(md.MarkdownConverter, object):
    """Overcharge markdownify.MarkdownConverter (https://github.com/matthewwithanm/python-markdownify)"""

    class DiscordDefaultOptions:

        # options de Markdownify
        bullets = '-+*'

        discordwrap = True
        discordwrap_width = 1012
        wrap = True
        wrap_width = 1020

        heading_style=md.ATX

        # options supplementaires
        newline_style=RETURN
        escape_gt=True
        escape_backslash=True
    #

    # Surcharge init
    def __init__(self, **options):
        super().__init__(**{**md._todict(self.DiscordDefaultOptions), **options})
    #

    # Reecriture fonctions
    def convert_hn(self, n, el, text, convert_as_inline):
        if convert_as_inline:
            return text

        style = self.options['heading_style'].lower()
        text = text.rstrip()
        if style == md.UNDERLINED and n <= 2:
            line = '=' if n == 1 else '-'
            return self.underline(text, line)
        hashes = '#' * n
        if style == md.ATX_CLOSED:
            return '%s %s %s\n\n' % (hashes, text, hashes)
        #

        if n == 1:
            return '\n\n%s %s\n\n' % (hashes, text)
        #
        return '\n%s %s\n\n' % (hashes, text)
    #

    def convert_blockquote(self, el, text, convert_as_inline):

        if convert_as_inline:
            return text

        return '\n' + (md.line_beginning_re.sub('>>> ', text) + '\n\n') if text else ''
    #

    def convert_quote(self, el, text, convert_as_inline):

        if convert_as_inline:
            return text

        return '\n' + (md.line_beginning_re.sub('> ', text) + '\n\n') if text else ''
    #

    def convert_br(self, el, text, convert_as_inline):
        if convert_as_inline:
            return ""

        if self.options['newline_style'].lower() == md.BACKSLASH:
            return '\\\n'
        elif self.options['newline_style'].lower() == RETURN:
            return '\n'
        else:
            return '  \n'
        #
    #
    def escape(self, text):
        if not text:
            return ''
        if self.options['escape_backslash']:
            text = text.replace(r'\\', r'\\\\')
        if self.options['escape_asterisks']:
            text = text.replace('*', r'\*')
        if self.options['escape_underscores']:
            text = text.replace('_', r'\_')
        if self.options['escape_gt']:
            text = text.replace('>', r'\>')
        #
        return text
    # Nouvelles fonctions
    convert_u = md.abstract_inline_conversion(lambda self: 2 * '_')

#


def discordify(
        html,
        keep_newline=True,
        max_characters=1020,
        **options):
    """Convert to Markdown with particular options for Discord norm (wrapping until 1020 characters, espace symbols, ...)
:param str html: Input string (HTML)
:param bool keep_newline: Keep new lines by replacing with \n (default: True)
:param int max_characters: Max characters if not passing in arguments with "discordwrap_width" (default: 1020)
:param bool options[discordwrap]: Wrap the content (default: False)
:param int options[discordwrap_width]: Number of characters when wrapping text (default: max_characters)
:param bool options[discordwrap_keeplines]: Split on new lines (default: False)
"""
    if keep_newline:
        html = html.replace("""
""", "\n")
    #

    out = DiscordMarkdownConverter(**options).convert(html)

    if options.get('discordwrap', False): #and len(out) > discord_wrap_length:
        out = out.replace("\xa0", " ")

        # print("DISCORDIFY : wrap", options.get('discordwrap'), options.get('discordwrap_width'), options.get('discordwrap_keeplines', False))

        if options.get('discordwrap_keeplines', False):
            out = out.replace("\n", "\xa0")
        #
        mylist = [
            wrap(i,
                 options.get('discordwrap_width', max_characters),
                 break_long_words=False,
                 drop_whitespace=True,
                 break_on_hyphens=True,
                 )
            for i in out.split('\n') if i != ''
        ]
        mylist = list(itertools.chain.from_iterable(mylist))
        if options.get('discordwrap_keeplines', False):
            mylist = [e.replace("\xa0", "\n") for e in mylist]
        #
        return mylist
    #

    out = out.replace("\xa0"," ")

    return out
#

def discordify_dict(data, key=None, **kwargs):
    """Discordify on a key or a full dictionnary
:param dict(|list|tuple|str|int|float|bool) data: Content to "discordify"
:param str key: key of the value be discordify ; if None, discordify all values of the dict. Default: None
"""
    if isinstance(data, (str, int, float, bool)) or data is None:
        print("(1)", data)
        return data
    elif isinstance(data, (list, tuple)):
        print("(2)", data)
        return [
            discordify_dict(data=e,
                            key=key,
                            **kwargs
                            )
            for e in data
        ]

    elif isinstance(data, dict) and key is not None and not data.get(key, False):
        print("(3)", data)
        return {
            k:discordify_dict(data=v,
                              key=key,
                              **kwargs
                              )
            for k,v in data.items()
        }

    elif isinstance(data, dict):
        print("(4)", data)
        return {
            k:
            discordify(v, **kwargs) if (k==key or key is None)
            else v
            for k,v in data.items()
        }
    else:
        raise ValueError(f"unknown type of datas {type(datas)}")
    #
