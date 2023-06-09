from src.parser import parse_arguments
from src.helper import compare_args_and_possibility, get_file_content_input_file, alter_ter, alter_chain, alter_rna_dna, \
    write_content

if __name__ == "__main__":
    args = parse_arguments()
    edits = compare_args_and_possibility(args)
    content: list[str] = get_file_content_input_file(args.input_filename)

    if 'chain_id' in edits:
        content: list[str] = alter_chain(content, edits['chain_id'])
    if 'ter' in edits:
        content: list[str] = alter_ter(content, edits['ter'])
    if 'rna_dna' in edits:
        content: list[str] = alter_rna_dna(content, edits['rna_dna'])

    write_content(args.output_filename)
