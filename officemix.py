"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class OfficeMixXBlock(XBlock):
    """
    An XBlock providing Office Mix embedding capabilities
    """

    href = String(help="URL of the mix you want to embed", default=None, scope=Scope.content)
    maxwidth = Integer(help="Maximum width of the video", default=1184, scope=Scope.content)
    maxheight = Integer(help="Maximum height of the video", default=716, scope=Scope.content)
    
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def studio_view(self, context):
        """
        Studio view part
        """
        html_str = pkg_resources.resource_string(__name__, "static/html/officemix_edit.html")
        href = self.href or ''
        frag = Fragment(unicode(html_str).format(href=href, maxwidth=self.maxwidth, maxheight=self.maxheight))

        js_str = pkg_resources.resource_string(__name__, "/static/js/officemix_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('SimpleVideoEditBlock')

        return frag

    def author_view(self, context):
        """
        Author view part
        """

        embed_code = self.href or ''
        html_str = pkg_resources.resource_string(__name__, "static/html/officemix_author.html")
        frag = Fragment(unicode(html_str).format(embed_code=embed_code))

        return frag

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        Create a fragment used to display the XBlock to a student
        `context` is a dictionary used to configure the display (unused).

        Returns a `Fragment` object specifying hte HTML, CSS and JavaScript to display
        """
        embed_code = self.href or ''
        html_str = pkg_resources.resource_string(__name__, "static/html/officemix.html")
        frag = Fragment(unicode(html_str).format(self=self, embed_code=embed_code))

        # CSS
        css_str = pkg_resources.resource_string(__name__, "static/css/officemix.css")
        frag.add_css(unicode(css_str))

        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffic=''):
        self.href = data.get('href')
        self.maxwidth = data.get('maxwidth')
        self.maxheight = data.get('maxheight')

        return {'result': 'success'}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TestXBlock",
             """
             <testxblock href="https://mix.office.com/embed/1otxpj7hz6kbx" maxwidth="1200" />
             """),
        ]
