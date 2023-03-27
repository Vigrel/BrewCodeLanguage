# EBNF

#### body
BLOCK = (STATEMENT, { STATEMENT }), "Cocoricooó";

STATEMENT = ( λ, "\n") | ASSIGNMENT | PRINT | WHILE | DEF_FUNC;

ASSIGNMENT = "Pata de ", IDENTIFIER, "Dança de ", EXPRESSION ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;

TERM = (FACTOR, { ("*" | "/"), FACTOR }) | STRING ;

FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;


#### print
PRINT = "Cocori ", EXPRESSION ;

#### func
DEF_FUNC = "Ta na hora do ", IDENTIFIER, "Ta na hora da turma do [", (IDENTIFIER, {",", IDENTIFIER}), "], OPS_FUNC ;

OPS_FUNC = STATEMENT, { STATEMENT },  "Cantando ", EXPRESSION, "rural" ;

CALL_FUNC = IDENTIFIER, "na gaita e  [", (IDENTIFIER, {",", IDENTIFIER}), "] no co-co-coral" ;


#### loop
WHILE = "Olha o có-có-có-có começando", CONDITIONAL, STATEMENT, { STATEMENT } "Cocoricó" ;

CONDITIONAL = COMPARE, {("e" | "ou"), COMPARE}, "chacoalhando!" ;

COMPARE = EXPRESSION, { (">" | ">=" | "==" | "!=" | "<=" | "<"), EXPRESSION };

##### chars/types
STRING = "'", {ALL CHARACTERS} ,"'";

ALL CHARACTERS = ? all visible characters ? ;

NUMBER = DIGIT, { DIGIT } ;

LETTER = ( a | ... | z | A | ... | Z ) ;

DIGIT = ( ccoó | cocó | cooó | coccó | cocoó | coooó | cocccó | coccoó | ccooó | có ) ;


##### Ex:
Ta na hora do Cocoricó ta na hora da turma do [Julio]
    Cocori Julio
    Cantando Cocori Julio + ccoó rural

Pata de Galinha Dança de cocó

Olha o có-có-có-có começando Galinha < ccooó chacoalhando!
    Cocoricó na gaita e Galha no co-co-coral
    Pata de Galinha Dança de cocó + cocó
    Cocoricó

Cocoricooó

output:
cocó
coccó
coooó
coccoó