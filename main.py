import argparse

from adapter.cli import InfixCalculator, RPNCalculator


def main():
    """Точка входа в программу"""
    parser = argparse.ArgumentParser(
        prog='Calculator',
    )
    parser.add_argument('--rpn', action='store_true')
    args = parser.parse_args()
    cli = RPNCalculator() if args.rpn else InfixCalculator()
    cli.run()


if __name__ == '__main__':
    main()
