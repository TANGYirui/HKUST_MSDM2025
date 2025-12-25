# 使用方法：
#   1. 将此文件与你的 utility_func.py 放在同一目录
#   2. 运行： python final_triangle_AI.py
#
# 关闭调试终端日志（只留 GUI 显示 AI 落子）：在本文件顶部把 DEBUG = True 注释掉或改为 False。
#
# 导出接口：
#   ai_move(board, color) -> (u, v)  # 供自动PK脚本调用（board 为 15x15 的 list-of-lists）

import time
import math
import random
import copy
import sys


import pygame as pg

# 保持对 utility_func.py 在同一路径下
import utility_func as uf

# ----------------- DEBUG switch -----------------
# 注：把下面这一行注释掉或改为 False 可以一行关闭所有终端日志
DEBUG = True

# If the user commented out DEBUG line above, ensure DEBUG defined
if 'DEBUG' not in globals():
    DEBUG = False


# ----------------- Configuration -----------------
BLINE = 15
SEARCH_TIME = 5.0     # MCTS time per move (course requirement)
UCT_C = 1.0

# Directions for tri board (as requested): vertical (1,0), horizontal (0,1), diag (1,-1)
DIRECTIONS = [(1, 0), (0, 1), (1, -1)]

# Build legal positions for a top row of 15 points triangle:
# u from 0..14 (row), v from 0..(14 - u)
LEGAL_POSITIONS = [(u, v) for u in range(BLINE) for v in range(BLINE) if v <= (BLINE - 1 - u)]
LEGAL_SET = set(LEGAL_POSITIONS)

# ----------------- Utility functions -----------------
def is_legal(u, v):
    return (u, v) in LEGAL_SET

def board_copy(board):
    return [row[:] for row in board]

def check_winner(board):
    """
    Return: 1 (black) / -1 (white) / 0 (no winner) / 2 (draw)
    """
    full = True
    for u, v in LEGAL_POSITIONS:
        val = board[u][v]
        if val == 0:
            full = False
            continue
        for du, dv in DIRECTIONS:
            cnt = 1
            for k in range(1, 5):
                uu = u + du * k
                vv = v + dv * k
                if (uu, vv) in LEGAL_SET and board[uu][vv] == val:
                    cnt += 1
                else:
                    break
            if cnt >= 5:
                return val
    return 2 if full else 0

