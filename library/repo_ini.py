#!/usr/bin/python
import os

from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.six as six

import ConfigParser

class RepoParser(ConfigParser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

DOCUMENTATION = '''
module: repo_ini
author:
  - Stan Chan <stanchan@gmail.com>
short_description: Returns a dictionary of an ini file.
description:
  - Returns a dictionary of an ini file.
version_added: "2.4"
options:
  path:
    description:
      - Path to the INI file
    required: true
    default: null
'''

EXAMPLES = '''
---
- hosts: localhost
  connection: local
  gather_facts: no
  tasks:
  - name: Read INI file
    repo_ini:
      path: file.repo
    register: repo_file
'''

def convert_ini(module, path):
    repo = RepoParser()
    try:
        with open(path) as fp:
            repo.readfp(fp)
    except IOError as e:
        raise ConfigParser.Error("Failed to read {}: {}".format(path, e))

    return repo.as_dict()

def main():
    """
    Ansible module to return an INI file as a python dictionary
    """
    argument_spec = {
        "path": {"required": True}
    }
    module = AnsibleModule(argument_spec=argument_spec)

    path = os.path.expanduser(module.params["path"])

    try:
        value = convert_ini(module, path)
        module.exit_json(path=path, changed=True, value=value)
    except ConfigParser.Error as e:
        module.fail_json(msg=str(e))

if __name__ == "__main__":
    main()
