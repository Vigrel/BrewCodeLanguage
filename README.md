### EBNF

program = "Let's brew a coffee", { block }, "Your coffee is ready" ; 

block = { statement } ;

statement = function_declaration | variable_declaration | expression | assignment | loop | condition | return_statement | serve_statement ;

function_declaration = "brew" , function_name , parameter_list , function_body ;

function_name = identifier ;

parameter_list = "(" , [ identifier , { "," , identifier } ] , ")" ;

function_body = "{" , block , "}" ;

variable_declaration = "cup" , variable_name, ["=",expression] ";" ;

variable_name = identifier ;

expression = term , { ( "+" | "-" ) , term } ;

term = factor , { ( "*" | "/" ) , factor } ;

factor = string | number | variable | function_call | "(" , expression , ")" ;

string = '"', ? any possible characte?, '"' ;

number = digit , { digit } ;

variable = variable_name ;

function_call = function_name , "()" ;

assignment = variable_name , "=" , expression , ";" ;

loop = "percolate" , "(" , expression , ")" , "{" , block , "}" ;

condition = "sip" , "(" , expression , ")" , "{" , block , "}" , [ "gulp" , "{" , block , "}" ] ;

return_statement = "pour" , expression , ";" ;

serve_statement = "serve" , expression , ";" ;

identifier = letter , { letter | digit | "_" } ;

letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;

digit = "0" | "1" | ... | "9" ;

#### example
```
Let's brew a coffee

cup coffeeBeans = 10;
cup water = 200;

percolate (coffeeBeans) {
  coffeeBeans = coffeeBeans - 1;
  water = water + 20;
  sip (i / 2 == 0) {
    addSugar(2);
  } gulp {
    addMilk(1);
  }
}

brew addSugar (amount) {
  cup sugar = amount;
  pour sugar;
}

brew addMilk (amount) {
  cup milk = amount;
  pour milk;
}

Your coffee is ready

```