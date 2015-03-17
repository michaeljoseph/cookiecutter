#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_resolve_template
---------------------

Tests for `cookiecutter.template` module.
"""

from os.path import join, expanduser
import pytest

from cookiecutter.config import get_user_config
from cookiecutter.template import resolve_template


def test_resolve_template():
    template = resolve_template(
        'https://bitbucket.org/pokoli/cookiecutter-trytonmodule',
        get_user_config(),
        no_input=True
    )

    assert template == join(
        expanduser('~/.cookiecutters'),
        'cookiecutter-trytonmodule'
    )
