#const width = 30.
#const height = 30.

endX(width).
endY(height).

gridSlot((X,Y), X, Y) :- X = 1..width, Y = 1..height.
    
{ chosen(G,T) : tile(T) } = 1 :- gridSlot(G,X,Y).
    
{chosen(A2,T2) : valid(y,T1,T2)} = 1 :- gridSlot(A1,X1,Y1), chosen(A1,T1), gridSlot(A2,X1,Y1+1).
{chosen(A2,T2) : valid(x,T1,T2)} = 1 :- gridSlot(A1,X1,Y1), chosen(A1,T1), gridSlot(A2,X1+1,Y1).

chosenTile(T) :- chosen(G,T).
    
allChosenClass(T) :- chosenTile((T,_,_)).
allChosenClass(T) :- chosenTile(T).
badChosenClass(A) :- allChosenClass(A), A = (T,_,_), allChosenClass(T).
tileChosenClass(T) :- allChosenClass(T), not badChosenClass(T).

blockLoc(Loc) :- chosen(Loc,Tile), blocker(Tile).
unblockLoc(Loc) :- chosen(Loc,Tile), not blocker(Tile).
    
:- blockLoc(Loc), access(_,Loc).
path(Pid) :- access(Pid,_).
    
{startLoc(Pid,Loc) : access(Pid,Loc)} = 1 :- path(Pid).
path(Pid,Loc) :- startLoc(Pid,Loc).
path(Pid,(X,Y)) :- path(Pid,(X-1,Y)), unblockLoc((X,Y)).
path(Pid,(X,Y)) :- path(Pid,(X+1,Y)), unblockLoc((X,Y)).
path(Pid,(X,Y)) :- path(Pid,(X,Y-1)), unblockLoc((X,Y)).
path(Pid,(X,Y)) :- path(Pid,(X,Y+1)), unblockLoc((X,Y)).
count(A,Loc) :- access(_,Loc), A = #count{Pid : path(Pid,Loc)}.
:- access(Pid,Loc), not path(Pid,Loc).
:- access(Pid,Loc), path(Pid2,Loc), Pid != Pid2.

%%%Projection (to ensure some bits of variance)
projectLocs((3,3)).
projTile(L,T) :- chosen(L,T), projectLocs(L).

#project projTile/2.

#show chosen/2.