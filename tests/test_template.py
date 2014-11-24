#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_template
---------

Tests for `cookiecutter.template` module.
"""

from os.path import join, expanduser
import pytest

from cookiecutter.config import get_user_config
from cookiecutter.template import expand_abbreviations, resolve_template


def test_abbreviation_expansion():
    template = expand_abbreviations('foo', {'abbreviations': {'foo': 'bar'}})
    assert template == 'bar'


def test_abbreviation_expansion_not_an_abbreviation():
    template = expand_abbreviations('baz', {'abbreviations': {'foo': 'bar'}})
    assert template == 'baz'


def test_abbreviation_expansion_prefix():
    template = expand_abbreviations('xx:a', {'abbreviations': {'xx': '<{0}>'}})
    assert template == '<a>'


def test_abbreviation_expansion_builtin():
    template = expand_abbreviations('gh:a', {})
    assert template == 'https://github.com/a.git'


def test_abbreviation_expansion_override_builtin():
    template = expand_abbreviations('gh:a', {'abbreviations': {'gh': '<{0}>'}})
    assert template == '<a>'


def test_abbreviation_expansion_prefix_ignores_suffix():
    template = expand_abbreviations('xx:a', {'abbreviations': {'xx': '<>'}})
    assert template == '<>'


def test_abbreviation_expansion_prefix_not_0_in_braces():
    with pytest.raises(IndexError):
        expand_abbreviations('xx:a', {'abbreviations': {'xx': '{1}'}})


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
