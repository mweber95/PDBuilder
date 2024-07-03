from src.parser import parse_arguments
from src.helper import (compare_args_and_possibility, alter_ter, alter_chain, remove_rna_dna, add_rna_dna,
                        Operations, Characters)
from src.file_operations import get_content_from_input, write_content_to_output

if __name__ == "__main__":
    args = parse_arguments()
    edits = compare_args_and_possibility(args)
    content: list[str] = get_content_from_input(args.input_filename)

    if Operations.ChainID.value in edits:
        content: list[str] = alter_chain(content, edits[Operations.ChainID.value])
    if Operations.RemoveRnaDna.value in edits:
        content: list[str] = remove_rna_dna(content, edits[Operations.RemoveRnaDna.value])
    if Operations.AddDna.value in edits:
        content: list[str] = add_rna_dna(content, edits[Operations.AddDna.value], Characters.Dna.value)
    if Operations.AddRna.value in edits:
        content: list[str] = add_rna_dna(content, edits[Operations.AddRna.value], Characters.Rna.value)
    if Operations.Ter.value in edits:
        content: list[str] = alter_ter(content, edits[Operations.Ter.value])

    write_content_to_output(args.output_filename, content)
