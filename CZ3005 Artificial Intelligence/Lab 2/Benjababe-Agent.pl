% predicates that can be updated in runtime
:- dynamic([
    % pair of XY coordinates to indicate whether relative cell has been visited
    visited/2,
    % possible locations for the wumpus
    wumpus/2,
    % confirmed not wumpus
    not_wumpus/2,
    % locations where confounded is felt
    confounded/2,
    % locations for the confundus portal
    confundus/2,
    % confirmed not portals
    not_confundus/2,
    % known locations where agent feels tingle
    tingle/2,
    % known locations where agent feels glitter
    glitter/2,
    % locations with stench perception
    stench/2,
    % known safe location
    safe/2,
    % current XY coordinates and relative direction of agent
    current/3,
    % tracks whether arrow has been shot
    hasarrow/0,
    % tracks boundaries of the map
    wall/2,
    % tracks number of coins on the floor
    coins/1,
    % tracks wumpus' living status
    wampus_dead/0,
    % wumpus has definitely been found
    wumpus_found/0
]).


% updates direction in current when turning left
tl :-
    retract(current(X, Y, Dir)),
    (
        Dir == rnorth -> assertz(current(X, Y, rwest));
        Dir == rwest -> assertz(current(X, Y, rsouth));
        Dir == rsouth -> assertz(current(X, Y, reast));
        Dir == reast -> assertz(current(X, Y, rnorth))
    ),
    current(NewX, NewY, NewDir),
    format('[Agent] Agent is now at (~d, ~d, ~w)', [NewX, NewY, NewDir]), nl.


% updates direction in current when turning right
tr :-
    retract(current(X, Y, Dir)),
    (
        Dir == rnorth -> assertz(current(X, Y, reast));
        Dir == reast -> assertz(current(X, Y, rsouth));
        Dir == rsouth -> assertz(current(X, Y, rwest));
        Dir == rwest -> assertz(current(X, Y, rnorth))
    ),
    current(NewX, NewY, NewDir),
    format('[Agent] Agent is now at (~d, ~d, ~w)', [NewX, NewY, NewDir]), nl.


fwd :-
    retract(current(X, Y, Dir)),
    (
        Dir == rnorth -> NextY is Y + 1, NextX is X;
        Dir == rsouth -> NextY is Y - 1, NextX is X;
        Dir == reast -> NextY is Y, NextX is X + 1;
        Dir == rwest -> NextY is Y, NextX is X - 1
    ),

    format('[Agent] Agent is now at (~d, ~d, ~w)', [NextX, NextY, Dir]), nl,
    asserta(current(NextX, NextY, Dir)),
    assert_visited(NextX, NextY),
    assert_safe(NextX, NextY),

    % clear hazards from cell since we can move there
    retract_wumpus(NextX, NextY),
    retract_confundus(NextX, NextY).

retract_wumpus(X, Y) :-
    retractall(wumpus(X, Y)); true.

retract_confundus(X, Y) :-
    retractall(confundus(X, Y)); true.


reborn :- 
    retractall(hasarrow),
    retractall(wumpus_dead),
    retractall(wumpus_found),
    retractall(coins(_)),

    assertz(hasarrow),
    assertz(coins(0)).    


