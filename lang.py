import re #regular expressions
import sys

class Token:
	def __init__(self, ttype, tvalue):
		self.ttype = ttype
		self.tvalue = tvalue

class Tokenizer:
	def __init__(self, origin):
		self.origin = origin
		self.position = 0
		self.current = self.selectNext()

	def selectNext(self): #updates position
		c = "" 

		while (self.position<(len(self.origin)) and (self.origin[self.position]).isspace() and self.origin[self.position] != "\n"): #for white spaces
			self.position += 1
			
		if self.position == len(self.origin):
			token = Token(EOF,"EOF")
			self.current = token
			c = "EOF"
			return token #return added

		if self.origin[self.position] == "\n": #checks if we reached the end of a line
			token = Token(BREAK,"\n") #this caused "string out of range"
			self.position += 1
			self.current = token
			return token

		while (self.position<(len(self.origin)) and (self.origin[self.position]).isdigit()): #we'll be good till we find a symbol/reach the end of inp
			c += self.origin[self.position] #stores the number
			self.position += 1

		if c == "":
			if self.origin[self.position] == "+": #we're about to sum something!
				token = Token(PLUS, "+") 
				self.position += 1
				self.current = token
				
			elif self.origin[self.position] == "-": #we're about to subtract something!
				token = Token(MINUS, "-") 
				self.position += 1
				self.current = token

			elif self.origin[self.position] == "*": #we're about to multiply something!
				token = Token(MULT, "*") 
				self.position += 1
				self.current = token

			elif self.origin[self.position] == "/": #we're about to divide something!
				token = Token(DIV, "/") 
				self.position += 1
				self.current = token

			elif self.origin[self.position] == "(": #we're about to give priority to something!
				token = Token(POPN, "(")
				self.position += 1
				self.current = token
			
			elif self.origin[self.position] == ")": #we're about to end someone's priority!
				token = Token(PCLS, ")")
				self.position += 1
				self.current = token

			elif self.origin[self.position] == "=": #we're about assign something
				token = Token(ASGN, "=")
				self.position += 1
				self.current = token

			elif self.origin[self.position] == "<": #we're about assign something
				token = Token(LSST, "<")
				self.position += 1
				self.current = token

			elif self.origin[self.position] == ">": #we're about assign something
				token = Token(GRTT, ">")
				self.position += 1
				self.current = token

			elif self.origin[self.position] == ",": #we're about assign something
				token = Token("COMMA", ",")
				self.position += 1
				self.current = token

			elif self.origin[self.position].isalpha(): #then Raul said: "python users will be blessed with .isalpha()"
				idntT = ""
				while (self.position<(len(self.origin)) and (self.origin[self.position]).isdigit() or 
				self.origin[self.position] == "_" or self.origin[self.position].isalpha()): #we'll be good till we find a symbol/reach the end of inp
					idntT += self.origin[self.position]
					self.position += 1
				
				temp = idntT.upper()

				if temp in RWL:
					if (temp == "INTEGER") or (temp == "BOOLEAN"):
						token = Token("TYPE", temp) 
						self.current = token
					else:	 
						token = Token(temp, temp) 
						self.current = token
				else:
					token = Token("IDENTIFIER", temp)
					self.current = token
	
			else:
				raise Exception("Token not found " + str(self.origin[self.position]))

		else:
			c = int(c)
			token = Token(INT, c)
			self.current = token

		return token



