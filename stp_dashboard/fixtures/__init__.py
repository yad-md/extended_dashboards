#
# STP various fixtures
#


# *** Panels access policies fix ***

import horizon, os

from django.utils.importlib import import_module
from horizon import loaders
from horizon.base import Dashboard, Horizon

default_panel = {
    'admin':    'instances',
#    'identity': 'xusers'
}

policy_rules = {
    'project': {
        'rating':        (('identity', 'cloud_admin'),),
        'reporting':     (('identity', 'cloud_admin'),),
#        'stacks':        (('identity', 'cloud_admin'),),
#        'stacks.resource_types': (('identity', 'cloud_admin'),),
#        'containers':    (('identity', 'cloud_admin'),),
    },
    'admin': {
        '*':            (('identity', 'cloud_admin'),),
#        'overview':     (('identity', 'cloud_admin'),),
#        'metering':     (('identity', 'cloud_admin'),),
#        'hypervisors':  (('identity', 'cloud_admin'),),
#        'aggregates':   (('identity', 'cloud_admin'),),
#        'defaults':     (('identity', 'cloud_admin'),),
#        'metadata_defs':(('identity', 'cloud_admin'),),
#        'info':         (('identity', 'cloud_admin'),),
#        'hashmap':      (('identity', 'cloud_admin'),),
#        'rating_modules': (('identity', 'cloud_admin'),),
#        'pyscripts':    (('identity', 'cloud_admin'),),
    },

    'identity': {
        'domains':      (('identity', 'cloud_admin'),),
#        'projects':     (('identity', 'cloud_admin'),),
#        'xprojects':    (('identity', 'cloud_admin'),),
        'groups':       (('identity', 'cloud_admin'),),
        'roles':        (('identity', 'cloud_admin'),),
#        'invoice':      (('identity', 'cloud_admin'),),
        'billing':      (('identity', 'cloud_admin'),),
        'signups':      (('identity', 'cloud_admin'),),
    },

    'inventory': {
        '*':            (('identity', 'cloud_admin'),),
    },

    'sidecar_dashboard': {
        '*':            (('identity', 'cloud_admin'),),
    },

}


Dashboard.register_orig = Dashboard.register

@classmethod
def dashboard_register_mock(cls, panel):

    dashboard = horizon.get_dashboard(cls.slug)

    panel_policy_rules = []

    # apply common rules
    if cls.slug in policy_rules:
        if '*' in policy_rules[cls.slug]:
            panel_policy_rules.extend(policy_rules[cls.slug]['*'])
        # apply required permissions/policy_rules
        if cls.slug in policy_rules and panel.slug in policy_rules[cls.slug]:
            panel_policy_rules.extend(policy_rules[cls.slug][panel.slug])
        if len(panel_policy_rules) > 0:
            panel.policy_rules = panel_policy_rules

    # apply dashboard default panel
    if cls.slug in default_panel:
        dashboard.default_panel = default_panel[cls.slug]

    # register panel (original code)
    '''Registers a :class:`~horizon.Panel` with this dashboard.'''
    panel_class = Horizon.register_panel(cls, panel)
    # Support template loading from panel template directories.
    panel_mod = import_module(panel.__module__)
    panel_dir = os.path.dirname(panel_mod.__file__)
    template_dir = os.path.join(panel_dir, 'templates')
    if os.path.exists(template_dir):
        key = os.path.join(cls.slug, panel.slug)
        loaders.panel_template_dirs[key] = template_dir
    return panel_class

Dashboard.register = dashboard_register_mock

