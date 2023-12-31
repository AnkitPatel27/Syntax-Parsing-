from collections import OrderedDict
import copy

class Grammar:
    def __init__(self):
        self.terminals = set()
        self.non_terminals = set()
        self.productions = {}

    def add_terminal(self, terminal):
        self.terminals.add(terminal)

    def add_non_terminal(self, non_terminal):
        self.non_terminals.add(non_terminal)

    def add_production(self, non_terminal, production):
        if non_terminal not in self.productions:
            self.productions[non_terminal] = []
        self.productions[non_terminal].extend(production)

    def display_grammar(self):
        file = open("GrammarLL.txt","w")
        lines = []
        for nt, prods in self.productions.items():
            s = f"{nt} -> "
            print(nt, "->", end=" ")
            productions_str = []
            for prod in prods:
                while(type(prod[0])==list):
                    prod = prod[0]
                if prod == ['']:
                    productions_str.append('ε')
                else:
                    productions_str.append(' '.join(str(item) for item in prod))
            print(' | '.join(productions_str))
            s += ' | '.join(productions_str)
            s += '\n'
            lines.append(s)
        file.writelines(lines)
        file.close()
            


 

    def find_index(self, target):
        for index, value in enumerate(list(OrderedDict.fromkeys(self.non_terminals))):
            # print(value,target)
            if value == target:
                return index
        return -1 


    def generate_strings(self,non_terminal, production_rules, replacement_rules):
        # print("Rules : ",non_terminal,production_rules,replacement_rules)
        generated_strings = []
        
        for rule in replacement_rules:
            # print("Rule : ",rule)
            if(rule[0]==non_terminal):
                for prod in production_rules:
                    # print(prod,rule)
                    newString = prod+rule[1:]   
                    generated_strings.append(newString)
            else:
                generated_strings.append(rule)
        
        # print("Gen : ",generated_strings)
        return generated_strings


    def dfs(self,node,parent,vis,par,indArray,lastNode,nter):
        par[node] = parent
        vis[node] = 1
        # nter = list(OrderedDict.fromkeys(self.non_terminals))
        # print("DFS : ",node,parent,nter[node],self.productions[nter[node]])
        # print(nter[node])
        for index, nxt in enumerate(self.productions[nter[node]]):
            # print("nxr",nxt)
            indArray[node] = index
            if len(nxt[0]):
                ind = self.find_index(nxt[0])
                # print("Char :" ,nxt[0],ind)
                if ind!=node and ind!=-1 and par[ind]==-1:
                    ans = self.dfs(ind,node,vis,par,indArray,lastNode,nter)
                    if ans!=-1:
                        return ans
                if ind!=node and ind!=-1 and vis[ind]==1 and par[ind]!=-1:
                    # print("Answer : ",node,ind)
                    lastNode[0] = node;
                    return ind
                indArray[node] = -1

        vis[node] = 0
        return -1
    

    def find_indirect_left_recursion(self):
        vis = [0]*len(self.non_terminals)
        par = [-1]*len(self.non_terminals)
        nter = list(OrderedDict.fromkeys(self.non_terminals))

        indArray = [-1]*len(self.non_terminals)
        lastNode = [-1]
        ans =-1
        for index, value in enumerate(list(OrderedDict.fromkeys(self.non_terminals))):
            if par[index]==-1:
                ans = self.dfs(index,index,vis,par,indArray,lastNode,nter)
                if ans!=-1:
                    break
        
        if(ans==-1):
            return False

        node = lastNode[0]
        replacement_rule = [self.productions[nter[node]][indArray[node]].copy()]
        # print("Rule ; ",replacement_rule)
        self.productions[nter[node]].pop(indArray[node])
        travel = []
        while(node!=ans):
            travel.append(node)
            node = par[node]
        travel.append(node)
        travel =  travel[::-1]
        travel.pop()
        for node in travel:
            temp = self.generate_strings(nter[node],self.productions[nter[node]],replacement_rule)
            replacement_rule = temp
            node = par[node]

        temp = self.generate_strings(nter[node],self.productions[nter[node]],replacement_rule)
        replacement_rule = temp
        # print("replace rule",replacement_rule)
        node = lastNode[0]
        # print(self.productions[nter[node]])  
        temp = set()
        
        # replacement_rule = list(set(replacement_rule))
        replacement_rule = [l for i,l in enumerate(replacement_rule ) if l not in replacement_rule [i+1:]]

        # for val in list(set(replacement_rule)):
        #     temp.add(val)

        # for val in self.productions[nter[node]]:
        #     temp.add(val[0])

        self.productions[nter[node]] = []
        self.productions[nter[node]] = replacement_rule

        

        return True
        
    def find_unique_character(self,list1, list2,k):
        return k+"'"

    def remove_left_recursion(self):
        new_production = dict();
        ret = False
        for node,prods in self.productions.items():
            flag = False
            for val in prods:
                # print(val[0])
                if len(val[0])>0 and val[0]==node:
                    flag = True
                    break
            
            if flag:
                ret = True
                beta = []
                alpha = []
                for val in prods:
                    if len(val[0])>0 and val[0]!=node:
                        beta.append(val)
                    elif len(val[0])>0 :
                        alpha.append(val[1:])
                tempNodeProd = []

                # print("beta : ",beta)
                # print("alpha : ",alpha)
                newNode = self.find_unique_character(list(self.non_terminals),list(self.terminals),node)
                self.add_non_terminal(newNode)
                if len(beta)==0:
                    tempNodeProd = [[newNode]]
                else:
                    for val in beta:
                        tempNodeProd.append(val+[newNode])
                
                nodePrimeProd = [[""]]
                for val in alpha:
                    nodePrimeProd.append(val+[newNode])
                
                # print(tempNodeProd,nodePrimeProd)
                new_production[node] = tempNodeProd
                # self.productions[newNode].extend(nodePrimeProd)
                new_production[newNode] = nodePrimeProd
            else :
                new_production[node]=prods
        
        # print(new_production)
        self.productions = new_production
        return ret

    def longest_common_prefix(self,str1,str2):
        # print("string : ",str1,str2)
        common_prefix = []
        min_length = min(len(str1), len(str2))
        for i in range(min_length):
            if str1[i] == str2[i]:
                common_prefix.append(str1[i])
            else:
                break
        
        return common_prefix
    
    def count_frequency(self,numbers, target):
        count = 0
        for num in numbers:
            if num == target:
                count += 1
        return count

    def remove_Left_factoring(self):
        newProduction = dict()
        ret = False
        for node,prods in self.productions.items():
            # commonProd = copy.deepcopy(prods)
            # print("prod")
            index = [0]*len(prods)
            prefixDict = dict()
            for ik,prod in enumerate(prods):
                if index[ik] == 0:
                    index[ik] = ik+1
                    # print("prod :",prod)
                    comStr = prod
                    for i,p in enumerate(prods):
                        if index[i]==0:
                            str = self.longest_common_prefix(comStr,p)
                            if len(str):
                                index[i] = ik+1;
                                comStr = str
                            
                    prefixDict[ik+1] = comStr

            # print("Comstr",prefixDict)

            flag = False

            for val in index:
                if val!=0:
                    count = self.count_frequency(index,val)
                    if count>1:
                        flag=True
                        break
            # print(index)
            if flag==False:
                newProduction[node] = prods
            else:
                ret = True
                done = set()
                oldProd = []
                for val in index:
                    if val!=0:
                        count = self.count_frequency(index,val)
                        if count>1 and val not in done:
                            newProd = []
                            done.add(val)
                            comStr = prefixDict[val]
                            # print("Comstr false : ",comStr)
                            # newProd.append([comStr])
                            
                            for i,v in enumerate(index):
                                if v==val:
                                    done.add(v)
                                    if len(prods[i][len(comStr):]):
                                        newProd.append(prods[i][len(comStr):]) 
                                    else:
                                        newProd.append([''])
                                    # print("NewProd : ",newProd)
                            
                            newNode = self.find_unique_character(list(self.terminals),list(self.non_terminals),node)
                            self.non_terminals.add(newNode)
                            newProduction[newNode] = newProd;
                            oldProd.append([comStr+[newNode]])
                            # print("oldProd: ",oldProd)
                        elif val not in done:
                            oldProd.append([prods[val-1][0]])
                        
                    # print("app opldProd : ",node,oldProd)    

                newProduction[node] = oldProd
        self.productions = newProduction
        # print(self.productions)
        return ret

