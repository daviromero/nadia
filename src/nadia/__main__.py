import argparse
from nadia.nadia_pt_fo import check_proof
import os

parser = argparse.ArgumentParser(description='NADIA - Natural Deduction Proof Assistant.')
parser.add_argument("-i", type=str, required=True, help="Arquivo de entrada com a prova em NADIA.")
parser.add_argument("-t", type=str,default=None, help="Entre com o teorema a ser analisado.")
args = parser.parse_args()
if args.i is not None: fileName = args.i
if args.t is not None: input_theorem = args.t


def app(fileName, input_theorem):
    if not os.path.isfile(fileName):
        return "Arquivo não encontradao"
    f = open(fileName, 'r')

    input_proof = f.read()
    return check_proof(input_proof,input_theorem=input_theorem,show_fitch=False,show_gentzen=False)

print(app(fileName,input_theorem))