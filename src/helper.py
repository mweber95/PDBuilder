import argparse


def compare_args_and_possibility(args: argparse.Namespace):
    pass


def get_possibilities(args: argparse.Namespace):
    check = CheckPossibilities(args)
    return {'ter': check.edit_ter,
            'ter_lines' : check.ter_lines,
            'chain_id': check.edit_chain,
            'chain_id_lines': check.chain_lines,
            'rna_dna': check.edit_rna_dna,
            'rna_dna_lines': check.rna_dna_lines}


class CheckPossibilities:
    def __init__(self, args: argparse.Namespace):
        self.filename: str = args.filename
        self.edit_ter: bool = False
        self.ter_lines: list[int] = []
        self.edit_chain: bool = False
        self.chain_lines: list[int] = []
        self.edit_rna_dna: bool = False
        self.rna_dna_lines: list[int] = []
        self.check_ter()
        self.check_chain()
        self.check_drop_rna_dna()

    def check_ter(self) -> None:
        with open(self.filename, 'r') as file:
            file_content = file.readlines()
            for i, line in enumerate(file_content):
                line = line.strip()
                try:
                    if line == 'TER' and file_content[i+1].strip() == 'TER':
                        self.edit_ter = True
                        self.ter_lines.append(i)
                except IndexError:
                    print(f'Found TER as last line in file, which causes IndexError -> please take a look at the file')
                    self.edit_ter = True
                    self.ter_lines.append(i)
                if line == 'TER' and file_content[i-1].startswith('ATOM') and file_content[i+1].startswith('ATOM'):
                    if file_content[i-1].strip()[21] == file_content[i+1].strip()[21] or \
                            not file_content[i-1].strip()[21] or \
                            not file_content[i+1].strip()[21]:
                        self.edit_ter = True
                        self.ter_lines.append(i)
                        print(f'Found TER between two ATOMS with same ChainIdentifier')

    def check_chain(self) -> None:
        pass

    def check_drop_rna_dna(self) -> None:
        pass
