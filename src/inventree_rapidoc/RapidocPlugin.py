"""Use RapiDoc for Inventree API docs."""

from django.urls import re_path

from drf_spectacular.plumbing import get_relative_url, set_query_parameters
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.utils import extend_schema
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from plugin import InvenTreePlugin
from plugin.mixins import AppMixin, UrlsMixin


class ApiDocView(APIView):
    """View to render the API schema with RapiDoc."""

    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = spectacular_settings.SERVE_PERMISSIONS
    url_name = "schema"

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        """Expand rendering function to add language parameter to schema url."""
        schema_url = get_relative_url(reverse(self.url_name, request=request))
        schema_url = set_query_parameters(schema_url, lang=request.GET.get("lang"))
        return Response(
            data={
                "title": spectacular_settings.TITLE + " - API docs",
                "schema_url": schema_url,
            },
            template_name="rapidoc.html",
        )


class RapidocPlugin(UrlsMixin, AppMixin, InvenTreePlugin):
    """Use RapiDoc for Inventree API docs."""

    NAME = "RapidocPlugin"
    SLUG = "inventree-rapidoc"
    TITLE = "InvenTree RapiDoc"

    def setup_urls(self):
        """Returns URL patterns for the plugin."""
        return [
            re_path(
                r"^doc/",
                ApiDocView.as_view(url_name="schema"),
                name="rapidoc",
            ),
        ]
