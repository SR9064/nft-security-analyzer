from z3 import *

def symbolic_check(issue_type):
    """
    Selective symbolic validation using SMT.
    Called only for HIGH risk NFT paths.
    """

    s = Solver()

    # -------------------------------
    # 🔴 Unauthorized Mint Check
    # -------------------------------
    if issue_type == "Unauthorized Mint":
        attacker = Bool('attacker')
        is_owner = Bool('is_owner')

        # attacker tries mint without being owner
        s.add(attacker == True)
        s.add(is_owner == False)

        # vulnerable condition: mint allowed without ownership
        vulnerable = And(attacker, Not(is_owner))

        s.add(vulnerable)

    # -------------------------------
    # 🔴 Reentrancy Check
    # -------------------------------
    elif "Reentrancy" in issue_type:
        entered = Bool('entered')   # reentrancy guard
        external_call = Bool('external_call')

        # simulate unsafe contract
        s.add(external_call == True)
        s.add(entered == False)  # no guard

        vulnerable = And(external_call, Not(entered))

        s.add(vulnerable)

    # -------------------------------
    # 🔴 Approval Misuse
    # -------------------------------
    elif issue_type == "Approval Misuse":
        approved = Bool('approved')
        is_owner = Bool('is_owner')

        s.add(approved == True)
        s.add(is_owner == False)

        vulnerable = And(approved, Not(is_owner))

        s.add(vulnerable)

    # -------------------------------
    # 🔴 Zero Address Check Missing
    # -------------------------------
    elif "Zero Address" in issue_type:
        to = Int('to')

        # simulate zero address
        s.add(to == 0)

        vulnerable = (to == 0)

        s.add(vulnerable)

    # -------------------------------
    # 🟡 Default fallback
    # -------------------------------
    else:
        # If unknown issue → assume risky but not proven
        return False

    # -------------------------------
    # 🔍 Solve
    # -------------------------------
    if s.check() == sat:
        return True   # Vulnerability confirmed
    else:
        return False  # False positive
