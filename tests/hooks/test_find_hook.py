# -*- coding: utf-8 -*-

import os
import sys
import textwrap

import pytest

from cookiecutter import hooks


def test_find_hook(monkeypatch, repo_dir_with_hooks):
    """Finds the specified hook."""

    monkeypatch.chdir(repo_dir_with_hooks)
    assert (
        os.path.abspath('hooks/pre_gen_project.py') ==
        hooks.find_hook('pre_gen_project')
    )

    post_hook_name = 'post_gen_project.{}'.format(
        'bat' if sys.platform.startswith('win') else 'sh'
    )
    assert (
        os.path.abspath('hooks/{}'.format(post_hook_name)) ==
        hooks.find_hook('post_gen_project')
    )


def test_no_hooks(monkeypatch):
    """find_hooks should return None if the hook could not be found."""
    monkeypatch.chdir('tests/fake-repo')
    assert None is hooks.find_hook('pre_gen_project')


def test_unknown_hooks_dir(monkeypatch, repo_dir_with_hooks):
    monkeypatch.chdir(repo_dir_with_hooks)
    assert hooks.find_hook(
        'pre_gen_project',
        hooks_dir='chooks'
    ) is None


def test_hook_not_found(monkeypatch, repo_dir_with_hooks):
    monkeypatch.chdir(repo_dir_with_hooks)
    assert hooks.find_hook('unknown_hook') is None


@pytest.fixture
def dir_with_hooks(tmpdir):
    """Yield a directory that contains hook backup files."""

    hooks_dir = tmpdir.mkdir('hooks')

    pre_hook_content = textwrap.dedent(
        u"""
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        print('pre_gen_project.py~')
        """
    )
    pre_gen_hook_file = hooks_dir / 'pre_gen_project.py~'
    pre_gen_hook_file.write_text(pre_hook_content, encoding='utf8')

    post_hook_content = textwrap.dedent(
        u"""
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        print('post_gen_project.py~')
        """
    )

    post_gen_hook_file = hooks_dir / 'post_gen_project.py~'
    post_gen_hook_file.write_text(post_hook_content, encoding='utf8')

    # Make sure to yield the parent directory as `find_hooks()`
    # looks into `hooks/` in the current working directory
    yield str(tmpdir)

    pre_gen_hook_file.remove()
    post_gen_hook_file.remove()


def test_ignore_hook_backup_files(monkeypatch, dir_with_hooks):
    # Change the current working directory that contains `hooks/`
    monkeypatch.chdir(dir_with_hooks)
    assert hooks.find_hook('pre_gen_project') is None
    assert hooks.find_hook('post_gen_project') is None