class Parser: #token parser

	def run(stg):
		proCode = (PrePro.filter(stg)).lower()
		Parser.token = Tokenizer(proCode) #previously missed something here
		#Parser.token.selectNext()
		tree = Parser.Program()
		#print(tree)
		return tree

	def parserFactor():
		if Parser.token.current.ttype == INT:
			total = IntVal(Parser.token.current.tvalue, [])
			Parser.token.selectNext()
			return total

		if Parser.token.current.ttype == PLUS: 
			Parser.token.selectNext()
			children = [Parser.parserFactor()]
			total = UnOp("+", children)
			return total

		if Parser.token.current.ttype == MINUS:
			Parser.token.selectNext()
			children = [Parser.parserFactor()]
			total = UnOp("-", children)
			return total

		if Parser.token.current.ttype == "NAO":
			Parser.token.selectNext()
			children = [Parser.parserFactor()]
			total = UnOp("not",children)
			return total

		if Parser.token.current.ttype == "TRUE":
			total = BoolValue(True)
			Parser.token.selectNext()
			return total

		if Parser.token.current.ttype == "FALSE":
			total = BoolValue(False)
			Parser.token.selectNext()
			return total

		if Parser.token.current.ttype == INPT:
			total = InputOp([],[])
			Parser.token.selectNext()
			return total

		if Parser.token.current.ttype == "IDENTIFIER":
			val = Parser.token.current.tvalue
			Parser.token.selectNext()

			if Parser.token.current.ttype == "(":
				fvars = []
				while Parser.token.current.ttype != ")":
					Parser.token.selectNext()	
					fvars.append(Parser.parserRelExpression())
				Parser.token.selectNext()
				return FuncCall(val, fvars)
			
			total = Identifier(val)
			return total

		if Parser.token.current.ttype == "INPT":
			total = InputOp([],[])
			Parser.token.selectNext()
			return total

		elif Parser.token.current.ttype == "(":
			Parser.token.selectNext()
			total = Parser.parserRelExpression()
			if Parser.token.current.ttype != ")":
				raise Exception("Error - missing parenthesis )")

			Parser.token.selectNext()
			return total


	def parserTerm():
		total = Parser.parserFactor()
		mdalist = ["MULT","DIV","ETMB"]
		while Parser.token.current.ttype in mdalist:
			if Parser.token.current.ttype == MULT: 
				Parser.token.selectNext()
				children = [total, Parser.parserFactor()]
				total = BinOp("*", children)

			if Parser.token.current.ttype == DIV:
				Parser.token.selectNext()
				children = [total, Parser.parserFactor()]
				total = BinOp("/", children)

			if Parser.token.current.ttype == "ETMB":
				Parser.token.selectNext()
				children = [total, Parser.parserFactor()]
				total = BinOp("and", children)

			Parser.token.selectNext()
		
		return total

	@staticmethod
	def parserExpression():
		total = Parser.parserTerm() #priority 
		oplist = ["PLUS", "MINUS", "OU"]
		while Parser.token.current.ttype in oplist: 
			if Parser.token.current.ttype == PLUS: 
				Parser.token.selectNext()
				children = [total, Parser.parserTerm()]
				total = BinOp("+", children)

			if Parser.token.current.ttype == MINUS:
				Parser.token.selectNext()
				children = [total, Parser.parserTerm()] 
				total = BinOp("-", children)

			if Parser.token.current.ttype == "OR":
				Parser.token.selectNext()
				children = [total, Parser.parserTerm()] 
				total = BinOp("or", children)

		return total

	def parserRelExpression():
		total = Parser.parserExpression() #priority 

		if Parser.token.current.ttype == "=":
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp("=", children)

		if Parser.token.current.ttype == GRTT: #greater than
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp(">", children)

		if Parser.token.current.ttype == LSST: #less than
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp("<", children)

		return total

	def parserStatements():
		statementList = [Parser.parserStatement()]
		while Parser.token.current.ttype == BREAK:
			Parser.token.selectNext()
			statementList.append(Parser.parserStatement())

		return Statements("statements", statementList)

	def parserStatement():
		if Parser.token.current.ttype == IDNT:
			ident = Parser.token.current.tvalue
			Parser.token.selectNext()
			if Parser.token.current.ttype == ASGN:
				assign = Parser.token.current.tvalue
				Parser.token.selectNext()
				total = Assignment(assign, [Identifier(ident), Parser.parserExpression()])

		elif Parser.token.current.ttype == "DEFINIR":
			Parser.token.selectNext()
			if Parser.token.current.ttype == "IDENTIFIER":
				var = Identifier(Parser.token.current.tvalue)
				Parser.token.selectNext()
				if Parser.token.current.ttype == "COMO":
					Parser.token.selectNext()
					if Parser.token.current.ttype == "TYPE":
						vartype = Parser.token.current.tvalue
						total = VarDec([var,NodeType(vartype)])
						Parser.token.selectNext()
		
		elif Parser.token.current.ttype == "PRINT":
			Parser.token.selectNext()
			total = Print("PRINT", [Parser.parserExpression()])
		
		elif Parser.token.current.ttype == "ENQUANTO":
			Parser.token.selectNext()
			total = WhileOp("while", [Parser.parserRelExpression()])

			if Parser.token.current.ttype == BREAK:
				Parser.token.selectNext()
				total.children.append(Parser.parserStatements())

			if Parser.token.current.ttype != FINALIZADO:
				raise Exception("Error - 'FINALIZADO' expected, got "+ Parser.token.current.ttype)
			Parser.token.selectNext()

		elif Parser.token.current.ttype == "CALL":
			Parser.token.selectNext()
			vn = Parser.token.current.tvalue
			Parser.token.selectNext()
			if Parser.token.current.ttype == "(":
				fvlist = []
				while Parser.token.current.ttype != ")":
					Parser.token.selectNext()
					fvlist.append(Parser.parserRelExpression())
				Parser.token.selectNext()
				return FuncCall(vn,fvlist)

		elif Parser.token.current.ttype == IF:
			Parser.token.selectNext()
			total = IfOp([Parser.parserRelExpression()])
			if Parser.token.current.ttype == FAZER:
				Parser.token.selectNext()

				if Parser.token.current.ttype == BREAK:
					Parser.token.selectNext()	
					total.children.append(Parser.parserStatements())

					if Parser.token.current.ttype == SENAO:
						Parser.token.selectNext()

						if Parser.token.current.ttype == BREAK:
							Parser.token.selectNext()
							total.children.append(Parser.parserStatements())
			
					if Parser.token.current.ttype != FIM:
						raise Exception("Error - 'FIM (IF)' expected")
					Parser.token.selectNext()

					if Parser.token.current.ttype != IF:
						raise Exception("Error - 'IF' expected")
					Parser.token.selectNext()
		else:
			total = NoOp(0,[])
		
		return total

	def Program():
		tempList = []
		mainF = False

		while Parser.token.current.ttype != "EOF":

			if Parser.token.current.ttype == "SUB":
				svarlist = []
				snodelist = []

				for i in ["sub", "identifier", "("]:
					if i.lower() == "identifier":
						subv = Parser.token.current.tvalue
						if subv.lower() == "principal":
							mainF =  True

					if Parser.token.current.ttype.lower() != i:
						raise Exception("Error - check your input file - got "+ Parser.token.current.tvalue)

					Parser.token.selectNext()

				while Parser.token.current.ttype != ")":
					if Parser.token.current.ttype == "IDENTIFIER":
						var =  Identifier(Parser.token.current.tvalue)
						Parser.token.selectNext()

						if Parser.token.current.ttype == "COMO":
							Parser.token.selectNext()
							if Parser.token.current.ttype == "TYPE":
								typevar = Parser.token.current.tvalue
								Parser.token.selectNext()
								svarlist.append(VarDec([var, NodeType(typevar)]))
								if Parser.token.current.ttype == ",":
									Parser.token.selectNext()
								elif Parser.token.current.ttype == ")":
									Parser.token.selectNext()
									break
								else: 
									raise Exception("Error - Expected ',' got "+ Parser.token.current.tvalue)
				
							else: 
								raise Exception("Error - Expected 'TYPE' got "+ Parser.token.current.tvalue)
						
						else: 
							raise Exception("Error - Expected 'COMO' got "+ Parser.token.current.tvalue)

				if Parser.token.current.ttype == ")":
					Parser.token.selectNext()

				if Parser.token.current.ttype != "\n":
					raise Exception("Error - Expected 'BREAK' got "+ Parser.token.current.tvalue)
				
				while Parser.token.current.ttype == "\n":
					Parser.token.selectNext()
					snodelist.append(Parser.parserStatement())

				if Parser.token.current.tvalue.lower() == "fim":
					Parser.token.selectNext()
					if Parser.token.current.tvalue.lower() == "sub":
						Parser.token.selectNext()
					else:
						raise Exception("Error - Expected 'SUB' got "+ Parser.token.current.tvalue)
				else:
					raise Exception("Error - Expected 'FIM' got "+ Parser.token.current.tvalue)

				tempList.append(SubDec(subv, [svarlist,snodelist]))


