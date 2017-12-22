using System;
using System.Collections.Generic;
/*
bolster: if pay 2 coin with 3 block then ((gain 1 power with 2 block or gain 2 any resources) and gain 1 heart)
trade: 
produce
gain/move


build
deploy
recruit
upgrade

parse bolster:
    parse if/then
    foreach action (comma block)
        for each option (earch or/and)
            find action (pay, gain)
            find number
            (optional) qualifier, e.g. any, of # kind
            find item
            (optional) find with
                find quantity
                find block
AST of bolster:
    if: (if block)
        (action) pay 2 coin -> 3 block
    then
     and
     => gain 1 heart
     => or
         => gain 1 power -> 2 block
         => gain 2 resources

process TRA()
    grab an action, find action type (pay, gain, custom), get quantity, get type, apply action on player 
    pay: player.type action quantity
    pay: player.coin -= 2
    process if:
        condition returns if user can carry out action
        execut then if condition returns true

 */
namespace HexBDL
{
    class Player{
        public Dictionary<string, int> inventory = new Dictionary<string, int>();
        public Player() {}
    }
    public class ASTNode
    {
        public ASTNode(string name) { action = name; }
        public string action = "";
        public int quantity = 1;
        public string type = "";
        public ASTNode left = null;
        public ASTNode right = null;

        public static void PrintTree(ASTNode node, int i)
        {
            if (node == null)
                return;
            Console.Write(node.action);
            if (node.left != null)
            {
            Console.Write("\t->L" + i + " ");
            PrintTree(node.left, i+1);
            }
            if (node.right == null)
                return;
            string tabs = "\t";
            for(int idx=0; idx < i; idx++)
            {
                tabs += "\t";
            }
            Console.WriteLine("");
            Console.Write(tabs + "->R" + i + " ");
            PrintTree(node.right, i+1);
        }
    }
    //head -> if -> condition
    //           -> then
    //     -> after if

    //parse (a op1 (b op2 c))
    //head -> op1 -> a
    //            -> op2 -> b
    //                   -> c
    
    class Parser
    {
        Dictionary<string, ASTNode> ruleList = new Dictionary<string,ASTNode>();
        bool simple = false;
        string ruleBolster = "bolster: pay 2 coin"; 
        //string ruleBolster = "bolster: if pay 2 coin with 3 block then ((gain 1 power with 2 block or gain 2 any resources) and gain 1 heart) endif";
        //rule ->L if ->L condition
        //            ->R ThenElse ->L then expression
        //                         ->R else expression
        //   ->R next expression
        //condition: can pay 2 coin ->L with 3 block
        //then:      and ->L gain 1 heart
        //               ->R or ->L gain 1 power ->L with 2 block
        //                      ->R gain 2 any resource
        string ruleSimple = "a + (b - c + (d * f + (g / h )))";
        List<string> opList = new List<string> {"+", "-", "/", "*", "and", "or"};
        List<string> verbList = new List<string> {"pay", "gain", "block"};

