def classify_severity(score: int,):
    if score >= 80:
        return "critical"
    
    if score >= 60:
        return "high"
    
    if score >= 40:
        return "medium"
    
    if score >= 20:
        return "low"
    
    return "info"