def main():
    grammar = Grammar()
    with open("input.txt",'r') as file:
        inputs = file.readlines()
        terminals_input = inputs[1]
        non_terminals_input = inputs[0]
        production_rules = inputs[2:]
    # terminals_input = input("Enter terminal symbols separated by spaces: ")
    # non_terminals_input = input("Enter non-terminal symbols separated by spaces: ")
    # non_terminals_input = 'S'
    
    terminals = terminals_input.split()
    non_terminals = non_terminals_input.split()

    for terminal in terminals:
        grammar.add_terminal(terminal)

    for non_terminal in non_terminals:
        grammar.add_non_terminal(non_terminal)

    # Take input for number of production rules
    # num_productions = int(input("Enter the number of production rules: "))
    # num_productions = 19

    # Take input for each production rule
    # with open("pro_rule.txt",'r') as file:
    #     production_rules = file.readlines();

    num_productions = len(production_rules)
    



    for rule in production_rules:
        production_input = rule
        non_terminal, productions = production_input.split("->")
        non_terminal = non_terminal.strip()
        # production_list = [prod.strip().split() for prod in productions.split('|')]
        production_list = [production.split() for production in productions.split('|')]
        try:
            for i in range(len(production_list)):
                if production_list[i] == ['ε']:
                    production_list[i] = ['']

        except:
            None
        # print(production_list)
        grammar.add_production(non_terminal, production_list)

    # print("\nGrammar:")
    print(grammar.non_terminals)
    print(grammar.terminals)
    print(grammar.productions)
    # grammar.display_grammar();
    while(1):
        flag = True
        while(grammar.find_indirect_left_recursion()):
            flag = False
        
        while(grammar.remove_left_recursion()):
            flag = False
        
        if(flag):
            break


    print("\n\n ********* Left Recursion *********")
    # grammar.display_grammar()
    
    print("\n\n ********* Left Factored *********")

    while(grammar.remove_Left_factoring()):
        None
    
    # print(grammar.non_terminals)
    with open("new_non_terminals.txt",'w') as file:
        file.write(' '.join(grammar.non_terminals))
    grammar.display_grammar()
    exit()


if __name__ == "__main__":
    main()

# write a regex for accepting numbers
# + − ∗ / = < > ( ) { } := ;  and else end ic id if int do fc float not or print prog scan str then while
# AE BE D DL E F ES IOS IS NE P PE RE S SL T TY VL WS