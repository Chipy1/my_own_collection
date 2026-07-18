#!/usr/bin/python

# Copyright: (c) 2024, Chipy1 <chipy1@users.noreply.github.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Creates a text file on the remote host
description:
  - Creates a text file at the specified path with the specified content.
  - If the file already exists with the same content, no change is made (idempotent).
options:
  path:
    description: Path to the file to create
    required: true
    type: str
  content:
    description: Content to write to the file
    required: true
    type: str
author:
  - Chipy1 (@Chipy1)
'''

EXAMPLES = r'''
- name: Create a test file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/test.txt
    content: "Hello, world!"
'''

RETURN = r'''
path:
  description: Path of the file that was created/modified
  type: str
  returned: always
content:
  description: Content that was written
  type: str
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import os


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        path='',
        content='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['path'] = path
    result['content'] = content

    if os.path.exists(path):
        with open(path, 'r') as f:
            existing = f.read()
        if existing == content:
            module.exit_json(**result)

    if module.check_mode:
        module.exit_json(**result)

    with open(path, 'w') as f:
        f.write(content)

    result['changed'] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
