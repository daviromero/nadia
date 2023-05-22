import rply
import traceback

## File formula.py
class BinaryFormula():
    def __init__(self, key = '', left = None, right = None):
        self.key = key
        self.left = left
        self.right = right

    def __eq__(self, other): 
        if not isinstance(other, BinaryFormula):
            return NotImplemented

        return self.key == other.key and self.left == other.left and self.right == other.right

    def __ne__(self, other): 
        if not isinstance(other, BinaryFormula):
            return NotImplemented

        return self.key != other.key or self.left != other.left or self.right != other.right

    def create_string_representation(self, formula, parentheses= False):
        if(parentheses):
          return formula.toString(parentheses=parentheses)
        elif isinstance(formula, BinaryFormula):
            return'({})'.format(formula.toString())
        else:
            return formula.toString()

    def create_latex_representation(self, formula, parentheses= False):
        if(parentheses):
          return formula.toLatex(parentheses=parentheses)
        elif isinstance(formula, BinaryFormula):
            return'({})'.format(formula.toLatex())
        else:
            return formula.toLatex()

    def is_implication(self):
      return self.key=='->'
    def is_conjunction(self):
      return self.key=='&'
    def is_disjunction(self):
      return self.key=='|'

    def toLatex(self, parentheses= False):
        operators = {
            '->': '\\rightarrow ',
            '&': '\\land ',
            '|': '\\lor ',
            '<->': '\\leftrightarrow ',
        }
        string = self.create_latex_representation(self.left, parentheses=parentheses)
        string += operators[self.key]
        string += self.create_latex_representation(self.right, parentheses=parentheses)
        if parentheses:
          return '('+string+')'
        return string

    def toString(self, parentheses= False):
        string = self.create_string_representation(self.left, parentheses=parentheses)
        string += self.key
        string += self.create_string_representation(self.right, parentheses=parentheses)
        if parentheses:
          return '('+string+')'
        return string

    def all_variables(self):
      return self.left.all_variables().union(self.right.all_variables())

    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      return self.left.free_variables().union(self.right.free_variables())

    def is_substitutable(self, x, y):
      return self.left.substitutable(x,y) and self.right.substitutable(x,y) 

    def substitution(self, var_x, a):
      return BinaryFormula(self.key, self.left.substitution(var_x, a), self.right.substitution(var_x, a))

class AndFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '&', left=left, right = right)

class OrFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '|', left=left, right = right)

class ImplicationFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '->', left=left, right = right)

class BiImplicationFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '<->', left=left, right = right)

class NegationFormula():
    def __init__(self, formula = None):
        self.formula = formula

    def __eq__(self, other): 
        if not isinstance(other, NegationFormula):
            return NotImplemented

        return self.formula == other.formula

    def __ne__(self, other): 
        if not isinstance(other, NegationFormula):
            return NotImplemented

        return self.formula != other.formula

    def toLatex(self, parentheses= False):
        if(parentheses):
          return '('+'\\lnot ' + self.formula.toLatex(parentheses=parentheses)+')'
        if not isinstance(self.formula, BinaryFormula):
            string = '\\lnot ' + self.formula.toLatex()
        else:
            string = '\\lnot({})'.format(self.formula.toLatex())
        return string   

    def toString(self, parentheses= False):
        if parentheses:
            string = '(~' + self.formula.toString(parentheses=parentheses)+')'
        elif not isinstance(self.formula, BinaryFormula):
            string = '~' + self.formula.toString()
        else:
            string = '~({})'.format(self.formula.toString())
        return string 

    def all_variables(self):
      return self.formula.all_variables()

    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      return self.formula.free_variables()

    def is_substitutable(self, x, y):
      return self.formula.substitutable(x,y)

    def substitution(self, var_x, a):
      return NegationFormula(self.formula.substitution(var_x, a))


class AtomFormula():
    def __init__(self, key = None):
        self.key = key

    def __eq__(self, other): 
        if not isinstance(other, AtomFormula):
            return NotImplemented

        return self.key == other.key
    
    def __ne__(self, other): 
        if not isinstance(other, AtomFormula):
            return NotImplemented

        return self.key != other.key

    def toLatex(self, parentheses= False):
        if(self.key != '@'):
            return self.key  
        else:
            return '\\bot' 

    def toString(self, parentheses= False):
        return self.key  

    def all_variables(self):
      return set()

    def bound_variables(self):
      return set()

    def free_variables(self):
      return set()

    def is_substitutable(self, x, y):
      return True 

    def substitution(self, var_x, a):
      return AtomFormula(self.key)

class BottonFormula(AtomFormula):
    def __init__(self):
      super().__init__(key='@')


class PredicateFormula():
    def __init__(self, name = '', variables = []):
        self.variables = variables
        self.name = name

    def __eq__(self, other): 
        if not isinstance(other, PredicateFormula):
            return NotImplemented
        return self.variables == other.variables and self.name == other.name
    
    def __ne__(self, other): 
        if not isinstance(other, PredicateFormula):
            return NotImplemented

        return self.variables != other.variables or self.name != other.name

    def toLatex(self, parentheses= False):
        if self.variables: 
            return self.name+'('+','.join(self.variables)+')'
        else:
            return self.name

    def toString(self, parentheses= False):
        if self.variables: 
            return self.name+'('+','.join(self.variables)+')'
        else:
            return self.name

    def all_variables(self):
      return set(self.variables)

    def bound_variables(self):
      return set()

    def free_variables(self):
      return set(self.variables)

    def is_substitutable(self, x, y):
      return True

    def substitution(self, var_x, a):
      aux_variables = []
      for v in self.variables:
        if(v==var_x): aux_variables.append(a)
        else: aux_variables.append(v)
      return PredicateFormula(self.name, aux_variables)

class QuantifierFormula():
    def __init__(self, forAll = True, variable=None, formula=None):
        self.forAll = forAll
        self.variable = variable
        self.formula = formula

    def __eq__(self, other): 
        if not isinstance(other, QuantifierFormula):
            return NotImplemented

        return self.forAll == other.forAll and self.variable == other.variable and self.formula == other.formula
    
    def __ne__(self, other): 
        if not isinstance(other, QuantifierFormula):
            return NotImplemented

        return self.forAll != other.forAll and self.variable != other.variable and self.formula != other.formula

    def is_universal(self):
      return self.forAll

    def is_existential(self):
      return not self.forAll

    def toLatex(self, parentheses= False):
        if parentheses:
          if self.forAll:        
              return '(\\forall {} {})'.format(self.variable, self.formula.toLatex(parentheses=parentheses))
          else:
              return '(\\exists {} {})'.format(self.variable, self.formula.toLatex(parentheses=parentheses))
        elif not isinstance(self.formula, BinaryFormula):
          if self.forAll:        
              return '\\forall {} {}'.format(self.variable, self.formula.toLatex())
          else:
              return '\\exists {} {}'.format(self.variable, self.formula.toLatex())
        else:
          if self.forAll:        
              return '\\forall {} ({})'.format(self.variable, self.formula.toLatex())
          else:
              return '\\exists {} ({})'.format(self.variable, self.formula.toLatex())

    def toString(self, parentheses= False):
        if parentheses:
          if self.forAll:        
              return '(A{} {})'.format(self.variable, self.formula.toString(parentheses=parentheses))
          else:
              return '(E{} {})'.format(self.variable, self.formula.toString(parentheses=parentheses))
        if not isinstance(self.formula, BinaryFormula):
          if self.forAll:        
              return 'A{} {}'.format(self.variable, self.formula.toString())
          else:
              return 'E{} {}'.format(self.variable, self.formula.toString())
        else:
          if self.forAll:        
              return 'A{} ({})'.format(self.variable, self.formula.toString())
          else:
              return 'E{} ({})'.format(self.variable, self.formula.toString())

    def all_variables(self):
      result = self.formula.all_variables()
      result.add(self.variable)
      return result
      
    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      result = self.formula.free_variables()
      result.discard(self.variable)
      return result 

    def is_substitutable(self, x, y):
      if (self.variable == y and x in self.formula.free_variables()):
        return False
      return self.formula.is_substitutable(x,y)# and (self.variable == y or x in self.formula.free_variables())

    def valid_substitution(self, formula):
      free_vars = formula.free_variables()
      for v in free_vars:
        fAux = self.formula.substitution(self.variable, v)
        if (fAux==formula):
          return True
      return False

    def substitution(self, var_x, a):
      if self.variable == var_x:
        return self#.formula#.clone()
      else:
        return QuantifierFormula(self.forAll,self.variable, self.formula.substitution(var_x, a))

class UniversalFormula(QuantifierFormula):
    def __init__(self, variable=None, formula=None):
      super().__init__( forAll = True, variable=variable, formula=formula)

class ExistentialFormula(QuantifierFormula):
    def __init__(self, variable=None, formula=None):
      super().__init__( forAll = False, variable=variable, formula=formula)



