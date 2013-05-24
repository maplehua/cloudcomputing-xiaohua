from settings import RESULT_SIZE

def gen_pos(pos):
    pre = 0 if (0 == pos) else (pos - RESULT_SIZE)
    post = pos + RESULT_SIZE
    cur = pos + 1
    return (pre, cur, post)
