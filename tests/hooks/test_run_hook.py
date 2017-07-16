# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import io
import os
import pytest

from cookiecutter import exceptions, hooks


def test_run_hook(tmpdir, monkeypatch, repo_dir_with_hooks):
    """Execute hook from specified template in specified output
    directory.
    """
    tests_dir = str(tmpdir)

    monkeypatch.chdir(repo_dir_with_hooks)

    hooks.run_hook('pre_gen_project', tests_dir, {})
    assert os.path.isfile(os.path.join(tests_dir, 'python_pre.txt'))

    hooks.run_hook('post_gen_project', tests_dir, {})
    assert os.path.isfile(os.path.join(tests_dir, 'shell_post.txt'))


def test_run_failing_hook(tmpdir, monkeypatch, repo_dir_with_hooks):
    tests_dir = str(tmpdir)

    hook_path = os.path.join(
        os.path.join(repo_dir_with_hooks, 'hooks'),
        'pre_gen_project.py'
    )

    with io.open(hook_path, 'w', encoding='utf-8') as f:
        f.write("#!/usr/bin/env python\n")
        f.write("import sys; sys.exit(1)\n")

    monkeypatch.chdir(repo_dir_with_hooks)
    with pytest.raises(exceptions.FailedHookException) as excinfo:
        hooks.run_hook('pre_gen_project', tests_dir, {})
    assert 'Hook script failed' in str(excinfo.value)
