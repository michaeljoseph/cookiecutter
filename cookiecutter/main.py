#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.main
-----------------

Main entry point for the `cookiecutter` command.

The code in this module is also a good example of how to use Cookiecutter as a
library rather than a script.
"""

from __future__ import unicode_literals
import logging
import os

from .config import get_user_config
from .prompt import prompt_for_config
from .generate import generate_context, generate_files
from .template import resolve_template


logger = logging.getLogger(__name__)


def cookiecutter(template, checkout=None, no_input=False,
                 extra_context=None, overwrite=True):
    """
    API equivalent to using Cookiecutter at the command line.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Prompt the user at command line for manual configuration?
    :param extra_context: A dictionary of context that overrides default
        and user configuration.
    :param overwrite: Whether to prompt for overwriting files that exist
        and are different.
    """

    # Get user config from ~/.cookiecutterrc or equivalent
    # If no config file, sensible defaults from config.DEFAULT_CONFIG are used
    tool_config = get_user_config()

    repo_dir = resolve_template(template, tool_config, checkout, no_input)

    context_file = os.path.join(repo_dir, 'cookiecutter.json')
    context = generate_context(
        context_file=context_file,
        default_context=tool_config['default_context'],
        extra_context=extra_context,
    )

    # prompt the user to manually configure at the command line.
    # except when 'no-input' flag is set
    context['cookiecutter'] = prompt_for_config(context, no_input)

    # Create project from local context and project template.
    generate_files(
        repo_dir=repo_dir,
        context=context,
        overwrite=overwrite
    )
