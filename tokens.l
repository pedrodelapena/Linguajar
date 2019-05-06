%{
#include <string>
#include "node.h"
#include "parser.hpp"
#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
extern "C" int yywrap() { }
%}

/* ref https://gnuu.org/2009/09/18/writing-your-own-toy-compiler/ https://aquamentus.com/flex_bison.html */

%%

"FAZER"				    {return tk_do ;} //
"SE"				    {return tk_if ;} //x
"SENAO"				    {return tk_else ;} //x

"TIPO"				    {return tk_type ;} //x
"INTEIRO"				{return tk_integer ;} //x
"FRAC"                  {return tk_float;} //x
"NOME"					{return tk_var ;} //x
"ETMB"					{return tk_and;} //x
"OU"				    {return tk_or ;} //x
"NEG"                   {return tk_not;} //x

"INICIO"				{return tk_begin ;} //x
"FIM"					{return tk_end ;} //x

"ENQUANTO"				{return tk_while ;} //x
"ENCERRADO"				{return tk_whileend ;} //x

"MAIS"					{return tk_plus;} //x
"MENOS"					{return tk_minus;} //x
"MULTIP"				{return tk_mult;} //x
"DIVIDE"				{return tk_division;} //x

"IG"					{return tk_equal;}  //x
"PABR"					{return tk_par_open;} // (  //x
"PFEC"					{return tk_par_close;} // )  //x
"MAIOR"				    {return tk_greater;} //x
"MENOR"					{return tk_less;} //x
"MAIORIG"				{return tk_greater_equal;} //x
"MENORIG"				{return tk_less_equal;} //x
"DIFER"					{return tk_different;}
"IGUAL"					{return tk_assign;} //(==)
"PONTO"					{return tk_dot;}
[ \t]					;

[ \t\n]                 ;
[a-zA-Z_][a-zA-Z0-9_]*  {return tk_id;}; //x
[0-9]+      			{return tk_int;} //x

.                       printf("Unknown token!n"); yyterminate();

%%