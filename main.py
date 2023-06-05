from src.parser import parse_arguments
from src.helper import get_possibilities, compare_args_and_possibility


if __name__ == "__main__":
    args = parse_arguments()
    operations: dict = get_possibilities(args)
    with open(args.filename) as file:
        if args.ter:
            pass
        if args.chain_id:
            pass
        if args.rna_dna:
            pass
