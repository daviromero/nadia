import argparse
from nadia.nadia_pt_fo import check_proof
import os


def main():
    parser = argparse.ArgumentParser(description='NADIA - Natural Deduction Proof Assistant.')
    parser.add_argument("-i", type=str, required=True, help="Arquivo de entrada com a prova em NADIA.")
    parser.add_argument("-t", type=str, help="Entre com o teorema a ser analisado.")
    parser.add_argument("-dg", type=int, default=0, help="Digite 1 para exibir o código LaTeX no estilo de Gentzen.")
    parser.add_argument("-df", type=int, default=0, help="Digite 1 para exibir o código LaTeX no estilo de Fitch.")
    parser.add_argument("-dt", type=int, default=0, help="Digite 1 para exibir o teorema.")
    args = parser.parse_args()
    input_theorem = None
    input_display_gentzen = False
    input_display_fitch = False
    input_display_theorem = False
    if args.i is not None: fileName = args.i
    if args.t is not None: input_theorem = args.t
    if args.dg is not None: input_display_gentzen = (args.dg==1)
    if args.df is not None: input_display_fitch = (args.df==1)
    if args.dt is not None: input_display_theorem = (args.dt==1)
    if not os.path.isfile(fileName):
        return "Arquivo não encontradao"
    f = open(fileName, 'r')

    input_proof = f.read()
    print( check_proof(input_proof,input_theorem=input_theorem, display_theorem=input_display_theorem, display_fitch=input_display_fitch,display_gentzen=input_display_gentzen))

    # print(app(fileName,input_theorem,input_display_theorem, input_display_fitch, input_display_gentzen))

if __name__ == '__main__':
    main()