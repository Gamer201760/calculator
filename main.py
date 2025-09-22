import argparse

from adapter.cli import SpaceInfixCalculator, SpaceRPNCalculator


def main():
    """Точка входа в программу"""
    parser = argparse.ArgumentParser(
        prog='Calculator',
    )
    parser.add_argument('--rpn', action='store_true')
    args = parser.parse_args()
    cli = SpaceRPNCalculator() if args.rpn else SpaceInfixCalculator()
    cli.run()


if __name__ == '__main__':
    main()
