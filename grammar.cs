using System.IO;
using System;
using System.Collections.Generic;

class Grammar
{
    public string MultiKind(ref List<string> kinds)
    {
        //ask user to select one
        string userSelected = "none selected";
        while (!kinds.Contains(userSelected))
        {
        string options = "Select: ";
        foreach(var k in kinds)
        {
            options += k + ", ";
        }
        Console.WriteLine(options);
        Console.Write("> ");
        userSelected = Console.ReadLine();
        }
        return userSelected;
    }
}