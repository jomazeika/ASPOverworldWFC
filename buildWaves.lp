%Construct the adjacency from the 
tile(T) :- map(M,L,T).
valid(x,T1,T2) :- map(M,(X,Y),T1), map(M,(X+1,Y),T2).
valid(y,T1,T2) :- map(M,(X,Y),T1), map(M,(X,Y+1),T2).

mapName(M) :- map(M,_,_).
tileSet(M,T) :- map(M,_,T).

allClass(T) :- tile((T,_,_)).
allClass(T) :- tile(T).
badClass(A) :- allClass(A), A = (T,_,_), allClass(T).
tileClass(T) :- allClass(T), not badClass(T).
    
allMapClass(M,T) :- tileSet(M,T).
allMapClass(M,T) :- tileSet(M,(T,_,_)).
badMapClass(M,A) :- allMapClass(M,A), A = (T,_,_), allMapClass(M,T).
mapTileClass(M,T) :- allMapClass(M,T), not badMapClass(M,T).