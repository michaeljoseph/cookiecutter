# -*- coding: utf-8 -*-

import os
import pytest
import sys
import textwrap

from cookiecutter import hooks


@pytest.yield_fixture
def repo_dir_with_hooks(tmpdir):
    """Yield a cookiecutter directory with hook files."""

    repo_dir = tmpdir
    hooks_dir = repo_dir.mkdir('hooks')

    pre_hook_content = textwrap.dedent(
        u"""\
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        from __future__ import print_function

        print('pre generation hook')
        f = open('python_pre.txt', 'w')
        f.close()
        """
    )
    pre_gen_hook_file = hooks_dir / 'pre_gen_project.py'
    pre_gen_hook_file.write_text(pre_hook_content, encoding='utf8')

    if sys.platform.startswith('win'):
        post_gen_hook_file = hooks_dir / 'post_gen_project.bat'
        post_hook_content = textwrap.dedent(
            u"""\
            @echo off

            echo post generation hook
            echo. >shell_post.txt
            """
        )
        post_gen_hook_file.write_text(post_hook_content, encoding='utf8')
    else:
        post_gen_hook_file = hooks_dir / 'post_gen_project.sh'
        post_hook_content = textwrap.dedent(
            u"""\
            #!/bin/bash

            echo 'post generation hook';
            touch 'shell_post.txt'
            """
        )
        post_gen_hook_file.write_text(post_hook_content, encoding='utf8')

    yield str(repo_dir)

    repo_dir.remove()


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


@pytest.yield_fixture
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
