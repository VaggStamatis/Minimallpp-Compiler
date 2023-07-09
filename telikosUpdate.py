
#Authors : Vaggelis Stamatis    AM: 3334  username cs : cse63334 
#		   Dimitris Mataragkas  AM: 3272  username cs : cse63272  


import string
import sys					
import copy					
import os

'''
The following program compiles code from minimall++ to assembly 
It generates 2 files. One that contains the quads named .int file and one that contains the finall code in assemble named .asm

For this functionality we followed the flow described in the undergraduate lesson Compilers

Computer Scinece and Enginnering, Univercity of Ioannina Greece


				####################
				#  Word analysis   #
				####################
						 |
						 V
				#######################
				#  Editorial analysis #
				#######################
						 |
						 V		 
				########################
				#  Intermediate Code   #
				########################
						 |
						 V
				#################### 
				#   Symbol Matrix  #
				####################
						 |
						 V
				###########################
				#  Assembly (Finall) Code #
				###########################

'''

				####################
				#  Word analysis   #
				####################
file_pos = 0 
file_line = 0
pointer_pos = 0

def lektikos():
	global file_pos 
	global file_line
	global pointer_pos 

	
	if(len(sys.argv) != 2) : 
		print("Re-run the programm and enter the file you want to compile as an argument ")
		sys.exit(1)
	file = open(sys.argv[1] , 'r')

	boundwords = [['programm', 10], ['declare', 11], ['if', 12], ['then',13], ['else', 14],['while', 15], ['forcase', 16], ['when', 17], ['default', 18], ['not', 19],
				['and', 20], ['or', 21], ['function', 22], ['procedure', 23], ['call', 24], ['return', 25], ['in', 26], ['inout', 27], ['input', 28], ['print', 29], ]

	symbol_phase = 1
	identifier_phase = 2 
	number_phase = 3 
	smaller_phase = 4
	bigger_phase = 5
	comment_phase = 6
	dots_phase = 7 
	COOL_phase = 100
	ERROR_phase = 200
	EOF_phase =  300

	word =[]
	wordList = []
	identifier = ''
	negative_num = 0
	letter_counter = 0
	number_flag = 0

	file.seek(pointer_pos)

	#Recognition of the symbols bound words numbers etc 
	phase = symbol_phase
	while(phase != COOL_phase and phase != ERROR_phase and phase != EOF_phase):
		input = file.read(1)
		if(not input and phase!=comment_phase):
			if(phase == identifier_phase):
				phase=COOL_phase
				identifier = "".join(word)
				wordList += [identifier] + [1]
			elif (phase == number_phase):
				phase = COOL_phase
				identifier = "".join(word)
				wordList += [identifier] + [2]
			else: 
				phase = EOF_phase 
		if(phase == symbol_phase):
			if(input == '\t' or input ==' ' or input == '\n'):
				if(input == '\t'):
					file_pos += 8
				if(input == '\n'):
					file_line += 1
					file_pos = 0
				phase = symbol_phase
			elif(input in string.ascii_letters):
				phase = identifier_phase
			elif(input in string.digits):
				phase = number_phase 
			elif(input == '<'):
				phase = smaller_phase
			elif(input == '>'):
				phase = bigger_phase
			elif(input == ':'):
				phase = dots_phase
			elif(input == '\\'):
				phase = comment_phase
			elif(input== ''):
				phase = EOF_phase
			elif(input =='\r'):
				phase = symbol_phase
			else: 
				phase = COOL_phase
				word = input 
				identifier = "".join(word)
				if(input == '+'):
					wordList += [identifier] + [3]
				elif(input == '-'):
					input = file.read(1)
					file_pos += 1
					if(input in string.digits):
						negative_num = 1
						phase = number_phase 
					else : 
						file.seek(file.tell()-2)
						file_pos-=2
						input = file.read(1)
						file_pos += 1 
						wordList += [identifier] + [4]
				elif(input == '*'):
					wordList += [identifier] + [5]
				elif(input == '/'):
					wordList += [identifier] + [6]
				elif(input == ';'):
					wordList += [identifier] + [7]
				elif(input == ','):
					wordList += [identifier] + [8]
				elif(input == '{'):
					wordList += [identifier] + [9]
				elif(input == '}'):
					wordList += [identifier] + [10]
				elif(input == '('):
					wordList += [identifier] + [11]
					phase = COOL_phase
				elif(input == ')'):
					wordList += [identifier] + [12]
				elif(input == '['):
					wordList += [identifier] + [13]
				elif(input == ']'):
					wordList += [identifier] + [14]
				elif(input == '='):
					wordList += [identifier] + [15]
				else:
					phase =ERROR_phase
					print('ERROR in line %d:%d Unknown Character = %s' % (file_line , file_pos , input))

		#identifier_phase
		if(phase == identifier_phase):
			if (input in string.ascii_letters or input in string.digits):
				letter_counter += 1
				if(letter_counter>30):
					number_flag = letter_counter-30
				if(number_flag >= 1):
					identifier = "".join(word)
					wordList+= [identifier] + [1]
				else:
					word += input
					phase =  identifier_phase 
			else: 
				phase = COOL_phase
				identifier = "".join(word)
				wordList = [identifier] + [1]
				if(number_flag >= 1):
					print('Found Word with size bigger than 30 chars in Line ----> %d:%d' % (file_line , file_pos))
				file.seek(file.tell()-1)
				#file_pos -= 1
			
		#number_phase
		if(phase == number_phase):
			if(input in string.digits):
				phase = number_phase
				word += input 
			else : 
				phase = COOL_phase
				identifier = "".join(word)
				wordList += [identifier] + [2] 
				file.seek(file.tell()-1)
				file_pos -= 1
				if(int(identifier)>32767 or int(identifier)<(-32767)):
					phase = ERROR_phase
					if(int(identifier)> 32767):
						print('Error the number in line ----> %d:%d is bigger than the positive limit ' % (file_line , file_pos ))
					else:
						print('Error the number in line ----> %d:%d is smaller than the negative limit ' % (file_line , file_pos ))

		#smaller_phase
		if(phase == smaller_phase):
			phase = COOL_phase
			input = file.read(1)
			file_pos += 1	
			if(input == '>'):
				word = '<>'
				identifier = "".join(word)
				wordList += [identifier] + [17]
			if(input == '='):
				word = '<='
				identifier = "".join(word)
				wordList += [identifier] + [16]
			else:
				word = '<'
				identifier = "".join(word)
				wordList += [identifier] + [18]
				file.seek(file.tell()-1)
				file_pos-=1		
					
		#bigger_phase
		if(phase == bigger_phase):
			phase = COOL_phase
			input = file.read(1)
			file_pos -= 1	
			if(input == '='):
				word = '>='
				identifier = "".join(word)
				wordList += [identifier] + [19]
			else:
				word = '>'
				identifier = "".join(word)
				wordList += [identifier] + [20]
				file.seek(file.tell()-1)
				file_pos-=1	
		
		#dots_phase
		if(phase == dots_phase):
			input = file.read(1)
			file_pos += 1
			if(input == '='):
				phase = COOL_phase
				word = ':='
				identifier = "".join(word)
				wordList += [identifier] + [21]
			else:
				phase = COOL_phase
				wordList = ':'
				file.seek(file.tell()-1)
				file_pos -=1
				identifier = "".join(word)
				wordList += [identifier] + [22]

		#comments_phase
		if(phase == comment_phase):
			input = file.read(1)
			file_pos += 1 
			if(input == '\\'):
				phase= symbol_phase
			elif(input == ''):
				phase = ERROR_phase
				print('Error the comments are unclosed at line ----> %d:%d' % (file_line,file_pos))
			else:
				phase = COOL_phase
				word = '//'
				identifier = "".join(word)
				wordList += [identifier] + [21]
				file.seek(file.tell()-1)
				file_pos-=1

		#checking for file ending 		
		if(phase == EOF_phase):
			wordList = ['EOF']

	pointer_pos = file.tell()

	identifier = "".join(word)
	for i in range(len(boundwords)):
		if (identifier == boundwords[i][0]):
			wordList.pop()
			wordList += [boundwords[i][1]]
			break
	file.close()
	return wordList[0],wordList[1]

