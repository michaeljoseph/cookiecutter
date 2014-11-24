#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.template
-----------------

Encapsulates cookiecutter templates.

"""
from __future__ import unicode_literals
import logging

from .vcs import clone


logger = logging.getLogger(__name__)

builtin_abbreviations = {
    'gh': 'https://github.com/{0}.git',
    'bb': 'https://bitbucket.org/{0}',
}


def expand_abbreviations(template, config_dict):
    """
    Expand abbreviations in a template name.

    :param template: The project template name.
    :param config_dict: The user config, which will contain abbreviation
        definitions.
    """

    abbreviations = builtin_abbreviations.copy()
    abbreviations.update(config_dict.get('abbreviations', {}))

    if template in abbreviations:
        return abbreviations[template]

    # Split on colon. If there is no colon, rest will be empty
    # and prefix will be the whole template
    prefix, sep, rest = template.partition(':')
    if prefix in abbreviations:
        return abbreviations[prefix].format(rest)

    return template


def resolve_template(template, tool_config, checkout=None, no_input=False):
    """
    Resolve the location of a cookiecutter template.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param tool_config: User cookiecutter configuration dict.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Prompt the user at command line for manual configuration?
    """

    template = expand_abbreviations(template, tool_config)

    # TODO: find a better way to tell if it's a repo URL
    if 'git@' in template or 'https://' in template:
        repo_dir = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=tool_config['cookiecutters_dir'],
            no_input=no_input
        )
    else:
        # If it's a local repo, no need to clone or copy to your
        # cookiecutters_dir
        repo_dir = template
    return repo_dir
