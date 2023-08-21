import graphviz

terminal = set()
terminal.add('n')
terminal.add('+')
terminal.add('*')
terminal.add('$')

prod = []
# curNode = 1;

def parse(tokens,grammar,nonTerminal,nodeN = 0,inp = 0):
    # global curNode
    # print("p : ",nonTerminal,tokens)

    if nonTerminal not in grammar:
        raise ValueError(f"Nonterminal '{nonTerminal}' not found in grammar.")

    for production in grammar[nonTerminal]:
        current_tokens = tokens.copy()
        flag = True
        # print("prod : ",production)
        if(production[0]=='$'):
            prod.append([nonTerminal,production,nodeN,inp])
            return current_tokens
        prod.append([nonTerminal,production,nodeN,inp])
        k = len(prod)
        # curNode = curNode+1
        for index,symbol in enumerate(production):
            try:
                if symbol not in terminal:
                    current_tokens = parse(current_tokens,grammar,symbol,k,index)
                elif symbol == current_tokens[0]:
                    if current_tokens[0]!="$":
                        current_tokens.pop(0)  
                    else:
                        return current_tokens
                else:
                    flag = False
                    break
            except ValueError:
                flag = False
                break
        # print("flag : ",nonTerminal,flag)
        if flag:
            token = current_tokens
            # print("return : ",token)
            return token
        else :
            prod.pop();

    raise ValueError(f"Nonterminal '{nonTerminal}' not found in grammar.")

def drawGraph(data):
    mp = dict()

    dot = graphviz.Digraph(comment='Parse Tree')

    dot.node('S')
    curNode = 0

    for index,dat in enumerate(data):
        if index==0:
            mp[0] = 0;
            for val in dat[1]:
                node_label = val
                node_value = curNode
                dot.edge('S',f"{node_label} ({node_value})")
                curNode = curNode+1;

        else:
            mp[index] = curNode
            k = mp[dat[2]-1]+dat[3]
            parNode = dat[0]+" ("+str(k)+")"
            for val in dat[1]:
                dot.edge(parNode,f"{val} ({curNode})")
                curNode =curNode+1



    dot.render('parse_tree_graph', view=True)


def main():
    # Define your context-free grammar as a dictionary of production rules
    grammar = {
        'S': [['n', 'B']],
        'B': [['n','B','A','B'], ['$']],
        'A': [['+'],['*']]
    }

    input_str = input("Enter a string of tokens (e.g., 'aabb'): ")
    tokens = list(input_str)
    tokens.append("$")
    # print("Tokens :",tokens)
    try:
        tokens = parse(tokens, grammar, 'S')
        if len(tokens)==1 and tokens[0]=='$':
            # print(prod)
            drawGraph(prod)
            print("Parsing successful.")
        else:
            print("Parsing failed. Unexpected tokens remaining:", tokens)
    except ValueError as e:
        print("Parsing failed. Error:", e)

if __name__ == "__main__":
    main()