## File lexer.py
from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        #Comma
        self.lexer.add('COMMA', r'\,')

        # Dot
        self.lexer.add('DOT', r'\.')

        # Parentheses
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        #Brackets
        self.lexer.add('OPEN_BRACKET', r'\{')
        self.lexer.add('CLOSE_BRACKET', r'\}')

        # Vdash
        self.lexer.add('V_DASH', r'\|-|\|=')

        #rules
        self.lexer.add('IMP_INTROD', r'->i')
        self.lexer.add('IMP_ELIM', r'->e')
        self.lexer.add('OR_INTROD', r'\|i')
        self.lexer.add('OR_ELIM', r'\|e')
        self.lexer.add('AND_INTROD', r'&i')
        self.lexer.add('AND_ELIM', r'&e')
        self.lexer.add('NEG_INTROD', r'~i')
        self.lexer.add('NEG_ELIM', r'~e')
        self.lexer.add('RAA', r'raa')
        self.lexer.add('BOTTOM_ELIM', r'@e')
        self.lexer.add('COPY', r'copie')

        # Connectives
        self.lexer.add('BOTTOM', r'@')
        self.lexer.add('NOT', r'~')
        self.lexer.add('AND', r'&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('IMPLIE', r'->')
        self.lexer.add('IFF', r'<->')

        #First order rules
        self.lexer.add('EXT_INTROD', r'Ei')
        self.lexer.add('EXT_ELIM', r'Ee')
        self.lexer.add('ALL_INTROD', r'Ai')
        self.lexer.add('ALL_ELIM', r'Ae')

        #First order connectives
        self.lexer.add('EXT', r'E[a-z][a-z0-9]*')
        self.lexer.add('ALL', r'A[a-z][a-z0-9]*')

        # definitions
        self.lexer.add('DEF_NOT', r'def\~')
        self.lexer.add('DEF_IMPLIE', r'def\->')
        self.lexer.add('DEF_AND', r'def\&')
        self.lexer.add('DEF_OR', r'def\|')
        self.lexer.add('DEF_IFF', r'def\<->')
        self.lexer.add('DEF_BASE', r'defAtomos')

        # Dash
        self.lexer.add('DASH', r'-')

        # Number
        self.lexer.add('NUM', r'\d+')

        #justification
        self.lexer.add('HYPOTHESIS', r'hip')
        self.lexer.add('PREMISE', r'pre')

        #Variable
        self.lexer.add('VAR', r'(?!pre|hip)[a-z][a-z0-9]*')

        # Atom
        self.lexer.add('ATOM', r'[A-Z][A-Z0-9]*' )

        # Ignore spaces and comments
        self.lexer.ignore('##[^##]*##')
        self.lexer.ignore('#[^\n]*\n?')
        self.lexer.ignore('\s+')  

        # Detect symbols out of grammar
        self.lexer.add('OUT', r'.*' )      

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()


## File symbol_table.py

class SymbolTable:

    def toString(self):
      for i in range(len(self.symbol_table)):
        print(self.symbol_table['scope_{}'.format(i)])

    def len_symbol_table(self):
      r = 0
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['scope_{}'.format(i)]['rules']:
          r+=1
      return r

    def find_token(self, line):
      for i in range(len(self.symbol_table)):
        for j in range(len(self.symbol_table['scope_{}'.format(i)]['rules'])):
          if (self.symbol_table['scope_{}'.format(i)]['rules'][j].line==line):
            return self.symbol_table['scope_{}'.format(i)]['lines'][j]
      return None


    def check_is_visible(self, formula1_line, formula2_line):
      #Find formula1_line scope.
      if (int(formula1_line) <= int(formula2_line)): return False
      current_scope = None
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['scope_{}'.format(i)]['rules']:
          if rule and (rule.line == formula1_line):
            current_scope = self.symbol_table['scope_{}'.format(i)]
            break
        if current_scope != None: break
      #Check if formula2_line in formula1_line scope 
      while current_scope != None:
        for rule in current_scope['rules']:
          if rule and (rule.line == formula2_line):
            return True
        current_scope = self.symbol_table[current_scope['parent']] if 'parent' in current_scope else None
      return False

    def find_scope(self, line):
        for key, scope in self.symbol_table.items():
            for rule in scope['rules']:
                if rule and (rule.line == line):
                    return key 
        #Verifica se a linha não tem fórmula (introdução do universal)
        for key, scope in self.symbol_table.items():
          if(int(scope['start_line'])==int(line)):
            return key

        return None

    # Returns True if the scope variable of the line is a fresh variable, i.e., it did not occur before this scope. 
    def is_fresh_variable(self, line):
      current_scope = self.find_scope(line)
      variable = self.symbol_table[current_scope]['variable'] if current_scope!= None else None
      return not variable in self.get_free_variables_before_scope(line)

    def get_free_variables_before_scope(self, line):
      free_variables = set()
      #Find formula1_line scope.
      scope = self.find_scope(line)
      scope = self.symbol_table[scope]['parent'] if scope in self.symbol_table else None
      while scope != None:
          for rule in self.symbol_table[scope]['rules']:
            if (int(rule.line) < int(line)):
              free_variables = free_variables.union(rule.formula.free_variables())
            #Adds the variable for the universal introduction rule, i.e., if the line does not have a formula
            if (int(self.symbol_table[scope]['start_line'])<int(line) and self.symbol_table[scope]['variable']):
              free_variables = free_variables.union(set(self.symbol_table[scope]['variable']))
          scope = self.symbol_table[scope]['parent']
      return free_variables

    def get_visible_lines(self, formula1_line):
      #Find formula1_line scope.
      lines = []
      current_scope = None
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['scope_{}'.format(i)]['rules']:
          if rule and (rule.line == formula1_line):
            current_scope = self.symbol_table['scope_{}'.format(i)]
            break
        if current_scope != None: break
      #Check if formula2_line in formula1_line scope 
      while current_scope != None:
        for rule in current_scope['rules']:
          if rule and (int(rule.line) < int(formula1_line)):
            lines.append(rule.line)
        current_scope = self.symbol_table[current_scope['parent']] if current_scope['parent'] else None
      return lines
      
      
    def getPremisses(self):
      lines = []
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['scope_{}'.format(i)]['rules']:
          if(isinstance(rule, PremisseDef) ):
            lines.append(rule.line)
      return lines

    def getPremissesFormulas(self):
      formulas = []
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['scope_{}'.format(i)]['rules']:
          if(isinstance(rule, PremisseDef) and rule.formula not in formulas):
            formulas.append(rule.formula)
      return formulas

    def getConclusionFormula(self):
      if self.symbol_table["scope_0"]["rules"][-1]:
        return self.symbol_table["scope_0"]["rules"][-1].formula
      else:
        return None
    
    def theoremToString(self,parentheses=False):
      premissas = sorted([p.toString(parentheses=parentheses) for p in self.getPremissesFormulas()])
      fConclusion = self.getConclusionFormula()
      if(fConclusion):
        return (', '.join(premissas)+' |- '+fConclusion.toString(parentheses=parentheses))

    def theoremToLatex(self,parentheses=False):
      premisses = ([p.toLatex(parentheses=parentheses) for p in self.getPremissesFormulas()])
      fConclusion = self.getConclusionFormula()
      if(fConclusion):
        return (', '.join(premisses)+' \\vdash '+fConclusion.toLatex(parentheses=parentheses))

    def set_lines_visible(self):
        self.line_visible_lines = {}
        n = self.len_symbol_table()
        for i in range(1,n):
          self.line_visible_lines[str(i)] = self.get_visible_lines(str(i))



    def __init__(self):
        self.line_visible_lines = {}
        self.symbol_table = {
            'scope_0': {
                'name': 'scope_0',
                'parent': None,
                'rules': [],
                'lines': [],
                'variable': None,
                'start_line': '1', #Robson Não estava presente
                'end_line': '1'
            }
        }
        self.current_scope = 'scope_0'

    def insert(self, symbol, line):
        self.symbol_table[self.current_scope]['rules'].append(symbol)
        self.symbol_table[self.current_scope]['lines'].append(line)

    def start_scope(self, scope):
        self.current_scope = scope

    def end_scope(self, end_line):
        self.symbol_table[self.current_scope]['end_line'] = end_line
        if(self.symbol_table[self.current_scope]['parent'] is not None):
            self.current_scope = self.symbol_table[self.current_scope]['parent']

    def add_scope(self, start_line, variable=None):
        scope = 'scope_{}'.format(len(self.symbol_table))
        self.symbol_table[scope] = {
            'name': scope,
            'parent': self.current_scope,
            'rules': [],
            'lines': [],
            'variable': variable,
            'start_line': start_line,
            'end_line': start_line#Robson, não ser start_line        
            }
        self.start_scope(scope)

#    def find_scope(self, line):
#        for key, scope in self.symbol_table.items():
#            for rule in scope['rules']:
#                if rule and (rule.line == line):
#                    return key
#        return None

#    def find_scope_variable(self, line):
#        for key, scope in self.symbol_table.items():
#          print("key,scope['variable'], scope['start_line'],line,scope['end_line'], int(scope['start_line'])<=int(line) and int(line)<=int(scope['end_line'])")
#          print(key, scope['variable'], scope['start_line'],line,scope['end_line'], int(scope['start_line'])<=int(line) and int(line)<=int(scope['end_line']))
#          if(int(scope['start_line'])<=int(line) and int(line)<=int(scope['end_line'])):
#            print("find_scope_variable(self, line)",scope['variable'])
#            return scope['variable']
#        return None
    def find_scope_variable(self, line):
        scope = self.find_scope(line)
        if scope != None:
          return self.symbol_table[scope]['variable']
        #Verifica se a linha não tem fórmula (introdução do universal)
        for key, scope in self.symbol_table.items():
          if(int(scope['start_line'])==int(line)):
#            print("find_scope_variable(self, line)",scope['variable'])
            return scope['variable']          
        return None

    def check_scope_is_valid(self, scope):
        current_scope = self.current_scope
        while current_scope != None:
            if current_scope == scope:
                return True
            current_scope = self.symbol_table[current_scope]['parent']
        return False

    def lookup_formula_by_line(self, symbol_line, line):
        scope = self.find_scope(symbol_line)
        while scope != None:
            for rule in self.symbol_table[scope]['rules']:
                if rule.line == line:
                    return rule.formula
            scope = self.symbol_table[scope]['parent']
        return None

    def check_scope_delimiter(self, line1, line2):
        for key, scope in self.symbol_table.items():
            if key != 'scope_0':
                if(scope['start_line'] == line1 and scope['end_line'] == line2):
                    start_rule = scope['rules'][0].formula if scope['rules'][0] is not None else None
                    end_rule = scope['rules'][-1].formula if scope['rules'][-1] is not None else None
                    return (start_rule, end_rule)
        return None, None

    def get_box_start(self):
        if self.current_scope != 'scope_0':
            return self.symbol_table[self.current_scope]['start_line']
        return None

    def get_box_end(self):
        if self.current_scope != 'scope_0':
            return self.symbol_table[self.current_scope]['end_line']
        return None        

    def get_box_end(self, line):
        scope = self.find_scope(line)
        if scope != 'scope_0':
            return self.symbol_table[scope]['end_line']
        return None        

    def get_first_rule_from_scope(self, line):
        scope = self.find_scope(line)
        if self.symbol_table[scope]['rules']==[]: return None
        return self.symbol_table[scope]['rules'][0]
   
    def get_last_rule_from_scope(self):
        if self.symbol_table[self.current_scope]['rules']==[]: return None
        return self.symbol_table[self.current_scope]['rules'][-1]

    def get_rule(self, rule_line):
        for key, scope in self.symbol_table.items():
            for key, line in enumerate(scope['lines']):
                if line.value == rule_line:
                    return scope['rules'][key]
        return None

    def count_formulas_by_end_box(self, line):
        for key, scope in self.symbol_table.items():
            if key != 'scope_0':
                if(scope['end_line'] == line):
                    return (line - int(scope['start_line']))
        return 0

## dados_json.py
import json

class natural_deduction_return:
    def __init__(self):
        self.premisses = []
        self.conclusion = None
        self.gentzen = ""
        self.fitch = ""
        self.errors = []

    def add_error(self, error):
        self.errors.append(error)

    def to_json(self):
        result = {
            'gentzen': self.gentzen,
            'fitch': self.fitch,
            'errors': self.errors
        }
        with open("result.json", "w", encoding='utf8') as f:
            f.write(json.dumps(result, sort_keys=True, indent=3, ensure_ascii=False))

## File constants.py
class constants:
  REFERENCED_FORMULE_NONE = 0
  INVALID_RESULT = 1 # Conclusão inválida da regra
  UNEXPECT_RESULT = 2 # Escolha errada de regra
  SUCCESS = 3
  INVALID_HYPOTHESIS = 4
  NONE_COPY = 5
  COPY_DIFFERENT_FORMULE = 6
  AUTO_REFERENCE = 7
  LINE_REPETITION = 8
  REFERENCED_BOX_NONE = 9
  INVALID_HIP_PRE_WRITE = 10
  EXCEDENT_HIP_PRE_WRITE = 11
  USING_DESCARTED_RULE = 12
  REFERENCED_LINE_NOT_DEFINED = 13
  HYPOTHESIS_WITHOUT_BOX = 14
  CLOSE_BRACKET_WITHOUT_BOX = 15
  HYPOTHESIS_WITHOUT_CLOSED_BOX = 16
  BOX_MUST_BE_DISPOSED = 17
  LINES_MUST_BE_SEQUENCE = 18
  INVALID_SUBSTITUTION_UNIVERSAL = 19
  INVALID_UNIVERSAL_FORMULA = 20
  INVALID_SUBSTITUTION_EXISTS = 21
  INVALID_EXISTENCIAL_FORMULA = 22
  INVALID_SUBSTITUTION_EXISTENCIAL = 23
  VARIABLE_IS_NOT_FRESH_VARIABLE = 24
  INVALID_CONCLUSION_EXISTENCIAL = 25
  INVALID_CONCLUSION_UNIVERSAL = 26
  INVALID_SCOPE_DELIMITER = 27
  BOX_MUST_HAVE_A_VARIABLE = 28
  BOX_MUST_BE_DISPOSED_BY_RULE = 29
  INVALID_CONCLUSION_EXISTENCIAL_LAST_RULE = 30
  INVALID_BOX_RESULT = 31
  IS_NOT_DISJUNCTION = 32
  IS_NOT_CONJUNCTION = 33
  IS_NOT_IMPLICATION = 34
  INVALID_LEFT_CONJUNCTION = 35
  INVALID_RIGHT_CONJUNCTION = 36
  INVALID_NEGATION = 37
  INVALID_LEFT_OR_RIGHT_DISJUNCTION = 38
  INVALID_LEFT_OR_RIGHT_CONJUNCTION = 39
  IS_NOT_BOTTOM = 40
  INVALID_CONCLUSION_UNIVERSAL_LAST_RULE = 41
  BOX_MUST_HAVE_ONLY_A_VARIABLE = 42
  INVALID_RULE = 43
  INVALID_RULE_ONE_REFERENCE = 44


## File ast.py
hypothesis = {}

def limpaHipotese():
    global hypothesis
    hypothesis = {}


class PremisseDef():
    def __init__(self,line, formula):
        self.line = line
        self.formula = formula
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
        return

    def toLatex(self, symbol_table):
        latex = '{'+self.formula.toLatex()+'}'
        return latex

class HypothesisDef():
    def __init__(self,line, formula):
        self.line = line
        self.formula = formula
        self.copied = None
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
        return
#    def eval(self, symbol_table, formula_reference):
#        if symbol_table.get_box_end(self.line)==None:
#            return (constants.SUCCESS, None)
#        elif symbol_table.get_box_end(self.line)==0:
#            return (constants.HYPOTHESIS_WITHOUT_CLOSED_BOX,formula_reference)
#        return (constants.SUCCESS, None)

    def toLatex(self, symbol_table):
        line = self.copied if self.copied else self.line
        if line not in hypothesis:
            hypothesis[line] = str(len(hypothesis) + 1)
        latex = '\\big['+self.formula.toLatex()+'\\big]^{_{'+hypothesis[line]+'}}'
        return latex

class HypothesisFirstOrderDef():
    def __init__(self,line, var, formula):
        self.line = line
        self.formula = formula
        self.variable = var
        self.copied = None
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      return
#   def eval(self, symbol_table, formula_reference):
#        if symbol_table.get_box_end(self.line)==None:
#            return (constants.SUCCESS, None)
#        elif symbol_table.get_box_end(self.line)==0:
#            return (constants.HYPOTHESIS_WITHOUT_CLOSED_BOX,formula_reference)
#        return (constants.SUCCESS, None)

    def toLatex(self, symbol_table):
        line = self.copied if self.copied else self.line
        if line not in hypothesis:
            hypothesis[line] = str(len(hypothesis) + 1)
        latex = '\\big['+self.formula.toLatex()+'\\big]^{_{'+hypothesis[line]+'}}'
        return latex

class ImplicationEliminationDef():
    def __init__(self,line, formula, reference1, reference2):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line  and the refernce2 occur in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True, reference2=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      formula2 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference2.value)
      if(formula1==None or formula2==None or formula_reference==None):
        return

      if(BinaryFormula(key='->', left = formula1, right=self.formula) != formula2
      and BinaryFormula(key='->', left = formula2, right=self.formula) != formula1):
          deduction_result.add_error(parser.get_error(constants.INVALID_RESULT, self.reference1, self))

    def toLatex(self, symbol_table):
        latex = '\\infer[\\!\\!{\\rightarrow\\text{e}}]{'+self.formula.toLatex()+'}{{'+symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)+'}&{'+symbol_table.get_rule(self.reference2.value).toLatex(symbol_table)+'}}'
        return latex

