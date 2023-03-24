%      _(1)_ 
%	 (2)	(3)
%    | _(4)_ |
%	 (5)	(6)
%    |_ (7)_ |

matches(0, R) :- R = [1,1,1,0,1,1,1].
matches(1, R) :- R = [0,0,1,0,0,1,0].
matches(2, R) :- R = [1,0,1,1,1,0,1].
matches(3, R) :- R = [1,0,1,1,0,1,1].
matches(4, R) :- R = [0,1,1,1,0,1,0].
matches(5, R) :- R = [1,1,0,1,0,1,1].
matches(6, R) :- R = [1,1,0,1,1,1,1].
matches(7, R) :- R = [1,0,1,0,0,1,0].
matches(8, R) :- R = [1,1,1,1,1,1,1].
matches(9, R) :- R = [1,1,1,1,0,1,1].
% it's very important that it is possible to tranform '+' to '-' by taking one '1'
matches(-, R) :- R = [1,0,0,0,0,0,0].
matches(+, R) :- R = [1,1,0,0,0,0,0].

number(Matches, R) :- 
    matches(N, Matches2),
    Matches = Matches2,
    R = N,
    !.

% if we hane breaked structure return number that 100% break expression
number(_, R) :- R = -100.

random_digit(R) :- random(0, 10, R).
random_operation(R) :- random_member(R, [+, -]).

equality_expr(N1, +, N2, N3) :- N3 is N1+N2.
equality_expr(N1, -, N2, N3) :- N3 is N1-N2.

% tranform expression to matrix (list)
expression_matrix(N1, Op, N2, NR, Matrix) :-
    matches(N1, N1_Matches),
    matches(Op, Op_Matches),
    matches(N2, N2_Matches),
    matches(NR, NR_Matches),
    append([N1_Matches, Op_Matches, N2_Matches, NR_Matches], Matrix).
    

% how many elements differ in two lists
diff([], [], 0) :- !.
diff([Xs_H|Xs_T], [Ys_H|Ys_T], Res) :-
    Xs_H \= Ys_H,
    diff(Xs_T, Ys_T, TailDiff),
    Res is 1 + TailDiff, !.
diff([Xs_H|Xs_T], [Ys_H|Ys_T], Res) :-
    Xs_H = Ys_H,
    diff(Xs_T, Ys_T, TailDiff),
    Res = TailDiff, !.

% first list can be transformed to second list by swaping one element to another
% we assume that lengths of both lists are same
one_move_list(Xs, Ys) :-
    diff(Xs, Ys, Diff),
    Diff = 2, % differ by 2 elements
    sum_list(Xs, SumXs), sum_list(Ys, SumYs), 
    SumXs=SumYs. % have same elements

% get input or ouput data of the puzzle
matches_puzzle(Number1In, OpIn, Number2In, Number3In,
               Number1Out, OpOut, Number2Out, Number3Out) :-
    expression_matrix(Number1In, OpIn, Number2In, Number3In, MatrixIn),
    expression_matrix(Number1Out, OpOut, Number2Out, Number3Out, MatrixOut),
    one_move_list(MatrixIn, MatrixOut),
    equality_expr(Number1Out, OpOut, Number2Out, Number3Out).


% random puzzle and its solution
matches_puzzle_random(Number1In, OpIn, Number2In, Number3In,Number1Out, OpOut, Number2Out, Number3Out) :-
    random_digit(Number1In),
    random_digit(Number2In),
    random_digit(Number3In),
    random_operation(OpIn),
    matches_puzzle(Number1In, OpIn, Number2In, Number3In,
                Number1Out, OpOut, Number2Out, Number3Out).

% Generate solution
% ?- matches_puzzle(Number1In, OpIn, Number2In, Number3In,2, +, 3, 7)

% Generate puzzle if we know solution
% ?- matches_puzzle(7, +, 0, 7, Number1Out, OpOut, Number2Out, Number3Out)



    
                                              

