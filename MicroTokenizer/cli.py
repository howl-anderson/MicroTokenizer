# -*- coding: utf-8 -*-

"""Console script for MicroTokenizer."""
import plac
import sys
from .cli_command import (
    train,
    download,
    link
)


def main(args=None):
    commands = {
        'train': train,
        'download': download,
        'link': link
    }
    if len(sys.argv) == 1:
        print("{title}: {content}, exits: {exits}".format(
            content=', '.join(commands),
            title="Available commands",
            exits=1)
        )

    command = sys.argv.pop(1)
    sys.argv[0] = 'spacy %s' % command

    if command in commands:
        plac.call(commands[command], sys.argv[1:])
    else:
        print("{title}: {content}, exits: {exits}".format(
            content="Available: %s" % ', '.join(commands),
            title="Unknown command: %s" % command,
            exits=1)
        )


if __name__ == "__main__":
    main()
