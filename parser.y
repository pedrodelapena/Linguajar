%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex();
extern int yyparse();
extern FILE* yyin;
void yyerror(const char* s);
%}

%union {
 int ival;
 float fval;
 char *sval;
}

%token<ival> tk_int
%token<fval> tk_float
%token<sval> tk_id
%token string

%token tk_begin
%token tk_end

%token tk_plus
%token tk_minus
%token tk_mult
%token tk_division

%token tk_equal
%token tk_different
%token tk_greater
%token tk_greater_equal
%token tk_less
%token tk_less_equal
%token tk_not

%token tk_if
%token tk_else
%token tk_do
%token tk_then
%token tk_while
%token tk_whileend

%token tk_assign
%token tk_or
%token tk_and

%token tk_par_open
%token tk_par_close
%token tk_break

%start program

%%

program: func_def | decl | ;

func_def: type_spec declaration compound_statement ;

decl: type_spec declaration tk_break;

type_spec: tk_int | tk_float ;

declaration: tk_id | tk_par_open declaration tk_par_close ;

compound_statement: tk_begin declaration statement_list tk_end
			| tk_begin statement_list tk_end
			;

statement_list: statement ;

statement: exp_statement
			| compound_statement 
			| if_statement
			| while_statement
			;

exp_statement: exp tk_break;

if_statement: tk_if tk_par_open exp tk_par_close tk_then tk_do statement tk_end
			| tk_if tk_par_open exp tk_par_close tk_then tk_do statement tk_else statement tk_end
			;

while_statement: tk_while tk_par_open exp tk_par_close tk_do statement tk_whileend ;

exp: assign_exp ;

assign_exp: log_exp | un_exp tk_assign assign_exp ;

log_exp: log_or | log_and ;

log_or: eq_exp | log_or assign_exp tk_or eq_exp ;

log_and: eq_exp | log_and tk_and eq_exp ;

eq_exp: rel_exp
			| eq_exp tk_equal rel_exp
      		| eq_exp tk_different rel_exp
			;

rel_exp: addsub_exp
      		| rel_exp tk_greater addsub_exp
      		| rel_exp tk_greater_equal addsub_exp
      		| rel_exp tk_less addsub_exp
			| rel_exp tk_less_equal addsub_exp
			;

addsub_exp: multdiv_exp
			| addsub_exp tk_plus multdiv_exp
			| addsub_exp tk_minus multdiv_exp
			;

multdiv_exp: un_exp
			| multdiv_exp tk_mult un_exp
			| multdiv_exp tk_division un_exp
			;


un_exp: primary_exp | un_op primary_exp ;

un_op: tk_plus 
      		| tk_minus 
      		| tk_not
			;

primary_exp: tk_id
			| string
			| const
			| tk_par_open exp tk_par_close
			;

const: tk_int | tk_float ;

%%
int main() {
	yyin = stdin;
	do {
		yyparse();
	} while(!feof(yyin));
	return 0;
}
void yyerror(const char* s) {
	fprintf(stderr, "Parse error: %s\n", s);
	exit(-1);
}
