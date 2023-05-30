import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='PDBuilder',
        description='This CLT simplifies annoying steps in Felix\'s data processing pipeline.',
    )

    parser.add_argument('-f', "--filename", required=True)
    parser.add_argument('-srd', "--switch_rna_dna", action='store_true')
    parser.add_argument('-drd', '--drop_rna_dna', action='store_true')
    return parser.parse_args()