#-------------------------------------- end sub --------------------------------------#

			if Parser.token.current.ttype == "FUNCTION":
				fvarlist = []
				fnodelist = []

				for i in ["function", "identifier", "("]:
					if i.lower() == "identifier":
						funcv = Identifier(Parser.token.current.tvalue)
					if Parser.token.current.ttype.lower() != i:
						raise Exception("Error - check your input file - got "+ Parser.token.current.tvalue)

					Parser.token.selectNext()

				while Parser.token.current.ttype != ")":
					if Parser.token.current.ttype == "IDENTIFIER":
						var =  Identifier(Parser.token.current.tvalue)
						Parser.token.selectNext()

						if Parser.token.current.ttype == "COMO":
							Parser.token.selectNext()
							if Parser.token.current.ttype == "TYPE":
								funcvar = Parser.token.current.tvalue
								Parser.token.selectNext()
								fvarlist.append(VarDec([var, NodeType(funcvar)]))
								if Parser.token.current.ttype == "COMMA":
									Parser.token.selectNext()
								elif Parser.token.current.ttype == ")":
									Parser.token.selectNext()
									break
								else: 
									raise Exception("Error - Expected ',' got "+ Parser.token.current.tvalue)
				
							else: 
								raise Exception("Error - Expected 'TYPE' got "+ Parser.token.current.tvalue)
						
						else: 
							raise Exception("Error - Expected 'COMO' got "+ Parser.token.current.tvalue)

				if Parser.token.current.ttype == ")":
					Parser.token.selectNext()

				if Parser.token.current.ttype == "COMO":
					Parser.token.selectNext()
					if Parser.token.current.ttype == "TYPE":	
						vtype =  Parser.token.current.tvalue
						Parser.token.selectNext()
						fvarlist.append(VarDec([funcv, NodeType(vtype)]))
				
				while Parser.token.current.ttype == "\n":
					Parser.token.selectNext()
					fnodelist.append(Parser.parserStatement())

				if Parser.token.current.tvalue == "FIM":
					Parser.token.selectNext()
					if Parser.token.current.tvalue == "FUNCTION":
						Parser.token.selectNext()
					else:
						raise Exception("Error - Expected 'FUNCTION' got "+ Parser.token.current.tvalue)
				else:
					raise Exception("Error - Expected 'FIM' got "+ Parser.token.current.tvalue)

				tempList.append(FuncDec(funcv.value, [fvarlist, fnodelist]))

			elif Parser.token.current.ttype == "\n":
				Parser.token.selectNext()

		if mainF:
			tempList.append(FuncCall("PRINCIPAL",[]))
		return Statements("statements", tempList)


