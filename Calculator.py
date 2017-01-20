'''

Calculator Class
@ Developer Jedsadakorn Jirapermpoonsap 5801012630041

'''
class calculator:
    def __init__(self,equation):
        self.equation = equation        # keep equation text
        self.example = []				# keep convert data from method numcheck
        self.numbracket = 0             # keep number of Bracket to check the equation 
        self.mainstack = []             # stack all data from text
        self.tempstack = []             # stack sub-data from text for calculate the result
     
    def calculate(self):
        self.numcheck(self.equation)    # method that check the the string and convert into negative or decimal value
        if ( self.numbracket%2 == 0 ):  # if the number of bracket is even ( have a pair of bracket )
            self.get_data()				# method that get data from self.example list by order of operation
            self.match()                # call the method that match the number and operator for calculate

            print ("Answer is " ,self.tempstack.pop())   # after calculate complete display result on screen
        else:
            print ("Equation Error. Please Try again")   # show error if the number of bracket is odd that means some bracket doesn't have a pair   
          
    # method for change string data to list and convert data to negative or decimal number
    def numcheck(self, text):
        char = ""       # empty string
        i = 0           # index
        operator = ["+","*","x","/"]  	# list of operator
        while i < (len(text)):
            if ((text[i] == "-" and i == 0) or 						# if found "-" in front of string
            	(text[i] == "-" and text[i-1] == "(") or 			# if found "-" and the front is "("
            	(text[i] == "-" and text[i-1] in operator)):        # if found "-" and the front is operator
                char += text[i]									    # add "-" in string

            elif (text[i].isdigit()):								# if found digit		
                char += text[i]										# add digit in string
                for j in range (i+1, len(text)):
                    if(text[j].isdigit() or text[j] == "."):		# if found next digit or "."
                       char += text[j]								# add the next digit or "." in string
                       i += 1
                    else:											# if not found other digit break out the loop
                        break
                self.example.append(float(char))                    # add string data to list
                char = ""											# make empty string to get next data
            else:
                self.example.append(text[i])						# add other data to the list
                if (text[i] == "(" or text[i] == ")"):				# if found "(" or ")"
                	self.numbracket = self.numbracket + 1			# count number of the bracket
            i += 1
      
    # method get and adjust data from self.example list by order of operation           
    def get_data(self):
        for i in range (len(self.example)):
            if (self.example[i] == "("):          								# if found "("      
                self.tempstack.append(self.example[i])						    # add "(" into tempstack
 
            elif (isinstance(self.example[i], (float))):						# if found number            
                self.mainstack.append(self.example[i])							# add number into mainstack

            elif (self.example[i] == "+" or self.example[i] == "-" or           # if found operator
                  self.example[i] == "*" or self.example[i] == "x" or
                  self.example[i] == "/"):
                self.tempstack.append(self.example[i])                          # add operator into mainstack
                
                if ( len(self.tempstack) > 1 ):                                 # if tempstack have more than 1 element
                    self.order_check()											# call method that adjust the operator by order of operation
            
            elif (self.example[i] == ")"):										# if found ")"
                self.order_bracket()											# call method that adjust the operator in bracket
                
        while (len(self.tempstack) > 0):										# add the rest of data in tempstack to mainstack
            self.mainstack.append(self.tempstack.pop())
            
    # method for adjust operator by order of operation      
    def order_check(self):
        opt_index = len(self.tempstack)      				# operator index
        for i in range (opt_index-1, opt_index-2, -1):

            if ((self.tempstack[opt_index-1] == "+" or self.tempstack[opt_index-1] == "-") and 	# if plus (+) or minus (-) position are after multiple (*,x) or divide (/) 
            	(self.tempstack[opt_index-2] == "/" or self.tempstack[opt_index-2] == "*" or self.tempstack[opt_index-2] == "x")):
                    self.mainstack.append(self.tempstack.pop(opt_index-2))				# move multiple or divide from tempstack to mainstack
                    
            elif ((self.tempstack[opt_index-2] == "*" or self.tempstack[opt_index-2] == "x") and # if multiple position is before divide
            	(self.tempstack[opt_index-1] == "/")):
                self.mainstack.append(self.tempstack.pop(opt_index-2))				    # move multiple from tempstack to mainstack

    # method for adjust the operator in bracket
    def order_bracket(self):
        while (self.tempstack[len(self.tempstack)-1] != "("):		# if the last operator before ")" isn't "("
            self.mainstack.append(self.tempstack.pop())   			# move operator from tempstack to mainstack
        self.tempstack.pop()										# if found "(" pop out from list

    # method that match the number and operator for calculate    
    def match(self):
        self.mainstack.reverse()      # reverse list

        # while mainstack is not empty
        while (len(self.mainstack) > 0):

            while (isinstance(self.mainstack[len(self.mainstack)-1], (float))):     # while the last element of mainstack is number             
                self.tempstack.append(self.mainstack.pop(len(self.mainstack)-1))	# move number to tempstack
                if (len(self.mainstack) == 0 and len(self.tempstack) == 1):			# if mainstack is empty and tempstack has 1 element break the loop
                  break 
            if (len(self.tempstack) > 2):		# if tempstack has more than 2 element
                    self.rematch()				# call the method that rearrange data to calculate
            elif (len(self.mainstack) == 0):    # if mainstack is empty break the method
               break
            else:
                self.split()                    # if found operator call method that split data for calculate
     
    # method for rearrange data to calculate
    def rematch(self):
        backup = [] 								# empty list
        self.tempstack.reverse()					# reverse data position in list
        while (len(self.tempstack) > 2):
            backup.append(self.tempstack.pop()) 	# move unused data to backup 
        self.split()								# call method to split data out off list
        backup.append(self.tempstack.pop())			# move calculated data to backup
        backup.reverse()							# reverse backup list
        while (len(backup) > 0):
            self.tempstack.append(backup.pop())		# move data from backup to tempstack again

    # method for split 2 number and 1 operator from each list    
    def split(self):
        a = float(self.tempstack.pop())				# keep 2 numbers and 1 operator to each variable
        b = float(self.tempstack.pop())
        o = self.mainstack.pop()
        if (a < 0.0 and o == "-"):					# if variable a is negative or opreator is minus
            self.process(a,b,o)						# call method that calculate the data
        elif ((a > b) and (b > 0) and (o != "/")):  # if value of variable a > b and operator isn't divide
            self.process(a,b,o)  					# call method that calculate the data
        else:
        	self.process(b,a,o) 					# in other case switch variable data and call method that calculate the data
        
    # method for solve the data that recieve from split method
    def process(self, num1, num2, opr):
        if (opr == "+"):
            self.tempstack.append(num1 + num2)
        elif (opr == "-" ):
            self.tempstack.append(num1 - num2)
        elif (opr == "*" or opr == "x"):
            self.tempstack.append(num1 * num2)
        elif (opr == "/"):
            self.tempstack.append(num1 / num2)
                
text = calculator("(10*5)*(5+5)")     # enter the equation
text.calculate()                                 
