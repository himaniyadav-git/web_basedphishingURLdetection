# src/features.py
import numpy as np

# List of keywords that usually appear in phishing URLs
KEYWORDS = ['login', 'secure', 'account', 'bank', 'verify', 'update', 'signin']

def extract_features_from_url(url):
    """
    Extract simple numeric features from a URL.
    These must match the features used while training your model.
    """
    u = str(url).strip()
    u_lower = u.lower()

    url_len = len(u)
    count_at = u_lower.count('@')
    count_dash = u_lower.count('-')
    count_dot = u_lower.count('.')
    count_slash = u_lower.count('/')
    has_https = 1 if 'https' in u_lower else 0
    kw_count = sum(1 for k in KEYWORDS if k in u_lower)

    features = [url_len, count_at, count_dash, count_dot, count_slash, has_https, kw_count]
    return np.array(features, dtype=float)