        ASTNode head = new ASTNode("head"); //empty?
        ASTNode node = null;
        public Parser()
        {
            node = head;
        }
        public void FormatInput(ref string s)
        {  
            Console.WriteLine("s: " + s);
            var prevIsParan = false;
            //add spaces before and after parens
            for( var i = s.Length-1; i > 0; i-- )
            {
                var curChar = s[i];
                if (prevIsParan && curChar != ' ')
                {
                    s = s.Insert(i+1, " ");
                }
                prevIsParan = false;
                if (curChar == '(' ||
                    curChar == ')')
                {
                    prevIsParan = true;
                    s = s.Insert(i+1, " ");
                }
            }
            s = s.Trim();
            //delete duplicate spaces
            var prevIsSpace = false;
            for( var i = s.Length-1; i > 0; i-- )
            {
                var curChar = s[i];
                if (prevIsSpace && curChar == ' ')
                {
                    s = s.Remove(i, 1);
                }
                prevIsSpace = false;
                if (curChar == ' ')
                {
                    prevIsSpace = true;
                }
            }
            Console.WriteLine("after format s: " + s);
        }
        public void Parse() {
            char[] del = {' '};
            //foreach(var token in tokens)
            Console.WriteLine("parsing parenthesises");
            if (simple)
            {
                int ii=0;
                FormatInput(ref ruleSimple);
                Console.WriteLine(ruleSimple);
                var tokens_ = ruleSimple.Split(del);
                List<string> tokens = new List<string>(tokens_);
                node = ParseExpressionSY(tokens, ref ii);
            } else {
                FormatInput(ref ruleBolster);
                var tokens_ = ruleBolster.Split(del);
                List<string> tokens = new List<string>(tokens_);
                Console.Write("raw tokens: ");
                foreach(var token in tokens) Console.Write(token + ", ");
                Console.WriteLine("");
                var e = tokens.GetEnumerator();
                node = ParseRule(ref e);
            }

                ASTNode.PrintTree(node, 0);
                Console.WriteLine("");
            
            Console.WriteLine("finished parsing parenthesises");
        }
        ASTNode ParseRule(ref List<string>.Enumerator e)
        {
            var ruleName = e.Current;
            e.MoveNext(); //move past rule name
            var ruleNode = ParseExpression(ref e);
            ruleList.Add(ruleName, ruleNode);
            return ruleNode;
        }
        //expects enumerator pointing to token after if
        ASTNode ParseIfThen(ref List<string>.Enumerator e)
        {
            var ifNode = new ASTNode("if");
            var thenElseNode = new ASTNode("thenElse");
            ifNode.left = ParseExpression(ref e , "then");
            ifNode.right = thenElseNode;
            thenElseNode.left = ParseExpression(ref e, "else");
            thenElseNode.right = ParseExpression(ref e, "endif");
            return ifNode;
        }
        //this function needs a lot of work... needs to chain and call it self or something...
        //parse this, then left, then right
        //parse a, parse a->left by default
        //if encounter or, return or, put a into or->left, find or->right = next
        //TODO - support rule with no operators (and/or/+/- etc)
        //returns with e pointing to next token
        ASTNode ParseExpression(ref List<string>.Enumerator e, string endMarker="eol")
        {
            Stack<ASTNode> outputs = new Stack<ASTNode>();
            Stack<ASTNode> ops = new Stack<ASTNode>();

            ASTNode localRoot = null;
            while( e.MoveNext() && e.Current != endMarker)
            {
                var token = e.Current;
                Console.WriteLine(token + ", ");
                continue;
                var localNode = new ASTNode(token);
                //ParseExpression(ref node, tokens, ref i);
                if (token == "if")
                {
                    e.MoveNext();
                    var subIfNode = ParseIfThen(ref e);
                } else 
                if (IsParen(token))
                {
                    e.MoveNext();
                    localNode = ParseExpression(ref e, ")");
                } else
                if (opList.Contains(token)) //really, any operator
                {
                    localRoot = localNode;
                } else
                {
                    if (verbList.Contains(token))
                    {
                        localNode = ParseVerb(ref e);
                    }
                    outputs.Push(localNode);
                }
                //else if isOperand, parse operand...
                Console.WriteLine(token);
                if (localRoot == null)
                    localRoot = localNode;
            }
            e.MoveNext();
            //debug
            Console.WriteLine("outputs: ");
            foreach(var node in outputs) Console.Write(node.action+ ", ");
            Console.WriteLine("\nops: ");
            foreach(var node in ops) Console.Write(node.action+", ");
            return localRoot;
        }
        ASTNode ParseVerb(ref List<string>.Enumerator e)
        {
            var verb = new ASTNode(e.Current);
            e.MoveNext();
            if (!Int32.TryParse(e.Current, out verb.quantity))
            {
                Console.WriteLine("invalid quantity in rule encountered while parsing verb: " + verb.action);
                return null;
            }
            e.MoveNext();
            //TODO check if extenuating type (any, of 1 kind)
            verb.type = e.Current;
            return verb;
        }
        Stack<List<string>> parenStack = new Stack<List<string>>();
        //
        void ParseParen(List<string> tokens, ref int i)
        {
            if (parenStack.Count == 0)
                parenStack.Push(new List<string>());
            if (tokens[i] == "(")
            {
                //push stack
                Console.WriteLine("got (, pushing");
                parenStack.Push(new List<string>());
            } else 
            if (tokens[i] == ")")
            {
                Console.WriteLine("got ), popping");
                parenStack.Pop();
            } else {
                Console.WriteLine(tokens[i]);
                var list = parenStack.Peek();
                list.Add(tokens[i]);
            }
        }

