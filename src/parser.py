import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='PDBuilder',
        description='This CLT simplifies some PDB editing steps in Felix\'s data processing pipeline.',
    )

    parser.add_argument('-i', '--input_filename', required=True)
    parser.add_argument('-o', '--output_filename', required=True)
    parser.add_argument('-t', '--ter', action='store_true')
    parser.add_argument('-c', '--chain_id', action='store_true')
    edits_rna_dna = parser.add_mutually_exclusive_group()
    edits_rna_dna.add_argument('-rrd', '--remove_rna_dna', action='store_true')
    edits_rna_dna.add_argument('-ar', '--add_rna', action='store_true')
    edits_rna_dna.add_argument('-ad', '--add_dna', action='store_true')
    return parser.parse_args()
