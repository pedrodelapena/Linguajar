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


%start external_decl

%%

external_decl: function_definition
			| decl
			;

function_definition: type_spec  declarator  compound_stat
			;

decl: type_spec  declarator  ';'
			;

type_spec:  tk_int
			| tk_float
			;

declarator: tk_id
			| tk_par_open  declarator  tk_par_close
			;

compound_stat: tk_begin  declarator  stat_list  tk_end
			| tk_begin  stat_list  tk_end
			| tk_begin  tk_end
			;

stat_list: stat
			| stat_list  stat
			;

stat: exp_stat
			| compound_stat
			| selection_stat
			| iteration_stat
			;

exp_stat: exp ';'
			;

selection_stat: tk_if  tk_par_open  exp  tk_par_close  stat
			| tk_if  tk_par_open  exp  tk_par_close  stat  tk_else  stat
			;

iteration_stat: tk_while  tk_par_open  exp  tk_par_close  stat tk_whileend
			;

exp:  assignment_exp;

assignment_exp: conditional_exp
			| unary_exp  tk_assign  assignment_exp
			;

conditional_exp: logical_or | logical_and ;

logical_or: equality_exp
			| logical_or tk_or equality_exp
			;

logical_and: equality_exp
			| logical_and tk_and equality_exp
			;

equality_exp: relational_exp
			| equality_exp tk_equal relational_exp
            | equality_exp tk_different relational_exp
			;

relational_exp: additive_exp
            | relational_exp tk_greater additive_exp
            | relational_exp tk_greater_equal additive_exp
            | relational_exp tk_less additive_exp
			| relational_exp tk_less_equal additive_exp
			;

additive_exp: mult_exp
			| additive_exp tk_plus mult_exp
			| additive_exp tk_minus mult_exp
			;

mult_exp: unary_exp
			| mult_exp tk_mult unary_exp
			| mult_exp tk_division unary_exp
			;

unary_exp: primary_exp
			| unary_operator primary_exp
			;

unary_operator:  tk_plus 
            | tk_minus 
            | tk_not
			;

primary_exp: tk_id
			| const
			| string
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