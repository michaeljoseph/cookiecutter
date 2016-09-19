# -*- coding: utf-8 -*-

import os
import pytest
import sys
import textwrap

from cookiecutter import hooks


@pytest.fixture
def hook_shell_script(tmpdir):
    script_dir = tmpdir

    if sys.platform.startswith('win'):
        post_gen_hook_file = script_dir / 'post_gen_project.bat'
        post_hook_content = textwrap.dedent(
            u"""\
            @echo off

            echo post generation hook
            echo. >shell_post.txt
            """
        )
        post_gen_hook_file.write_text(post_hook_content, encoding='utf8')

    else:
        post_gen_hook_file = script_dir / 'post_gen_project.sh'
        post_hook_content = textwrap.dedent(
            u"""\
            #!/bin/bash

            echo 'post generation hook';
            touch 'shell_post.txt'
            """
        )
        post_gen_hook_file.write_text(post_hook_content, encoding='utf8')

    return str(post_gen_hook_file)


def test_run_script(hook_shell_script):
    """Execute a hook script, independently of project generation"""
    hooks.run_script(
        os.path.join(hook_shell_script)
    )
    assert os.path.isfile('shell_post.txt')

    os.remove('shell_post.txt')


def test_run_script_cwd(hook_shell_script):
    """Change directory before running hook"""
    hooks.run_script(
        hook_shell_script,
        'tests'
    )
    assert os.path.isfile('tests/shell_post.txt')
    assert 'tests' not in os.getcwd()

    os.remove('tests/shell_post.txt')
