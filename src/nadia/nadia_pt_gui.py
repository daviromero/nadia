import ipywidgets as widgets
from IPython.display import display, Markdown, HTML
import traceback
from nadia.nadia_pt_fo import ParserNadia, ParserTheorem, ParserFormula

def nadia(input_proof='', input_text_assumptions=[], input_text_conclusion='', height_layout='300px',default_gentzen=False, default_fitch=False):
  layout = widgets.Layout(width='90%', height=height_layout)
  run = widgets.Button(description="Verificar")
  input = widgets.Textarea(
      value=input_proof,
      placeholder='Digite sua demonstração:',
      description='',
      layout=layout
      )
  cGentzen = widgets.Checkbox(value=default_gentzen, description='Exibir Gentzen')
  cFitch = widgets.Checkbox(value=default_fitch, description='Exibir Fitch')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cGentzen, cFitch])
  
  if input_text_conclusion!='':
    display(Markdown( r'<b>Considere as seguintes afirmações:</b>'))
    q_assumptions =''
    i = 1
    for assumption in input_text_assumptions:
      q_assumptions += f'\n1. {assumption}'
      i+=1
    display(Markdown(q_assumptions))
    display(Markdown(r'<b>Considere a afirmação abaixo segue logicamente das afirmações acima:'))
    q_conclusion =f'\n{i}. {input_text_conclusion}'
    display(Markdown(q_conclusion))
    display(Markdown('### Represente as afirmações acima em lógica e digite sua demonstração em Dedução Natural:'))
    if input_proof=='':
      #input.value = '# Considere a seguinte linguagem não lógica:\n# - ...\n# - ...\n# - ...\n# Representamos as afirmações através das seguintes fórmulas:'
      input.value = '# Representamos as afirmações através das seguintes fórmulas:'
      i = 1
      for assumption in input_text_assumptions:
        input.value += f'\n# {i}. ... para "{assumption}"'
        i+=1
      input.value += f'\n# {i}. ... para "{input_text_conclusion}"'
      input.value += '\n# Assim, devemos demonstrar que o raciocínio abaixo é válido:'
      input.value += '\n# ...'
  else:  
    display(Markdown('### Digite sua demonstração em Dedução Natural:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
        result = ParserNadia.getProof(input.value)
        if result!=None:
          if(result.errors==[]):
              s_theorem = ParserNadia.toString(result.premisses, result.conclusion)
              l_theorem = ParserNadia.toLatex(result.premisses, result.conclusion)
              display(HTML(rf'<font color="blue">Parabéns! A demonstração de {s_theorem} está correta.</font>'))
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
            display(HTML(rf'<font color="red">Sua demonstração contém os seguintes erros:</font>'))
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
    display(HTML(rf'<font color="red">{input_theorem} não é um teorema válido!</font>'))
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
                display(HTML(rf'<font color="blue">Parabéns! A demonstração de {s_theorem} está correta.</font>'))
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
                display(HTML(rf'<font color="red">Sua demostração de {s_theorem} é válida, mas é diferente da demonstração solicitada {input_theorem}!</font>'))

          else:
            display(HTML(rf'<font color="red">Sua demonstração contém os seguintes erros:</font>'))
            for error in result.errors:
                print(error)
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


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
  
  display(HTML(rf'A variável {input_var} é substituível pelo termo {input_term} na fórmula {input_formula}:'))
  display(cResult, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = ParserFormula.getFormula(input_formula)
          if(f!=None):
            if (f.is_substitutable(input_var,input_term) and cResult.value=='Sim'):
              display(HTML(r'<font color="blue">Parabéns você acertou a questão!</font>'))              
              display(HTML(rf'A variável {input_var} é substituível pelo termo {input_term} na fórmula {input_formula}.'))              
            elif not f.is_substitutable(input_var,input_term) and cResult.value=='Não':
              display(HTML(r'<font color="blue">Parabéns você acertou a questão!</font>'))              
              display(HTML(rf'A variável {input_var} não é substituível pelo termo {input_term} na fórmula {input_formula}.')) 
            else:
              display(HTML(rf'<font color="red">Infelizmente, você errou a questão.</font>'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>'))
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
  
  display(HTML(rf'Digite o conjunto de variávels da fórmula {input_formula}:'))
  display(HTML(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.all_variables():
              display(HTML(r'<font color="blue">Parabéns você acertou a questão.</font>'))              
            else:
              display(HTML(rf'<font color="red">Você errou a questão.</font>'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>'))
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
  
  display(HTML(rf'Digite o conjunto de variávels livres da fórmula {input_formula}:'))
  display(HTML(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.free_variables():
              display(HTML(r'<font color="blue">Parabéns você acertou a questão.</font>'))              
            else:
              display(HTML(rf'<font color="red">Você errou a questão.</font>'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>'))
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
  
  display(HTML(rf'Digite o conjunto de variávels ligadas da fórmula {input_formula}:'))
  display(HTML(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.bound_variables():
              display(HTML(r'<font color="blue">Parabéns você acertou a questão.</font>'))              
            else:
              display(HTML(rf'<font color="red">Você errou a questão.</font>'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>'))
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
  
  display(HTML(rf'Digite a fórmula que é resultado da substituição da variável {input_var} pelo termo {input_term} na fórmula {input_formula}:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = ParserFormula.getFormula(input_formula)
          result = ParserFormula.getFormula(input.value)
          if(result!=None):
            if result==f.substitution(input_var,input_term):
              display(HTML(r'<font color="blue">Parabéns essa é a subtituição correta:</font>'))              
              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                display(HTML(rf'{result.toString(parentheses=cParentheses.value)}'))
            else:
              display(HTML(rf'<font color="red">A fórmula {result.toString()} não é o resultado da substituição de {input_var} por {input_term} na fórmula {input_formula}.</font>'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>'))
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
  questao = 'Considere as seguintes afirmações:'
  i = 1
  for assumption in input_assumptions:
    questao += f'\n1. {assumption}'
    i+=1
  questao+='\nPodemos concluir que a afirmação abaixo segue logicamente das afirmações acima?'
  questao+=f'\n{i}. {input_conclusion}'
  display(HTML(questao))
  display(widgets.HBox([cResult,wButtons]), output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      if (cResult.value==None):
        display(HTML('<font color="red">Escolha uma das alternativas! Tente novamente!</font>'))
      elif(result_value==(cResult.value=='Sim')):
        display(HTML('<font color="blue">Parabéns, você acertou a questão.</font>'))
      else:
        display(HTML('<font color="red">Infelizmente, você errou a questão. Tente novamente!</font>'))
  run.on_click(on_button_run_clicked)

def verify_formula(input_string=''):
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
  
  display(HTML(r'Digite sua fórmula:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input.value)
          if(result!=None):
              display(HTML(r'<font color="blue">Parabéns essa é uma fórmula da lógica:</font>'))
              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                display(HTML(rf'{result.toString(parentheses=cParentheses.value)}'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

