def validate_feature_columns(df, features):
    missing = [c for c in features if c not in df.columns]
    if missing:
        raise ValueError(f"Missing features: {missing}")
    return True
