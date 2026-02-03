def hanoi(n, source, target, aux, move_counter):
    if n == 0:
        return move_counter
    move_counter = hanoi(n-1, source, aux, target, move_counter)
    move_counter += 1
    print(f"Move {move_counter}: Move disk {n} from {source} -> {target}")
    move_counter = hanoi(n-1, aux, target, source, move_counter)
    return move_counter

def main():
    N = 5  # number of disks
    print(f"Tower of Hanoi — {N} disks (minimal recursive solution)")
    total = hanoi(N, 'A', 'C', 'B', 0)
    print(f"Total moves: {total}")

if __name__ == "__main__":
    main()
