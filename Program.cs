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
            i++;
            PrintTree(node.left, i);
            }
            if (node.right == null)
                return;
            string tabs = "";
            for(int idx=0; idx < i; idx++)
            {
                tabs += "\t";
            }
            Console.WriteLine("");
            Console.Write(tabs + "->R" + i + " ");
            PrintTree(node.right, i);
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
        //string rule = "bolster: if pay 2 coin with 3 block then ( ( gain 1 power with 2 block or gain 2 any resources ) and gain 1 heart )";
        string rule = "a + b - c";

        ASTNode head = new ASTNode("head"); //empty?
        ASTNode node = null;
        public Parser()
        {
            node = head;
        }
        public void Parse() {
            char[] del = {':', ' '};
            var tokens_ = rule.Split(del);
            List<string> tokens = new List<string>(tokens_);
            //foreach(var token in tokens)
            Console.WriteLine("parsing parenthesises");
            int ii=0;
                var node = ParseExpressionSY(tokens, ref ii);
                ASTNode.PrintTree(node, 0);
                Console.WriteLine("");
            for (int i=0; i<tokens.Count; i++)
            {
                //ParseExpression(ref node, tokens, ref i);
                continue;
                ParseParen(tokens, ref i);
                continue;
                if (node == null)
                    node = new ASTNode("temp");
                node.action = tokens[i];
                if (tokens[i] == "if")
                {
                    //node.left = ParseCondition(tokens, ref i);
                    //node.right = ParseThen(tokens, ref i);
                } else 
                if (tokens[i] == "then")
                {
                    var prev = node;
                    node = new ASTNode("then");
                    prev.right = node;
                } else 
                if (tokens[i] == "pay")
                {

                }
                Console.WriteLine(tokens[i]);
            }
            Console.WriteLine("finished parsing parenthesises");
        }
        void ParseCondition(List<string> tokens, ref int i)
        {
            //basic parse conditions
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
            for( int ii = i; ii < tokens.Count; ii++)
            {
                var token = tokens[ii];
                if (IsOperator(token))
                {
                    ops.Push(new ASTNode(token));
                } else 
                if (IsParen(token))
                {
                    //if (tokens[i] == ")")
                        //return root
                    //create a new set ouf outputs/ops?
                    //outputs.Add(ParseExpressionSY(tokens, ref i));
                } else
                {
                    outputs.Push(new ASTNode(token));
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
                node.right = outputs.Pop();
                prevNode = node;
            }
            return root;
        }
        //ASTNode AssembleAST()
        bool IsOperator(string token)
        {
            return (token == "+")
                || token == "-"
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