class ImplicationIntroductionDef():
    def __init__(self,line, formula, reference1, reference2):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the box is a valid scope
      valid_box = parser.check_scope_reference_error(deduction_result,self)

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1, formula2 = parser.symbol_table.check_scope_delimiter(self.reference1.value, self.reference2.value)
      if(formula1==None or formula2==None or formula_reference==None):
        return

      # If the formula is not an implicaton formula
      if(not isinstance(self.formula, BinaryFormula) or (isinstance(self.formula, BinaryFormula) and not self.formula.is_implication())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_RESULT, formula_reference, self))
      else:
          # If the hypothese (reference1) is the left formula of the conclusion
          if(self.formula.left != formula1):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_HYPOTHESIS, self.reference1, self))
          # If the conclusion of the box (reference2) is the right formula of the conclusion
          if(self.formula.right != formula2):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_BOX_RESULT, self.reference2, self))


    def toLatex(self, symbol_table):
        hypothesis_number = str(len(hypothesis) + 1)
        hypothesis[self.reference1.value] = hypothesis_number
        latex = '\\infer[\\!\\!{\\rightarrow\\text{i}^{_'+ hypothesis_number +'}}]{'+self.formula.toLatex()+'}{'+symbol_table.get_rule(self.reference2.value).toLatex(symbol_table)+'}'
        return latex

class DisjunctionIntroductionDef():
    def __init__(self, line, formula, reference1):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      if(formula1==None):
        return

      # If the formula (reference 1) is not a disjunction formula
      if(not isinstance(self.formula, BinaryFormula) or (isinstance(self.formula, BinaryFormula) and not self.formula.is_disjunction())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_DISJUNCTION, formula_reference, self))
      else:
          # If the left formula of conclusion (the conjunction) is one of the references 
          if(not (self.formula.left == formula1 or self.formula.right == formula1)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_OR_RIGHT_DISJUNCTION, self.reference1, self))

    def toLatex(self, symbol_table):
        latex = '\\infer[\\!\\!{\\lor\\text{i}}]{'+self.formula.toLatex()+'}{'+symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)+'}'
        return latex
        
class AndIntroductionDef():
    def __init__(self,line, formula, reference1, reference2):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 and referece2 line occur in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True, reference2=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      formula2 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference2.value)
      if(formula1==None or formula2==None or formula_reference==None):
        return

      # If the formula (reference 1) is not a conjunction formula
      if(not isinstance(self.formula, BinaryFormula) or (isinstance(self.formula, BinaryFormula) and not self.formula.is_conjunction())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_CONJUNCTION, self.reference1, self))
      else:
          # If the left formula of conclusion (the conjunction) is one of the references 
          if(not (self.formula.left == formula1 or self.formula.left == formula2)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_CONJUNCTION, formula_reference, self))
          # If the right formula of conclusion (the conjunction) is one of the references 
          if(not (self.formula.right == formula1 or self.formula.right == formula2)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_RIGHT_CONJUNCTION, formula_reference, self))

    def toLatex(self, symbol_table):
        latex = '\\infer[\\!\\!{\\land\\text{i}}]{'+self.formula.toLatex()+'}{{'+symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)+'}&{'+symbol_table.get_rule(self.reference2.value).toLatex(symbol_table)+'}}'
        return latex

class AndEliminationDef():
    def __init__(self, line, formula, reference1):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      if(formula1==None):
        return

      # If the formula (reference 1) is not a conjunction formula
      if(not isinstance(formula1, BinaryFormula) or (isinstance(formula1, BinaryFormula) and not formula1.is_conjunction())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_CONJUNCTION, formula_reference, self))
      else:
          # If the left formula of conclusion (the conjunction) is one of the references 
          if(not (formula1.left == self.formula or formula1.right == self.formula)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_OR_RIGHT_CONJUNCTION, self.reference1, self))

    def toLatex(self, symbol_table):
        latex = '\\infer[\\!\\!{\\land\\text{e}}]{'+self.formula.toLatex()+'}{'+symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)+'}'
        return latex

class DisjunctionEliminationDef():
    def __init__(self,line, formula, reference1, reference2, reference3, reference4, reference5):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.reference3 = reference3
        self.reference4 = reference4
        self.reference5 = reference5
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the box is a valid scope
      valid_box = parser.check_scope_reference_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      if(formula1==None):
        return
      formula2, formula3 = parser.symbol_table.check_scope_delimiter(self.reference2.value, self.reference3.value)
      formula4, formula5 = parser.symbol_table.check_scope_delimiter(self.reference4.value, self.reference5.value)
      if(formula1==None or formula2==None or formula3==None or formula4==None or formula_reference==None):
        return

      # If the formula (reference 1) is not a disjunction formula
      if(not isinstance(formula1, BinaryFormula) or (isinstance(formula1, BinaryFormula) and not formula1.is_disjunction())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_DISJUNCTION, self.reference1, self))
      else:
          # If the hypothese (reference1) is the left formula of the disjunction formula
          if(formula1.left != formula2):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_HYPOTHESIS, self.reference2, self))
          # If the conclusion of the box (reference2) is the right formula of the conclusion
          if(formula1.right != formula4):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_HYPOTHESIS, self.reference4, self))
          # If the conclusion of the box (reference3) it the same of the conclusion
          if(self.formula != formula3):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_BOX_RESULT, self.reference3, self))
          # If the conclusion of the box (reference5) it the same of the conclusion
          if(self.formula != formula5):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_BOX_RESULT, self.reference5, self))

    def toLatex(self, symbol_table):
        hypothesis_number1 = str(len(hypothesis) + 1)
        hypothesis[self.reference2.value] = hypothesis_number1
        hypothesis_number2 = str(len(hypothesis) + 1)
        hypothesis[self.reference4.value] = hypothesis_number2
        latex = '\\infer[\\!\\!{\\lor\\text{e}^{_{'+ hypothesis_number1 + ', ' + hypothesis_number2 +'} } }]{'+self.formula.toLatex()+'}{{'+symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)+'}&{'+symbol_table.get_rule(self.reference3.value).toLatex(symbol_table)+'}&{'+symbol_table.get_rule(self.reference5.value).toLatex(symbol_table)+'}}'
        return latex

class NegationIntroductionDef():
    def __init__(self,line, formula, reference1, reference2):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the box is a valid scope
      valid_box = parser.check_scope_reference_error(deduction_result,self)

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1, formula2 = parser.symbol_table.check_scope_delimiter(self.reference1.value, self.reference2.value)
      if(formula1==None or formula2==None or formula_reference==None):
        return

      # If the formula is not a negation formula
      if(not isinstance(self.formula, NegationFormula)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_RESULT, formula_reference, self))
      else:
          # If the hypothese (reference1) is the left formula of the conclusion
          if(self.formula != NegationFormula(formula1)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_HYPOTHESIS, self.reference1, self))
          # If the conclusion of the box (reference2) is the @
          if(formula2.toString() != '@'):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_BOX_RESULT, self.reference2, self))

    def toLatex(self, symbol_table):
        hypothesis_number = str(len(hypothesis) + 1)
        hypothesis[self.reference1.value] = hypothesis_number
        latex = '\\infer[\\!\\!{\\lnot\\text{i}^{_'+ hypothesis_number +'}}]{'+self.formula.toLatex()+'}{'+symbol_table.get_rule(self.reference2.value).toLatex(symbol_table)+'}'
        return latex

class NegationEliminationDef():
    def __init__(self,line, formula, reference1, reference2):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True, reference2=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      formula2 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference2.value)
      if(formula1==None or formula2==None or formula_reference==None):
        return

      # If the formula (reference 1) is not a contradiction
      if(self.formula.toString()!='@'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_RESULT, formula_reference, self))
      else:
          # If the left formula of conclusion (the conjunction) is one of the references 
          if(not (NegationFormula(formula2) == formula1 or NegationFormula(formula1) == formula2)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_NEGATION, self.reference1, self))

    def toLatex(self, symbol_table):
        latex = '\\infer[\\!\\!{\\lnot\\text{e}}]{'+self.formula.toLatex()+'}{{'+symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)+'}&{'+symbol_table.get_rule(self.reference2.value).toLatex(symbol_table)+'}}'
        return latex