        //a + b - c
        //- -> c
        //  -> + -> a
        //       -> b
        //a + ( b - c )
        //+ -> a
        //  -> - -> b
        //       -> c

        //Shunt yard algorithm: packs strings into output/ops and then construct AST from that
        ASTNode ParseExpressionSY(List<string>tokens, ref int i)
        {
            Stack<ASTNode> outputs = new Stack<ASTNode>();
            Stack<ASTNode> ops = new Stack<ASTNode>();
            //pack tokens into output/ops stack
            for( ; i < tokens.Count; i++)
            {
                var token = tokens[i];
                var newNode = new ASTNode(token);
                if (IsParen(token))
                {
                    if (token == ")")
                    {
                        i++;
                        break; //stop packing; assemble AST if any, go up 1 level
                    } else 
                    if (token == "(")
                    {
                        //go 1 level down!
                        i++;
                       newNode = ParseExpressionSY(tokens, ref i);
                       outputs.Push(newNode);
                    } else {
                        Console.WriteLine("ERROR!");
                    }
                } else
                if (IsOperator(token))
                {
                    ops.Push(newNode);
                } else 
                {
                    outputs.Push(newNode);
                }
            }
            Console.WriteLine("outputs: ");
            foreach(var node in outputs) Console.Write(node.action+ ", ");
            Console.WriteLine("\nops: ");
            foreach(var node in ops) Console.Write(node.action+", ");
            Console.WriteLine("");
            //assemble AST
            var root = ops.Peek();
            ASTNode prevNode = null;
            while (ops.Count > 0)
            {
                var node = ops.Pop();
                if (prevNode != null)
                    prevNode.left = node;
                var os = " ";
                foreach (var n in outputs)
                    os += n.action + ", ";
                Console.WriteLine("curr Node: " + node.action + os);
                node.right = outputs.Pop();
                if (ops.Count == 0 && outputs.Count > 0)
                    node.left = outputs.Pop();
                prevNode = node;
            }
            return root;
        }
        //ASTNode AssembleAST()
        bool IsOperator(string token)
        {
            return (token == "+")
                || token == "-" 
                || token == "*"
                || token == "/"
                || token == "if"
                || token == "thenElse"
                //check if token in operator dictionary (user extendable)
                ;
        }
        bool IsParen(string token)
        {
            return (token == "(")
                || token == ")"
                ;
        }
        void ParseExpression(ref ASTNode node, List<string>tokens, ref int i)
        {
            //ignore parens for now
            //ignore operator at beginning of expressions for now
            var lhNode = new ASTNode(tokens[i]);
            i++;
            if (tokens.Count <= i)
            {
                node.right = lhNode;
                return;
            }
            var op = new ASTNode(tokens[i]);
            node.right = op;
            op.left = lhNode;
            i++; 
            ParseExpression(ref op, tokens, ref i);
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            Parser parser = new Parser();
            parser.Parse();
            Console.WriteLine("Hello World!");
        }
    }
}
