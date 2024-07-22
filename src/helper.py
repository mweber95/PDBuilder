import argparse
from src.exceptions import ChainIdentifierIrregularityError
from enum import Enum, unique


class Operations(Enum):
    Ter = 'ter'
    ChainID = 'chain_id'
    RemoveRnaDna = 'remove_rna_dna'
    AddRna = 'add_rna'
    AddDna = 'add_dna'


@unique
class Characters(Enum):
    Rna = 'R'
    Dna = 'D'
    Chain = 'A'
    Empty = ' '


def compare_args_and_possibility(args: argparse.Namespace) -> dict:
    pdb_edits: dict = get_possibilities(args)
    filter_pdb_edits: list = [k for k, v in pdb_edits.items() if v[0]]
    desired_edits: list = [k for k, v in args.__dict__.items() if type(v) == bool and v]
    edit_intersection = set(desired_edits).intersection(set(filter_pdb_edits))
    return {k: v for k, v in pdb_edits.items() if k in edit_intersection}


def get_possibilities(args: argparse.Namespace):
    check = CheckPossibilities(args)
    return {Operations.Ter.value: (check.edit_ter, check.ter_lines),
            Operations.ChainID.value: (check.edit_chain, check.chain_lines),
            Operations.RemoveRnaDna.value: (check.remove_rna_dna, check.remove_rna_dna_lines),
            Operations.AddDna.value: (check.add_dna, check.add_dna_lines),
            Operations.AddRna.value: (check.add_rna, check.add_rna_lines)}


def alter_ter(content: list[str], edits: list) -> list[str]:
    altered_content = []
    for i, line in enumerate(content):
        if i not in edits[-1]:
            altered_content.append(line)
    return altered_content


def alter_chain(content: list[str], edits: list) -> list[str]:
    altered_content = []
    for i, line in enumerate(content):
        if i in edits[-1]:
            line = line[:21] + Characters.Chain.value + line[22:]
        altered_content.append(line)
    return altered_content


def remove_rna_dna(content: list[str], edits: list) -> list[str]:
    altered_content = []
    for i, line in enumerate(content):
        if i in edits[-1]:
            line = line[:18] + Characters.Empty.value + line[19:]
        altered_content.append(line)
    return altered_content


def add_rna_dna(content: list[str], edits: list, value: str) -> list[str]:
    altered_content = []
    for i, line in enumerate(content):
        if i in edits[-1]:
            line = line[:18] + value + line[19:]
        altered_content.append(line)
    return altered_content


class CheckPossibilities:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.filename: str = self.args.input_filename
        self.edit_ter: bool = False
        self.ter_lines: list[int] = []
        self.edit_chain: bool = False
        self.chain_lines: list[int] = []
        self.remove_rna_dna: bool = False
        self.remove_rna_dna_lines: list[int] = []
        self.add_rna: bool = False
        self.add_dna: bool = False
        self.add_rna_lines: list[int] = []
        self.add_dna_lines: list[int] = []
        self.check_ter()
        self.check_chain()
        self.check_drop_rna_dna()
        self.check_add_rna_dna()

    def check_ter(self) -> None:
        with open(self.filename, 'r') as file:
            file_content = file.readlines()
            for i, line in enumerate(file_content):
                line = line.strip()
                try:
                    if line == Operations.Ter.value.upper() and file_content[i+1].strip() == Operations.Ter.value.upper():
                        self.edit_ter = True
                        self.ter_lines.append(i)
                except IndexError:
                    print(f'Found TER as last line in file, which causes IndexError -> please take a look at the file')
                    self.edit_ter = True
                    self.ter_lines.append(i)
                if line == Operations.Ter.value.upper() and file_content[i-1].startswith('ATOM')\
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
            if (Characters.Dna.value or Characters.Rna.value) in set(atom_lines):
                self.remove_rna_dna = True
                self.remove_rna_dna_lines = [i for i in range(len(file_content)) if file_content[i].startswith('ATOM')]

    def check_add_rna_dna(self) -> None:
        with open(self.filename, 'r') as file:
            file_content: list = file.readlines()
            atom_lines: list[bool] = [atom_line[19].strip() for atom_line in file_content
                                      if atom_line.startswith('ATOM') and atom_line[19]]
            if Characters.Dna.value and Characters.Rna.value not in set(atom_lines):
                self.add_dna = True
                self.add_dna_lines = [i for i in range(len(file_content)) if file_content[i].startswith('ATOM')]
                self.add_rna = True
                self.add_rna_lines = [i for i in range(len(file_content)) if file_content[i].startswith('ATOM')]