class BottomDef():
    def __init__(self,line, formula, reference1):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.is_copied = False
    
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      if(formula1==None):
        return

      # If the formula (reference 1) is not a bottom formula
      if(formula1.toString()!='@'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_BOTTOM, self.reference1, self))

    def toLatex(self, symbol_table):
        latex = '\\infer[\\!\\!{\\bot e}]{'+self.formula.toLatex()+'}{'+symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)+'}'
        return latex

class RaaDef():
    def __init__(self,line, formula, reference1, reference2):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the box is a valid scope
      valid_box = parser.check_scope_reference_error(deduction_result,self)

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1, formula2 = parser.symbol_table.check_scope_delimiter(self.reference1.value, self.reference2.value)
      if(formula1==None or formula2==None or formula_reference==None):
        return

      # If the hypothese (reference1) is the left formula of the conclusion
      if(formula1 != NegationFormula(self.formula)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_HYPOTHESIS, self.reference1, self))
      # If the conclusion of the box (reference2) is the @
      if(formula2.toString() != '@'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_BOX_RESULT, self.reference2, self))

    def toLatex(self, symbol_table):
        hypothesis_number = str(len(hypothesis) + 1)
        hypothesis[self.reference1.value] = hypothesis_number
        latex = '\\infer[\\!\\!{\\text{raa}^_{'+ hypothesis_number +'} }]{'+self.formula.toLatex()+'}{'+symbol_table.get_rule(self.reference2.value).toLatex(symbol_table)+'}'
        return latex

class CopyDef():
    def __init__(self, line, formula, reference1):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      if(formula1==None):
        return

      # If the formula (reference 1) is not a conjunction formula
      if(formula1!=self.formula):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.COPY_DIFFERENT_FORMULE, formula_reference, self))

    def toLatex(self, symbol_table):
        formula1 = symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
        latex = '{'+formula1.toLatex()+'}'
#        latex = '{'+self.formula.toLatex()+'}'#'\\infer[\\!\\!{\\land\\text{e}}]{'+self.formula.toLatex()+'}{'+symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)+'}'
        return latex

class WrongDef():
    def __init__(self,line, formula):
        self.line = line
        self.formula = formula
        self.is_copied = False

class ForAllEliminationDef():
    def __init__(self, line, formula, reference1):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      if(formula1==None):
        return

      # If the formula is not a universal formula
      if(not isinstance(formula1, QuantifierFormula) or (isinstance(formula1, QuantifierFormula) and not formula1.is_universal())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_UNIVERSAL_FORMULA, self.reference1, self))

      # If the conclusion is a valid substitution of the universal formula (referecence 1)
      if(isinstance(formula1, QuantifierFormula) and not formula1.valid_substitution(self.formula)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_SUBSTITUTION_UNIVERSAL, formula_reference, self))

    def toLatex(self, symbol_table):
        latex = '\\infer[\\!\\!\\forall\\text{e}]{'
        latex += self.formula.toLatex()
        latex += '}{'
        latex += symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)
        latex += '}'
        return latex


class ExistsIntroductionDef():
    def __init__(self, line, formula, reference1):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True)      


      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      if(formula1==None):
        return
      # If the formula is not a existential formula
      if(not isinstance(self.formula, QuantifierFormula) or (isinstance(self.formula, QuantifierFormula) and not self.formula.is_existential())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_EXISTENCIAL_FORMULA, formula_reference, self))
      # If the conclusion is a valid substitution for the variable in formula1
      if(isinstance(self.formula, QuantifierFormula) and not self.formula.valid_substitution(formula1)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_SUBSTITUTION_EXISTS, formula_reference, self))

    def toLatex(self, symbol_table):
        latex = '\\infer[\\!\\!\\exists\\text{i}]{'
        latex += self.formula.toLatex()
        latex += '}{'
        latex += symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)
        latex += '}'
        return latex

class ExistsEliminationtionDef():
    def __init__(self,line, formula, reference1, reference2, reference3):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.reference3 = reference3
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the scope of the rule line 
      if before:
        parser.check_line_scope_reference_error(deduction_result,self, reference1=True)      
      # If the box is a valid scope
      valid_box = parser.check_scope_reference_error(deduction_result,self)

      variable = parser.symbol_table.find_scope_variable(self.reference2.value)
      # If no variable is at the hypothesis line.
      if variable==None:
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.BOX_MUST_HAVE_A_VARIABLE, self.reference2, self))
          return
      # If the variable is not a fresh variable 
      if(not parser.symbol_table.is_fresh_variable(self.reference2.value)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.VARIABLE_IS_NOT_FRESH_VARIABLE, self.reference2, self))

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1.value)
      formula2, formula3 = parser.symbol_table.check_scope_delimiter(self.reference2.value, self.reference3.value)
      if(formula1==None or formula2==None or formula3==None or formula_reference==None):
        return

      # If the rule conclusion is the same as the last formula of the box
      if(self.formula != formula3):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_CONCLUSION_EXISTENCIAL_LAST_RULE, self.reference3, self))
      # If the formula of the first reference is not a existential formula
      if(not isinstance(formula1, QuantifierFormula) or (isinstance(formula1, QuantifierFormula) and not formula1.is_existential())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_EXISTENCIAL_FORMULA, formula_reference, self))
      # If the hypothesis formula (reference line 2) is a valid subtitutotion of the existential formula (reference line 1)
      if(isinstance(formula1, QuantifierFormula) and formula1.formula.substitution(formula1.variable, variable)!=formula2):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_SUBSTITUTION_EXISTENCIAL, self.reference2, self))
      # if the variable is a free variable at the conclusion formula (referecne line 3)
      if(variable in formula3.free_variables()):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_CONCLUSION_EXISTENCIAL, self.reference2, self))

    def toLatex(self, symbol_table):
        hypothesis_number = str(len(hypothesis) + 1)
        hypothesis[self.reference2.value] = hypothesis_number
        latex = '\\infer[\\!\\!{\\exists\\text{e}^{_'+ hypothesis_number +'} }]{'
        latex += self.formula.toLatex()+'}{'
        latex += symbol_table.get_rule(self.reference1.value).toLatex(symbol_table)
        latex += ' & '+symbol_table.get_rule(self.reference3.value).toLatex(symbol_table)+ '}'
        return latex

class ForAllIntroductiontionDef():
    def __init__(self,line, formula, reference1, reference2):
        self.line = line
        self.formula = formula
        self.reference1 = reference1
        self.reference2 = reference2
        self.is_copied = False

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the box is a valid scope
      valid_box = parser.check_scope_reference_error(deduction_result,self)

      variable = parser.symbol_table.find_scope_variable(self.reference1.value)
      first_rule = parser.symbol_table.get_first_rule_from_scope(self.reference1.value)
      # If no variable is at the hypothesis line.
      if variable==None:
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.BOX_MUST_HAVE_A_VARIABLE, self.reference1, self))
          return
      elif isinstance(first_rule, HypothesisFirstOrderDef):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.BOX_MUST_HAVE_ONLY_A_VARIABLE, self.reference1, self))
          return
        
      # If the variable is not a fresh variable 
      if(not parser.symbol_table.is_fresh_variable(self.reference1.value)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.VARIABLE_IS_NOT_FRESH_VARIABLE, self.reference1, self))

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1, formula2 = parser.symbol_table.check_scope_delimiter(self.reference1.value, self.reference2.value)
      if(formula1==None or formula2==None or formula_reference==None):
        return

      # If the formula of the first reference is not a existential formula
      if(not isinstance(self.formula, QuantifierFormula) or (isinstance(self.formula, QuantifierFormula) and not self.formula.is_universal())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_EXISTENCIAL_FORMULA, formula_reference, self))
      # If the conclusion is a universal formula of the last formula (reference line 2) by substitution of the variable
      if(isinstance(self.formula, QuantifierFormula) and self.formula.formula.substitution(self.formula.variable, variable)!=formula2):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_CONCLUSION_UNIVERSAL_LAST_RULE, self.reference2, self))
      # if the variable is a free variable at the conclusion formula (reference line 3)
      if(variable in self.formula.free_variables()):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_CONCLUSION_UNIVERSAL, formula_reference, self))

    def toLatex(self, symbol_table):
        hypothesis_number = str(len(hypothesis) + 1)
        hypothesis[self.reference2.value] = hypothesis_number
        latex = '\\infer[\\!\\!{\\forall\\text{i}}]{'
        latex += self.formula.toLatex()+'}{'
        latex += symbol_table.get_rule(self.reference2.value).toLatex(symbol_table)+ '}'
        return latex


## File analisys.py

from rply import ParserGenerator
import sys
import copy

deduction_result = natural_deduction_return()

def value_error_handle(exctype, value, tb):
    deduction_result.add_error(str(value))
    deduction_result.to_json()

sys.excepthook = value_error_handle

