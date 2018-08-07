# -*- coding: utf-8 -*-

"""Console script for MicroTokenizer."""
import plac
import sys
from .cli_command import train


def _wrap(text, wrap_max=80, indent=4):
    """Wrap text at given width using textwrap module.

    text (unicode): Text to wrap. If it's a Path, it's converted to string.
    wrap_max (int): Maximum line length (indent is deducted).
    indent (int): Number of spaces for indentation.
    RETURNS (unicode): Wrapped text.
    """
    indent = indent * ' '
    wrap_width = wrap_max - len(indent)
    if isinstance(text, Path):
        text = path2str(text)
    return textwrap.fill(text, width=wrap_width, initial_indent=indent,
                         subsequent_indent=indent, break_long_words=False,
                         break_on_hyphens=False)


def prints(*texts, **kwargs):
    """Print formatted message (manual ANSI escape sequences to avoid
    dependency)

    *texts (unicode): Texts to print. Each argument is rendered as paragraph.
    **kwargs: 'title' becomes coloured headline. exits=True performs sys exit.
    """
    exits = kwargs.get('exits', None)
    title = kwargs.get('title', None)
    title = '\033[93m{}\033[0m\n'.format(_wrap(title)) if title else ''
    message = '\n\n'.join([_wrap(text) for text in texts])
    print('\n{}{}\n'.format(title, message))
    if exits is not None:
        sys.exit(exits)


def main(args=None):
    commands = {
        'train': train,
    }
    if len(sys.argv) == 1:
        prints(', '.join(commands), title="Available commands", exits=1)

    command = sys.argv.pop(1)
    sys.argv[0] = 'spacy %s' % command

    if command in commands:
        plac.call(commands[command], sys.argv[1:])
    else:
        prints(
            "Available: %s" % ', '.join(commands),
            title="Unknown command: %s" % command,
            exits=1)


if __name__ == "__main__":
    main()
