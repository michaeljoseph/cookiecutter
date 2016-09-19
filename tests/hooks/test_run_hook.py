# -*- coding: utf-8 -*-

import os
import pytest
import sys
import textwrap

from cookiecutter import exceptions, hooks


@pytest.fixture
def repo_dir_with_hooks(tmpdir):
    repo_dir = tmpdir
    hooks_dir = repo_dir.mkdir('hooks')
    repo_dir.mkdir('input{{hooks}}')

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

    return str(repo_dir)


def test_run_hook(monkeypatch, repo_dir_with_hooks):
    """Execute hook from specified template in specified output
    directory.
    """
    tests_dir = os.path.join(repo_dir_with_hooks, 'input{{hooks}}')
    monkeypatch.chdir(repo_dir_with_hooks)

    hooks.run_hook('pre_gen_project', tests_dir, {})
    assert os.path.isfile(os.path.join(tests_dir, 'python_pre.txt'))

    hooks.run_hook('post_gen_project', tests_dir, {})
    assert os.path.isfile(os.path.join(tests_dir, 'shell_post.txt'))


def test_run_failing_hook(monkeypatch, repo_dir_with_hooks):
    hook_path = os.path.join(
        os.path.join(repo_dir_with_hooks, 'hooks'),
        'pre_gen_project.py'
    )
    tests_dir = os.path.join(repo_dir_with_hooks, 'input{{hooks}}')

    with open(hook_path, 'w') as f:
        f.write("#!/usr/bin/env python\n")
        f.write("import sys; sys.exit(1)\n")

    monkeypatch.chdir(repo_dir_with_hooks)
    with pytest.raises(exceptions.FailedHookException) as excinfo:
        hooks.run_hook('pre_gen_project', tests_dir, {})
    assert 'Hook script failed' in str(excinfo.value)
