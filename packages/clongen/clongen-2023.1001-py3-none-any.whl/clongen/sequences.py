from textwrap import dedent
from typing import NamedTuple

U6 = (
    "GAGGGCCTATTTCCCATGATTCCTTCATATTTGCATATACGATACAAGGCTGTTAGAGAGATAATTAGAATTAATTTGAC"
    "TGTAAACACAAAGATATTAGTACAAAATACGTGACGTAGAAAGTAATAATTTCTTGGGTAGTTTGCAGTTTTAAAATTAT"
    "GTTTTAAAATGGACTATCATATGCTTACCGTAACTTGAAAGTATTTCGATTTCTTGGCTTTATATATCTTGTGGAAAGGA"
    "CGAAACACCG"
)

REST = (
    "GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTT"
    "TTAAGCTTGGCGTAACTAGATCTTGAGACACTGCTTTTTGCTTGTACTGGGTCTCTCTGGTTAGACCAGATCTGAGCCTG"
    "GGAGCTCTCTGGCTAACTAGGGAACCCACTGCTTAAGCCTCAATAAAGCTTGCCTTGAGTGCTTCAAGTAGTGTGTGCCC"
    "GTCTGTTGTGTGACTCTGGTAACTAGAGATCCCTCAGACCCTTTTAGTCAGTGTGGAAAATCTCTAGCA"
)


class Lineage(NamedTuple):
    id: str
    lineage: str

    def sequence(self) -> str:
        return f"{U6}{self.lineage}{REST}"

    def fasta(self) -> str:
        return dedent(
            f"""
        >{self.id}
        {U6}{self.lineage}{REST}
        """
        )

    def gtf(self) -> str:
        # NOTE: length is hardcoded for now
        return (
            f"{self.id}\tunknown\texon\t1\t309\t.\t+\t.\t"
            f'gene_id "{self.id}"; transcript_id "{self.id}"; gene_name "{self.id}";\n'
        )
