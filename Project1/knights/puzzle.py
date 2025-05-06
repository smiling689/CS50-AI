from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
P0_A =  And(AKnave, AKnight)
knowledge0 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),

    Or(And(AKnave,Not(P0_A)),And(AKnight,P0_A)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
P1_A = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),


    Or(And(AKnave,Not(P1_A)),And(AKnight,P1_A)),
    Or(And(BKnave,Not(BKnave)),And(BKnight,(BKnight))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
P2_A = Or(And(AKnave, BKnave),And(AKnight, BKnight))
P2_B = Or(And(AKnave, BKnight),And(AKnight, BKnave))
knowledge2 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),

    Or(And(AKnave,Not(P2_A)),And(AKnight,P2_A)),
    Or(And(BKnave,Not(P2_B)),And(BKnight,(P2_B))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    Or(AKnight,AKnave),Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),Not(And(BKnight,BKnave)),
    Or(CKnight,CKnave),Not(And(CKnight,CKnave)),
    Implication(AKnight,Or(AKnave,AKnight)),
    Implication(AKnave,Not(Or(AKnave,AKnight))),
    Implication(BKnight ,And(Not(Implication(AKnight,Or(AKnave,AKnight))),Implication(AKnight,Or(AKnave,AKnight)))),
    Implication(BKnave ,Not(And(Not(Implication(AKnight,Or(AKnave,AKnight))),Implication(AKnight,Or(AKnave,AKnight))))),
    Implication(BKnight,CKnave),
    Implication(BKnave,CKnight),
    Implication(CKnight,AKnight),
    Implication(CKnave,AKnave)
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
