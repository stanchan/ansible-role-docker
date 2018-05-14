#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
lookup: repo_ini
author: Stan Chan <stanchan@gmail.com>
version_added: "2.4"
short_description: return a dictionary of an ini file.
description:
  - This lookup returns a dictionary of an ini file.
options:
  _terms:
    description: full or relative path to ini file
    required: True
"""
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

import os
import ConfigParser

class RepoParser(ConfigParser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []
        for term in terms:
            repo = RepoParser()
            path = os.path.expanduser(term)
            try:
                with open(path) as fp:
                    repo.readfp(fp)
            except IOError as e:
                raise ConfigParser.Error("Failed to read {}: {}".format(term, e))
            ret.append(repo.as_dict())
        return ret
