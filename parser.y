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
%token tk_while
%token tk_whileend

%token tk_assign
%token tk_or
%token tk_and


%token tk_par_open
%token tk_par_close


%start program

%%

program: func_def
			| decl
			;

func_def: type_spec  declarator  comb_statement
			;

decl: type_spec  declarator  ';' ;

type_spec:  tk_int
			| tk_float
			;

declarator: tk_id
			| tk_par_open  declarator  tk_par_close
			;

comb_statement: tk_begin  declarator  statement_list  tk_end
			| tk_begin  statement_list  tk_end
			| tk_begin  tk_end
			;

statement_list: statement | statement_list  statement ;

statement: exp_statement
			| comb_statement
			| selection_statement
			| iteration_statement
			;

exp_statement: exp ';' ;

selection_statement: tk_if  tk_par_open  exp  tk_par_close  statement
			| tk_if  tk_par_open  exp  tk_par_close  statement  tk_else  statement
			;

iteration_statement: tk_while  tk_par_open  exp  tk_par_close  statement tk_whileend
			;

exp: assign_exp ;

assign_exp: log_exp
			| un_exp  tk_assign  assign_exp
			;

log_exp: logical_or | logical_and ;

logical_or: eq_exp
			| logical_or assign_exp tk_or eq_exp
			;

logical_and: eq_exp
			| logical_and tk_and eq_exp
			;

eq_exp: rel_exp
			| eq_exp tk_equal rel_exp
            | eq_exp tk_different rel_exp
			;

rel_exp: add_exp
            | rel_exp tk_greater add_exp
            | rel_exp tk_greater_equal add_exp
            | rel_exp tk_less add_exp
			| rel_exp tk_less_equal add_exp
			;

add_exp: mult_exp
			| add_exp tk_plus mult_exp
			| add_exp tk_minus mult_exp
			;

mult_exp: un_exp
			| mult_exp tk_mult un_exp
			| mult_exp tk_division un_exp
			;

un_exp: primary_exp
			| un_op primary_exp
			;

un_op:  tk_plus 
            | tk_minus 
            | tk_not
			;

primary_exp: tk_id
			| string
			| const
			| tk_par_open  exp  tk_par_close
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