class ParserNadia():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUM', 'DOT', 'COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT', 'RAA',
             'AND', 'OR', 'OR_INTROD', 'OR_ELIM', 'BOTTOM','BOTTOM_ELIM', 'OPEN_BRACKET', 'AND_INTROD',
             'AND_ELIM', 'NEG_INTROD', 'NEG_ELIM', 'HYPOTHESIS', 'PREMISE', 'ATOM', 'CLOSE_BRACKET',
             'DASH', 'COPY', 'IMP_ELIM', 'IMPLIE', 'IMP_INTROD',
             'VAR', 'EXT', 'ALL', 'ALL_ELIM', 'EXT_INTROD', 'EXT_ELIM', 'ALL_INTROD' ],
            #The precedence $\lnot,\forall,\exists,\land,\lor,\rightarrow,\leftrightarrow$
            precedence=[
                ('right', ['IMPLIE']),
                ('right', ['OR']),
                ('right', ['AND']),
                ('right', ['EXT']),
                ('right', ['ALL']),
                ('right', ['NOT']),
            ]
        )
        self.symbol_table = SymbolTable()
        self.box_latex = "\\begin{logicproof}{6}\n"
        self.has_error = False


    def verify_sequence_lines_error(self, deduction_result):
        productions = self.state.splitlines()
        i = 1
        for p in productions:
          x = p.split('.')[0]
          if x.isdigit():
            if int(x)!=i: 
              self.has_error = True
              if(i==1): deduction_result.add_error("{}\n^, A numeração da linha {} deveria ser {}, pois a numeração da prova deve ser sequencial e iniciar em 1.\n".format(p,x,i))
              else: deduction_result.add_error("{}\n^, A numeração da linha {} deveria ser {}, pois a numeração da prova deve ser sequencial.\n".format(p,x,i))
              break
            i+=1

    def check_is_closed_boxes_by_rule(self,deduction_result):
      current_scope = None
      for i in range(1,len(self.symbol_table.symbol_table)):
        current_scope = self.symbol_table.symbol_table['scope_{}'.format(i)]
        current_scope_parent = self.symbol_table.symbol_table[current_scope['parent']] if current_scope['parent'] else None
        if(current_scope_parent==None):
          self.has_error = True
          deduction_result.add_error("Erro no escopo da demontração: escopo pai não encontrado.")
        next_line_parent = None
        rule_next = None
        for rule in current_scope_parent['rules']:
          if(int(rule.line)>int(current_scope['end_line'])):
            rule_next = rule
            break
        if (rule_next==None or ( not (isinstance(rule_next, NegationIntroductionDef) or isinstance(rule_next, RaaDef)
          or isinstance(rule_next, ImplicationIntroductionDef) or isinstance(rule_next, DisjunctionEliminationDef)
          or isinstance(rule_next, ExistsEliminationtionDef) or isinstance(rule_next, ForAllIntroductiontionDef)))):
          self.has_error = True
          begin_rule = current_scope["rules"][0]
          begin_token =current_scope["lines"][0]
          deduction_result.add_error(self.get_error(constants.BOX_MUST_BE_DISPOSED, begin_token, begin_rule))

    def check_line_reference_before_rule_error(self, deduction_result, rule):
      result = True
      if hasattr(rule, 'reference1'):
        if(int(rule.reference1.value) >= int(rule.line)):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.REFERENCED_LINE_NOT_DEFINED, rule.reference1, rule))
            result = False
      if hasattr(rule, 'reference2'):
        if(int(rule.reference2.value) >= int(rule.line)):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.REFERENCED_LINE_NOT_DEFINED, rule.reference2, rule))
            result = False
      if hasattr(rule, 'reference3'):
        if(int(rule.reference3.value) >= int(rule.line)):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.REFERENCED_LINE_NOT_DEFINED, rule.reference3, rule))
            result = False
      if hasattr(rule, 'reference4'):
        if(int(rule.reference4.value) >= int(rule.line)):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.REFERENCED_LINE_NOT_DEFINED, rule.reference4, rule))
            result = False
      if hasattr(rule, 'reference5'):
        if(int(rule.reference5.value) >= int(rule.line)):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.REFERENCED_LINE_NOT_DEFINED, rule.reference5, rule))
            result = False
      return result

    def check_line_scope_reference_error(self, deduction_result, rule, reference1=False, reference2=False, reference3=False, reference4=False, reference5=False):
      result = True
      if reference1:
        if (self.symbol_table.lookup_formula_by_line(rule.line, rule.reference1.value)==None):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.USING_DESCARTED_RULE, rule.reference1, rule))
            result = False
      if reference2:
        if (self.symbol_table.lookup_formula_by_line(rule.line, rule.reference2.value)==None):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.USING_DESCARTED_RULE, rule.reference2, rule))
            result = False
      if reference3:
        if (self.symbol_table.lookup_formula_by_line(rule.line, rule.reference3.value)==None):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.USING_DESCARTED_RULE, rule.reference3, rule))
            result = False
      if reference4:
        if (self.symbol_table.lookup_formula_by_line(rule.line, rule.reference4.value)==None):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.USING_DESCARTED_RULE, rule.reference3, rule))
            result = False
      if reference5:
        if (self.symbol_table.lookup_formula_by_line(rule.line, rule.reference5.value)==None):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.USING_DESCARTED_RULE, rule.reference5, rule))
            result = False
      return result

    def check_scope_reference_error(self, deduction_result, rule):
        result = True
        if (isinstance(rule, NegationIntroductionDef) or isinstance(rule, RaaDef)
          or isinstance(rule, ImplicationIntroductionDef) or isinstance(rule, ForAllIntroductiontionDef)):
          formula1, formula2 = self.symbol_table.check_scope_delimiter(rule.reference1.value, rule.reference2.value)
          # If the box references does not form a valid box 
          if(formula1==None):
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.INVALID_SCOPE_DELIMITER, rule.reference1, rule))
              result = False
          #If the box references are not followed by each other.
          elif not (int(rule.line) > int(rule.reference2.value) and int(rule.reference2.value)>= int(rule.reference1.value)):
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.INVALID_SCOPE_DELIMITER, rule.reference1, rule))
              result = False
          # If box is not imediatally closed by the rule 
          if int(rule.line) != int(rule.reference2.value)+1 and not rule.is_copied:
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.BOX_MUST_BE_DISPOSED_BY_RULE, rule.reference1, rule))
              result = False

        elif (isinstance(rule, ExistsEliminationtionDef)):
          formula1, formula2 = self.symbol_table.check_scope_delimiter(rule.reference2.value, rule.reference3.value)
          # If the box references does not form a valid box 
          if(formula1==None):
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.INVALID_SCOPE_DELIMITER, rule.reference2, rule))
              result = False
          #If the box references are not followed by each other.
          elif not (int(rule.line) > int(rule.reference3.value) and int(rule.reference3.value)>= int(rule.reference2.value) 
                and int(rule.reference2.value)>= int(rule.reference1.value)):
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.INVALID_SCOPE_DELIMITER, rule.reference2, rule))
              result = False
          # If box is not imediatally closed by the rule 
          if int(rule.line) != int(rule.reference3.value)+1:
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.BOX_MUST_BE_DISPOSED_BY_RULE, rule.reference2, rule))
              result = False

        elif isinstance(rule, DisjunctionEliminationDef):   
          formula1, formula2 = self.symbol_table.check_scope_delimiter(rule.reference2.value, rule.reference3.value)
          # If the box references does not form a valid box 
          if(formula1==None):
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.INVALID_SCOPE_DELIMITER, rule.reference2, rule))
              result = False
          #If the box references are not followed by each other.
          elif not (int(rule.line) > int(rule.reference3.value) and int(rule.reference3.value)>= int(rule.reference2.value) 
                and int(rule.reference2.value)>= int(rule.reference1.value)):
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.INVALID_SCOPE_DELIMITER, rule.reference2, rule))
              result = False
          formula1, formula2 = self.symbol_table.check_scope_delimiter(rule.reference4.value, rule.reference5.value)
          # If the box references does not form a valid box 
          if(formula1==None):
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.INVALID_SCOPE_DELIMITER, rule.reference4, rule))
              result = False
          #If the box references are not followed by each other.
          elif not (int(rule.line) > int(rule.reference5.value) and int(rule.reference5.value)>= int(rule.reference4.value) 
                and int(rule.reference4.value)== int(rule.reference3.value)+1):
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.INVALID_SCOPE_DELIMITER, rule.reference4, rule))
              result = False
          # If box is not imediatally closed by the rule 
          if int(rule.line) != int(rule.reference5.value)+1:
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.BOX_MUST_BE_DISPOSED_BY_RULE, rule.reference4, rule))
              result = False
        
        return result


    def parse(self):
        deduction_result = natural_deduction_return()
        @self.pg.production('program : steps')
        def program(p):
            self.symbol_table.set_lines_visible()
            self.verify_sequence_lines_error(deduction_result)
            self.check_is_closed_boxes_by_rule(deduction_result)

            rule_info = p[0]
            for i in rule_info:
                rule_line, formula_reference = rule_info[i]

                formula_reference = self.symbol_table.find_token(rule_line.value)

                rule = self.symbol_table.get_rule(rule_line.value)
                if(isinstance(rule, PremisseDef) ):
                    pass
                elif(isinstance(rule, HypothesisDef)):
                    pass
                elif(isinstance(rule, HypothesisFirstOrderDef)):
                    pass
                elif(isinstance(rule, NegationIntroductionDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, NegationEliminationDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, AndIntroductionDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, AndEliminationDef)):
                    rule.evaluation(self, deduction_result)
                elif isinstance(rule, ImplicationIntroductionDef):
                    rule.evaluation(self, deduction_result)
                elif isinstance(rule, ImplicationEliminationDef):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, DisjunctionEliminationDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, DisjunctionIntroductionDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, RaaDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, BottomDef)):
                    rule.evaluation(self, deduction_result)
                #elif(isinstance(rule, CopyDef)):
                #    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, ExistsIntroductionDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, ExistsEliminationtionDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, ForAllIntroductiontionDef)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, ForAllEliminationDef)):
                    rule.evaluation(self, deduction_result)

            if(not self.has_error):
                latex = '\\['
                formula_reference = str(sorted(list(map(int, rule_info.keys())))[-1])
                rule = self.symbol_table.get_rule(rule_info[formula_reference][0].value)
                latex += rule.toLatex(self.symbol_table)
                latex += '\\]'
                limpaHipotese()
                deduction_result.premisses = self.symbol_table.getPremissesFormulas()
                deduction_result.conclusion = self.symbol_table.getConclusionFormula()
                deduction_result.fitch = self.box_latex[:-3] + '\n\end{logicproof}'
                deduction_result.gentzen = latex + "\n"
