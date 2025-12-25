# final_project_MCTS_triangle.py
# Put this file in same folder as your utility_func.py
# Run: python final_project_MCTS_triangle.py

import time
import math
import random
import copy

# try import pygame and utility_func (your provided file)
try:
    import pygame as pg
    PYGAME = True
except Exception:
    PYGAME = False

try:
    import utility_func as uf
    HAVE_UF = True
except Exception:
    HAVE_UF = False

# Board parameters
BLINE = 15  # triangular top row = 15, next 14, ... bottom 1
TIME_LIMIT = 4.5  # seconds per move
UCT_C = 1.0

# Build list of legal triangular positions: u in [0..14], v in [0..14-u]
LEGAL_POSITIONS = [(u, v) for u in range(BLINE) for v in range(BLINE) if v <= (BLINE - 1 - u)]

# quick lookup set
LEGAL_SET = set(LEGAL_POSITIONS)

# ---------- winner check (3 directions: vertical, horizontal, diag) ----------
def check_winner_tri(board):
    """
    board: list of lists shape (15,15) where positions outside triangle may be unused
    return: 1 if black wins, -1 if white wins, 0 otherwise, 2 for draw
    Directions: (1,0) vertical (u+), (0,1) horizontal (v+), (1,-1) diag (down-left -> up-right)
    """
    # 只有横纵斜三种方向，(-1,1)不成立
    directions = [(1,0), (0,1), (1,-1)]
    full = True
    for u,v in LEGAL_POSITIONS:
        val = board[u][v]
        if val == 0:
            full = False
            continue
        for du,dv in directions:
            cnt = 1
            for k in range(1,5):
                uu = u + du*k
                vv = v + dv*k
                if (uu, vv) in LEGAL_SET and board[uu][vv] == val:
                    cnt += 1
                else:
                    break
            if cnt >= 5:
                return val
    if full:
        return 2
    return 0

