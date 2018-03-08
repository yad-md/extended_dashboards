from django.views.defaults import permission_denied
from openstack_dashboard import policy

import re

PATH_POLICY = (
    (r'^\/admin\/.*$', (("identity", "cloud_admin"),)),
)

class STPFixturesMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        for regex, rules in PATH_POLICY:
            if re.match(regex, request.path) and not policy.check(rules, request):
                return permission_denied(request)
        return None

