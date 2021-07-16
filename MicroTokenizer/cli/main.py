import plac
import sys
from MicroTokenizer.cli.commands.train import train


def main(args=None):
    commands = {
        'train': train,
    }
    if len(sys.argv) == 1:
        print("{title}: {content}, exits: {exits}".format(
            title="Available commands",
            content=', '.join(commands),
            exits=1)
        )

    command = sys.argv.pop(1)
    sys.argv[0] = 'MicroTokenizer %s' % command

    if command in commands:
        plac.call(commands[command], sys.argv[1:])
    else:
        print("{title}: {content}, exits: {exits}".format(
            title="Unknown command: %s" % command,
            content="Available: %s" % ', '.join(commands),
            exits=1)
        )


if __name__ == "__main__":
    main()
