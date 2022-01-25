from logic import *
import python

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
AKnightClaim = Symbol("I am a Knight")
AKnaveClaim = Symbol("I am a Knave")
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(And(AKnightClaim, AKnaveClaim), AKnave),
    AKnightClaim,
    AKnaveClaim
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnave, BKnight),
    Implication(AKnaveClaim, AKnave),
    AKnaveClaim
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
BDifferentKind = Symbol("We are different kinds")
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Biconditional(AKnight, BKnave),
    Biconditional(AKnave, BKnight),
    BDifferentKind,
    Implication(BDifferentKind, BKnight),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight, CKnight),
    Biconditional(AKnave, CKnave),
    Biconditional(CKnave, BKnight),
    Biconditional(CKnight, BKnave),
    BKnave
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
