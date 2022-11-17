import argparse
import traceback
from nadia_pt_fo import ParserNadia

parser = argparse.ArgumentParser(description='NADIA - Natural Deduction Proof Assistant.')
parser.add_argument("-i", type=str,help="Arquivo de entrada com a prova em NADIA.")
parser.add_argument("-o", type=str,help="Arquivo de saída do resultado da verificação da prova na NADIA")
args = parser.parse_args()
fileName = 'example_nadia.txt'
fileSave = 'result_nadia.txt'
if args.i is not None: fileName = args.i
if args.o is not None: fileSave = args.o

f = open(fileName, 'r')

text_input = f.read()

try:
    result = ParserNadia.getProof(text_input)

    with open(fileSave, "w", encoding='utf8') as fs:
        if(result.errors==[]):
            fs.write("A demonstração está correta.")
            fs.write("\n\nCódigo da demonstração no estilo Fitch em Latex:\n")
            fs.write(""+str(result.fitch))
            fs.write("\n\nCódigo da demonstração no estilo Gentzen em Latex:\n")
            fs.write(""+str(result.gentzen))
        else:
            fs.write("Os seguintes erros foram encontrados:\n\n")
            for error in result.errors:
                fs.write(str(error))
    fs.close()
except ValueError:
    s = traceback.format_exc()
    result = (s.split("@@"))[-1]
    with open(fileSave, "w", encoding='utf8') as fs:
        fs.write("Os seguintes erros foram encontrados:\n\n")
        fs.write(result)
    print (f'{result}')
else:
    pass