using System.IO;
using System;
using System.Collections.Generic;

class GameLogic
{
    Dictionary<string, string> verbs = new Dictionary<string, string>();
    Dictionary<string, string> nouns = new Dictionary<string, string>();
    string ruleText = @"verb: bolster, trade, produce, move
    noun: coin, power, resource, metal, oil, wood, food, worker, mech, building, tile, upgrade, recruit, worker, character
    resource: metal, oil, wood, food
    bolster: pay 1 coin, gain 2 power or gain 1 heart
    trade: pay 2 coin, gain 2 resource
    produce: for 2 tiles, gain one resource per worker
    move: move 2 units by 1 tile each or gain 2 coins
    deploy: pay 1 coin, gain 1 mech on a worker tile
    build: pay 1 coin, gain 1 building on a worker tile
    enlist: pay 1 coin, gain 1 recruit
    upgrade: pay 1 coin, gain 1 upgrade
    card: action card, mech card, building card
    faction: polania, saxony, khanate, nordic
    polania: gain 2 heart, gain 4 coin, gain 2 power, gain 3 combat card 
    :gain 1 character and gain 2 worker
    :mechs: gain 1 move per unit, cross river, lake move
    rule: 
    combat: win by combat number, loser units flee back to home base
    confrontation: worker flee
    flee: worker move to home base if confronted, mover lose 1 heart per worker
    combat card: random range between 2 to 5";

    AST ast = new AST();
    public void ExecuteAction(string exec, ref Player player)
    {
        if (verbs.ContainsKey(exec))
        {
            var commandStr = verbs[exec];
            char[] delimiters = {','};
            var actions = commandStr.Split(delimiters);
            foreach (var action in actions)
            {
                char[] actionDel = {' '};
                var commands = action.Split(actionDel,
                StringSplitOptions.RemoveEmptyEntries); Console.WriteLine("Executing: ");
                foreach (var command in commands)
                    Console.Write(command + ", ");
                ast.Execute(ref commands, ref player, nouns);
            }
        }
    }
    public void ParseRule()
    {
        char[] delimiter = {'\n', '\r'};
        var lines = ruleText.Split(delimiter);
        foreach(var line in lines)
        {
            Console.WriteLine("line: " + line);
            ParseLine(line);
        }
    }
    void ParseLine(string line)
    {
        char[] delimiter = {':'};
        var tokens = line.Split(delimiter, StringSplitOptions.RemoveEmptyEntries);
        //find first token and parse command
        /* 
        var str = "|";
        foreach(var token in tokens)
        {
            str += token + "| ";
        }
        Console.WriteLine("Line: " + str);
*/
        char[] whitespacedel = {' ', '\t'};
        var labels = tokens[0].Split(whitespacedel, StringSplitOptions.RemoveEmptyEntries);
        var label = labels[0];
        if (label == "verb")
        {
            AddToDictionary(ref verbs, tokens[1]);
        } else if (label == "noun")
        {
            AddToDictionary(ref nouns, tokens[1]);
        } else {
            //label should be either in either noun or verbs dictionary
            Console.WriteLine("Processing: " + label);
            if (verbs.ContainsKey(label))
            {
                verbs[label] = tokens[1];
                Console.WriteLine("added verb def: " + label);
            } else
            if (nouns.ContainsKey(label))
            {
                nouns[label] = tokens[1];
                Console.WriteLine("added noun def: " + label);
            }
        }
    }
    public GameLogic() {}
    void AddToDictionary(ref Dictionary<string, string> dict, string input)
    {
        char[] delimiters = {' ', ','};
        var tokens = input.Split(delimiters);
        foreach(var token in tokens)
        {
            if (token == "")
                continue;
            Console.WriteLine("adding keyterm: " + token);
            dict.Add(token, "void");
        }
    }
}