# (c) NephoScale, 2018

from django.utils.translation import ugettext_lazy as _

import horizon


class Tenants(horizon.Panel):
    name = _("Projects")
    slug = 'projects'
    policy_rules = (("identity", "identity:list_projects"),
                    ("identity", "identity:list_user_projects"))
