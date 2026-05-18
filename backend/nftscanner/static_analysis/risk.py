def calculate_risk(issues):

    score = 0

    for issue in issues:

        severity = issue.get("severity", "").lower()

        # ---------------------------------
        # High severity
        # ---------------------------------
        if severity == "high":
            score += 10

        # ---------------------------------
        # Medium severity
        # ---------------------------------
        elif severity == "medium":
            score += 5

        # ---------------------------------
        # Low severity
        # ---------------------------------
        elif severity == "low":
            score += 1

        # ---------------------------------
        # Critical severity
        # ---------------------------------
        elif severity == "critical":
            score += 20

    return score