class PrePro:
	def filter(inp_stg):
		#print("Input = " + inp_stg)
		return re.sub("'.*\n","", inp_stg) #replace substrings module

class Node:
	def __init__(self):
		self.value = None
		self.children = []

	def Evaluate(self):
		pass

class BinOp(Node): #binary ops -> a(binop)b = c
	def __init__(self, value, children):
		self.value = value
		self.children = children

		if len(children) != 2:
			raise Exception("Error - two children expected, got" +self.children)			

	def Evaluate(self,symb):
		#checking if variables types match so we can go on and do ops!
		var1 = self.children[0].Evaluate(symb)[0]
		var2 = self.children[1].Evaluate(symb)[0]

		if self.value == "+":
			return (var1 + var2, "integer")
		elif self.value == "-":
			return (var1 - var2, "integer")
		elif self.value == "*":
			return (var1 * var2, "integer")
		elif self.value == "/":
			return (var1 // var2, "integer")
		elif self.value == "=":
			return (var1 == var2, "boolean")
		elif self.value == "<":
			return (var1 < var2, "boolean")
		elif self.value == ">":
			return (var1 > var2, "boolean")
		elif self.value == "or":
			return (var1 or var2, "boolean")
		elif self.value == "and":
			return (var1 and var2, "boolean")

class UnOp(Node): #unary ops -> -(a) = -a | -(-a) = a
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self, symb):
		if self.value == "+":
			return self.children[0].Evaluate(symb)
		elif self.value == "-":
			var = self.children[0].Evaluate(symb)
			var = (var[0]*-1,var[1])
			return var
		elif self.value == "not":
			var = self.children[0].Evaluate(symb)
			var = (not var[0],var[1])		
			return var
		else:
			raise Exception("Error - undefined UnOp: "+ str(self.value))

class IntVal(Node): #gets and returns int
	def __init__(self, value, children): 
		self.value = value
		self.children = children	
	
	def Evaluate(self, symb):
		return (self.value,"integer")

class NoOp(Node): #dummy - nothing to do here
	def __init__(self, value, children):
		self.value = value
		self.children = children	

	def Evaluate(self,symb):
		pass

class Assignment(Node): #sets value to given variable - a = K
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self, symb):
		symb.setter(self.children[0].value, self.children[1].Evaluate(symb))


class Identifier(Node):
	def __init__(self, value):
		self.value = value
	
	def Evaluate(self, symb):
		return symb.getter(self.value)

class Statements(Node): #statement in statements
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self, symb):
		for i in self.children:
			i.Evaluate(symb)

class Print(Node): 
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self,symb):
		if type(self.children[0].Evaluate(symb)) is tuple:
			print(self.children[0].Evaluate(symb)[0])
		else:
			print(self.children[0].Evaluate(symb))

class WhileOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self,symb):
		while self.children[0].Evaluate(symb)[0]:
			self.children[1].Evaluate(symb)

