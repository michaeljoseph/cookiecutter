# -*- coding: utf-8 -*-

import os
import pytest
import sys
import textwrap

from cookiecutter import hooks


@pytest.fixture
def hook_shell_script_with_context(tmpdir):

    if sys.platform.startswith('win'):
        post_gen_hook_file = tmpdir / 'post_gen_project.bat'
        post_hook_content = textwrap.dedent(
            u"""\
            @echo off

            echo post generation hook
            echo. >{{cookiecutter.file}}
            """
        )
    else:
        post_gen_hook_file = tmpdir / 'post_gen_project.sh'
        post_hook_content = textwrap.dedent(
            u"""\
            #!/bin/bash

            echo 'post generation hook';
            touch '{{cookiecutter.file}}'
            """
        )

    post_gen_hook_file.write_text(post_hook_content, encoding='utf8')

    yield str(post_gen_hook_file)

    tmpdir.remove()


def test_run_script_with_context(hook_shell_script_with_context):
    """Execute a hook script, passing a context"""

    hooks.run_script_with_context(
        hook_shell_script_with_context,
        'tests',
        {
            'cookiecutter': {
                'file': 'context_post.txt'
            }
        })
    assert os.path.isfile('tests/context_post.txt')
    assert 'tests' not in os.getcwd()

    os.remove('tests/context_post.txt')
