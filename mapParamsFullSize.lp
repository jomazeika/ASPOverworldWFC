
access(1,(4..6,1)).
access(1,(9..11,30)).
access(1,(1,13..15)).

access(2,(48..60,30)).
access(2,(48..60,1)).

access(3,(130..140,125..126)).
access(3,(70..75,100..105)).
access(3,(100..105,40)).

noCrossPaths.

:- #count{T: tileChosenClass(T)} < 12.