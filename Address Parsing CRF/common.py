import re



components = {
    "au": ["house_name", "unit", "house_number", "street", "suburb", "city", "state", "postcode", "country"],
    "jp": ["state", "city", "street", "house_number", "unit", "postcode", "country"]
}

def remove_control_chars(s):
    # remove control characters
    s = re.sub("[\x00-\x1f\x7f\u0080-\u009f]+", '', s)
    # replace `NO-BREAK SPACE`
    return re.sub("\u00a0+", ' ', s)

def contains_digit(s):
    for c in s:
        if c.isdigit():
            return True
    else:
        return False

def token2feature(prev_token, token, next_token):
    # for now, use features from https://sklearn-crfsuite.readthedocs.io/en/latest/tutorial.html
    features = {
        'bias': 1.0,
        'token[-3:]': token[-3:],
        'token[-2:]': token[-2:],
        'token.lower()': token.lower(),
        'token.isupper()': token.isupper(),
        'token.istitle()': token.istitle(),
        'token.isdigit()': contains_digit(token)
    }

    if prev_token:
        features.update({
            '-1:token.lower()': prev_token.lower(),
            '-1:token.isupper()': prev_token.isupper(),
            '-1:token.istitle()': prev_token.istitle()
        })
    else:
        features['BOS'] = True

    if next_token:
        features.update({
            '+1:token.lower()': next_token.lower(),
            '+1:token.isupper()': next_token.isupper(),
            '+1:token.istitle()': next_token.istitle()
        })
    else:
        features['EOS'] = True

    return features