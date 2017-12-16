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
        bool simple = false;
        string ruleBolster = "bolster: if pay 2 coin with 3 block then ((gain 1 power with 2 block or gain 2 any resources) and gain 1 heart)";
        //rule ->L if ->L condition
        //            ->R ThenElse ->L then expression
        //                         ->R else expression
        //   ->R next expression
        //condition: can pay 2 coin ->L with 3 block
        //then:      and ->L gain 1 heart
        //               ->R or ->L gain 1 power ->L with 2 block
        //                      ->R gain 2 any resource
        string ruleSimple = "a + (b - c + (d * f + (g / h )))";

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
            char[] del = {':', ' '};
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
                var e = tokens.GetEnumerator();
                node = ParseRule(ref e);
            }

                ASTNode.PrintTree(node, 0);
                Console.WriteLine("");
            
            Console.WriteLine("finished parsing parenthesises");
        }
        ASTNode ParseRule(ref List<string>.Enumerator e)
        {
            Stack<ASTNode> outputs = new Stack<ASTNode>();
            var ruleNode = new ASTNode(e.Current);
            //pack into operands and outputs
            while (e.MoveNext())
            {
                if (e.Current == "if")
                {
                    outputs.Push(ParseIfThen(ref e));
                } else
                {

                }
            }
            return ruleNode;
        }
        //expects enumerator pointing to token after if
        ASTNode ParseIfThen(ref List<string>.Enumerator e)
        {
            var ifNode = new ASTNode("if");
            var thenElseNode = new ASTNode("thenElse");
            ifNode.right = thenElseNode;
            //basic parse conditions
            //parse then
            //parse else
            while( e.MoveNext())
            {
                Console.WriteLine(e.Current + ", ");
                continue;
                //ParseExpression(ref node, tokens, ref i);
                if (node == null)
                    node = new ASTNode("temp");
                node.action = e.Current;
                if (e.Current == "if")
                {
                    e.MoveNext();
                    var subIfNode = ParseIfThen(ref e);
                    //node.left = ParseCondition(tokens, ref i);
                    //node.right = ParseThen(tokens, ref i);
                } else 
                if (e.Current == "then")
                {
                    var prev = node;
                    node = new ASTNode("then");
                    prev.right = node;
                } else 
                if (e.Current == "pay")
                {

                }
                Console.WriteLine(e.Current);
            }
            return ifNode;
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