##                print(deduction_result.gentzen)
##                print(deduction_result.fitch)
            return deduction_result

        @self.pg.production('steps : steps step')
        @self.pg.production('steps : step')
        def steps(p):
            if len(p) == 1:
                result = p[0]
                return {result[0].value: result}
            else:
                result = p[1]
                p[0][result[0].value] = result
                return p[0]

        @self.pg.production('step : NUM DOT formula PREMISE')
        def Premisse(p):
            formula_result = p[2]
            formula = formula_result[1]
            premisse = PremisseDef(p[0].value, formula)
            self.symbol_table.insert(premisse, p[0])
            self.box_latex += "{} & premissa\\\\\n".format(formula.toLatex())
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT OPEN_BRACKET formula HYPOTHESIS')
        @self.pg.production('step : NUM DOT OPEN_BRACKET VAR')
        @self.pg.production('step : NUM DOT OPEN_BRACKET VAR formula HYPOTHESIS')
        def Hypothesis(p):
            formula_result = {}
            if len(p) == 4 and p[3].gettokentype() == 'VAR':
                variable = p[3].value
                self.symbol_table.add_scope(p[0].value,variable=variable)
                self.box_latex += "\\begin{subproof}\n"
                self.box_latex += "\\llap{$"+str(variable)+"\\quad$} &"+"\\\\\n"
                return p[0], None
            elif len(p) == 5:
                formula_result = p[3]
                self.symbol_table.add_scope(p[0].value)
                formula = formula_result[1]
                self.box_latex += "\\begin{subproof}\n"
                self.box_latex += "{} & hipótese\\\\\n".format(formula.toLatex())
                hypothesis = HypothesisDef(p[0].value, formula)
            elif len(p) == 6:
                variable = p[3].value
                formula_result = p[4]
                self.symbol_table.add_scope(p[0].value,variable=variable)
                formula = formula_result[1]
                self.box_latex += "\\begin{subproof}\n"
                self.box_latex += "\\llap{$"+str(variable)+"\\quad$}"+"{} & hipótese\\\\\n".format(formula.toLatex())
                hypothesis = HypothesisFirstOrderDef(p[0].value, variable, formula)
            elif len(p) == 4 and p[3].gettokentype() != 'VAR':
                formula_result = p[2]
                formula = formula_result[1]
                self.box_latex += "{} & hipótese\\\\\n".format(formula.toLatex())
                hypothesis = HypothesisDef(p[0].value, formula)

            self.symbol_table.insert(hypothesis, p[0])
            if(self.symbol_table.current_scope == "scope_0"):
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.HYPOTHESIS_WITHOUT_BOX, formula_result[0], hypothesis))
            return p[0], formula_result[0]




        @self.pg.production('step : NUM DOT formula HYPOTHESIS')
        @self.pg.production('step : NUM DOT formula ATOM')
        @self.pg.production('step : NUM DOT OPEN_BRACKET formula ATOM')
        def Wrong_pre_hip(p):
            self.has_error = True
            wrong_rule = WrongDef(p[0].value, p[-2])
            deduction_result.add_error(self.get_error(constants.INVALID_HIP_PRE_WRITE, p[-1], wrong_rule))
            return p[0], p[-2]

        @self.pg.production('step : NUM DOT formula PREMISE ATOM')
        @self.pg.production('step : NUM DOT formula HYPOTHESIS ATOM')
        @self.pg.production('step : NUM DOT OPEN_BRACKET formula HYPOTHESIS ATOM')
        def Wrong_pre_hip(p):
            self.has_error = True
            wrong_rule = WrongDef(p[0].value, p[-3])
            deduction_result.add_error(self.get_error(constants.EXCEDENT_HIP_PRE_WRITE, p[-1], wrong_rule))
            return p[0], p[-3]

        @self.pg.production('step : NUM DOT formula NEG_ELIM NUM COMMA NUM')
        def Neg_elim(p):
            formula_result = p[2]
            formula = formula_result[1]
            negationElimination = NegationEliminationDef(p[0].value, formula, p[4], p[6])
            self.symbol_table.insert(negationElimination, p[0])
            self.box_latex += "{} & $\lnot e$ {}, {}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value)
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula IMP_ELIM NUM COMMA NUM')
        def Imp_elim(p):
            formula_result = p[2]
            formula = formula_result[1]
            implicationElimination = ImplicationEliminationDef(p[0].value, formula, p[4], p[6])
            self.symbol_table.insert(implicationElimination, p[0])
            self.box_latex += "{} & $\\rightarrow e$ {}, {}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value)
            return p[0], formula_result[0]
            
        @self.pg.production('step : NUM DOT formula IMP_INTROD NUM DASH NUM')
        def Imp_introd(p):
            formula_result = p[2]
            formula = formula_result[1]
            implicationIntrod = ImplicationIntroductionDef(p[0].value, formula, p[4], p[6])
            self.symbol_table.insert(implicationIntrod, p[0])
            self.box_latex += "{} & $\\rightarrow i$ {}-{}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value)
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula OR_INTROD NUM')
        def Or_introd(p):
            formula_result = p[2]
            formula = formula_result[1]
            disjunctionIntrod = DisjunctionIntroductionDef(p[0].value, formula, p[4])
            self.symbol_table.insert(disjunctionIntrod, p[0])
            self.box_latex += "{} & $\\lor i$ {}\\\\\n".format(formula.toLatex(), p[4].value)
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula AND_INTROD NUM COMMA NUM')
        def And_introd(p):
            formula_result = p[2]
            formula = formula_result[1]
            andIntrod = AndIntroductionDef(p[0].value, formula, p[4], p[6])
            self.symbol_table.insert(andIntrod, p[0])
            self.box_latex += "{} & $\\land i$ {},{}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value)
                
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula AND_ELIM NUM')
        def And_elim(p):
            formula_result = p[2]
            formula = formula_result[1]
            andElim = AndEliminationDef(p[0].value, formula, p[4])
            self.symbol_table.insert(andElim, p[0])
            self.box_latex += "{} & $\\land e$ {}\\\\\n".format(formula.toLatex(), p[4].value)
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula OR_ELIM NUM COMMA NUM DASH NUM COMMA NUM DASH NUM')
        def Or_elim(p):
            formula_result = p[2]
            formula = formula_result[1]
            orElim = DisjunctionEliminationDef(p[0].value, formula, p[4], p[6], p[8], p[10], p[12])
            self.symbol_table.insert(orElim, p[0])
            self.box_latex += "{} & $\\lor e$ {}, {}-{}, {}-{}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value, p[8].value, p[10].value, p[12].value)
            return p[0], formula_result[0]
        
        @self.pg.production('step : NUM DOT formula NEG_INTROD NUM DASH NUM')
        def Neg_introd(p):
            formula_result = p[2]
            formula = formula_result[1]
            negationIntrod = NegationIntroductionDef(p[0].value, formula, p[4], p[6])
            self.symbol_table.insert(negationIntrod, p[0])
            self.box_latex += "{} & $\lnot i$ {}-{}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value)
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula BOTTOM_ELIM NUM')
        def Bottom(p):
            formula_result = p[2]
            formula = formula_result[1]
            bottom = BottomDef(p[0].value, formula, p[4])
            self.symbol_table.insert(bottom, p[0])
            self.box_latex += "{} & $\\bot e$ {}\\\\\n".format(formula.toLatex(), p[4].value)
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula RAA NUM DASH NUM')
        def Raa(p):
            formula_result = p[2]
            formula = formula_result[1]
            raa = RaaDef(p[0].value, formula, p[4], p[6])
            self.symbol_table.insert(raa, p[0])
            self.box_latex += "{} & raa {}-{}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value)
            return p[0], formula_result[0]

#        @self.pg.production('step : NUM DOT formula COPY NUM')
#        def Copy(p):
#            formula_result = p[2]
#            formula = formula_result[1]
#            fCopy = CopyDef(p[0].value, formula, p[4])
#            self.symbol_table.insert(fCopy, p[0])
#            copied_scope = self.symbol_table.find_scope(p[4].value)
#            self.box_latex += "{} & copie {}\\\\\n".format(formula.toLatex(), p[4].value)
#            return p[0], formula_result[0]
        @self.pg.production('step : NUM DOT formula COPY NUM')
        def Copy(p):
            copied_scope = self.symbol_table.find_scope(p[4].value)
            if self.symbol_table.check_scope_is_valid(copied_scope):
                line = p[4].value
                formula_result = p[2]
                rule = copy.deepcopy(self.symbol_table.get_rule(line))
                rule.is_copied = True
                if(rule is not None):
                    if isinstance(rule, HypothesisDef):
                        rule.copied = rule.line
                    formula = formula_result[1]
                    rule.line = p[0].value 
                    if(rule.formula != formula):
                        formula_diff = rule.formula
                        rule.formula = formula
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.COPY_DIFFERENT_FORMULE, formula_result[0], rule))
                        rule.formula = formula_diff
                    self.box_latex += "{} & copie {}\\\\\n".format(formula.toLatex(), p[4].value)
                else:
                    self.has_error = True
                    deduction_result.add_error(self.get_error(constants.NONE_COPY, p[4], rule))
                self.symbol_table.insert(rule, p[0])
            else:
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.USING_DESCARTED_RULE, p[4], None))
            return p[0], p[2][0]



        @self.pg.production('step : CLOSE_BRACKET')
        def close_box(p):
            rule = self.symbol_table.get_last_rule_from_scope()
            if rule==None:
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.BOX_MUST_BE_DISPOSED_BY_RULE, p[0], rule))              
                return p[0], rule
            elif(self.symbol_table.get_box_start()):
                self.symbol_table.end_scope(rule.line)
                self.box_latex = self.box_latex[:-3] + '\n'
                self.box_latex += "\end{subproof}\n"
            else:
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.CLOSE_BRACKET_WITHOUT_BOX, p[0], rule))
            token = p[0]
            token.value = rule.line
            return p[0], rule.formula


        @self.pg.production('step : NUM DOT formula ALL_ELIM NUM')
        def For_all_elim(p):
          formula_result = p[2]
          formula = formula_result[1]
          forAllElimination = ForAllEliminationDef(p[0].value, formula, p[4])
          self.symbol_table.insert(forAllElimination, p[0])
          self.box_latex += "{} & $\\forall e$ {}\\\\\n".format(formula.toLatex(), p[4].value)
          return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula EXT_INTROD NUM')
        def Exists_intro(p):
          formula_result = p[2]
          formula = formula_result[1]
          #self.symbol_table.add_scope(p[0].value)
          existsIntroduction = ExistsIntroductionDef(p[0].value, formula, p[4])
          self.symbol_table.insert(existsIntroduction, p[0])
          self.box_latex += "{} & $\\exists i$ {}\\\\\n".format(formula.toLatex(), p[4].value)
          return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula EXT_ELIM NUM COMMA NUM DASH NUM')
        def Exists_elim(p):
            formula_result = p[2]
            formula = formula_result[1]
            existsElim = ExistsEliminationtionDef(p[0].value, formula, p[4], p[6], p[8])
            self.symbol_table.insert(existsElim, p[0])
            self.box_latex += "{} & $\\exists e$ {},{}-{}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value, p[8].value)
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula ALL_INTROD NUM DASH NUM')
        def For_all_intro(p):
            formula_result = p[2]
            formula = formula_result[1]
            allIntrod = ForAllIntroductiontionDef(p[0].value, formula, p[4], p[6])
            self.symbol_table.insert(allIntrod, p[0])
            self.box_latex += "{} & $\\forall i$ {}-{}\\\\\n".format(formula.toLatex(), p[4].value, p[6].value)
            return p[0], formula_result[0]

        @self.pg.production('step : NUM DOT formula IMP_ELIM NUM ')
        @self.pg.production('step : NUM DOT formula IMP_ELIM NUM DASH NUM')
        @self.pg.production('step : NUM DOT formula AND_INTROD NUM ')
        @self.pg.production('step : NUM DOT formula AND_INTROD NUM DASH NUM')
        @self.pg.production('step : NUM DOT formula NEG_ELIM NUM ')
        @self.pg.production('step : NUM DOT formula NEG_ELIM NUM DASH NUM')
        def Wrong_use_conective_references(p):
            self.has_error = True
            wrong_rule = WrongDef(p[0].value, p[2])
            deduction_result.add_error(self.get_error(constants.INVALID_RULE, p[3], wrong_rule))
            return p[0], p[2]

        @self.pg.production('step : NUM DOT formula AND_ELIM NUM COMMA NUM ')
        @self.pg.production('step : NUM DOT formula AND_ELIM NUM DASH NUM')
        def Wrong_use_conective_reference(p):
            self.has_error = True
            wrong_rule = WrongDef(p[0].value, p[2])
            deduction_result.add_error(self.get_error(constants.INVALID_RULE_ONE_REFERENCE, p[3], wrong_rule))
            return p[0], p[2]


        @self.pg.production('formula : EXT formula')
        @self.pg.production('formula : ALL formula')
        @self.pg.production('formula : formula OR formula')
        @self.pg.production('formula : formula AND formula')
        @self.pg.production('formula : formula IMPLIE formula')
        @self.pg.production('formula : NOT formula')
        @self.pg.production('formula : ATOM OPEN_PAREN variableslist CLOSE_PAREN')
        @self.pg.production('formula : ATOM')
        @self.pg.production('formula : BOTTOM')
        def formula(p):
            #print(p)
            if len(p) < 3:
                if p[0].gettokentype() == 'ATOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'BOTTOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'NOT':
                    result = p[1]
                    return p[0], NegationFormula(formula=result[1])  
                elif( not type(p[0]) is tuple):
                  result1 = p[0]
                  result2 = p[1]
                  # Universal Formula
                  if p[0].gettokentype() == 'EXT':  
                    var = p[0].value.split('E')[1]
                    return p[0], ExistentialFormula(variable=var, formula=p[1][1])
                  elif p[0].gettokentype() == 'ALL':  
                    var = p[0].value.split('A')[1]
                    return p[0], UniversalFormula(variable=var, formula=p[1][1])
            elif len(p)==4:
              # Predicate Formula
              name = p[0]
              varlist = p[2]
              return p[0], PredicateFormula(name=p[0].value,variables=varlist[1])            
            elif len(p) == 3:
              # Binary Formula
              result1 = p[0]
              result2 = p[2]
              if(p[1].value=='&'):
                return result1[0], AndFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='|'):
                return result1[0], OrFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='->'):
                return result1[0], ImplicationFormula(left=result1[1], right=result2[1])
              else:
                return result1[0], BinaryFormula(key=p[1].value, left=result1[1], right=result2[1])


        @self.pg.production('variableslist : VAR')
        @self.pg.production('variableslist : VAR COMMA variableslist')
        def variablesList(p):
             if len(p) == 1:
                 return p[0], [p[0].value]
             else:
                result = p[2]
             return p[0], [p[0].value] + result[1]



        @self.pg.production('formula : OPEN_PAREN formula CLOSE_PAREN')
        def paren_formula(p):
            result = p[1]
            return p[0], result[1]

        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            error = ''  

            if(productions == ['']):
                error = 'Nenhuma demonstração foi recebida, verifique a entrada.'
            if token.gettokentype() == '$end':
                error = 'Uma das definições não está completa, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma regra de inferência sempre inicia com um número seguido de um . (linha de referência), tem uma fórmula e uma justificativa (premissa, hipóteses ou uma das regras de inferência com suas respectivas referências para fórmulas anteriores).'
            else:
                source_position = token.getsourcepos()
                error = 'Uma das definições não está completa, verifique se todas regras foram aplicadas corretamente.\nLembre-se que uma regra de inferência sempre inicia com um número seguido de um . (linha de referência), tem uma fórmula e uma justificativa (premissa, hipóteses ou uma das regras de inferência com suas respectivas referências para fórmulas anteriores).\n'
                error += "Erro de sintaxe:\n"
                error += productions[source_position.lineno - 1]
                string = '\n'
                for i in range(source_position.colno -1):
                    string += ' '
                string += '^'
                if token.gettokentype() == 'OUT':
                    string += ' Símbolo não pertence a linguagem.'
                error += string
                
            raise ValueError("@@"+error)

    def get_error(self, type_error, token_error, rule):
        productions = self.state.splitlines()
        column_error = token_error.getsourcepos().colno
        erro = "Erro de sintaxe na linha {}:\n".format(token_error.getsourcepos().lineno)
        erro += productions[token_error.getsourcepos().lineno-1] + "\n"
        for i in range(column_error-1):
            erro += ' '
        if type_error == constants.REFERENCED_FORMULE_NONE:## REVER SE NAO EXCLUIR
            erro += '^, A fórmula {} não foi definida anteriormente ou foi descartada.\n'.format(token_error.value)
        elif type_error == constants.INVALID_RESULT:
            erro += "^, A fórmula {} não é um resultado válido para esta regra.".format(rule.formula.toString())
