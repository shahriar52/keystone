# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_log import versionutils
from oslo_policy import policy

from keystone.common.policies import base

DEPRECATED_REASON = """
As of the Stein release, the domain API now understands how to handle
system-scoped tokens in addition to project-scoped tokens, making the API more
accessible to users without compromising security or manageability for
administrators. The new default policies for this API account for these changes
automatically
"""

deprecated_list_domains = policy.DeprecatedRule(
    name=base.IDENTITY % 'list_domains',
    check_str=base.RULE_ADMIN_REQUIRED
)
deprecated_get_domain = policy.DeprecatedRule(
    name=base.IDENTITY % 'get_domain',
    check_str=base.RULE_ADMIN_OR_TARGET_DOMAIN
)
deprecated_update_domain = policy.DeprecatedRule(
    name=base.IDENTITY % 'update_domain',
    check_str=base.RULE_ADMIN_REQUIRED
)
deprecated_create_domain = policy.DeprecatedRule(
    name=base.IDENTITY % 'create_domain',
    check_str=base.RULE_ADMIN_REQUIRED
)
deprecated_delete_domain = policy.DeprecatedRule(
    name=base.IDENTITY % 'delete_domain',
    check_str=base.RULE_ADMIN_REQUIRED
)

domain_policies = [
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'get_domain',
        check_str=(
            '(role:reader and system_scope:all) or '
            'token.project.domain.id:%(target.domain.id)s'
        ),
        # NOTE(lbragstad): This policy allows system-scope and project-scoped
        # tokens because it should be possible for users who have a token
        # scoped to a project within a domain to list the domain itself, at
        # least according to the legacy policy.
        scope_types=['system', 'project'],
        description='Show domain details.',
        operations=[{'path': '/v3/domains/{domain_id}',
                     'method': 'GET'}],
        deprecated_rule=deprecated_get_domain,
        deprecated_reason=DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.STEIN),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'list_domains',
        check_str=base.READER_ROLE,
        scope_types=['system'],
        description='List domains.',
        operations=[{'path': '/v3/domains',
                     'method': 'GET'}],
        deprecated_rule=deprecated_list_domains,
        deprecated_reason=DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.STEIN),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'create_domain',
        check_str=base.ADMIN_ROLE,
        scope_types=['system'],
        description='Create domain.',
        operations=[{'path': '/v3/domains',
                     'method': 'POST'}],
        deprecated_rule=deprecated_create_domain,
        deprecated_reason=DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.STEIN),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'update_domain',
        check_str=base.ADMIN_ROLE,
        scope_types=['system'],
        description='Update domain.',
        operations=[{'path': '/v3/domains/{domain_id}',
                     'method': 'PATCH'}],
        deprecated_rule=deprecated_update_domain,
        deprecated_reason=DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.STEIN),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'delete_domain',
        check_str=base.ADMIN_ROLE,
        scope_types=['system'],
        description='Delete domain.',
        operations=[{'path': '/v3/domains/{domain_id}',
                     'method': 'DELETE'}],
        deprecated_rule=deprecated_delete_domain,
        deprecated_reason=DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.STEIN),
]


def list_rules():
    return domain_policies