def print_lektikos():
	while(1):
		tupl = lektikos()
		lektikos_list = tupl[0]
		case = tupl[1]
		print('>\t( %s,%d )' % (tupl[0], tupl[1]))
		print('______________________________________________________________|')
		

#print_lektikos()
#lektikos()

				#######################
				#  Editorial analysis #
				#######################

def syntaktikos(cFile):
	global token 
	global temporary 
	global FunctionFlag
	FunctionFlag = 0 

	token = lektikos()
	def program():
		global token
		global file_line
		global file_pos
		if(token[0]=='program'):
			token = lektikos()
			if(token[1] == 1):
				programName = token[0]
				token = lektikos()
				if(token[0]=='{'):
					token = lektikos()
					block(programName , 1)
					if(token == '}'):
						token = lektikos()
						return
					else:
						print('Error the program does not close correctrly missing } at Line ---> %d:%d' % (file_line , file_pos))
						exit(1)
				else:
					print('Error the program does not open correctrly missing { at Line ---> %d:%d' % (file_line , file_pos))
					exit(1)
			else:
				print('Error missing program name at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			print('Error missing bound word program at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return
	
	def block(blockName , blockFlag):
		global token
		new_scope(blockName)
		if(blockFlag != 1):
			make_parameters()
		if(token[0] == 'declare'):
			declarations()
		subPrograms()
		genQuad('begin_block',blockName, '_','_')

		if(blockFlag!= 1):
			calculate_startQuad()
		statements()
		if(blockFlag==1):
			genQuad('halt','_','_','_')
		else:
			calculate_framelength()
		genQuad('end_block',blockName,'_','_')

		print("Symbol Table")
		print_Symbol_table()
		final_asm_file()
		delete_scope()
		return

	def declarations():
		global token
		while(token[0]=='declare'):
			cFile.write("int")
			token = lektikos()
			varList()
			if(token[0]==';'):
				cFile.write(";\n\t")
				token = lektikos()
			else:
				print('Error declerations do not close correctrly missing ";" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		return

	def varList():
		global token
		if(token[1]==1):
			cFile.write(token[0])
			enti = Entity()
			enti.type = 'VAR'
			enti.name = token[0]
			enti.variable.offset = calculate_offset()
			new_entity(enti)

			token=lektikos()
			while(token[0]==','):
				cFile.write(token[0])
				token= lektikos()
				if(token[1]==1):
					cFile.write(token[0])
					enti = Entity()
					enti.type = 'VAR'
					enti.name = token[0]
					enti.variable.offset = calculate_offset()
					new_entity(enti)
					token=lektikos()
				else:
					print('Error varList expected variables in declarations at Line ---> %d:%d' % (file_line , file_pos))
					exit(1)
		return
	
	def subPrograms():
		global token
		while(token[0]=='procedure' or token[0]=='function'):
			subProgram()
		return

	def subProgram():
		global token
		if(token[0]=='function'):
			token = lektikos()
			if(token[1]==1):
				name=token[0]
				enti = Entity()
				enti.type = 'SUBPR'
				enti.name = token[0]
				enti.subprogram.type = 'Function'
				enti.subprogram.nestingLevel = topScope.nestingLevel+1
				new_entity(enti)
				token=lektikos()
				funcBody(name,1)
			else:
				print('Error SubProgram name was expected at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)

		elif(token[0]=='procedure'):
			token = lektikos()
			if(token[1]==1):
				name=token[0]
				enti = Entity()
				enti.type = 'SUBPR'
				enti.name = token[0]
				enti.subprogram.type = 'Procedure'
				enti.subprogram.nestingLevel = topScope.nestingLevel+1
				new_entity(enti)
				token=lektikos()
				funcBody(name,0)
			else:
				print('Error Procedure name was expected at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		return
	
	def funcBody(blockName , isFunc):
		global token
		formalPars()
		if(token[0]=='{'):
			token = lektikos()
			block(blockName,-1)
			if(token[0]=='}'):
				token=lektikos()
			else:
				print('Error "{" was expected at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
				return
		else:
			print('Error "}" was expected at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return

	def formalPars():
		global token
		if(token[0]=='('):
			token=lektikos()
			if(token[0]=='in' or token[0]== 'inout'):
				formalParList()
				if(token[0]==')'):
					token = lektikos()
					return
				else:
					print('Error ")" was expected at Line ---> %d:%d' % (file_line , file_pos))
					exit(1)
			elif(token[0]==')'):
				token=lektikos()
				return
			else:
				print('Error the bound word "in" or "inout" was expected at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			print('Error "(" was expected at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)		

	def formalParList():
		global token
		formalParItem()
		while(token[0]==','):
			token = lektikos()
			if(token[0]== 'in' or token[0] == 'inout'):
				formalParItem()
			else:
				print('Error the bound word "in" or "inout" was expected at Line ---> %d:%d' % (file_line , file_pos))	
				exit(1)	
		return

	def formalParItem():
		global token 
		if(token[0]== 'in'):
			token = lektikos()
			if(token[1]==1):
				argu =Argument()
				argu.name = token[0] 
				argu.parMode = 'CV'
				new_argument(argu)
				token = lektikos()
				return
			else:
				print('Error variable name was expected after "in" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		elif(token[0]=='inout'):
			token = lektikos()
			if(token[1]==1):
				argu =Argument()
				argu.name = token[0] 
				argu.parMode = 'REF'
				new_argument(argu)
				token = lektikos()
				return
			else:
				print('Error variable name was expected after "inout" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		return

	def statements():
		global token 
		statement()
		while(token[0]==';'):
			token=lektikos()
			statement()
		return

	def statement():
		global token
		if(token[1]==1):
			assignmentStat()
		elif(token[0]=='if'):
			ifStat()
		#elif(token[0]=='doublewhile'):
			#doublewhileStat()
		elif(token[0]=='while'):
			whileStat()
		elif(token[0]=='forcase'):
			forcaseStat()
		elif(token[0]=='input'):
			inputStat()
		#elif(token[0]=='incase'):
			#incaseStat()
		elif(token[0]=='print'):
			printStat()
		elif(token[0]=='return'):
			returnStat()
		elif(token[0]=='exit'):
			exitStat()
		return 
	
	def assignmentStat():
		global token 
		global temporary
		global FunctionFlag
		id = token[0]
		token = lektikos()
		if(token[0] == ':='):
			token = lektikos()
			Eplace = expression()
			if(FunctionFlag ==1):
				genQuad(':=', temporary , '_' , id)
				FunctionFlag = 0
			else:
				genQuad(':=', Eplace, '_' , id)
		else:
			print('Error expected ":=" operator at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return

	def expression():
		global token
		optionalSign()
		T1place = term()
		while(token[0]=='+' or token[0]=='-'):
			plusORminus = addOperator()
			T2place = term()
			w = newTemp()
			genQuad(plusORminus , T1place , T2place , w)
			T1place = w 
		Eplace = T1place
		return Eplace

	def optionalSign():
		global token
		if(token[0]=='+' or token[0] == '-'):
			addORsub = addOperator()
			return
		
	def addOperator():
		global token
		if(token[0]=='+' or token[0] == '-'):
			addOp = token
			token = lektikos()
		return addOp

	def term():
		global token
		F1place = factor()
		while(token[0]=='*' or token[0]=='/'):
			mulORdiv = mulOper()
			F2place = factor()
			w = newTemp()
			genQuad(mulORdiv , F1place , F2place ,w)
			F1place = w 
		Tplace = F1place
		return Tplace
	
	def factor():
		global token 
		if(token[1]==2):
			fact = token[0]
			token = lektikos()
		elif(token[0]=='('):
			token = lektikos()
			Eplace = expression()
			if(token[0]==')'):
				fact = Eplace
				token = lektikos()
			else:
				print('Error expected ")"  at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		elif(token[1]==1):
			fact= token[0]
			token = lektikos() 
			idTail(fact)
		else:
			print('Error expected constant , expression or variable at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return fact

	def idTail(idName):
		global token
		global FunctionFlag
		if(token[0] == '('):
			FunctionFlag = 1
			actualPars(1,idName)
			return
	
	def actualPars(FunctionFlag , idName):
		global token
		global temporary

		if(token[0] == '('):
			token = lektikos()
			actualParList()
			if(token[0]==")"):
				token = lektikos()
				if(FunctionFlag == 1):
					w = newTemp()
					genQuad('par', w, 'RET', '_')
					genQuad('call' , idName , '_' , '_')
					temporary = w
				else : 
					genQuad('call' , idName , '_' , '_')
			else: 
				print('Error expected ")" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			print('Error expected "(" at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return

	def actualParList():
		global token
		actualParItem()
		while(token[0]==','):
			token = lektikos()
			actualParItem()
		return

	def actualParItem():
		global token 
		if(token[0]=='in'):
			token = lektikos()
			thisExpression = expression()
			genQuad('par', thisExpression , 'CV' , '_')
		elif(token[0]=='inout'):
			token = lektikos()
			if(token[1]==1):
				genQuad('par' , token[0] , 'REF' , '_')
				token = lektikos()
			else:
				print('Error expected variable (id) at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			print('Error expected "in" or "inout" at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return

	def relationalOper():
		global token 
		if(token[0]=='=' or token[0]=='<' or token[0]=='>' or token[0]=='<=' or token[0]=='>=' or token[0]=='<>'):
			relop = token[0]
			token = lektikos()
		else:
			print('Error expected relational operator at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return relop

	def mulOper():
		global token 
		if(token[0]=='*' or token[0]=='/'):
			oper = token[0]
			token = lektikos()
		return oper

	def ifStat():
		global token 
		token = lektikos()
		if(token[0] =='(' ):
			token = lektikos()
			B = condition()
			if(token[0]==')'):
				token = lektikos()
				if(token[0] != 'then'):
					print('Error expected "then" at Line ---> %d:%d' % (file_line , file_pos))
					exit(1)
				token = lektikos()
				backPatch(B[0],nextQuad())
				statements()
				ifList = makeList(nextQuad())
				genQuad('JUMP' , '_', '_', '_')
				backPatch(B[1], nextQuad())
				elsePart()
				backPatch(ifList, nextQuad())
			else:
				print('Error expected ")" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			print('Error expected "(" at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		Is_true = B[0]
		Is_false= B[1]
		return Is_true , Is_false

	def elsePart():
		global token
		if(token[0]== 'else'):
			token = lektikos()
			statements()
		return

	def whileStat():
		global token 
		token = lektikos()
		if(token[0]=='('):
			token = lektikos()
			Bquad = nextQuad()
			B = condition()
			if(token[0]== ')'):
				backPatch(B[0], nextQuad)
				token = lektikos()
				statements()
				genQuad('Jump', '_', '_', '_')
				backPatch(B[1], nextQuad())
			else:
				print('Error expected ")" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			print('Error expected "(" at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		wStat_true = B[0]
		wStat_false = B[1]
		return wStat_true , wStat_false

	def forcaseStat():
		global token
		token = lektikos()
		for_stat_true = []
		for_stat_false = []
		q = nextQuad()
		while(token[0]== 'default'):
			token = lektikos()
			B = condition()
			if(token[0]== '('):
				token= lektikos()
				B= condition()
				if(token[0]== ')'):
					token = lektikos()
					if(token[0]== ':'):
						for_stat_true = B[0]
						for_stat_false = B[1]
						backPatch(for_stat_true , nextQuad())
						#S1 = statements()
						genQuad('JUMP', '_', '_', q)
						backPatch(for_stat_false , nextQuad())
					else:
						print('Error expected ":" at Line ---> %d:%d' % (file_line , file_pos))
						exit(1)
				else:
					print('Error expected ")" at Line ---> %d:%d' % (file_line , file_pos))
					exit(1)
			else:
				print('Error expected "(" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		if(token[0]=='default'):
			token = lektikos()
			if(token[0]==':'):
				token = lektikos()
				statements()
			else:
				print('Error expected ":" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		return
		
	def inputStat():
		global token 
		token = lektikos()
		if(token[0]== '('):
			token = lektikos()
			if(token[1]== 1):
				token = lektikos()
				if(token[0]== ')'):
					token = lektikos()
					genQuad('inp' , token[0], '_', '_')
				else:
					print('Error expected ")" at Line ---> %d:%d' % (file_line , file_pos))
					exit(1)
			else:
				print('Error expected id at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			print('Error expected "(" at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return

	def callStat():
		global token 
		token = lektikos()
		if(token[1]==1):
			token = lektikos()
			idName = token[0]
			actualPars(0,idName)
			return
		else:
			print('Error expected name of the function at Line ---> %d:%d' % (file_line , file_pos))
			exit()

	def condition():
		global token
		cond_true = []
		cond_false = []
		Q1 = boolTerm()
		cond_true = Q1[0]
		cond_false = Q1[1]
		while(token[0]=='or'):
			token = lektikos()
			backPatch(cond_false , nextQuad())
			Q2 = boolTerm()
			cond_true = merge(cond_true , Q2[0])
			cond_false = Q2[1] 
		return cond_true , cond_false

	def boolTerm():
		global token 
		bool_true = []
		bool_false=[]
		R1 = boolFactor()
		bool_true = R1[0]
		bool_false = R1[1]
		while(token[0]== 'and'):
			token = lektikos()
			backPatch(bool_true , nextQuad())
			R2 = boolFactor()
			bool_false = merge(bool_false , R2[1])
			bool_true = R2[0]
		return bool_true , bool_false

	def boolFactor():
		global token 
		boolfac_true = []
		boolfac_false = []
		Eplace1 = ''
		Eplaxe2 = ''
		relop = ''
		if(token[0]== 'not'):
			token = lektikos()
			if(token[0]=='['):
				token = lektikos()
				B=condition()
				if(token[0]==']'):
					token = lektikos()
					boolfac_true = B[1]
					boolfac_false = B[0]
				else:
					print('Error expected "]" at Line ---> %d:%d' % (file_line , file_pos))
					exit(1)
			else:
				print('Error expected "[" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		elif(token[0]== '['):
			token = lektikos()
			B = condition()
			if(token[0]==']'):
				token = lektikos()
				boolfac_true = B[0]
				boolfac_false = B[1]
			else:
				print('Error expected "]" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			Eplace1 = expression()
			relop = relationalOper()
			Eplaxe2 = expression()
			boolfac_true = makeList(nextQuad())
			genQuad(relop , Eplace1 , Eplaxe2 , '_')
			boolfac_false = makeList(nextQuad())
			genQuad('JUMP', '_' , '_' , '_' )
		return boolfac_true , boolfac_false
	

			

	def printStat():
		global token 
		if(token[0]=='('):
			token = lektikos()
			Eplace = expression()
			if(token[0]== ')'):
				token = lektikos()
				genQuad('out' , Eplace , '_','_')
			else:
				print('Error expected ")" at Line ---> %d:%d' % (file_line , file_pos))
				exit(1)
		else:
			print('Error expected "(" at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return

	def returnStat():
		global token 
		global OneReturn
		OneReturn=1
		if(token[0]=='return'):
			token=lektikos()
			Eplace =expression()
			genQuad('retv', Eplace, '_', '_')
		else:
			print('Error expected "return" at Line ---> %d:%d' % (file_line , file_pos))
			exit(1)
		return

	def exitStat():
		global token
		token=lektikos()
		return
	
	program()
	print('\n ___________________END OF SYNTAKTIKH ANALYSH___________________ ')

				########################
				#  Intermediate Code   #
				########################		
					
global allQuads
allQuads  = []        #quad list
Quad_counter = 1 #identifier for every quad
def nextQuad():
	global Quad_counter
	return Quad_counter

allQuadsFinal = []
def genQuad(a, b, c, d):
	global Quad_counter
	global allQuads
	global allQuadsFinal 

	list=[]
	list = [nextQuad()]
	list += [a]+ [b]+ [c]+[d]
	Quad_counter += 1 
	allQuads += [list]
	allQuadsFinal += [list]
	return list

T_i = 1
tempList = []
def newTemp():
	global T_i
	global tempList
	list = ['T_']
	list.append(str(T_i))
	tempVar= "".join(list)
	T_i +=1

	tempList += [tempVar]
	enti = Entity()
	enti.type = 'TEMP'
	enti.name = tempVar
	enti.tempVar.offset = calculate_offset()
	new_entity(enti)
	return tempVar

def emptyList():
	listPointer = []
	return listPointer

def makeList(a):
	listThis = [a]
	return listThis

def merge(l1 , l2):
	list = []
	list += l1 + l2
	return list

def backPatch(list , z):
	global allQuads
	for i in range(len(list)):
		for j in range(len(allQuads)):
			if(list[i]==allQuads[j][0] and allQuads[j][4]=='_'):
				allQuads[j][4] = z
				j=len(allQuads)	
	return
		

				#################### 
				#   Symbol Matrix  #
				####################
topScope = None							

class Entity():
	def __init__(self):
		self.name = ''					
		self.type = ''	
		
		self.variable = self.Variable()
		self.subprogram = self.SubProgram()
		self.parameter = self.Parameter()
		self.tempVar = self.TempVar()
		
	class Variable:
		def __init__(self):
			self.type = 'Int'
			self.offset = 0				
	class SubProgram:					
		def __init__(self):
			self.type = ''				
			self.startQuad = 0			
			self.frameLength = 0		
			self.argumentList = []		
			self.nestingLevel = 0       
			
	class Parameter:
		def __init__(self):
			self.mode = ''				
			self.offset = 0				
	class TempVar:
		def __init__(self):
			self.type = 'Int'			
			self.offset = 0				
class Scope():
	def __init__(self):
		self.name = ''						
		self.entityList = []				
		self.nestingLevel = 0			
		self.enclosingScope = None			
		
class Argument():
	def __init__(self):
		self.name = ''	
		self.type = 'Int'	
		self.parMode = ''	

def new_argument(object):
	global topScope
	
	topScope.entityList[-1].subprogram.argumentList.append(object) 	
def new_entity(object):
	global topScope
	
	topScope.entityList.append(object)
def new_scope(name):
	global topScope

	nextScope = Scope()
	nextScope.name = name
	nextScope.enclosingScope=topScope
	if(topScope == None):
		nextScope.nestingLevel = 0
	else:
		nextScope.nestingLevel = topScope.nestingLevel + 1
	topScope = nextScope
def delete_scope():
	global topScope
	freeScope = topScope
	topScope = topScope.enclosingScope
	del freeScope

def calculate_offset():
	global topScope
	counter=0
	if(topScope.entityList is not []):
		for ent in (topScope.entityList):
			if(ent.type == 'VAR' or ent.type == 'TEMP' or ent.type=='PARAM'):
				counter +=1
	offset = 12+(counter*4)
	return offset

def calculate_startQuad():
	global topScope
	topScope.enclosingScope.entityList[-1].subprogram.startQuad = nextQuad()
		
def calculate_framelength():
	global topScope
	topScope.enclosingScope.entityList[-1].subprogram.frameLength = calculate_offset()
	
def make_parameters():
	global topScope
	for arg in topScope.enclosingScope.entityList[-1].subprogram.argumentList:
		ent = Entity()
		ent.name = arg.name
		ent.type = 'PARAM'
		ent.parameter.mode = arg.parMode
		ent.parameter.offset = calculate_offset()
		new_entity(ent)

def print_Symbol_table():
	global topscope
	
	print("|-----------------------------------------------------------------------------------------------------------------|")
	print("")

	scopeA=topScope
	while scopeA != None:
		print("SCOPE: "+"name:"+scopeA.name+" nestingLevel:"+str(scopeA.nestingLevel))
		print("\tENTITIES:")
		for ent in scopeA.entityList:
			if(ent.type == 'TEMP'):
				print("\t \t "+"|"+" name-->"+ent.name+"\t type-->"+ent.type+"\t temp-type-->"+ent.tempVar.type+"\t offset-->"+str(ent.tempVar.offset)+ "|")
			elif(ent.type == 'VAR'):
				print("\t \t "+"|"+" name-->"+ent.name+"\t type-->"+ent.type+"\t variable-type-->"+ent.variable.type+"\t offset-->"+str(ent.variable.offset) + "|")
			elif(ent.type == 'PARAM'):
				print("\t \t "+"|"+" name-->"+ent.name+"\t type-->"+ent.type+"\t mode-->"+ent.parameter.mode+"\t offset-->"+str(ent.parameter.offset)+ "|")
			elif(ent.type == 'SUBPR'):
				if(ent.subprogram.type == 'Procedure'):
					print("\t   \t"+"|"+" name-->"+ent.name+"\t type-->"+ent.type+"\t procedure-type-->"+ent.subprogram.type+"\t startQuad-->"+str(ent.subprogram.startQuad)+"\t frameLength-->"+str(ent.subprogram.frameLength)+ "|")
					print("\tARGUMENTS:")
					for arg in ent.subprogram.argumentList:
						print("\t\t "+"|"+" name-->"+arg.name+"\t type-->"+arg.type+"\t parMode-->"+arg.parMode+ "|")
				elif(ent.subprogram.type == 'Function'):
					print("\t   \t"+"|"+" name-->"+ent.name+"\t type-->"+ent.type+"\t function-type-->"+ent.subprogram.type+"\t startQuad-->"+str(ent.subprogram.startQuad)+"\t frameLength-->"+str(ent.subprogram.frameLength)+ "|")
					print("\tARGUMENTS:")
					for arg in ent.subprogram.argumentList:
						print("\t\t"+"|"+" name-->"+arg.name+"\t type-->"+arg.type+"\t parMode-->"+arg.parMode+ "|")
		scopeA = scopeA.enclosingScope

	print("|-----------------------------------------------------------------------------------------------------------------|")
	
def search_array(a):
	global topScope
	scopeA=topScope
	while scopeA != None:
		for enti in scopeA.entityList:
			if(enti.name == a):
				return (scopeA,enti)
		scopeA=scopeA.enclosingScope
	
	print("In symbol table there is no node with the name " + str(a))
	exit()

				###########################
				#  Assembly (Finall) Code #
				###########################

ascFile = open('ascFile.asm','w')

def gnlvcode(name):
	global topScope
	global ascFile
	ascFile.write('lw $t0, -4($sp)\n')
	(scope_1,entity_1) = search_array(name)
	timesofloop = topScope.nestingLevel - scope_1.nestingLevel
	timesofloop = timesofloop -1

	for i in range(0,timesofloop):
		ascFile.write('lw $t0, -4($t0)\n')
	if(entity_1.type == 'VAR'):
		x = entity_1.variable.offset
	elif(entity_1.type == 'PARAM'):
		x = entity_1.parameter.offset
	ascFile.write('add $t0, $t0 , -%d\n' %(x))

def loadvr(v,r):
	global topScope
	global ascFile

	if v.isdigit():
		ascFile.write('li $t%d , %s\n' %(r,v))
	else:
		(scope_1,entity_1) = search_array(v)           
		if scope_1.nestingLevel==0 and entity_1.type=='TEMP': 
			ascFile.write('lw $t%d,-%d($s0)\n' % (r,entity_1.tempVar.offset))
		elif scope_1.nestingLevel==0 and entity_1.type=='VAR': 
			ascFile.write('lw $t%d,-%d($s0)\n' % (r,entity_1.variable.offset))  
		elif scope_1.nestingLevel == topScope.nestingLevel:
			if entity_1.type=='TEMP': 
				ascFile.write('lw $t%d,-%d($sp)\n' % (r,entity_1.tempVar.offset))
			elif entity_1.type=='VAR':
				ascFile.write('lw $t%d,-%d($sp)\n' % (r,entity_1.variable.offset))
			elif entity_1.type=='PARAM' and entity_1.parameter.mode=='CV':
				ascFile.write('lw $t%d,-%d($sp)\n' % (r,entity_1.parameter.offset))
			elif entity_1.type=='PARAM' and entity_1.parameter.mode=='REF': 
				ascFile.write('lw $t0,-%d($sp)\n' % (entity_1.parameter.offset))
				ascFile.write('lw $t%d,($t0)\n' % (r))
		elif scope_1.nestingLevel < topScope.nestingLevel:
			if entity_1.type=='VAR':
				gnlvcode(v)
				ascFile.write('lw $t%d,($t0)\n' % (r))
			elif entity_1.type=='PARAM' and entity_1.parameter.mode=='CV':
				gnlvcode(v)
				ascFile.write('lw $t%d,($t0)\n' % (r))
			elif entity_1.type=='PARAM' and entity_1.parameter.mode=='REF':
				gnlvcode(v)
				ascFile.write('lw $t0,($t0)\n')
				ascFile.write('lw $t%d,($t0)\n' % (r))

def storerv(r,v):  

	global topScope
	global ascFile

	(scope_1,entity_1)=search_array(v)
	
	if scope_1.nestingLevel==0 and entity_1.type=='TEMP':
		ascFile.write('sw $t%d,-%d($s0)\n' % (r,entity_1.tempVar.offset))
	elif scope_1.nestingLevel==0 and entity_1.type=='VAR':
		ascFile.write('sw $t%d,-%d($s0)\n' % (r,entity_1.variable.offset))
	elif scope_1.nestingLevel == topScope.nestingLevel:	
		if entity_1.type=='TEMP':
			ascFile.write('sw $t%d,-%d($sp)\n' % (r,entity_1.tempVar.offset))
		elif entity_1.type=='VAR':
			ascFile.write('sw $t%d,-%d($sp)\n' % (r,entity_1.variable.offset))
		elif entity_1.type=='PARAM' and entity_1.parameter.mode=='CV':
			ascFile.write('sw $t%d,-%d($sp)\n' % (r,entity_1.parameter.offset))
		elif entity_1.type=='PARAM' and entity_1.parameter.mode=='REF':
			ascFile.write('lw $t0,-%d($sp)\n' %  (entity_1.parameter.offset))
			ascFile.write('sw $t%d,($t0)\n' % (r))
	elif scope_1.nestingLevel < topScope.nestingLevel:
		if entity_1.type=='VAR':
			gnlvcode(v)
			ascFile.write('sw $t%d,($t0)\n' % (r))
		elif entity_1.type=='PARAM' and entity_1.parameter.mode=='CV':
			gnlvcode(v)
			ascFile.write('sw $t%d,($t0)\n' % (r))
		elif entity_1.type=='PARAM' and entity_1.parameter.mode=='REF':
			gnlvcode(v)
			ascFile.write('lw $t0,($t0)\n')
			ascFile.write('sw $t%d,($t0)\n' % (r))


def search_quads(a):
	global allQuads
	begin = a
	while begin>=a:
		if (allQuads[begin][1] == 'call'):  
			return str(allQuads[begin][2]) 
		begin=begin+1



my_turn=-1

def final_asm_file():
	global topScope
	global allQuads
	global my_turn
	global ascFile

	for i in range(len(allQuads)):
		ascFile.write('L%d: \n' % (allQuads[i][0]))
		if (allQuads[i][1] == 'JUMP'): 
			ascFile.write('j L'+str(allQuads[i][4])+'\n')
		elif (allQuads[i][1] == 'out'): 
			ascFile.write('li $v0,1'+'\n') 
			loadvr(allQuads[i][2],1)   
			ascFile.write('move $a0,$t1'+'\n')
			ascFile.write('syscall'+'\n')
		elif (allQuads[i][1] == 'inp'): 
			ascFile.write('li $v0,5'+'\n')
			ascFile.write('syscall'+'\n')
			ascFile.write('move $t1,$v0'+'\n') 
			storerv(1,allQuads[i][2])  
		elif (allQuads[i][1] == 'retv'):  
			loadvr(allQuads[i][2],1)
			ascFile.write('lw $t0,-8($sp)\n')
			ascFile.write('sw $t1,($t0)\n')  
		elif (allQuads[i][1] == 'par'):  
			if my_turn==-1:  
				fname=search_quads(i)  
				(scope_1,entity_1)=search_array(fname)
				ascFile.write('add $fp,$sp,%d\n' % (entity_1.subprogram.frameLength))  
				my_turn=0 
			if (allQuads[i][3] == 'CV'):  
				loadvr(allQuads[i][2],0)
				ascFile.write('sw $t0,-%d($fp)\n' % (12+4*my_turn))
				my_turn=my_turn+1 
			elif (allQuads[i][3] == 'RET'):
				(scope_1,entity_1)=search_array(allQuads[i][2])  
				ascFile.write('add $t0,$sp,-%d\n' % (entity_1.tempVar.offset))
				ascFile.write('sw $t0,-8($fp)\n')
			elif (allQuads[i][3] == 'REF'): 
				(scope_1,entity_1)=search_array(allQuads[i][2])  
				if scope_1.nestingLevel==topScope.nestingLevel: 
					if entity_1.type=='VAR':  
						ascFile.write('add $t0,$sp,-%d\n' % (entity_1.variable.offset))
						ascFile.write('sw $t0,-%d($fp)\n' % (12+4*my_turn))
					elif entity_1.type=='PARAM' and entity_1.parameter.mode=='CV':  
						ascFile.write('add $t0,$sp,-%d\n' % (entity_1.parameter.offset))
						ascFile.write('sw $t0,-%d($fp)\n' % (12+4*my_turn))
					elif entity_1.type=='PARAM' and entity_1.parameter.mode=='REF':  
						ascFile.write('lw $t0,-%d($sp)\n' % (entity_1.parameter.offset))
						ascFile.write('sw $t0,-%d($fp)\n' % (12+4*my_turn))
				elif scope_1.nestingLevel<topScope.nestingLevel:  
					gnlvcode(allQuads[i][2])
					if entity_1.type=='PARAM' and entity_1.parameter.mode=='REF':  
					    ascFile.write('lw $t0,($t0)\n')
					    ascFile.write('sw $t0,-%d($fp)\n' % (12+4*my_turn))
					else:
					    ascFile.write('sw $t0,-%d($fp)\n' % (12+4*my_turn))
				my_turn=my_turn+1
		elif (allQuads[i][1] == 'call'): 
			my_turn=-1 
			(scope_1,entity_1)=search_array(allQuads[i][2])
			if topScope.nestingLevel==entity_1.subprogram.nestingLevel: 
				ascFile.write('lw $t0,-4($sp)\n')
				ascFile.write('sw $t0,-4($fp)\n')
			elif topScope.nestingLevel < entity_1.subprogram.nestingLevel:
				ascFile.write('sw $sp,-4($fp)\n')
			ascFile.write('add $sp,$sp,%d\n' % (entity_1.subprogram.frameLength)) 
			ascFile.write('jal L%d\n' % (entity_1.subprogram.startQuad))          
			ascFile.write('add $sp,$sp,-%d\n' % (entity_1.subprogram.frameLength)) 
		elif ( allQuads[i][1] == 'begin_block' and topScope.nestingLevel!=0):
			ascFile.write('sw $ra,($sp)\n')
		elif ( allQuads[i][1] == 'begin_block' and topScope.nestingLevel==0):  
			ascFile.seek(0, os.SEEK_SET)
			ascFile.write('j L%d\n'% (allQuads[i][0])) 
			ascFile.seek(0, os.SEEK_END)
			ascFile.write('add $sp,$sp,%d\n' % (calculate_offset()))   
			ascFile.write('move $s0,$sp\n')                           
		elif ( allQuads[i][1] == 'end_block' and topScope.nestingLevel!=0):
			ascFile.write('lw $ra,($sp)\n')
			ascFile.write('jr $ra\n')
		elif (allQuads[i][1] == '='): 
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('beq,$t1,$t2,L'+str(allQuads[i][4])+'\n')
		elif (allQuads[i][1] == '<>'): 
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('bne,$t1,$t2,L'+str(allQuads[i][4])+'\n')
		elif (allQuads[i][1] == '>'):
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('bgt,$t1,$t2,L'+str(allQuads[i][4])+'\n')
		elif (allQuads[i][1] == '<'): 
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('blt,$t1,$t2,L'+str(allQuads[i][4])+'\n')
		elif (allQuads[i][1] == '>='):	 
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('bge,$t1,$t2,L'+str(allQuads[i][4])+'\n')
		elif (allQuads[i][1] == '<='): 
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('ble,$t1,$t2,L'+str(allQuads[i][4])+'\n')	
		elif (allQuads[i][1] == ':='): 
			loadvr(allQuads[i][2],1)
			storerv(1,allQuads[i][4])
		elif (allQuads[i][1] == '+'): 
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('add,$t1,$t1,$t2'+'\n')
			storerv(1,allQuads[i][4])
		elif (allQuads[i][1] == '-'):
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('sub,$t1,$t1,$t2'+'\n')
			storerv(1,allQuads[i][4])
		elif (allQuads[i][1] == '*'): 
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('mul,$t1,$t1,$t2'+'\n')
			storerv(1,allQuads[i][4])
		elif (allQuads[i][1] == '/'): 
			loadvr(allQuads[i][2],1)
			loadvr(allQuads[i][3],2)
			ascFile.write('div,$t1,$t1,$t2'+'\n')
			storerv(1,allQuads[i][4])

		################
		#     FILES    #
		################
def cCode(cF):
	global tempList 
	
	if(len(tempList)!=0):
		cF.write("int ")
	for i in range(len(tempList)):
		cF.write(tempList[i])
		if(len(tempList) == i+1):
			cF.write(";\n\n\t")
		else:
			cF.write(",")
	for j in range(len(allQuads)):
		if(allQuads[j][1] == 'begin_block'):
			cF.write("L_"+str(j+1)+":\n\t")
		elif(allQuads[j][1] == "out"): 
			cF.write("L_"+str(j+1)+": "+"printf(\""+allQuads[j][2]+"= %d\", "+allQuads[j][2]+");\n\t")
		elif(allQuads[j][1] == 'halt'):
			cF.write("L_"+str(j+1)+": {}\n\t")
		elif(allQuads[j][1] == "JUMP"):
			cF.write("L_"+str(j+1)+": "+"goto L_"+str(allQuads[j][4])+ ";\n\t")
		elif(allQuads[j][1] == "<"):
			cF.write("L_"+str(j+1)+": "+"if ("+allQuads[j][2]+"<"+allQuads[j][3]+") goto L_"+str(allQuads[j][4])+";\n\t")
		elif(allQuads[j][1] == ">"):
			cF.write("L_"+str(j+1)+": "+"if ("+allQuads[j][2]+">"+allQuads[j][3]+") goto L_"+str(allQuads[j][4])+";\n\t")
		elif(allQuads[j][1] == ">="):
			cF.write("L_"+str(j+1)+": "+"if ("+allQuads[j][2]+">="+allQuads[j][3]+") goto L_"+str(allQuads[j][4])+";\n\t")
		elif(allQuads[j][1] == "<="):
			cF.write("L_"+str(j+1)+": "+"if ("+allQuads[j][2]+"<="+allQuads[j][3]+") goto L_"+str(allQuads[j][4])+";\n\t")
		elif(allQuads[j][1] == "<>"):
			cF.write("L_"+str(j+1)+": "+"if ("+str(allQuads[j][2])+"!="+str(allQuads[j][3])+") goto L_"+str(allQuads[j][4])+";\n\t")
		elif(allQuads[j][1] == "="):
			cF.write("L_"+str(j+1)+": "+"if ("+allQuads[j][2]+"=="+allQuads[j][3]+") goto L_"+str(allQuads[j][4])+";\n\t")
		elif(allQuads[j][1] == ":="):
			cF.write("L_"+str(j+1)+": "+ allQuads[j][4]+"="+allQuads[j][2]+";\n\t")
		elif(allQuads[j][1] == "+"):
			cF.write("L_"+str(j+1)+": "+ allQuads[j][4]+"="+allQuads[j][2]+"+"+allQuads[j][3]+";\n\t")
		elif(allQuads[j][1] == "-"):
			cF.write("L_"+str(j+1)+": "+ allQuads[j][4]+"="+allQuads[j][2]+"-"+allQuads[j][3]+";\n\t")
		elif(allQuads[j][1] == "*"):
			cF.write("L_"+str(j+1)+": "+ allQuads[j][4]+"="+allQuads[j][2]+"*"+allQuads[j][3]+";\n\t")
		elif(allQuads[j][1] == "/"):
			cF.write("L_"+str(j+1)+": "+ allQuads[j][4]+"="+allQuads[j][2]+"/"+allQuads[j][3]+";\n\t")


def intCode(intF):
	'Write allQuads at intFile.int'
	intF.write("Dimitris Mataragkas  AM: 3272  \n ")
	intF.write("Vaggelis Stamatis    AM: 3334  \n")
	intF.write("\n")
	for i in range(len(allQuadsFinal)):
		quad = allQuadsFinal[i]
		intF.write("LINE  ")
		intF.write(str(quad[0]))
		intF.write("-->  ")
		intF.write(str(quad[1]))
		intF.write("  ")
		intF.write(str(quad[2]))
		intF.write("  ")
		intF.write(str(quad[3]))
		intF.write("  ")
		intF.write(str(quad[4]))
		intF.write("\n")

def files():
	'intFile.int & cFile.c'
	intF = open('intFile.int', 'w')
	cFile = open('cFile.c', 'w')
	
	cFile.write("// Dimitris Mataragkas A.M: 3272 \n")
	cFile.write("// Vaggelis Stamatis A.M: 3334 \n")
	cFile.write("int main(){\n\t")
	syntaktikos(cFile)
	
	intCode(intF)
	ascFile.write("# Dimitris Mataragkas A.M : 3272 \n")
	ascFile.write("# Vaggelis Stamatis  A.M : 3334 \n")
	cCode(cFile)
	cFile.write("\n}")
	
	cFile.close()
	intF.close()
	ascFile.close()
files()