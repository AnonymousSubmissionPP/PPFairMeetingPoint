import random

 
FIELD_SIZE = 11**6

def shares(n, s):
    """
    Randomly generate a list of t shares given n participants and a secert s
    """
    shares = [random.randint(1, FIELD_SIZE) for _ in range(n - 1)]
    shares.append(s-sum(shares))
    return shares
