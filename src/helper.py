import argparse
from src.exceptions import ChainIdentifierIrregularityError
from enum import Enum, unique


@unique
class Operations(Enum):
    Ter = 'ter'
    ChainID = 'chain_id'
    RnaDna = 'rna_dna'


@unique
class Characters(Enum):
    Rna = 'R'
    Dna = 'D'
    Chain = 'A'
    Empty = ' '


def compare_args_and_possibility(args: argparse.Namespace) -> dict:
    pdb_edits: dict = get_possibilities(args)
    possible_edits: list = [arg for arg in vars(args) if arg in pdb_edits and pdb_edits[arg]]
    desired_edits = [k for k, v in vars(args).items() if type(v) == bool]
    edit_intersection = set(desired_edits).intersection(set(possible_edits))
    return {k: v[1] for k, v in pdb_edits.items() if k in edit_intersection}


def get_possibilities(args: argparse.Namespace):
    check = CheckPossibilities(args)
    return {Operations.Ter: (check.edit_ter, check.ter_lines),
            Operations.ChainID: (check.edit_chain, check.chain_lines),
            Operations.RnaDna: (check.edit_rna_dna, check.rna_dna_lines)}


def alter_ter(content: list[str], edits: list) -> list[str]:
    altered_content = []
    for i, line in enumerate(content):
        if i not in edits:
            altered_content.append(line)
    return altered_content


def alter_chain(content: list[str], edits: list) -> list[str]:
    altered_content = []
    for i, line in enumerate(content):
        if i in edits:
            line = line[:21] + Characters.Chain.value + line[22:]
        altered_content.append(line)
    return altered_content


def alter_rna_dna(content: list[str], edits: list) -> list[str]:
    altered_content = []
    for i, line in enumerate(content):
        if i in edits:
            line = line[:18] + Characters.Empty.value + line[19:]
        altered_content.append(line)
    return altered_content


class CheckPossibilities:
    def __init__(self, args: argparse.Namespace):
        self.filename: str = args.input_filename
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
                    if line == Operations.Ter.upper() and file_content[i+1].strip() == Operations.Ter.upper():
                        self.edit_ter = True
                        self.ter_lines.append(i)
                except IndexError:
                    print(f'Found TER as last line in file, which causes IndexError -> please take a look at the file')
                    self.edit_ter = True
                    self.ter_lines.append(i)
                if line == Operations.Ter.upper() and file_content[i-1].startswith('ATOM')\
                        and file_content[i+1].startswith('ATOM'):
                    if file_content[i-1].strip()[21] == file_content[i+1].strip()[21] or \
                            not file_content[i-1].strip()[21] or \
                            not file_content[i+1].strip()[21]:
                        self.edit_ter = True
                        self.ter_lines.append(i)
                        print(f'Found TER between two ATOMS with same ChainIdentifier')

    def check_chain(self) -> None:
        with open(self.filename, 'r') as file:
            file_content: list = file.readlines()
            atom_lines: list[bool] = [bool(atom_line[21].strip()) for atom_line in file_content
                                      if atom_line.startswith('ATOM') and atom_line[21]]
            if len(set(atom_lines)) >= 2:
                raise ChainIdentifierIrregularityError
            if len(set(atom_lines)) == 1 and False in atom_lines:
                self.edit_chain = True
                self.chain_lines = [i for i in range(len(file_content)) if file_content[i].startswith('ATOM')]

    def check_drop_rna_dna(self) -> None:
        with open(self.filename, 'r') as file:
            file_content: list = file.readlines()
            atom_lines: list[bool] = [atom_line[18].strip() for atom_line in file_content
                                      if atom_line.startswith('ATOM') and atom_line[18]]
            if Characters.Dna.value or Characters.Rna.value in set(atom_lines):
                self.edit_rna_dna = True
                self.rna_dna_lines = [i for i in range(len(file_content)) if file_content[i].startswith('ATOM')]
