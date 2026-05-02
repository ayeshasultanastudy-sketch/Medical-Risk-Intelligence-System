def calculate_risk(age, bmi, smoking, activity, diet):
    
    score = 0

    if age > 50:
        score += 2
    if bmi > 30:
        score += 2
    if smoking:
        score += 3
    if activity == "Low":
        score += 2
    if diet < 4:
        score += 1

    # Normalize to percentage
    risk_percent = min(score * 10, 100)

    return risk_percent