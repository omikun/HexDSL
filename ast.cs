using System.IO;
using System;
using System.Collections.Generic;
using System.Collections;

class Player
{
    public Dictionary<string, int> inventory = new Dictionary<string, int>();
    public Player() {}
}
//example:
//bolster: pay 1 coin, gain 2 powers
//trade: pay 1 coin, gain 2 resources
//trade: pay 1 coin, gain 2 resource of one kind
class AST
{
    Grammar grammar = new Grammar();
    //converts List<tokens> into an AST
    public void Execute(ref string[] commands, ref Player player, Dictionary<string, string>nouns)
    {
        //check if multiple statements
        var tokens = new List<string>(commands);
        int commandNum = 1;
            int numSelected = 0;
        if (tokens.Contains("or") )
        {
            //ask user which one to do?
            //assuming each statement is 3 tokens
            Console.WriteLine("Select an option: ");
            string option = "1. ";
            int number = 1;
            foreach(var token in commands)
            {
                if (token != "or")
                {
                    option += token + " ";
                } else {
                    number++;
                    Console.WriteLine(option);
                    option = number.ToString() + ". ";
                }
            }
            while (numSelected <= 0 || numSelected > number)
            {
                Console.WriteLine(option);
                Console.Write("> ");
                var commandInput = Console.ReadLine();
                numSelected = Convert.ToInt32(commandInput);
            }
            commandNum = numSelected;
        }

        int offset = (numSelected - 1) * 4;
        if (numSelected == 0) offset = 0;
        Console.WriteLine("num: " + numSelected + " offset: " + offset + " token: " + commands[offset+1]);
        var amount = Convert.ToInt32(commands[offset+1]);
        var kind = commands[offset+2];
        if (nouns.ContainsKey(kind))
        {
            if(nouns[kind] != "void")
            {
                char[] del = {' ', ','};
                var kindsArray = nouns[kind].Split(del, StringSplitOptions.RemoveEmptyEntries);
                var kinds = new List<string>(kindsArray);
                if (kinds.Count > 1)
                {
                    //ask user to select one
                    kind = grammar.MultiKind(ref kinds);
                } else 
                if (kinds.Count == 1)
                {
                    kind = kinds[0];
                } else 
                {
                    Console.WriteLine("Unrecognized kind!?");
                }
            }
        } else {
            Console.WriteLine("Invalid kind!");
            return;
        }
        var inv = player.inventory[kind];
        if (commands[offset] == "pay")
        {
            player.inventory[kind] = inv - amount;
        } else if (commands[offset] == "gain")
        {
            player.inventory[kind] = inv + amount;
        }
    }
    public AST() {}
}
class NProgram
{
    static void NMain()
    {
        Player player = new Player();
        Console.WriteLine("Hello, World!");
        player.inventory["coin"] = 4;
        player.inventory["power"] = 2;
        player.inventory["metal"] = 0;
        player.inventory["heart"] = 2;
        
        GameLogic gl = new GameLogic();
        gl.ParseRule();
        bool gameEnd = false;
        while(!gameEnd)
        {
            Console.Write("> ");
            string input = Console.ReadLine();
            if (input == "quit")
            {
                gameEnd = true;
                break;
            }
            Console.WriteLine("Executing: " + input);
            gl.ExecuteAction(input, ref player);
        Console.WriteLine("coin: " + player.inventory["coin"]);
        Console.WriteLine("power: " + player.inventory["power"]);
        Console.WriteLine("metal: " + player.inventory["metal"]);
            
                gameEnd = true;
        }
        return;
    }
}