class IfOp(Node):
	def __init__(self, children):
		self.children = children
	
	def Evaluate(self,symb):
		if self.children[0].Evaluate(symb)[0] == True:
			self.children[1].Evaluate(symb)
		else:
			if len(self.children) == 3:
				self.children[2].Evaluate(symb)
			else:
				pass

class InputOp(Node):
	def __init__(self, value,children):
		self.value = value
		self.children = children
	
	def Evaluate(self,symb):
		return (int(input()),"integer")

class NodeType(Node):
	def __init__(self, value):
		self.value = value

		temptrylist = ["integer","boolean"]
		if value.lower() not in temptrylist:
			raise Exception("Error - unexpected type " + str(self.value))
			
	def Evaluate(self, symb):
		if self.value == "integer":
			return (self.value,0)
		elif self.value == "boolean":
			return (self.value, False)

class SymbolTable:
	def __init__(self):
		self.varDict = {}

	def getter(self, var): #returns value for variable
		if var in self.varDict.keys():
			return self.varDict[var]
		else:
			raise Exception("Error - undeclared variable")

	def setter(self, var, value): #assigns value to variable
		if var not in self.varDict:
			raise Exception("Error - undeclared variable")		
		self.varDict[var] = value
	
	def declarator(self, var, value):
		if var in self.varDict:
			raise Exception("Error - duplicate variable")
		self.varDict[var] = value

	def clone(self, ancsymb):
		self.varDict = ancsymb.varDict.copy()

class VarDec(Node):
	def __init__(self, children):
		self.children = children
	
	def Evaluate(self, symb):
		symb.declarator(self.children[0].value,[None, self.children[1]])

class SubDec(Node):
	def __init__(self, value, children):
		self.children = children	
		self.value = value

	def Evaluate(self, symb):
		symb.declarator(self.value,["SUB",[self.children[0], self.children[1]]])

class FuncDec(Node):
	def __init__(self, value, children):
		self.children = children	
		self.value = value

	def Evaluate(self, symb):
		symb.declarator(self.value,["FUNCTION", [self.children[0],self.children[1]]])

class FuncCall(Node):
	def __init__(self, value, children):
		self.children = children	
		self.value = value
	
	def Evaluate(self, symb):
		#get fundec node
		func =  symb.getter(self.value)
		newsymb = SymbolTable()
		newsymb.clone(symb)
		ford = []

		for i in func[1][0][0:-1]:
			ford.append(i.children[0].value)
			i.Evaluate(newsymb)

		for j in range(len(ford)):
			val = self.children[j].value
			if val in symb.varDict:
				val = symb.getter(val)
			newsymb.setter(ford[j], val)
		
		for e in func[1][1]:
			e.Evaluate(newsymb)

		if func[0] == "FUNCTION":
			return newsymb.getter(self.value)



class BoolValue(Node):
	def __init__(self, value):
		self.value = value
	
	def Evaluate(self,symb):
		return (self.value,"boolean")


#Tokens
PLUS = "PLUS" #sum 
MINUS = "MINUS" #subtract | negative numbers
INT = "INT" #digits (currently ints only)
EOF = "EOF" #end of input
MULT = "MULT" #multiply
DIV = "DIV" #divide	
POPN = "(" #parenthesis open
PCLS = ")"	#parenthesis close

ASGN = "=" #assignment
BREAK = "\n" #line break
IDNT = "IDENTIFIER" #identifier, O RLY?
GRTT = ">" #greater than
LSST = "<" #less than
INPT = "INPUT" #input
ENQUANTO = "ENQUANTO" #while start
FINALIZADO = "FINALIZADO" #while end 
IF = "SE" #if token
FAZER = "FAZER" #then token
FIM = "FIM"
SENAO = "SENAO"

#reserved words list
RWL = ["BEGIN", "FIM", "PRINT", "SE", "FAZER", "SENAO", "OU", "ETMB", "ENQUANTO", "FINALIZADO", "EOF",
		"INPUT", "NAO", "DEFINIR", "INTEGER", "BOOLEAN", "TRUE", "FALSE", "COMO", "SUB", "FUNCTION"] 

def main():
	
	symb = SymbolTable()
	try:
	#inpFile = "test.vbs"
		inpFile = sys.argv[1]
	except IndexError:
		print("failed to find file")
		sys.exit(1)

	with open(inpFile, "r") as file:
		inp = file.read() +"\n"
	try:
		inp = inp.replace("\\n", "\n") 
		out = Parser.run(inp)
		out.Evaluate(symb)
	except Exception as err:
		print(err)

if __name__== "__main__":
    main()
