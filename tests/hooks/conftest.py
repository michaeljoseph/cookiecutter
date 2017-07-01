# -*- coding: utf-8 -*-

import pytest
import sys
import textwrap


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
