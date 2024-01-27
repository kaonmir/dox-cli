# dox (DevOps eXperience)

`pip install -e .`: 소스코드를 빌드해 dox 명령어로 만든다. (로컬 개발용)

``` shell
# zsh을 할 때, dox 명령을 입력하면 폴더로 이동한다. 이를 막고 cli를 사용하려면 아래와 같이 설정한다.
echo "rehash" >> ~/.zshrc
```

## Setup flags and arguments

```python
r"""
    :param show_default: Show the default value for this option in its
        help text. Values are not shown by default, unless
        :attr:`Context.show_default` is ``True``. If this value is a
        string, it shows that string in parentheses instead of the
        actual value. This is particularly useful for dynamic options.
        For single option boolean flags, the default remains hidden if
        its value is ``False``.
    :param show_envvar: Controls if an environment variable should be
        shown on the help page. Normally, environment variables are not
        shown.
    :param prompt: If set to ``True`` or a non empty string then the
        user will be prompted for input. If set to ``True`` the prompt
        will be the option name capitalized.
    :param confirmation_prompt: Prompt a second time to confirm the
        value if it was prompted for. Can be set to a string instead of
        ``True`` to customize the message.
    :param prompt_required: If set to ``False``, the user will be
        prompted for input only when the option was specified as a flag
        without a value.
    :param hide_input: If this is ``True`` then the input on the prompt
        will be hidden from the user. This is useful for password input.
    :param is_flag: forces this option to act as a flag.  The default is
                    auto detection.
    :param flag_value: which value should be used for this flag if it's
                       enabled.  This is set to a boolean automatically if
                       the option string contains a slash to mark two options.
    :param multiple: if this is set to `True` then the argument is accepted
                     multiple times and recorded.  This is similar to ``nargs``
                     in how it works but supports arbitrary number of
                     arguments.
    :param count: this flag makes an option increment an integer.
    :param allow_from_autoenv: if this is enabled then the value of this
                               parameter will be pulled from an environment
                               variable in case a prefix is defined on the
                               context.
    :param help: the help string.
    :param hidden: hide this option from help outputs.
    :param attrs: Other command arguments described in :class:`Parameter`.


    :param param_decls: the parameter declarations for this option or
                        argument.  This is a list of flags or argument
                        names.
    :param type: the type that should be used.  Either a :class:`ParamType`
                 or a Python type.  The latter is converted into the former
                 automatically if supported.
    :param required: controls if this is optional or not.
    :param default: the default value if omitted.  This can also be a callable,
                    in which case it's invoked when the default is needed
                    without any arguments.
    :param callback: A function to further process or validate the value
        after type conversion. It is called as ``f(ctx, param, value)``
        and must return the value. It is called for all sources,
        including prompts.
    :param nargs: the number of arguments to match.  If not ``1`` the return
                  value is a tuple instead of single value.  The default for
                  nargs is ``1`` (except if the type is a tuple, then it's
                  the arity of the tuple). If ``nargs=-1``, all remaining
                  parameters are collected.
    :param metavar: how the value is represented in the help page.
    :param expose_value: if this is `True` then the value is passed onwards
                         to the command callback and stored on the context,
                         otherwise it's skipped.
    :param is_eager: eager values are processed before non eager ones.  This
                     should not be set for arguments or it will inverse the
                     order of processing.
    :param envvar: a string or list of strings that are environment variables
                   that should be checked.
    :param shell_complete: A function that returns custom shell
        completions. Used instead of the param's type completion if
        given. Takes ``ctx, param, incomplete`` and must return a list
        of :class:`~click.shell_completion.CompletionItem` or a list of
        strings.

```