reposition(L) :-
    retractall(wumpus(_, _)),
    retractall(not_wumpus(_, _)),
    retractall(confounded(_, _)),
    retractall(confundus(_, _)),
    retractall(not_portal(_, _)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(visited(_, _)),
    retractall(safe(_, _)),
    retractall(current(_, _, _)),
    retractall(wall(_, _)),
    retractall(wumpus_found),
    
    assertz(visited(0, 0)),
    assertz(safe(0, 0)),
    assertz(current(0, 0, rnorth)),
    
    format('[Agent] User repositioned to (0, 0)'), nl,
    handle_perception(L).


manual_reset :- 
    reborn,
    reposition([on, off, off, off, off, off]).


% retrives action after updating agent with perceptions
move(A, L) :-
    handle_action(A);
    handle_perception(L).


handle_action(A) :-
    current(X, Y, _),
    (
        write('[Agent] '),
        A == none -> write('Agent did nothing'), nl, !;
        A == pickup -> handle_pickup(X, Y), write('Agent picked up gold!'), nl, !;
        (A == shoot, hasarrow) -> retract(hasarrow), write('Agent shot arrow!'), nl, !;
        (A == shoot, \+hasarrow) -> write('Agent does not have arrow!'), nl, !;
        A == moveforward -> format('Agent moved forward!'), nl, fwd, !;
        A == turnleft -> write('Agent turned left'), nl, tl, !;
        A == turnright -> write('Agent turned right'), nl, tr, !
    ),
    \+true.


% removes glitter and adds 1 coin to coins/1
handle_pickup(X, Y) :-
    retract(glitter(X, Y)), !,
    coins(CX),
    NX is CX - 1,
    retractall(coins(_)),
    asserta(coins(NX)).


handle_perception([Confounded, Stench, Tingle, Glitter, Bump, Scream]) :-
    has_confounded(Confounded);
    has_bump(Bump);
    has_stench(Stench);
    has_tingle(Tingle);
    has_glitter(Glitter);
    has_scream(Scream);
    check_safe;
    check_wumpus;
    check_portal,
    true.


% when your step onto a portal
has_confounded(on) :-
    \+true.


% if stench is sensed, set surrounding cells to possibly be wumpus
has_stench(on) :-
    current(X, Y, _), 
    assertz(stench(X, Y)),
    current(X, Y, _), N is Y + 1, set_wumpus(X, N), !;
    current(X, Y, _), S is Y - 1, set_wumpus(X, S), !;
    current(X, Y, _), E is X + 1, set_wumpus(E, Y), !;
    current(X, Y, _), W is X - 1, set_wumpus(W, Y), !;
    \+true.


has_stench(off) :-
    current(X, Y, _),
    N is Y + 1, S is Y - 1, E is X + 1, W is X - 1, !,
    assertz(not_wumpus(X, N)),
    assertz(not_wumpus(X, S)),
    assertz(not_wumpus(E, Y)),
    assertz(not_wumpus(W, Y)),
    retract(wumpus(X, N)),
    retract(wumpus(X, S)),
    retract(wumpus(E, Y)),
    retract(wumpus(W, Y)),
    \+true.



% to confirm wumpus location, coordinate must have at least 3 stench cells adjacent
% if any of the adjacent cells have been visited and doesn't have stench, confirmed no wumpus here
set_wumpus(X, Y) :-
    % if wumpus hasn't been found or is dead, add suspected wumpus spot
    % spot also musn't be safe, visited nor is a wall
    (\+wumpus_found, \+wumpus_dead, \+safe(X, Y), \+visited(X, Y), \+wall(X, Y), \+not_wumpus(X, Y)) -> (assertz(wumpus(X, Y))),

    % adjacent cells to the suspected wumpus cell
    N is Y + 1, S is Y - 1, E is X + 1, W is X - 1, !,

    % checks all pairs of adjacent cells for 3 stenches
    (   
        stench(W, Y), stench(X, N), stench(E, Y), !;
        stench(X, N), stench(E, Y), stench(X, S), !;
        stench(E, Y), stench(X, S), stench(W, Y), !;
        stench(X, S), stench(W, Y), stench(X, N), !
    )
    -> 
    % if found, wumpus is on the cell!
    (
        assertz(wumpus_found),
        retractall(wumpus(_, _)),
        assertz(wumpus(X, Y)),
        format('[Agent] Wumpus confirmed to be at (~d, ~d)', [X, Y]), nl,

        % reset stench cells and set the 4 adjacent cells of the wumpus
        retractall(stench(_, _)),
        assertz(stench(X, N)), assertz(stench(X, S)),
        assertz(stench(E, Y)), assertz(stench(W, Y))
    ).


% if tingle is sensed, set surrounding cells to possibly be portal
has_tingle(on) :-
    current(X, Y, _),
    assertz(tingle(X, Y)),
    N is Y + 1, set_confundus(X, N), !,
    S is Y - 1, set_confundus(X, S), !,
    E is X + 1, set_confundus(E, Y), !,
    W is X - 1, set_confundus(W, Y), !,
    \+true.


has_tingle(off) :-
    current(X, Y, _),
    N is Y + 1, S is Y - 1, E is X + 1, W is X - 1, !,
    assertz(not_portal(X, N)),
    assertz(not_portal(X, S)),
    assertz(not_portal(E, Y)),
    assertz(not_portal(W, Y)),
    \+true.


% only set as possible confundus portal if 
% cell isn't flagged safe
% cell hasn't been visited
% cell isn't a wall
% cell isn't already possible portal
set_confundus(X, Y) :-
    ((\+safe(X, Y), \+visited(X, Y)), \+wall(X, Y), \+confundus(X, Y)) -> assertz(confundus(X, Y));
    true.


% if glitter is sensed, set current position to glitter
has_glitter(on) :-
    current(X, Y, _),
    (\+glitter(X, Y)) -> (
        assertz(glitter(X, Y)),
        coins(CX),
        NX is CX + 1,
        retractall(coins(_)),
        asserta(coins(NX)),
        format('[Agent] Coin confirmed to be at (~d, ~d)!', [X, Y]), nl
    ),
    \+true.


% if a bump is sensed, move agent backwards
has_bump(on) :-
    write('[Agent] Agent has sensed a bump, retracting moveforward action'), nl,
    retract(current(X, Y, Dir)),
    (
        Dir == rnorth -> PrevX is X, PrevY is Y - 1, !;
        Dir == reast -> PrevX is X - 1, PrevY is Y, !;
        Dir == rsouth -> PrevX is X, PrevY is Y + 1, !;
        Dir == rwest -> PrevX is X + 1, PrevY is Y, !
    ),
    assertz(wall(X, Y)),
    (
        retractall(wumpus(X, Y)), !;
        retractall(confundus(X, Y)), !;
        true
    ),
    assertz(current(PrevX, PrevY, Dir)), !,
    format('[Agent] Agent is now at (~d, ~d, ~w)', [PrevX, PrevY, Dir]), nl,
    \+true.


% if a scream is sensed, wumpus is kill
% and set all wumpus cells to safe
has_scream(on) :-
    assertz(wumpus_dead),
    retractall(stench(_, _)),
    call(wumpus(X, Y)),
    replace_wumpus_safe(X, Y),
    retractall(wumpus(_, _)),
    \+true.


replace_wumpus_safe(X, Y) :-
    \+confundus(X, Y), !,
    assert_safe(X, Y);
    true.


% checks all wumpus cells whether they can contain a wumpus
% they cannot if any visited cells adjacent to them do not have stench
check_wumpus :-
    wumpus(X, Y),
    N is Y + 1, S is Y - 1, E is X + 1, W is X - 1,
    (
        (visited(X, N), \+stench(X, N));
        (visited(X, S), \+stench(X, S));
        (visited(E, Y), \+stench(E, Y));
        (visited(W, Y), \+stench(W, Y)) 
    ) 
    -> 
    (
        retract(wumpus(X, Y)),
        assertz(not_wumpus(X, Y))
    ),
    (not_wumpus(X, Y), not_portal(X, Y))
    ->
    assert_safe(X, Y).


% checks all confundus cells whether they can contain a portal
% they cannot if any visited cells adjacent to them do not have tingle
check_portal :-
    confundus(X, Y),
    N is Y + 1, S is Y - 1, E is X + 1, W is X - 1,
    (
        (visited(X, N), \+tingle(X, N));
        (visited(X, S), \+tingle(X, S));
        (visited(E, Y), \+tingle(E, Y));
        (visited(W, Y), \+tingle(W, Y)) 
    ) 
    -> 
    (
        retract(confundus(X, Y)),
        assertz(not_portal(X, Y))
    ),
    (not_wumpus(X, Y), not_portal(X, Y))
    ->
    assert_safe(X, Y).


% if current cell doesn't have stench nor tingle, all adjacent cells must be safe
check_safe :-
    call(current(X, Y, _)),
    (\+stench(X, Y), \+tingle(X, Y)) -> 
    (
        N is Y + 1, S is Y - 1, E is X + 1, W is X - 1,
        assert_safe(X, N),
        assert_safe(X, S),
        assert_safe(E, Y),
        assert_safe(W, Y)
    ),
    \+true.

assert_safe(X, Y) :-
    \+safe(X, Y), \+wall(X, Y) -> assertz(safe(X, Y));
    true.

assert_visited(X, Y) :-
    \+visited(X, Y) -> assertz(visited(X, Y));
    true.



%%%%%%%%%%%%%%%%
% CANCER BELOW %
%%%%%%%%%%%%%%%%

% i have no clue why but this keeps the backtracking from going insane
% maybe this makes prolog set the variable as a list and not as 1 action?
iter_list([]).
iter_list([_|L]) :-
    iter_list(L).


explore(L) :-
    iter_list(L),
    current(X, Y, Dir),
    (
        % limit no. of actions to ~15 because any more actions take a ton of time to compute
        check_return_home(X, Y, Dir, L), !;
        call_with_depth_limit(find_path(X, Y, Dir, L, safe), 30, D), !,
        D \= depth_limit_exceeded
    ).


% return home when
% no more unvisited safe cells
% no more coins on visited spots
% relative position is not (0, 0)
check_return_home(X, Y, Dir, HL):-
    \+explore_conditions,
    (X \= 0; Y \= 0),
    find_path(X, Y, Dir, HL, home), !.


% true when a new unvisited safe cell or coin on visited spot exists
explore_conditions :- (safe(SX, SY), \+visited(SX, SY), \+wall(SX, SY)); (glitter(GX, GY), visited(GX, GY)).


% handles action one at a time
find_path(X, Y, Dir, [A|L], Dest) :-
    % ensure current cell in path is either safe or already visited, no taking chances here
    (visited(X, Y); safe(X, Y), \+wall(X, Y)), !,

    % makes appropriate changes based on the action
    update_path(X, Y, Dir, A, L, Dest), !.


% terminating point for moving to safe unvisited cell
% checks if final destination is safe and unvisited
find_path(X, Y, _, [], safe) :- safe(X, Y), \+visited(X, Y), \+wall(X, Y).


% terminating point for returning to relative origin
% checks if final coordinates if (0, 0)
find_path(X, Y, _, [], home) :- X=0, Y=0.


% only allow pickup when it is the terminating action
update_path(X, Y, _, pickup, [], _) :- visited(X, Y), glitter(X, Y), \+wall(X, Y).


update_path(X, Y, Dir, turnleft, L, Dest) :-
    (
        Dir = rnorth -> NextDir = rwest;
        Dir = rwest -> NextDir = rsouth;
        Dir = rsouth -> NextDir = reast;
        Dir = reast -> NextDir = rnorth
    ),
    find_path(X, Y, NextDir, L, Dest).


update_path(X, Y, Dir, turnright, L, Dest) :-
    (
        Dir = rnorth -> NextDir = reast;
        Dir = rwest -> NextDir = rnorth;
        Dir = rsouth -> NextDir = rwest;
        Dir = reast -> NextDir = rsouth
    ),
    find_path(X, Y, NextDir, L, Dest).


update_path(X, Y, Dir, moveforward, L, Dest) :-
    (
        Dir = rnorth -> NextX is X, NextY is Y + 1;
        Dir = rsouth -> NextX is X, NextY is Y - 1;
        Dir = reast -> NextX is X + 1, NextY is Y;
        Dir = rwest -> NextX is X - 1, NextY is Y
    ),
    ((visited(NextX, NextY); safe(NextX, NextY)), \+wall(NextX, NextY)), !,
    find_path(NextX, NextY, Dir, L, Dest).