#            erro += "^, A fórmula resultante {} não pode ser obtido a partir das fórmulas utilizadas.".format(rule.formula.toString())
        elif type_error == constants.INVALID_HYPOTHESIS:
            erro += "^, A hipótese da linha {} não corresponde a hipótese esperada para a fórmula da conclusão desta regra.".format(token_error.value)
        elif type_error == constants.INVALID_BOX_RESULT:
            erro += "^, A fórmula da linha {} não corresponde a conclusão esperada desta caixa para esta regra.".format(token_error.value)
        elif type_error == constants.UNEXPECT_RESULT:
            erro += "^, A fórmula {} não é um resultado válido para a regra aplicada.".format(rule.formula.toString())
        elif type_error == constants.IS_NOT_DISJUNCTION:
            erro += "^, A fórmula referenciada na linha {} não é disjunção.".format(token_error.value)
        elif type_error == constants.IS_NOT_CONJUNCTION:
            erro += "^, A fórmula referenciada na linha {} não é conjunção.".format(token_error.value)
        elif type_error == constants.IS_NOT_IMPLICATION:
            erro += "^, A fórmula referenciada na linha {} não é implicação.".format(token_error.value)
        elif type_error == constants.IS_NOT_BOTTOM:
            erro += "^, A fórmula referenciada na linha {} deveria ser @.".format(token_error.value)
        elif type_error == constants.INVALID_NEGATION:
            erro += "^, Nenhuma das fórmulas referencias pelas linhas é a negação da outra fórmula."
        elif type_error == constants.INVALID_LEFT_CONJUNCTION:
            erro += "^, A fórmula à esquerda fórmula da conclusão não é demonstrada por nenhuma das linhas referenciadas nesta regra."
        elif type_error == constants.INVALID_RIGHT_CONJUNCTION:
            erro += "^, A fórmula à direita da fórmula da conclusão não é demonstrada por nenhuma das linhas referenciadas nesta regra."
        elif type_error == constants.INVALID_LEFT_OR_RIGHT_DISJUNCTION:
            erro += "^, A fórmula à direita ou à equerda da fórmula da conclusão deve ser a mesma da fórmula referencia na linha {}.".format(token_error.value)
        elif type_error == constants.INVALID_LEFT_OR_RIGHT_CONJUNCTION:
            erro += "^, A fórmula à direita ou à equerda da fórmula da linha {} deve ser a mesma da fórmula da conclusão da regra.".format(token_error.value)
        elif type_error == constants.NONE_COPY:
            erro += "^, A Fórmula referenciada para cópia não existe."
        elif type_error == constants.COPY_DIFFERENT_FORMULE:
            erro += "^, A Fórmula referenciada para cópia é diferente da definida para essa regra."
        elif type_error == constants.INVALID_HIP_PRE_WRITE:
            erro += "^, uma hipótese só pode ser usado no início de uma caixa e é introduzida apenas por uma regra de inferência."
        elif type_error == constants.INVALID_RULE:
            erro += "^, a regra {} deve ter duas referências separadas por vírgula.".format(token_error.value)
        elif type_error == constants.INVALID_RULE_ONE_REFERENCE:
            erro += "^, a regra {} deve ter uma única referência.".format(token_error.value)
        elif type_error == constants.EXCEDENT_HIP_PRE_WRITE:
            erro += "^, Não é esperado texto depois de pre."
        elif type_error == constants.USING_DESCARTED_RULE:
            erro += "^, a referência a fórmula da linha {} não pode ser utilizada, pois esta fórmula já foi descartada.".format(token_error.value)
        elif type_error == constants.REFERENCED_LINE_NOT_DEFINED:
            erro += "^, a referência a fórmula da linha {} não pode ser utilizada, pois todas as referências devem ocorrer antes desta regra.".format(token_error.value)
        elif type_error == constants.INVALID_SCOPE_DELIMITER:
            erro += "^, esta não é uma caixa (escopo) válida."      
        elif type_error == constants.HYPOTHESIS_WITHOUT_BOX:
            erro += "^, A hipótese definida não está dentro de uma caixa."
        elif type_error == constants.CLOSE_BRACKET_WITHOUT_BOX:
            erro += "^, Fechamento de caixa sem caixa aberta."
        elif type_error == constants.HYPOTHESIS_WITHOUT_CLOSED_BOX:
            erro += "^, É necessário fechar o escopo desta caixa."
        elif type_error == constants.BOX_MUST_BE_DISPOSED:
            erro += "^, A hipótese que foi introduzida por essa caixa dever ser descartada pela regra que a introduziu em linha imediatamente posterior ao fechamento desta caixa."
        elif type_error == constants.BOX_MUST_BE_DISPOSED_BY_RULE:
            erro += "^, Esta caixa dever ser fechada em linha imediatamente posterior pela regra que a introduziu."
        elif type_error == constants.INVALID_SUBSTITUTION_UNIVERSAL:
            erro += "^, A fórmula {} não é uma substituição válida da fórmula universal refenciada na linha {}.".format(rule.formula.toString(), rule.reference1.value)
        elif type_error == constants.INVALID_CONCLUSION_EXISTENCIAL_LAST_RULE:
            erro += "^, A formula da conclusão desta regra deve ser a mesma fórmula refenciada na linha {}.".format(token_error.value)
        elif type_error == constants.INVALID_CONCLUSION_UNIVERSAL_LAST_RULE:
            erro += "^, A formula da conclusão desta regra deve ser a quantificação universal da fórmula refenciada na linha {} com a variável definida neste escopo.".format(token_error.value)
        elif type_error == constants.INVALID_UNIVERSAL_FORMULA:
            erro += "^, A fórmula referenciada na regra do universal não é uma fórmula do tipo universal."
        elif type_error == constants.INVALID_SUBSTITUTION_EXISTENCIAL:
            erro += "^, A fórmula {} não é uma substituição válida da fórmula existencial refenciada na linha {}.".format(rule.formula.toString(), rule.reference1.value)
#            erro += "^, A fórmula refenciada na linha {} não é uma substituição correta da variável na fórmula do existencial desta regra.".format(token_error.value)
        elif type_error == constants.VARIABLE_IS_NOT_FRESH_VARIABLE:
            erro += "^, A variável utilizada na linha {} é uma variável livre de uma fórmula definida anteriormente e, portanto, não pode ser utilizada nesta regra.".format(token_error.value)
        elif type_error == constants.BOX_MUST_HAVE_A_VARIABLE:
            erro += "^, A caixa que inicia na linha {} deve iniciar com uma variável para esta regra.".format(token_error.value) 
        elif type_error == constants.BOX_MUST_HAVE_ONLY_A_VARIABLE:
            erro += "^, A caixa que inicia na linha {} não tem hipótese. A caixa deve iniciar com uma variável apenas para a regra da introdução do universal.".format(token_error.value) 
        elif type_error == constants.INVALID_CONCLUSION_EXISTENCIAL:
            erro += "^, A variável utilizada na conclusão dessa regra não pode ser a variável utilizada na caixa que inicia na linha {}.".format(token_error.value)
        elif type_error == constants.INVALID_CONCLUSION_UNIVERSAL:
            erro += "^, A variável utilizada na caixa que inicia na linha {} não pode ocorrer como variável livre na conclusão da fórmula e, portanto, não pode ser utilizada nesta regra.".format(token_error.value)
        
        return erro
    
    def get_parser(self):
        return self.pg.build()
    def get_premisses(self):
      return self.symbol_table.getPremissesFormulas()

    def get_conclustion(self):
      return self.symbol_table.getConclusionFormula()

    def get_theorem(self):
      return self.symbol_table.getPremissesFormulas(), self.symbol_table.getConclusionFormula()

    def theorem_to_string(self,parentheses=False):
      return self.symbol_table.theoremToString(parentheses=parentheses)

    def theorem_to_latex(self,parentheses=False):
      return self.symbol_table.theoremToLatex(parentheses=parentheses)

    @staticmethod
    def getProof(input_text=''):
      lexer = Lexer().get_lexer()
      tokens = lexer.lex(input_text)

      pg = ParserNadia(state=input_text)
      pg.parse()
      parser = pg.get_parser()
      result = parser.parse(tokens)
      return result
    # def getProof(input_text=''):
    #     try:
    #       lexer = Lexer().get_lexer()
    #       tokens = lexer.lex(input_text)

    #       pg = ParserNadia(state=input_text)
    #       pg.parse()
    #       parser = pg.get_parser()
    #       result = parser.parse(tokens)
    #       return result
    #     except ValueError:
    #         s = traceback.format_exc()
    #         return None
    #     else:
    #         return None
    #         pass

    @staticmethod
    def toString(premisses,conclusion,parentheses=False):
      if (premisses==[]):
        return '|- '+conclusion.toString(parentheses=parentheses)
      else:
        return ", ".join(f.toString(parentheses=parentheses) for f in premisses)+' |- '+conclusion.toString(parentheses=parentheses)

    @staticmethod
    def toLatex(premisses,conclusion,parentheses=False):
      if (premisses==[]):
        return '\\vdash '+conclusion.toLatex(parentheses=parentheses)
      else:
        return ", ".join(f.toLatex(parentheses=parentheses) for f in premisses) +' \\vdash '+conclusion.toLatex(parentheses=parentheses)