# ---------- helper: empty neighbors within padding, restricted to triangle ----------
def empty_neighbors(board, padding=2):
    """
    Return list of empty positions within padding-neighborhood of any occupied position.
    If board empty, return middle-top heuristic: choose near top row center (u=0..)
    """
    occ = []
    for u,v in LEGAL_POSITIONS:
        if board[u][v] != 0:
            occ.append((u,v))
    if not occ:
        # prefer top-middle row u=0 center v=7 maybe
        center = (0, (BLINE-1)//2)
        if center in LEGAL_SET:
            return [center]
        return LEGAL_POSITIONS.copy()

    cands = set()
    for (u,v) in occ:
        for du in range(-padding, padding+1):
            for dv in range(-padding, padding+1):
                uu = u + du
                vv = v + dv
                if (uu, vv) in LEGAL_SET and board[uu][vv] == 0:
                    cands.add((uu, vv))
    if not cands:
        return [p for p in LEGAL_POSITIONS if board[p[0]][p[1]] == 0]
    return list(cands)

# ---------- immediate win or block ----------
def immediate_win_or_block(board, my_color):
    # check my immediate win
    for (u,v) in LEGAL_POSITIONS:
        if board[u][v] == 0:
            board[u][v] = my_color
            if check_winner_tri(board) == my_color:
                board[u][v] = 0
                return (u,v)
            board[u][v] = 0
    # check opponent immediate win -> block
    opp = -my_color
    for (u,v) in LEGAL_POSITIONS:
        if board[u][v] == 0:
            board[u][v] = opp
            if check_winner_tri(board) == opp:
                board[u][v] = 0
                return (u,v)
            board[u][v] = 0
    return None

# ---------- rollout policy (heuristic) ----------
def rollout_policy_tri(state, turn):
    # 1) immediate win
    for m in empty_neighbors(state, padding=2):
        if state[m[0]][m[1]] == 0:
            state[m[0]][m[1]] = turn
            if check_winner_tri(state) == turn:
                state[m[0]][m[1]] = 0
                return m
            state[m[0]][m[1]] = 0
    # 2) block opponent immediate win
    opp = -turn
    for m in empty_neighbors(state, padding=2):
        if state[m[0]][m[1]] == 0:
            state[m[0]][m[1]] = opp
            if check_winner_tri(state) == opp:
                state[m[0]][m[1]] = 0
                return m
            state[m[0]][m[1]] = 0
    # 3) adjacency score sampling
    cands = empty_neighbors(state, padding=2)
    if not cands:
        cands = [p for p in LEGAL_POSITIONS if state[p[0]][p[1]] == 0]
    scored = []
    for (u,v) in cands:
        score = 0
        for du in range(-2,3):
            for dv in range(-2,3):
                uu = u+du
                vv = v+dv
                if (uu, vv) in LEGAL_SET:
                    if state[uu][vv] == turn:
                        score += 3
                    elif state[uu][vv] == -turn:
                        score += 1
        scored.append((score, (u,v)))
    scored.sort(reverse=True)
    topk = [mv for _, mv in scored[:max(1, min(6, len(scored)))]]
    return random.choice(topk)

def simulate_rollout_tri(state, turn, max_steps=200):
    board = [row[:] for row in state]
    cur = turn
    steps = 0
    while steps < max_steps:
        steps += 1
        mv = rollout_policy_tri(board, cur)
        if mv is None:
            return 2
        board[mv[0]][mv[1]] = cur
        w = check_winner_tri(board)
        if w != 0:
            return w
        cur = -cur
    return 0

# ---------- MCTS Node ----------
class Node:
    def __init__(self, state, to_play, parent=None, move=None):
        self.state = state
        self.to_play = to_play
        self.parent = parent
        self.move = move
        self.children = []
        self._untried = None
        self.visits = 0
        self.wins = 0.0

    def untried_moves(self):
        if self._untried is None:
            self._untried = empty_neighbors(self.state, padding=2)
        return self._untried

    def add_child(self, move, state, to_play):
        child = Node(state=state, to_play=to_play, parent=self, move=move)
        self.children.append(child)
        if self._untried and move in self._untried:
            self._untried.remove(move)
        return child

    def uct_select(self):
        best = None
        best_val = -1e9
        for c in self.children:
            if c.visits == 0:
                val = 1e9 + random.random()
            else:
                exploit = c.wins / c.visits
                explore = UCT_C * math.sqrt(math.log(self.visits) / c.visits)
                val = exploit + explore
            if val > best_val:
                best_val = val
                best = c
        return best

    def update(self, result, perspective):
        self.visits += 1
        if result == perspective:
            self.wins += 1.0
        elif result == 2:
            self.wins += 0.5

# ---------- AI (interface) ----------
def ai_move(board_in, color):
    """
    board_in: list of lists 15x15 (triangular game uses only LEGAL_POSITIONS)
    color: 1 (black) or -1 (white) - color of player to move (AI)
    returns (u,v) tuple
    """
    start = time.time()
    state0 = [list(row) for row in board_in]

    # quick rule
    quick = immediate_win_or_block(state0, color)
    if quick is not None:
        return quick

    root = Node(state=[row[:] for row in state0], to_play=color)

    while time.time() - start < TIME_LIMIT:
        node = root
        state = [row[:] for row in root.state]

        # Selection
        while node.untried_moves() == [] and node.children:
            node = node.uct_select()
            mr, mc = node.move
            state[mr][mc] = node.parent.to_play

        # Expansion
        untries = node.untried_moves()
        if untries:
            m = random.choice(untries)
            new_state = [row[:] for row in state]
            new_state[m[0]][m[1]] = node.to_play
            node = node.add_child(move=m, state=new_state, to_play=-node.to_play)
            state = new_state

        # Simulation
        winner = simulate_rollout_tri(state, node.to_play, max_steps=200)

        # Backpropagate
        cur = node
        while cur is not None:
            if cur.parent is None:
                perspective = color
            else:
                perspective = cur.parent.to_play
            cur.update(winner, perspective)
            cur = cur.parent

    # choose best child by visits
    best = None
    best_visits = -1
    for c in root.children:
        if c.visits > best_visits:
            best_visits = c.visits
            best = c
    if best is None:
        empties = [p for p in LEGAL_POSITIONS if board_in[p[0]][p[1]] == 0]
        return random.choice(empties) if empties else (0,0)
    return best.move

# alias if needed
computer_move = ai_move

# ---------- GUI integration ----------
def run_gui():
    if not PYGAME:
        print("pygame not installed. Install pygame to run GUI.")
        return

    pg.init()
    surf = uf.draw_board() if HAVE_UF and hasattr(uf, "draw_board") else None
    if surf is None:
        # if uf not available or draw_board missing, abort because your utility_func exists per earlier message
        print("utility_func.draw_board not available; GUI expects your utility_func.py")
        return

    # prepare empty board
    board = [[0]*BLINE for _ in range(BLINE)]
    # Human = black (1) first, AI = white (-1)
    # 先后手改这里
    human_color = -1
    ai_color = 1
    turn = 1  # human starts
    running = True

    # initial draw via uf.draw_board done in uf
    uf.print_turn(surf, turn)

    while running:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False
            elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                # click -> translate via your click2index
                pos = pg.mouse.get_pos()
                if HAVE_UF and hasattr(uf, "click2index"):
                    idx = uf.click2index(pos)
                else:
                    idx = False
                if idx and idx in LEGAL_SET:
                    u,v = idx
                    if board[u][v] == 0 and turn == human_color:
                        board[u][v] = human_color
                        uf.draw_stone(surf, (u,v), human_color)
                        # check win
                        w = check_winner_tri(board)
                        if w != 0:
                            uf.print_winner(surf, w)
                            turn = 0
                        else:
                            turn = -turn  # AI turn next
                # else: click outside triangle -> ignore
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_r:
                    board = [[0]*BLINE for _ in range(BLINE)]
                    turn = 1
                    uf.draw_board()
                    uf.print_turn(surf, turn)
                if ev.key == pg.K_SPACE:
                    # force AI move even if human's turn (AI vs AI debugging)
                    mv = ai_move(board, ai_color)
                    if board[mv[0]][mv[1]] == 0:
                        board[mv[0]][mv[1]] = ai_color
                        uf.draw_stone(surf, mv, ai_color)
                        w = check_winner_tri(board)
                        if w != 0:
                            uf.print_winner(surf, w)
                            turn = 0
                        else:
                            turn = -turn

        # If it's AI's turn and game not over -> compute AI move and draw it
        if turn == ai_color:
            mv = ai_move(board, ai_color)
            if board[mv[0]][mv[1]] == 0:
                board[mv[0]][mv[1]] = ai_color
                uf.draw_stone(surf, mv, ai_color)
                w = check_winner_tri(board)
                if w != 0:
                    uf.print_winner(surf, w)
                    turn = 0
                else:
                    turn = -turn

        if turn != 0:
            uf.print_turn(surf, turn)
        pg.time.wait(20)

    pg.quit()

if __name__ == "__main__":
    run_gui()

