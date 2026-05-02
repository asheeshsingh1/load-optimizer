# optimizer.py

from itertools import combinations

def is_valid_subset(subset, truck):
    total_weight = sum(o.weight_lbs for o in subset)
    total_volume = sum(o.volume_cuft for o in subset)

    if total_weight > truck.max_weight_lbs:
        return False
    if total_volume > truck.max_volume_cuft:
        return False

    # route check
    origins = {o.origin for o in subset}
    destinations = {o.destination for o in subset}

    if len(origins) > 1 or len(destinations) > 1:
        return False

    # hazmat check (simple version)
    hazmat_flags = {o.is_hazmat for o in subset}
    if len(hazmat_flags) > 1:
        return False

    return True


def optimize(truck, orders):
    best = None
    max_payout = 0

    n = len(orders)

    for mask in range(1 << n):
        subset = [orders[i] for i in range(n) if mask & (1 << i)]

        if not subset:
            continue

        if not is_valid_subset(subset, truck):
            continue

        payout = sum(o.payout_cents for o in subset)

        if payout > max_payout:
            max_payout = payout
            best = subset

    return best