def check_proof(text_input, show_fitch=True, show_gentzen=True):
    try:
        result = ParserNadia.getProof(text_input)
        r = ''
        if(result.errors==[]):
            r += "A demonstração está correta."
            if show_fitch:
                r += "\n\nCódigo da demonstração no estilo Fitch em Latex:\n"
                r += str(result.fitch)
            if show_gentzen:
                r += "\n\nCódigo da demonstração no estilo Gentzen em Latex:\n"
                r += str(result.gentzen)
        else:
            r += "Os seguintes erros foram encontrados:\n\n"
            for error in result.errors:
                r += str(error)
        return r
    except ValueError:
        s = traceback.format_exc()
        result = (s.split("@@"))[-1]
        r = "Os seguintes erros foram encontrados:\n\n"
        return r
    else:
        pass



# PARSER DE UM TEOREMA

class ParserTheorem():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT',
             'AND', 'OR',  'BOTTOM','ATOM', 'IMPLIE', 'IFF',
             'VAR','EXT','ALL', 'V_DASH' ],
            #The precedence $\lnot,\forall,\exists,\land,\lor,\rightarrow,\leftrightarrow$
            precedence=[
                ('right', ['IFF']),
                ('right', ['IMPLIE']),
                ('right', ['OR']),
                ('right', ['AND']),
                ('right', ['EXT']),
                ('right', ['ALL']),
                ('right', ['NOT']),
            ]
        )

    def parse(self):
        @self.pg.production('program : formulaslist V_DASH formula')
        @self.pg.production('program : V_DASH formula')
        def program(p):
            if len(p) == 2:
              return [], p[1][1]
            else:
              return p[0][1], p[2][1]

        @self.pg.production('formula : EXT formula')
        @self.pg.production('formula : ALL formula')
        @self.pg.production('formula : formula OR formula')
        @self.pg.production('formula : formula AND formula')
        @self.pg.production('formula : formula IMPLIE formula')
        @self.pg.production('formula : formula IFF formula')
        @self.pg.production('formula : NOT formula')
        @self.pg.production('formula : ATOM OPEN_PAREN variableslist CLOSE_PAREN')
        @self.pg.production('formula : ATOM')
        @self.pg.production('formula : BOTTOM')
        def formula(p):
            if len(p) < 3:
                if p[0].gettokentype() == 'ATOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'BOTTOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'NOT':
                    result = p[1]
                    return p[0], NegationFormula(formula=result[1])  
                elif( not type(p[0]) is tuple):
                  result1 = p[0]
                  result2 = p[1]
                  # Universal Formula
                  if p[0].gettokentype() == 'EXT':  
                    var = p[0].value.split('E')[1]
                    return p[0], ExistentialFormula(variable=var, formula=p[1][1])
                  elif p[0].gettokentype() == 'ALL':  
                    var = p[0].value.split('A')[1]
                    return p[0], UniversalFormula(variable=var, formula=p[1][1])
            elif len(p)==4:
              # Predicate Formula
              name = p[0]
              varlist = p[2]
              return p[0], PredicateFormula(name=p[0].value,variables=varlist[1])            
            elif len(p) == 3:
              # Binary Formula
              result1 = p[0]
              result2 = p[2]
              if(p[1].value=='&'):
                return result1[0], AndFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='|'):
                return result1[0], OrFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='->'):
                return result1[0], ImplicationFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='<->'):
                return result1[0], BiImplicationFormula(left=result1[1], right=result2[1])
              else:
                return result1[0], BinaryFormula(key=p[1].value, left=result1[1], right=result2[1])

        @self.pg.production('formula : OPEN_PAREN formula CLOSE_PAREN')
        def paren_formula(p):
            result = p[1]
            return p[0], result[1]

        @self.pg.production('variableslist : VAR')
        @self.pg.production('variableslist : VAR COMMA variableslist')
        def variablesList(p):
             if len(p) == 1:
                 return p[0], [p[0].value]
             else:
                result = p[2]
             return p[0], [p[0].value] + result[1]

        @self.pg.production('formulaslist : formula')
        @self.pg.production('formulaslist : formula COMMA formulaslist')
        def formulasList(p):
             if len(p) == 1:
                 return p[0], [p[0][1]]
             else:
                result = p[2]
             return p[0], [p[0][1]] + result[1]


        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            error = ''  

            if(productions == ['']):
                error = 'Nenhuma fórmula foi recebida, verifique a entrada.'
            if token.gettokentype() == '$end':
                error = 'Nenhuma fórmula foi recebida, verifique a entrada.'
            else:
                source_position = token.getsourcepos()
                error = 'A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente.\nLembre-se que uma uma fórmula é definida pela seguinte BNF:\nF :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q são átomos.\n'
                error += "Erro de sintaxe:\n"
                error += productions[source_position.lineno - 1]
                string = '\n'
                for i in range(source_position.colno -1):
                    string += ' '
                string += '^'
                if token.gettokentype() == 'OUT':
                    string += ' Símbolo não pertence a linguagem.'
                error += string
                
            raise ValueError("@@"+error)

    def get_error(self, type_error, token_error, rule):
        productions = self.state.splitlines()
        column_error = token_error.getsourcepos().colno
        erro = "Erro de sintaxe na linha {}:\n".format(token_error.getsourcepos().lineno)
        erro += productions[token_error.getsourcepos().lineno-1] + "\n"
        for i in range(column_error-1):
            erro += ' '
#        if type_error == constants.REFERENCED_FORMULE_NONE:## REVER SE NAO EXCLUIR
#            erro += '^, A fórmula {} não foi definida anteriormente ou foi descartada.\n'.format(token_error.value)
        
        return erro
    
    def get_parser(self):
        return self.pg.build()
    
    @staticmethod
    def getTheorem(input_text=''):
        try:
          lexer = Lexer().get_lexer()
          tokens = lexer.lex(input_text)

          pg = ParserTheorem(state=input_text)
          pg.parse()
          parser = pg.get_parser()
          formulas, conclusion = parser.parse(tokens)
          return formulas, conclusion
        except ValueError:
            s = traceback.format_exc()
            #print (f'Erro ao fazer o parser da fórmula!')
            return [], None
        else:
            return [], None
            pass

    @staticmethod
    def toString(premisses,conclusion,parentheses=False):
      if (premisses==[]):
        return '|- '+conclusion.toString(parentheses=parentheses)
      else:
        return ", ".join(f.toString(parentheses=parentheses) for f in premisses)+' |- '+conclusion.toString(parentheses=parentheses)

    @staticmethod
    def toLatex(premisses,conclusion,parentheses=False):
      if (premisses==[]):
        return '\\vdash '+conclusion.toLatex(parentheses=parentheses)
      else:
        return ", ".join(f.toLatex(parentheses=parentheses) for f in premisses) +' \\vdash '+conclusion.toLatex(parentheses=parentheses)




# PARSER DE UMA Fórmula
import traceback

class ParserFormula():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT',
             'AND', 'OR',  'BOTTOM','ATOM', 'IMPLIE', 'IFF',
             'VAR','EXT','ALL' ],
            #The precedence $\lnot,\forall,\exists,\land,\lor,\rightarrow,\leftrightarrow$
            precedence=[
                ('right', ['IFF']),
                ('right', ['IMPLIE']),
                ('right', ['OR']),
                ('right', ['AND']),
                ('right', ['EXT']),
                ('right', ['ALL']),
                ('right', ['NOT']),
            ]
        )

    def parse(self):
        @self.pg.production('program : formula')
        def program(p):
            rule_info = p[0]
            return p[0][1]

        @self.pg.production('formula : EXT formula')
        @self.pg.production('formula : ALL formula')
        @self.pg.production('formula : formula OR formula')
        @self.pg.production('formula : formula AND formula')
        @self.pg.production('formula : formula IMPLIE formula')
        @self.pg.production('formula : formula IFF formula')
        @self.pg.production('formula : NOT formula')
        @self.pg.production('formula : ATOM OPEN_PAREN variableslist CLOSE_PAREN')
        @self.pg.production('formula : ATOM')
        @self.pg.production('formula : BOTTOM')
        def formula(p):
            #print(p)
            if len(p) < 3:
                if p[0].gettokentype() == 'ATOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'BOTTOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'NOT':
                    result = p[1]
                    return p[0], NegationFormula(formula=result[1])  
                elif( not type(p[0]) is tuple):
                  result1 = p[0]
                  result2 = p[1]
                  # Universal Formula
                  if p[0].gettokentype() == 'EXT':  
                    var = p[0].value.split('E')[1]
                    return p[0], ExistentialFormula(variable=var, formula=p[1][1])
                  elif p[0].gettokentype() == 'ALL':  
                    var = p[0].value.split('A')[1]
                    return p[0], UniversalFormula(variable=var, formula=p[1][1])
            elif len(p)==4:
              # Predicate Formula
              name = p[0]
              varlist = p[2]
              return p[0], PredicateFormula(name=p[0].value,variables=varlist[1])            
            elif len(p) == 3:
              # Binary Formula
              result1 = p[0]
              result2 = p[2]
              if(p[1].value=='&'):
                return result1[0], AndFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='|'):
                return result1[0], OrFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='->'):
                return result1[0], ImplicationFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='<->'):
                return result1[0], BiImplicationFormula(left=result1[1], right=result2[1])
              else:
                return result1[0], BinaryFormula(key=p[1].value, left=result1[1], right=result2[1])

        @self.pg.production('formula : OPEN_PAREN formula CLOSE_PAREN')
        def paren_formula(p):
            result = p[1]
            return p[0], result[1]

        @self.pg.production('variableslist : VAR')
        @self.pg.production('variableslist : VAR COMMA variableslist')
        def variablesList(p):
             if len(p) == 1:
                 return p[0], [p[0].value]
             else:
                result = p[2]
             return p[0], [p[0].value] + result[1]


        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            error = ''  

            if(productions == ['']):
                error = 'Nenhuma fórmula foi recebida, verifique a entrada.'
            if token.gettokentype() == '$end':
                error = 'Nenhuma fórmula foi recebida, verifique a entrada.'
            else:
                source_position = token.getsourcepos()
                error = 'A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente.\nLembre-se que uma uma fórmula é definida pela seguinte BNF:\nF :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q são átomos.\n'
                error += "Erro de sintaxe:\n"
                error += productions[source_position.lineno - 1]
                string = '\n'
                for i in range(source_position.colno -1):
                    string += ' '
                string += '^'
                if token.gettokentype() == 'OUT':
                    string += ' Símbolo não pertence a linguagem.'
                error += string
                
            raise ValueError("@@"+error)

    def get_error(self, type_error, token_error, rule):
        productions = self.state.splitlines()
        column_error = token_error.getsourcepos().colno
        erro = "Erro de sintaxe na linha {}:\n".format(token_error.getsourcepos().lineno)
        erro += productions[token_error.getsourcepos().lineno-1] + "\n"
        for i in range(column_error-1):
            erro += ' '
#        if type_error == constants.REFERENCED_FORMULE_NONE:## REVER SE NAO EXCLUIR
#            erro += '^, A fórmula {} não foi definida anteriormente ou foi descartada.\n'.format(token_error.value)
        
        return erro
    
    def get_parser(self):
        return self.pg.build()
    @staticmethod
    def getFormula(input_text=''):
        try:
          lexer = Lexer().get_lexer()
          tokens = lexer.lex(input_text)

          pg = ParserFormula(state=input_text)
          pg.parse()
          parser = pg.get_parser()
          result = parser.parse(tokens)
          return result
        except ValueError:
            s = traceback.format_exc()
            #print (f'Erro ao fazer o parser da fórmula!')
            return None
        else:
            return None
            pass