def neighbors_positions(board, padding=2):
    """
    Return empty neighbor positions within 'padding' of any occupied stone.
    If board empty, return an upper-middle preference (better than corner).
    """
    occ = []
    for u, v in LEGAL_POSITIONS:
        if board[u][v] != 0:
            occ.append((u, v))
    if not occ:
        # choose a sensible start near upper-middle for inverted triangle
        mid_u = max(0, BLINE // 3)           # push toward upper rows (smaller u)
        # ideal v for row mid_u (center of that row)
        mid_v = int(round((BLINE - 1 - mid_u) / 2.0))
        mid = (mid_u, mid_v)
        if mid in LEGAL_SET:
            return [mid]
        # fallback to the previous top-middle if something odd
        fallback = (0, (BLINE - 1) // 2)
        if fallback in LEGAL_SET:
            return [fallback]
        return LEGAL_POSITIONS[:]
    cands = set()
    for (u, v) in occ:
        for du in range(-padding, padding + 1):
            for dv in range(-padding, padding + 1):
                uu = u + du
                vv = v + dv
                if (uu, vv) in LEGAL_SET and board[uu][vv] == 0:
                    cands.add((uu, vv))
    if not cands:
        return [p for p in LEGAL_POSITIONS if board[p[0]][p[1]] == 0]
    return list(cands)


# ----------------- Pattern-based heuristics (强力部分) -----------------
def immediate_win_or_block(board, turn):
    """
    First-level check: immediate win for 'turn', otherwise immediate block for opponent.
    """
    # win
    for u, v in LEGAL_POSITIONS:
        if board[u][v] != 0: continue
        board[u][v] = turn
        if check_winner(board) == turn:
            board[u][v] = 0
            if DEBUG: print("[HEUR] Immediate win at", (u, v))
            return (u, v)
        board[u][v] = 0
    # block opponent
    opp = -turn
    for u, v in LEGAL_POSITIONS:
        if board[u][v] != 0: continue
        board[u][v] = opp
        if check_winner(board) == opp:
            board[u][v] = 0
            if DEBUG: print("[HEUR] Immediate block at", (u, v))
            return (u, v)
        board[u][v] = 0
    return None

def count_line_pattern(board, turn, u, v, du, dv):
    """
    Count contiguous stones of 'turn' including (u,v) in both directions (like for pattern checks).
    """
    cnt = 1
    # forward
    for k in range(1, 6):
        uu = u + du * k
        vv = v + dv * k
        if (uu, vv) in LEGAL_SET and board[uu][vv] == turn:
            cnt += 1
        else:
            break
    # backward
    for k in range(1, 6):
        uu = u - du * k
        vv = v - dv * k
        if (uu, vv) in LEGAL_SET and board[uu][vv] == turn:
            cnt += 1
        else:
            break
    return cnt

def find_four_like_moves(board, turn):
    """
    Find moves that create a (forcible) four-in-line (i.e., 4 in 5 with one empty).
    Return list of moves that produce such 'four-like' (strong threats).
    """
    res = []
    for u, v in LEGAL_POSITIONS:
        if board[u][v] != 0: continue
        # try placing
        board[u][v] = turn
        # check if there exists any direction where there are 4 contiguous of turn within 5-window
        found = False
        for du, dv in DIRECTIONS:
            # Check windows of length 5 that include (u,v)
            # iterate offset of window start from -4..0 such that (u,v) is inside
            for offset in range(-4, 1):
                cnt = 0
                empties = 0
                empty_pos = None
                ok_window = True
                for k in range(5):
                    uu = u + du * (offset + k)
                    vv = v + dv * (offset + k)
                    if (uu, vv) not in LEGAL_SET:
                        ok_window = False
                        break
                    val = board[uu][vv]
                    if val == turn:
                        cnt += 1
                    elif val == 0:
                        empties += 1
                        empty_pos = (uu, vv)
                    else:
                        # opponent stone blocks this window
                        ok_window = False
                        break
                if ok_window and cnt == 4 and empties == 1:
                    found = True
                    break
            if found:
                break
        board[u][v] = 0
        if found:
            res.append((u, v))
    return res

def count_open_three(board, turn, u, v):
    """
    After placing at (u,v) for turn, count how many 'open three' (three with both ends open) are created.
    Simplified detection: a window of length 5 that contains exactly three turn stones and two empties, and empties are at ends.
    """
    cnt_open = 0
    board[u][v] = turn
    for du, dv in DIRECTIONS:
        for offset in range(-4, 1):
            positions = []
            ok = True
            tcount = 0
            empties = []
            for k in range(5):
                uu = u + du * (offset + k)
                vv = v + dv * (offset + k)
                positions.append((uu, vv))
                if (uu, vv) not in LEGAL_SET:
                    ok = False
                    break
                val = board[uu][vv]
                if val == turn:
                    tcount += 1
                elif val == 0:
                    empties.append((uu, vv))
                else:
                    ok = False
                    break
            if not ok:
                continue
            # open three pattern: exactly 3 stones and two empties at ends
            if tcount == 3 and len(empties) == 2:
                # check empties at ends condition (ends are positions[0] and positions[4])
                if positions[0] in empties and positions[4] in empties:
                    cnt_open += 1
    board[u][v] = 0
    return cnt_open

def find_double_open_threes(board, turn):
    """
    Find moves that create at least two open-threes (double-threat), which is often decisive.
    """
    moves = []
    for u, v in LEGAL_POSITIONS:
        if board[u][v] != 0: continue
        num = count_open_three(board, turn, u, v)
        if num >= 2:
            moves.append((u, v))
    return moves

def block_opponent_future_forks(board, turn):
    opp = -turn
    dangerous_moves = []

    for u, v in LEGAL_POSITIONS:
        if board[u][v] != 0: continue

        board[u][v] = opp
        # After opponent plays here, do they get >=2 open-threes?
        cnt = count_open_three(board, opp, u, v)
        board[u][v] = 0

        if cnt >= 2:
            dangerous_moves.append((u, v))

    if dangerous_moves:
        if DEBUG:
            print("[HEUR] Prevent opponent fork:", dangerous_moves)
        return dangerous_moves[0]

    return None

def creates_double_threat_after_move(board, turn, move):
    """
    检测：在 board 上先手放 move，为 turn（放完后），
    是否会产生 >=2 个独立的 open-three / four-like 威胁（即双威胁）
    """
    u, v = move
    if board[u][v] != 0:
        return False
    board[u][v] = turn
    # count number of distinct critical threat squares opponent must block next
    threats = set()
    # scan all empty squares; if playing there gives immediate win for turn, that's a threat position
    for x, y in LEGAL_POSITIONS:
        if board[x][y] != 0:
            continue
        board[x][y] = turn
        if check_winner(board) == turn:
            threats.add((x, y))
        board[x][y] = 0
    board[u][v] = 0
    return len(threats) >= 2

def solve_two_step_kill(board, color):
    """
    For current player 'color', check if there exists a move m such that:
      - after playing m, no matter what opponent does (one move),
        current player can force a win on next move.
    That indicates a forced 2-ply kill; prefer such moves.
    Returns a winning move (u,v) or None.
    """
    # Candidate moves: neighbors + all forced heuristic moves
    cands = neighbors_positions(board, padding=2)
    # also include moves found by heuristics to not miss important ones
    for (u,v) in LEGAL_POSITIONS:
        if board[u][v] != 0: continue
        if (u,v) not in cands:
            cands.append((u,v))

    for m in cands:
        # simulate playing m
        u, v = m
        board[u][v] = color
        # now check: can opponent find any reply r that stops our immediate win next?
        opp = -color
        opp_can_stop_all = False
        # list all opponent replies (only neighbors to reduce branching)
        opp_replies = neighbors_positions(board, padding=2)
        if not opp_replies:
            opp_replies = [p for p in LEGAL_POSITIONS if board[p[0]][p[1]] == 0]
        # If there exists an opponent reply r such that we cannot win next, then m is not forced kill
        for r in opp_replies:
            rx, ry = r
            if board[rx][ry] != 0:
                continue
            board[rx][ry] = opp
            # check whether we (color) have a direct winning move now
            win_found = False
            for x,y in LEGAL_POSITIONS:
                if board[x][y] != 0: continue
                board[x][y] = color
                if check_winner(board) == color:
                    win_found = True
                    board[x][y] = 0
                    break
                board[x][y] = 0
            board[rx][ry] = 0
            if not win_found:
                opp_can_stop_all = True
                break
        board[u][v] = 0
        if not opp_can_stop_all:
            # for every opponent reply we still have a winning move -> forced 2-ply kill
            if DEBUG: print("[TSS] Two-step kill found at", m)
            return m
    return None

def attack_score(board, color):
    """
    Improved center gravity for an INVERTED triangle:
    Prefer upper-middle area instead of deep bottom corner.
    """
    best = None
    best_score = -1

    CENTER_U = BLINE // 3   # move toward top (smaller u)
    # center v depends on row width
    # roughly half of width of row u
    def ideal_v(u):
        return (BLINE - 1 - u) / 2

    for u, v in LEGAL_POSITIONS:
        if board[u][v] != 0:
            continue

        score = 0

        # ---- Center Gravity: prefer upper-middle ----
        du = abs(u - CENTER_U)
        dv = abs(v - ideal_v(u))

        score -= du * 40    # farther from top-middle = worse
        score -= dv * 40

        # ---- Local tactical influence ----
        for du2 in range(-2, 3):
            for dv2 in range(-2, 3):
                uu = u + du2
                vv = v + dv2
                if (uu, vv) in LEGAL_SET:
                    if board[uu][vv] == color:
                        score += 120
                    elif board[uu][vv] == -color:
                        score += 30

        if score > best_score:
            best_score = score
            best = (u, v)

    if best_score <= 0:
        return None

    if DEBUG:
        print(f"[ATTACK-center-fixed] best={best}  score={best_score}")

    return best

def forced_move_stronger(board, turn):
    """
    Compose heuristic: immediate win/block -> four-like -> block opponent's four-like -> double-open-three -> open-three -> else None
    """
    # immediate
    mv = immediate_win_or_block(board, turn)
    if mv: return mv

    # block opponent future deadly fork
    mv = block_opponent_future_forks(board, turn)

    # my four-like (strong attack)
    my_fours = find_four_like_moves(board, turn)
    if my_fours:
        if DEBUG: print("[HEUR] My four-like moves:", my_fours)
        return my_fours[0]

    # opponent fours block
    opp = -turn
    opp_fours = find_four_like_moves(board, opp)
    if opp_fours:
        if DEBUG: print("[HEUR] Block opponent four:", opp_fours)
        return opp_fours[0]

    # double open threes (winning fork)
    my_double_threes = find_double_open_threes(board, turn)
    if my_double_threes:
        if DEBUG: print("[HEUR] My double open threes:", my_double_threes)
        return my_double_threes[0]

    # open three (aggressive)
    # we pick the best open-three by count
    best = None
    best_score = -1
    for u, v in LEGAL_POSITIONS:
        if board[u][v] != 0: continue
        score = count_open_three(board, turn, u, v)
        if score > best_score:
            best_score = score
            best = (u, v)
    if best_score > 0:
        if DEBUG: print("[HEUR] My best open three:", best, "score", best_score)
        return best

    return None

# ----------------- Rollout policy -----------------
def rollout_policy(board, turn):
    """
    Heuristic rollout: prefer forced moves, adjacency + center-control, random among top-k
    Safe against empty topk and near-full board
    """
    # Forced win/block first
    mv = immediate_win_or_block(board, turn)
    if mv:
        return mv

    # local candidate region
    cands = neighbors_positions(board, padding=2)
    if not cands:
        # fallback to all empty legal positions
        cands = [(u, v) for u, v in LEGAL_POSITIONS if board[u][v] == 0]
        if not cands:
            return None  # board full → signal draw

    scored = []
    for (u, v) in cands:
        if board[u][v] != 0:
            continue

        score = 0.0

        # adjacency heuristic
        for du in range(-2, 3):
            for dv in range(-2, 3):
                uu = u + du
                vv = v + dv
                if (uu, vv) in LEGAL_SET:
                    if board[uu][vv] == turn:
                        score += 3.0
                    elif board[uu][vv] == -turn:
                        score += 1.0

        # center control (avoid always corner move)
        cu, cv = max(0, BLINE // 2), max(0, (BLINE - 1) // 2)  # safe approximate center
        score -= 0.15 * (abs(u - cu) + abs(v - cv))

        scored.append((score, (u, v)))

    if not scored:
        return None  # still safe fallback

    # sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # top-k but safe: ensure ≥1
    k = max(1, min(6, len(scored)))
    topk = [mv for _, mv in scored[:k]]

    # defensive guard: if topk somehow empty, pick random legal empty
    if not topk:
        empties = [(u, v) for u, v in LEGAL_POSITIONS if board[u][v] == 0]
        if not empties:
            return None
        return random.choice(empties)

    return random.choice(topk)


def simulate_rollout(board, turn, max_steps=200):
    b = board_copy(board)
    cur = turn
    for _ in range(max_steps):
        mv = rollout_policy(b, cur)
        if mv is None:
            return 2
        b[mv[0]][mv[1]] = cur
        w = check_winner(b)
        if w != 0:
            return w
        cur = -cur
    return 0

# ----------------- MCTS -----------------
class MCTSNode:
    def __init__(self, state, to_play, move=None, parent=None):
        self.state = state
        self.to_play = to_play
        self.move = move
        self.parent = parent
        self.children = []
        self.untried = None
        self.visits = 0
        self.wins = 0.0  # wins for perspective = parent.to_play

    def get_untried(self):
        if self.untried is None:
            self.untried = neighbors_positions(self.state, padding=2)
        return self.untried

    def uct_select(self):
        best = None
        best_val = -1e9
        for c in self.children:
            if c.visits == 0:
                val = float('inf')
            else:
                exploit = c.wins / c.visits
                explore = UCT_C * math.sqrt(math.log(self.visits) / c.visits)
                val = exploit + explore
            if val > best_val:
                best_val = val
                best = c
        return best

    def add_child(self, move, state, to_play):
        child = MCTSNode(state=state, to_play=to_play, move=move, parent=self)
        self.children.append(child)
        if self.untried and move in self.untried:
            self.untried.remove(move)
        return child

    def update(self, winner, perspective):
        self.visits += 1
        if winner == perspective:
            self.wins += 1.0
        elif winner == 2:
            self.wins += 0.5

def mcts_search(root_state, color, time_limit=SEARCH_TIME):
    root = MCTSNode(state=board_copy(root_state), to_play=color)
    start = time.time()
    iters = 0
    while time.time() - start < time_limit:
        node = root
        state = board_copy(root.state)

        # Selection
        while node.get_untried() == [] and node.children:
            node = node.uct_select()
            # play node.move on state: parent.to_play moved to child
            mr, mc = node.move
            state[mr][mc] = node.parent.to_play

        # Expansion
        untries = node.get_untried()
        if untries:
            m = random.choice(untries)
            new_state = board_copy(state)
            new_state[m[0]][m[1]] = node.to_play
            node = node.add_child(m, new_state, -node.to_play)
            state = new_state

        # Simulation
        winner = simulate_rollout(state, node.to_play, max_steps=200)

        # Backpropagate
        cur = node
        while cur is not None:
            if cur.parent is None:
                perspective = color
            else:
                perspective = cur.parent.to_play
            cur.update(winner, perspective)
            cur = cur.parent

        iters += 1

    # pick best child by visits
    best_child = None
    best_visits = -1
    for c in root.children:
        if c.visits > best_visits:
            best_visits = c.visits
            best_child = c
    if best_child is None:
        empties = [p for p in LEGAL_POSITIONS if root_state[p[0]][p[1]] == 0]
        return random.choice(empties) if empties else (0, 0)
    return best_child.move

# ----------------- Top-level AI move -----------------
def computer_move(board_in, color):
    """
    board_in: 15x15 list-of-lists, color = 1 (black) or -1 (white)
    returns (u, v)
    """
    board = board_copy(board_in)

    # 0) quick immediate checks first
    mv = immediate_win_or_block(board, color)
    if mv:
        if DEBUG: print("[AI-Heur] Immediate:", mv)
        return mv

    # 1) check for forced two-step kill (TSS) for me
    mv = solve_two_step_kill(board, color)
    if mv:
        if DEBUG: print("[AI-Heur] Two-step kill (me):", mv)
        return mv

    # 2) prevent opponent two-step kill (TSS defense)
    mv = solve_two_step_kill(board, -color)
    if mv:
        # if opponent has a two-step kill, we must block a key square
        # try blocking by playing at one of opponent's critical reply squares:
        if DEBUG: print("[AI-Heur] Opponent two-step kill threat detected, try to block:", mv)
        # pick a neighbor blocking square (prefer the actual move)
        if board[mv[0]][mv[1]] == 0:
            return mv
        # otherwise fallthrough to more general block
    # 3) block opponent future forks (double open-three)
    mv = block_opponent_future_forks(board, color)
    if mv:
        if DEBUG: print("[AI-Heur] Block opponent future fork:", mv)
        return mv

    # 4) choose aggressive move (try to make forks)
    mv = attack_score(board, color)
    if mv:
        if DEBUG: print("[AI-Heur] Attack move:", mv)
        return mv

    # 5) previous combined heuristics (fallback)
    mv = forced_move_stronger(board, color)
    if mv:
        if DEBUG: print("[AI-Heur] Forced fallback:", mv)
        return mv

    # 6) final fallback: MCTS with SEARCH_TIME
    if DEBUG:
        print("[AI] Running MCTS for up to", SEARCH_TIME, "s ...")
    mv = mcts_search(board, color, time_limit=SEARCH_TIME)
    if DEBUG:
        print("[AI] MCTS chosen:", mv)
    return mv

# highlight last move on board
def draw_last_edge(surf, last_move, board=None):
    """
    Draw a red edge around last_move (u,v).
    Prefer to use uf.draw_highlighted_stone (keeps coordinates consistent).
    board: optional current board to extract stone color (1 or -1).
    """
    if last_move is None:
        return
    u, v = last_move

    # Prefer using utility function's highlight (keeps coordinates exact)
    try:
        if hasattr(uf, "draw_highlighted_stone"):
            color = None
            if board is not None:
                try:
                    color = board[u][v]
                except Exception:
                    color = None
            # If color missing or 0, just pick a red highlight that won't overwrite stone badly:
            if color is None or color == 0:
                # use 2 as fallback (utility_func treats 2 as black+green border),
                # but we want red border: for safety pass 1 (black with red border)
                # If the actual stone was white this will redraw black under it — it's only fallback.
                color = 1
            # draw_highlighted_stone also draws the stone itself, so it's safe and aligned
            uf.draw_highlighted_stone(surf, (u, v), color)
            return
    except Exception:
        # fall through to manual drawing fallback
        pass

    # Fallback: try to reconstruct pixel center from uf parameters (defensive)
    center = None
    try:
        pad_x = getattr(uf, "pad_x", None)
        pad_y = getattr(uf, "pad_y", None)
        sep_x = getattr(uf, "sep_x", None)
        sep_y = getattr(uf, "sep_y", None)
        if pad_x is not None and pad_y is not None and sep_x is not None and sep_y is not None:
            cx = int(round(pad_x + u * sep_x/2 + v * sep_x))
            cy = int(round(pad_y + u * sep_y))
            center = (cx, cy)
    except Exception:
        center = None

    # As ultimate fallback, try other names pad/sep
    if center is None:
        try:
            pad = getattr(uf, "pad", None)
            sep = getattr(uf, "sep", None)
            if pad is not None and sep is not None:
                cx = int(round(pad + (v + 4) * sep))
                cy = int(round(pad + (u + 4) * sep))
                center = (cx, cy)
        except Exception:
            center = None

    # fallback if still none: use surface central-ish pos
    if center is None:
        try:
            w, h = surf.get_size()
            center = (w // 2, h // 4)
        except Exception:
            return

    # radius guess (try piece_radius if available)
    radius = None
    try:
        radius = int(getattr(uf, "piece_radius", 0) or 0)
    except Exception:
        radius = None
    if not radius:
        try:
            sep_x = getattr(uf, "sep_x", None)
            if sep_x:
                radius = max(6, int(sep_x * 0.3))
            else:
                w, h = surf.get_size()
                radius = max(6, min(w, h) // 40)
        except Exception:
            radius = 8

    try:
        pg.draw.circle(surf, (255, 0, 0), center, radius + 2, width=3)
    except Exception:
        pass


# ----------------- MAIN GAME LOOP -----------------
def main(player_is_black=False):
    """
    player_is_black=True  → Human is Black goes first
    player_is_black=False → AI is Black goes first
    """
    pg.init()
    surf = uf.draw_board()
    board = [[0] * BLINE for _ in range(BLINE)]
    last_move = None

    # Assign colors based on who goes first
    if player_is_black:
        human_color = 1
        ai_color = -1
        turn = 1  # human places black first
    else:
        human_color = -1
        ai_color = 1
        turn = 1  # AI places black first

    if DEBUG:
        print(f"[INFO] Human={human_color}, AI={ai_color}, TURN={turn}")

    # If AI goes first → make the first move immediately
    if ai_color == 1 and turn == 1:
        mv = computer_move(board, ai_color)
        u, v = mv
        board[u][v] = ai_color
        uf.draw_stone(surf, (u, v), ai_color)
        last_move = (u, v)
        # highlight the first move
        draw_last_edge(surf, last_move, board)
        turn = -turn
        try: uf.print_turn(surf, turn)
        except: pass

    running = True
    gameover = False

    while running:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False
            if ev.type == pg.KEYDOWN and ev.key == pg.K_q:
                running = False

            # Human move
            # inside main(): Human move branch (replace original block handling drawing)
            if (not gameover) and turn == human_color and ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                pos = pg.mouse.get_pos()
                idx = uf.click2index(pos)
                if idx and idx in LEGAL_SET:
                    u, v = idx
                    if board[u][v] == 0:
                        board[u][v] = human_color
                        # redraw board surface (defensive): uf.draw_board may return new surface or update global surface
                        try:
                            surf = uf.draw_board()
                        except Exception:
                            pass
                        # draw all stones from board (in case uf.draw_board clears surface)
                        for uu, vv in LEGAL_POSITIONS:
                            if board[uu][vv] != 0:
                                uf.draw_stone(surf, (uu, vv), board[uu][vv])
                        last_move = (u, v)
                        draw_last_edge(surf, last_move, board)

                        w = check_winner(board)
                        if w != 0:
                            uf.print_winner(surf, w)
                            gameover = True
                        else:
                            turn = -turn
                            try: uf.print_turn(surf, turn)
                            except: pass


        # AI move
        # AI move branch (replace original block)
        if (not gameover) and turn == ai_color:
            mv = computer_move(board, ai_color)
            u, v = mv
            board[u][v] = ai_color

            try:
                surf = uf.draw_board()
            except Exception:
                pass
            for uu, vv in LEGAL_POSITIONS:
                if board[uu][vv] != 0:
                    uf.draw_stone(surf, (uu, vv), board[uu][vv])
            last_move = (u, v)
            draw_last_edge(surf, last_move, board)

            w = check_winner(board)
            if w != 0:
                uf.print_winner(surf, w)
                gameover = True
            else:
                turn = -turn
                try: uf.print_turn(surf, turn)
                except: pass

            pg.time.wait(40)


    pg.quit()


# ----------------- Run script -----------------
if __name__ == "__main__":
    # Default: AI first (Black)
    main(player_is_black=False)
