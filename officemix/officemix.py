"""

XBlock for Office Mix

Allows for the easy selection and embedding of an Office Mix within an XBlock.
Makes use of the Office Mix oEmbed entry points to look up the embed code and then
inserts it within the XBlock.

"""

import cgi
import decimal
import pkg_resources
import requests
import string

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment


class OfficeMixXBlock(XBlock):  # pylint: disable=too-many-ancestors
    """
    An XBlock providing Office Mix embedding capabilities
    """

    # Stored values for the XBlock
    href = String(
        display_name="Office Mix Embed URL",
        help="URL of the Office Mix you want to embed",
        scope=Scope.content,
        default='https://mix.office.com/watch/10g8h9tvipyg8')

    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="Office Mix")

    def studio_view(self, context):  # pylint: disable=unused-argument
        """
        Studio view part
        """

        href = self.href or ''
        display_name = self.display_name or ''

        html_str = self.resource_string("static/html/officemix_edit.html")
        frag = Fragment(html_str.format(href=cgi.escape(href), display_name=cgi.escape(display_name)))

        js_str = self.resource_string("/static/js/officemix_edit.js")
        frag.add_javascript(js_str)

        css_str = self.resource_string("/static/css/officemix_edit.css")
        frag.add_css(css_str)

        frag.initialize_js('OfficeMixEditBlock')

        return frag

    def student_view(self, context=None):  # pylint: disable=unused-argument
        """
        Create a fragment used to display the XBlock to a student
        `context` is a dictionary used to configure the display (unused).

        Returns a `Fragment` object specifying the HTML, CSS and JavaScript to display
        """
        href = self.href or ''
        display_name = self.display_name or ''

        # Make the oEmbed call to get the embed code
        try:
            embed_code, width, height = self.get_embed_code(href)
            html_str = self.resource_string("static/html/officemix.html")
        except requests.exceptions.HTTPError as ex:
            html_str = self.resource_string("static/html/embed_error.html")
            frag = Fragment(html_str.format(self=self, exception=cgi.escape(str(ex))))
            return frag

        # Grab and round the aspect ratio
        ratio = decimal.Decimal(float(height) / width * 100.0)

        # Construct the HTML
        frag = Fragment(html_str.format(
            self=self,
            embed_code=embed_code,
            display_name=cgi.escape(display_name)))

        # Construct the JavaScript
        frag.add_javascript(self.resource_string("/static/js/player-0.0.11.js"))
        frag.add_javascript(self.resource_string("/static/js/officemix_view.js"))

        # And construct the CSS
        css_str = self.resource_string("static/css/officemix.css")
        css_str = string.replace(unicode(css_str), "{aspect_ratio}", cgi.escape(unicode(round(ratio, 2))))
        frag.add_css(css_str)

        frag.initialize_js('OfficeMixBlock')
        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        AJAX handler to save the XBlock settings on Studio.
        """
        self.href = data.get('href')
        self.display_name = data.get('display_name')

        return {'result': 'success'}

    @XBlock.json_handler
    def publish_event(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        AJAX handler to allow client-side code to publish a server-side event.
        """
        try:
            event_type = data.pop('event_type')
        except KeyError:
            return {'result': 'error', 'message': 'Missing event_type in JSON data'}

        self.runtime.publish(self, event_type, data)
        return {'result': 'success'}

    @staticmethod
    def resource_string(path):
        """
        Handy helper for getting resources from our kit.
        """

        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @staticmethod
    def get_embed_code(url):
        """
        Makes an oEmbed call out to Office Mix to retrieve the embed code and width and height of the mix
        for the given url.
        """

        parameters = {'url': url}

        oembed_request = requests.get("https://mix.office.com/oembed/", params=parameters)
        oembed_request.raise_for_status()
        response_json = oembed_request.json()

        return response_json['html'], response_json['width'], response_json['height']

    @staticmethod
    def workbench_scenarios():
        """ Returns a single element which is the Office Mix xblock """
        return [
            ("Office Mix",
             """
             <officemix href="https://mix.office.com/watch/1otxpj7hz6kbx" />
             """),
        ]
