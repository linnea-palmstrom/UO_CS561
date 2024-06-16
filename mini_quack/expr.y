%token ID
%token PLUS
%token LT
%%
S: L ;

L:  L I 
     |
     ;
I: <li> i optEnd
optEnd: </li>
     | 
     ;
%%
