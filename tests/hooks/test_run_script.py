# -*- coding: utf-8 -*-

import os
import pytest

from cookiecutter import hooks


@pytest.fixture
def hook_shell_script(tmpdir, shell_hook_content):
    script_dir = tmpdir

    hook_filename, hook_content = shell_hook_content('post_gen_project')
    post_gen_hook_file = script_dir / hook_filename
    post_gen_hook_file.write_text(hook_content, encoding='utf8')

    yield str(post_gen_hook_file)

    tmpdir.remove()


def test_run_script(hook_shell_script):
    """Execute a hook script, independently of project generation"""
    hooks.run_script(hook_shell_script)
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
