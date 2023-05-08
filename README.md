### EBNF
program = "Let's brew a coffee", { block }, "Your coffee is ready" ; 
block = { statement } ;
statement = function_declaration | variable_declaration | rel_expression | assignment | loop | condition | return_statement | serve_statement ;
function_declaration = "brew" , function_name , parameter_list , function_body ;
function_name = identifier ;
parameter_list = "(" , [ identifier , { "," , identifier } ] , ")" ;
function_body = "{" , block , "}" ;
variable_declaration = "cup" , variable_name, ["=",rel_expression] ";" ;
variable_name = identifier ;
rel_expression = expression , { ( "same as" | "stronger than" | "weaker than" ) , expression } ;
expression = term , { ( "+" | "-" | "or maybe" ) , term } ;
term = factor , { ( "*" | "/" | "and also" ) , factor } ;
factor = string | number | variable | function_call | "(" , rel_expression , ")" ;
string = '"', ? any possible characte?, '"' ;
number = digit , { digit } ;
variable = variable_name ;
function_call = function_name , "()" ;
assignment = variable_name , "=" , rel_expression , ";" ;
loop = "percolate" , "(" , rel_expression , ")" , "{" , block , "}" ;
condition = "sip" , "(" , rel_expression , ")" , "{" , block , "}" , [ "gulp" , "{" , block , "}" ] ;
return_statement = "pour" , rel_expression , ";" ;
serve_statement = "serve" , rel_expression , ";" ;
identifier = letter , { letter | digit | "_" } ;
letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
digit = "0" | "1" | ... | "9" ;

#### example
```
Let's brew a coffee
  cup blackCoffee = 10;
  cup americanCoffee = 0;
  cup water = 1;
  percolate(blackCoffee stronger than americanCoffee) {
    sip (blackCoffee weaker than 5) {
      sip(blackCoffee weaker than 2) {
        serve "No sugar added";
      } gulp {
        serve "Adding sugar";
      }
    }
    blackCoffee = blackCoffee - water;
  }
Your coffee is ready
```