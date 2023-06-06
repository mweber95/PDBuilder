import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='PDBuilder',
        description='This CLT simplifies annoying steps in Felix\'s data processing pipeline.',
    )

    parser.add_argument('-i', '--input_filename', required=True)
    parser.add_argument('-o', '--output_filename', required=True)
    parser.add_argument('-t', '--ter', action='store_true')
    parser.add_argument('-c', '--chain_id', action='store_true')
    parser.add_argument('-rd', '--rna_dna', action='store_true')
    return parser.parse_args()
