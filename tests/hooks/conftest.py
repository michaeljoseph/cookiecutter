# -*- coding: utf-8 -*-

import pytest
import sys
import textwrap


@pytest.fixture
def shell_hook_content():
    def generate_hook(project_phase):
        if sys.platform.startswith('win'):
            hook_extension = 'bat'
            hook_content = textwrap.dedent(
                u"""\
                @echo off

                echo {} hook
                echo. >shell_post.txt
                """.format(
                    project_phase.replace('_', ' '),
                )
            )
        else:
            hook_extension = 'sh'
            hook_content = textwrap.dedent(
                u"""\
                #!/bin/bash

                echo '{} hook';
                touch 'shell_post.txt'
                """.format(
                    project_phase.replace('_', ' '),
                )
            )

        hook_filename = '{}.{}'.format(
            project_phase,
            hook_extension
        )
        return hook_filename, hook_content

    return generate_hook


@pytest.fixture
def repo_dir_with_hooks(tmpdir, shell_hook_content):
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

    hook_filename, hook_content = shell_hook_content('post_gen_project')
    hook_filename = hooks_dir / hook_filename
    hook_filename.write_text(hook_content, encoding='utf8')

    yield str(repo_dir)

    repo_dir.remove()
