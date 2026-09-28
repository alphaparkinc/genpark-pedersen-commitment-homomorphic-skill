from client import PedersenCommitment

def main():
    val = 12500  # Private agent budget
    C, r = PedersenCommitment.commit(val)
    print("Pedersen Commitment point X:", hex(C[0])[:16], "...")
    print("Commitment Validated:", PedersenCommitment.verify(C, val, r))

if __name__ == "__main__":
    main()
