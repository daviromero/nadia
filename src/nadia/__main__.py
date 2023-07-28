import argparse
from nadia.nadia_pt_fo import check_proof

parser = argparse.ArgumentParser(description='NADIA - Natural Deduction Proof Assistant.')
parser.add_argument("-i", type=str,help="Arquivo de entrada com a prova em NADIA.")
args = parser.parse_args()
fileName = 'example_nadia.txt'
if args.i is not None: fileName = args.i


def app(fileName):
    f = open(fileName, 'r')
    print(f)
    if f==None:
        return "Arquivo não encontradao"

    input_proof = f.read()

    return check_proof(input_proof,show_fitch=False,show_gentzen=False)

print(app(fileName))