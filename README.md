# EBNF

program = "Let's brew a coffee", [ block ], "Your coffee is ready" 

block = statement, {statement}

statement = λ | function_declaration | variable_declaration | rel_expression | variable_assignment | loop | condition | return_statement | print_statement
## Function
---

function_declaration = "brew", type_declaration, function_name , parameter_list , function_body 

function_name = identifier 

parameter_list = "(" , [ variable_declaration , { "," , variable_declaration } ] , ")" 

function_body = "{" , [ block ] , "}" 

function_call = function_name, "(", [ rel_expression, { ",", rel_expression } ], ")"

return_statement = "pour" , rel_expression , ";" 

## Variable
---

type_declaration = "cup" | "lungo"

variable_declaration = type_declaration, variable_name , ";"

variable_name = identifier 

variable_assignment = variable_name, "=", rel_expression, ";"

## Expressions 
---

rel_expression = expression , { ( "same" | "stronger" | "weaker" ) , expression }, , ";"

expression = term , { ( "+" | "-" | "maybe" ) , term } ;

term = factor , { ( "*" | "/" | "also" ) , factor } ;

factor = string | number | variable_name | function_call | "(" , rel_expression , ")" ;
 
## Loop
---
loop = "percolate" , rel_expression , "{" , block , "}" ;

## If/else
---
condition = "sip" , rel_expression , "{" , block , "}" , [ "gulp" , "{" , block , "}" ] ;

## Others
---
print_statement = "serve" , rel_expression , ";" ;

number = digit , { digit } ;

string = '"', ?any possible character?, '"' ;

identifier = letter , { letter | digit | "_" } ;

letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;

digit = "0" | "1" | ... | "9" ;

#### example
```
Let's brew a coffee
  cup blackCoffee;
  cup americanCoffee;
  cup water;
  blackCoffee = 10;
  americanCoffee = 10;
  water = 10;
  percolate(blackCoffee stronger americanCoffee) {
    sip (blackCoffee weaker 5) {
      sip(blackCoffee weaker 2) {
        serve "No sugar added";
      } gulp {
        serve "Adding sugar";
      }
    }
    blackCoffee = blackCoffee - water;
  }
Your coffee is ready
```