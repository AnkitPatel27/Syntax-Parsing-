import graphviz

terminal = set()
prod = []

def parse(tokens,grammar,nonTerminal,nodeN = 0,inp = 0):

    if nonTerminal not in grammar:
        raise ValueError(f"Nonterminal '{nonTerminal}' not found in grammar.")

    for production in grammar[nonTerminal]:
        current_tokens = tokens.copy()
        flag = True
        if(production[0]=='$'):
            prod.append([nonTerminal,production,nodeN,inp])
            return current_tokens
        prod.append([nonTerminal,production,nodeN,inp])
        k = len(prod)
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
        if flag:
            token = current_tokens
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


def get_terminal_symbols():
    
    terminal_input = input("Enter terminal symbols separated by space: ")
    return set(terminal_input.split())

def get_non_terminal_symbols():
    non_terminal_input = input("Enter non-terminal symbols separated by space: ")
    return set(non_terminal_input.split())

def get_production_rules(non_terminals):
    grammar = {}
    for non_terminal in non_terminals:
        productions_input = input(f"Enter production rules for {non_terminal} (separated by '|'): ")
        productions = [production.split() for production in productions_input.split('|')]
        grammar[non_terminal] = productions
    return grammar


def main():
    global terminal
    # Define your context-free grammar as a dictionary of production rules
    terminal = get_terminal_symbols()
    non_terminal_symbols = get_non_terminal_symbols()
    grammar = get_production_rules(non_terminal_symbols)


    while(int(input("Enter the string to Check (1/0)"))):
        global prod
        prod = []
        input_str = input("Enter a string of tokens (e.g., 'aabb'): ")
        tokens = list(input_str)
        tokens.append("$")
        try:
            tokens = parse(tokens, grammar, 'S')
            if len(tokens)==1 and tokens[0]=='$':
                print(prod)
                drawGraph(prod)
                print("Parsing successful.")
            else:
                print("Parsing failed. Unexpected tokens remaining:", tokens)
        except ValueError as e:
            print("Parsing failed. Error:", e)

if __name__ == "__main__":
    main()
