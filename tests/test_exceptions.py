# -*- coding: utf-8 -*-
import json

from jinja2.exceptions import UndefinedError

from cookiecutter import exceptions


def test_undefined_variable_to_str():
    context = {'cookiecutter': {'foo': 'bar'}}
    undefined_var_error = exceptions.UndefinedVariableInTemplate(
        'Beautiful is better than ugly',
        UndefinedError('Errors should never pass silently'),
        context
    )

    expected_str = '\n'.join([
        "Beautiful is better than ugly.",
        "Error message: Errors should never pass silently.",
        "Context: {}".format(json.dumps(context, indent=4, sort_keys=True))
    ])

    assert str(undefined_var_error) == expected_str
