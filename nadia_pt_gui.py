import ipywidgets as widgets
from IPython.display import display, Markdown
import traceback
from nadia_pt_fo import ParserNadia, ParserTheorem, ParserFormula

def nadia(input_string='', height_layout='300px',default_gentzen=True, default_fitch=True):
  layout = widgets.Layout(width='90%', height=height_layout)
  run = widgets.Button(description="Verificar")
  input = widgets.Textarea(
      value=input_string,
      placeholder='Digite sua demonstração:',
      description='',
      layout=layout
      )
  cGentzen = widgets.Checkbox(value=default_gentzen, description='Exibir Gentzen')
  cFitch = widgets.Checkbox(value=default_fitch, description='Exibir Fitch')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cGentzen, cFitch])
  
  display(widgets.HTML('<h3>Digite a demonstração em Dedução Natural:</h3>'), 
          input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
        result = ParserNadia.getProof(input.value)
        if result!=None:
          if(result.errors==[]):
              s_theorem = ParserNadia.toString(result.premisses, result.conclusion)
              l_theorem = ParserNadia.toLatex(result.premisses, result.conclusion)
              display(Markdown(rf'**<font color="blue">Parabéns! A demonstração de {s_theorem} está correta.</font>**'))
              msg =[]
              if(cGentzen.value):
                msg.append("Código Latex no Estilo de Gentzen:")
                msg.append("%"+l_theorem )
                msg.append(result.gentzen)
              if(cFitch.value):
                msg.append("Código Latex no Estilo de Fitch:")
                msg.append("%"+l_theorem )
                msg.append(result.fitch)
              display(widgets.HTML('<br>'.join(msg)))       
          else:
            display(Markdown(rf'**<font color="red">Sua demonstração contém os seguintes erros:</font>**'))
            for error in result.errors:
                print(error)
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def nadia_theorem(input_theorem, input_proof='', height_layout='300px',default_gentzen=False, default_fitch=False):
  layout = widgets.Layout(width='90%', height=height_layout)
  run = widgets.Button(description="Verificar")
  input = widgets.Textarea(
      value=input_proof,
      placeholder='Digite sua demonstração:',
      description='',
      layout=layout
      )
  premisses, conclusion = ParserTheorem.getTheorem(input_theorem)
  if conclusion == None:
    display(Markdown(rf'**<font color="red">{input_theorem} não é um teorema válido!</font>**'))
    return

  cGentzen = widgets.Checkbox(value=default_gentzen, description='Exibir Gentzen')
  cFitch = widgets.Checkbox(value=default_fitch, description='Exibir Fitch')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cGentzen, cFitch])
  
  display(widgets.HTML(f'<h3>Digite a demonstração de {input_theorem} em Dedução Natural:</h3>'), 
          input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
        result = ParserNadia.getProof(input.value)
        if result!=None:
          if(result.errors==[]):
              s_theorem = ParserNadia.toString(result.premisses, result.conclusion)
              l_theorem = ParserNadia.toLatex(result.premisses, result.conclusion)
              set_premisses = set([p.toString() for p in premisses])
              set_premisses_result = set([p.toString() for p in result.premisses])
              if(conclusion==result.conclusion and set_premisses==set_premisses_result):
                display(Markdown(rf'**<font color="blue">Parabéns! A demonstraçãoo de {s_theorem} está correta.</font>**'))
                msg =[]
                if(cGentzen.value):
                  msg.append("Código Latex no Estilo de Gentzen:")
                  msg.append("%"+l_theorem )
                  msg.append(result.gentzen)
                if(cFitch.value):
                  msg.append("Código Latex no Estilo de Fitch:")
                  msg.append("%"+l_theorem )
                  msg.append(result.fitch)
                display(widgets.HTML('<br>'.join(msg)))       
              else:
                display(Markdown(rf'**<font color="red">Sua demostração de {s_theorem} é válida, mas é diferente da demonstração solicitada {input_theorem}!</font>**'))

          else:
            display(Markdown(rf'**<font color="red">Sua demonstração contém os seguintes erros:</font>**'))
            for error in result.errors:
                print(error)
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

from random import randrange

lTheorems = [' |- Ax P(x)->~Ex ~P(x)', ' |- ~Ex ~P(x)->Ax P(x)', ' |- ~Ex ~P(x)->Ax P(x)', ' |- Ex P(x)->~Ax ~P(x)', ' |- Ax (P(x)&Q(x))->(Ax P(x)&Ax Q(x))', ' |- Ax Ay P(x,y)->Ay Ax P(x,y)', ' |- Ax (P->Q(x))->(P->Ax Q(x))', ' |- Ex (P(x)|Q(x))->(Ex P(x)|Ex Q(x))', ' |- ~Ax P(x)->Ex ~P(x)', ' |- Ex ~P(x)->~Ax P(x)', ' |- ~Ex P(x)->Ax ~P(x)', ' |- Ax ~P(x)->~Ex P(x)', ' |- Ex (P(x)&Q)->(Ex P(x)&Q)', ' |- (Ex P(x)&Q)->Ex (P(x)&Q)', ' |- Ax (P(x)|Q)->(Ax P(x)|Q)', ' |- (Ax P(x)|Q)->Ax (P(x)|Q)', ' |- Ex (P(x)->Q)->(Ax P(x)->Q)', ' |- (Ax P(x)->Q)->Ex (P(x)->Q)', ' |- Ex (P->Q(x))->(P->Ex Q(x))', ' |- (P->Ex Q(x))->Ex (P->Q(x))', ' |- Ex (P(x)->Ax P(x))']

import ipywidgets as widgets
from IPython.display import display, Markdown


def verifica_conclusao_valida(input_assumptions, input_conclusion, result_value=False):
  layout = widgets.Layout(width='40%')
  run = widgets.Button(description="Verificar")
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  cResult = widgets.RadioButtons(
    options=['Sim', 'Não'],
    value=None, 
    description='Resposta:',
    disabled=False
)
  questao = '**Considere as seguintes afirmações:**'
  i = 1
  for assumption in input_assumptions:
    questao += f'\n1. {assumption}'
    i+=1
  questao+='\n**Podemos concluir que a afirmação abaixo segue logicamente das afirmações acima?**'
  questao+=f'\n{i}. {input_conclusion}'
  display(Markdown(questao))
  display(widgets.HBox([cResult,wButtons]), output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      if (cResult.value==None):
        display(Markdown('<font color="red">**Escolha uma das alternativas! Tente novamente!**</font>'))
      elif(result_value==(cResult.value=='Sim')):
        display(Markdown('<font color="blue">**Parabéns, você acertou a questão.**</font>'))
      else:
        display(Markdown('<font color="red">**Infelizmente, você errou a questão. Tente novamente!**</font>'))
  run.on_click(on_button_run_clicked)


def verifica_eh_substituivel(input_formula='', input_var ='x', input_term='a'):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  cResult = widgets.RadioButtons(
    options=['Sim', 'Não'],
    value=None, 
    description='Resposta:',
    disabled=False
)
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**A variável {input_var} é substituível pelo termo {input_term} na fórmula {input_formula}:**'))
  display(cResult, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = ParserFormula.getFormula(input_formula)
          if(f!=None):
            if (f.is_substitutable(input_var,input_term) and cResult.value=='Sim'):
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão!</font>**'))              
              display(Markdown(rf'A variável {input_var} **é substituível** pelo termo {input_term} na fórmula {input_formula}.'))              
            elif not f.is_substitutable(input_var,input_term) and cResult.value=='Não':
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão!</font>**'))              
              display(Markdown(rf'A variável {input_var} **não é substituível** pelo termo {input_term} na fórmula {input_formula}.')) 
            else:
              display(Markdown(rf'**<font color="red">Infelizmente, você errou a questão.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verifica_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ;',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Digite o conjunto de variávels da fórmula {input_formula}:**'))
  display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.all_variables():
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão.</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Você errou a questão.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def verifica_free_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ;',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Digite o conjunto de variávels livres da fórmula {input_formula}:**'))
  display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.free_variables():
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão.</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Você errou a questão.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verifica_bound_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ;',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Digite o conjunto de variávels ligadas da fórmula {input_formula}:**'))
  display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.bound_variables():
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão.</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Você errou a questão.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verifica_substituicao(input_string='', input_formula = '', input_var ='x', input_term='a'):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite sua fórmula:',
      description='',
      layout=layout
      )
  cParentheses = widgets.Checkbox(value=False, description='Exibir Fórmula com Parênteses')
  cLatex = widgets.Checkbox(value=False, description='Exibir Fórmula em Latex')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cParentheses, cLatex])
  
  display(Markdown(rf'**Digite a fórmula que é resultado da substituição da variável {input_var} pelo termo {input_term} na fórmula {input_formula}:**'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = ParserFormula.getFormula(input_formula)
          result = ParserFormula.getFormula(input.value)
          if(result!=None):
            if result==f.substitution(input_var,input_term):
              display(Markdown(r'**<font color="blue">Parabéns essa é a subtituição correta:</font>**'))              
              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                display(Markdown(rf'{result.toString(parentheses=cParentheses.value)}'))
            else:
              display(Markdown(rf'**<font color="red">A fórmula {result.toString()} não é o resultado da substituição de {input_var} por {input_term} na fórmula {input_formula}.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

lTheorems = [' |- (A|(A&B))->A', 
        ' |- (A&(A|B))->A', 
        ' |- (A->(B->C))->(B->(A->C))', 
        ' |- (A->(A->B))->(A->B)', 
        ' |- (~A->B)->((~A->~B)->A)', 
        ' |- A|~A', 
        ' |- (A->B)|(B->A)', 
        ' |- A->A', 
        ' |- (A->B)->((C->A)->(C->A))', 
        'A&B->C |- B->(A->C)', 
        'B->(A->C) |- A&B->C', 
        ' |- (A->(B->C))->((A->B)->(A->C))', 
        ' |- A->(B->A)', 
        ' |- ((A->B)->A)->A', 
        'A->C, A|B, B->C |- C', 
        'A |- ~~A', '~~A |- A', 
        'A->B, ~B |- ~A', 
        '~B->~A |- A->B', 
        'A->B |- ~B->~A', 
        '~(A|B) |- ~A&~B', 
        '~A&~B |- ~(A|B)', 
        '~(A&B) |- ~A|~B', 
        '~A|~B |- ~(A&B)', 
        'A|(B&C) |- (A|B)&(A|C)', 
        '(A|B)&(A|C) |- A|(B&C)', 
        'A&(B|C) |- (A&B)|(A&C)', 
        '(A&B)|(A&C) |- A&(B|C)', 
        'A|B, ~B |- A', 
        'A|B |- ~A->B', 
        '~A->B |- A|B', 
        'A&B |- ~(A->~B)', 
        '~(A->~B) |- A&B', 
        'A|B |- ~(~A&~B)', 
        '~(~A&~B) |- A|B', 
        'A->B |- ~(A&~B)', 
        '~(A&~B) |- A->B', 
        'A&B |- ~(~A|~B)', 
        '~(~A|~B) |- A&B', 
        'A->B |- ~A|B', 
        '~A|B |- A->B', 
        ' |- Ax P(x)->~Ex ~P(x)', 
        ' |- ~Ex ~P(x)->Ax P(x)',  
        ' |- Ex P(x)->~Ax ~P(x)', 
        ' |- ~Ax ~P(x)->Ex P(x)', 
        ' |- Ax (P(x)&Q(x))->(Ax P(x)&Ax Q(x))', 
        ' |- Ax Ay P(x,y)->Ay Ax P(x,y)', 
        ' |- Ax (P->Q(x))->(P->Ax Q(x))', 
        ' |- Ex (P(x)|Q(x))->(Ex P(x)|Ex Q(x))', 
        ' |- ~Ax P(x)->Ex ~P(x)', 
        ' |- Ex ~P(x)->~Ax P(x)', 
        ' |- ~Ex P(x)->Ax ~P(x)', 
        ' |- Ax ~P(x)->~Ex P(x)', 
        ' |- Ex (P(x)&Q)->(Ex P(x)&Q)', 
        ' |- (Ex P(x)&Q)->Ex (P(x)&Q)', 
        ' |- Ax (P(x)|Q)->(Ax P(x)|Q)', 
        ' |- (Ax P(x)|Q)->Ax (P(x)|Q)', 
        ' |- Ex (P(x)->Q)->(Ax P(x)->Q)', 
        ' |- (Ax P(x)->Q)->Ex (P(x)->Q)', 
        ' |- Ex (P->Q(x))->(P->Ex Q(x))', 
        ' |- (P->Ex Q(x))->Ex (P->Q(x))', 
        ' |- Ex (P(x)->Ax P(x))'
        ]

def is_substitutable(input_formula='', input_var ='x', input_term='a'):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  cResult = widgets.RadioButtons(
    options=['Sim', 'Não'],
    value=None, 
    description='Resposta:',
    disabled=False
)
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**A variável {input_var} é substituível pelo termo {input_term} na fórmula {input_formula}:**'))
  display(cResult, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = ParserFormula.getFormula(input_formula)
          if(f!=None):
            if (f.is_substitutable(input_var,input_term) and cResult.value=='Sim'):
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão!</font>**'))              
              display(Markdown(rf'A variável {input_var} **é substituível** pelo termo {input_term} na fórmula {input_formula}.'))              
            elif not f.is_substitutable(input_var,input_term) and cResult.value=='Não':
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão!</font>**'))              
              display(Markdown(rf'A variável {input_var} **não é substituível** pelo termo {input_term} na fórmula {input_formula}.')) 
            else:
              display(Markdown(rf'**<font color="red">Infelizmente, você errou a questão.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ;',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Digite o conjunto de variávels da fórmula {input_formula}:**'))
  display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.all_variables():
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão.</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Você errou a questão.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def verify_free_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ;',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Digite o conjunto de variávels livres da fórmula {input_formula}:**'))
  display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.free_variables():
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão.</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Você errou a questão.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_bound_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ;',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Digite o conjunto de variávels ligadas da fórmula {input_formula}:**'))
  display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.bound_variables():
              display(Markdown(r'**<font color="blue">Parabéns você acertou a questão.</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Você errou a questão.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_substitution(input_string='', input_formula = '', input_var ='x', input_term='a'):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite sua fórmula:',
      description='',
      layout=layout
      )
  cParentheses = widgets.Checkbox(value=False, description='Exibir Fórmula com Parênteses')
  cLatex = widgets.Checkbox(value=False, description='Exibir Fórmula em Latex')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cParentheses, cLatex])
  
  display(Markdown(rf'**Digite a fórmula que é resultado da substituição da variável {input_var} pelo termo {input_term} na fórmula {input_formula}:**'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = ParserFormula.getFormula(input_formula)
          result = ParserFormula.getFormula(input.value)
          if(result!=None):
            if result==f.substitution(input_var,input_term):
              display(Markdown(r'**<font color="blue">Parabéns essa é a subtituição correta:</font>**'))              
              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                display(Markdown(rf'{result.toString(parentheses=cParentheses.value)}'))
            else:
              display(Markdown(rf'**<font color="red">A fórmula {result.toString()} não é o resultado da substituição de {input_var} por {input_term} na fórmula {input_formula}.</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def verify_valid_conclusion(input_assumptions, input_conclusion, result_value=False):
  layout = widgets.Layout(width='40%')
  run = widgets.Button(description="Verificar")
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  cResult = widgets.RadioButtons(
    options=['Sim', 'Não'],
    value=None, 
    description='Resposta:',
    disabled=False
)
  questao = '**Considere as seguintes afirmações:**'
  i = 1
  for assumption in input_assumptions:
    questao += f'\n1. {assumption}'
    i+=1
  questao+='\n**Podemos concluir que a afirmação abaixo segue logicamente das afirmações acima?**'
  questao+=f'\n{i}. {input_conclusion}'
  display(Markdown(questao))
  display(widgets.HBox([cResult,wButtons]), output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      if (cResult.value==None):
        display(Markdown('<font color="red">**Escolha uma das alternativas! Tente novamente!**</font>'))
      elif(result_value==(cResult.value=='Sim')):
        display(Markdown('<font color="blue">**Parabéns, você acertou a questão.**</font>'))
      else:
        display(Markdown('<font color="red">**Infelizmente, você errou a questão. Tente novamente!**</font>'))
  run.on_click(on_button_run_clicked)
