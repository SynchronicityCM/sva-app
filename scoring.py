"""
SVA Scoring Engine — Version 2
Synchronicity Change Management · April 2026
"""

from items import LEVELS, RANK_CONVERSION


def convert_acceptance_score(rank, intensity):
    """Convert rank + intensity to acceptance score using conversion table."""
    key = (rank, intensity)
    return RANK_CONVERSION.get(key, 2.70)


def compute_acceptance_scores(rank_order, intensities):
    """
    rank_order: dict {level: rank_position (1-7)}
    intensities: dict {level: intensity_label or None}
    Returns: dict {level: acceptance_score}
    """
    scores = {}
    for level in LEVELS:
        rank = rank_order.get(level)
        intensity = intensities.get(level)
        if rank is None:
            scores[level] = 2.70
        else:
            scores[level] = convert_acceptance_score(rank, intensity)
    return scores


def compute_shadow_scores(shadow_responses):
    """
    shadow_responses: dict {level: [score1, score2, score3]}
    where scores are 1–5 (1=Strongly agree, 5=Disagree)
    Returns: dict {level: mean_shadow_score}
    Note: shadow items are agreement items — higher agreement = higher shadow
    We invert the scale: 1=Strongly agree → 5, 5=Disagree → 1
    """
    scores = {}
    for level in LEVELS:
        responses = shadow_responses.get(level, [3, 3, 3])
        # Invert: Strongly agree (1) = highest shadow (5)
        inverted = [6 - r for r in responses]
        scores[level] = sum(inverted) / len(inverted) if inverted else 3.0
    return scores


def compute_shadow_ratios(acceptance_scores, shadow_scores):
    """Returns dict {level: shadow_ratio}"""
    ratios = {}
    for level in LEVELS:
        acc = acceptance_scores.get(level, 2.70)
        shad = shadow_scores.get(level, 3.0)
        if acc > 0:
            ratios[level] = round(shad / acc, 3)
        else:
            ratios[level] = 1.000
    return ratios


def compute_net_cog_scores(acceptance_scores, shadow_scores):
    """Net CoG = Acceptance - (Shadow × 0.30)"""
    net = {}
    for level in LEVELS:
        acc = acceptance_scores.get(level, 2.70)
        shad = shadow_scores.get(level, 3.0)
        net[level] = round(acc - (shad * 0.30), 3)
    return net


def classify_access(shadow_ratio):
    """Classify access quality from shadow ratio."""
    if shadow_ratio < 0.70:
        return 'Full access'
    elif shadow_ratio < 0.85:
        return 'Partial access'
    elif shadow_ratio < 1.00:
        return 'Unstable access'
    else:
        return 'Shadow primary'


def determine_cog(acceptance_scores, shadow_ratios, net_cog_scores):
    """
    Determine operative CoG using grounding chain.
    Returns: {
        'operative_cog': level or None,
        'grounding_status': description,
        'aspirational': level or None,
        'access_profile': {level: classification},
    }
    """
    access_profile = {level: classify_access(shadow_ratios[level]) for level in LEVELS}

    # Check for aspirational levels (above current CoG)
    aspirational = None

    # Find operative CoG — highest level with full or partial access
    # grounding chain: starts at Purple, each level grounds the next
    operative_cog = None
    grounding_status = {}

    grounded = True
    for level in LEVELS:
        ratio = shadow_ratios[level]
        acc_score = acceptance_scores[level]
        access = access_profile[level]

        if not grounded:
            grounding_status[level] = 'Not grounded — foundation above not established'
            continue

        if access == 'Full access':
            grounding_status[level] = 'Fully grounded'
            operative_cog = level
        elif access == 'Partial access':
            grounding_status[level] = 'Partially grounded'
            operative_cog = level
        elif access == 'Unstable access':
            grounding_status[level] = 'Conditional — partial grounding (Option A)'
            operative_cog = f'{level} (Conditional)'
            grounded = False  # Unstable breaks the chain
        else:  # Shadow primary
            grounding_status[level] = 'Not grounded — shadow primary'
            grounded = False

    # Check for aspirational
    for level in LEVELS:
        ratio = shadow_ratios[level]
        acc = acceptance_scores[level]
        if ratio >= 1.00 and acc >= 4.50:
            # Check variance across acceptance items
            # Simplified — flag as aspirational candidate
            aspirational = level

    return {
        'operative_cog': operative_cog,
        'grounding_status': grounding_status,
        'aspirational': aspirational,
        'access_profile': access_profile,
    }


def compute_self_group(acceptance_scores):
    """
    Self/Group derived from acceptance scores.
    Self levels: Red, Orange, Yellow
    Group levels: Purple, Blue, Green, Turquoise
    """
    self_levels = ['Red', 'Orange', 'Yellow']
    group_levels = ['Purple', 'Blue', 'Green', 'Turquoise']

    self_scores = [acceptance_scores.get(l, 2.70) for l in self_levels]
    group_scores = [acceptance_scores.get(l, 2.70) for l in group_levels]

    self_mean = sum(self_scores) / len(self_scores)
    group_mean = sum(group_scores) / len(group_scores)
    total = self_mean + group_mean

    if total > 0:
        self_pct = round((self_mean / total) * 100)
        group_pct = 100 - self_pct
    else:
        self_pct = 50
        group_pct = 50

    return {'self_pct': self_pct, 'group_pct': group_pct}


def compute_shadow_priority_ranking(shadow_ratios, lc_professional_scores):
    """
    Shadow priority = shadow_ratio × LC_professional_score
    Returns sorted list of (level, priority_score)
    """
    priorities = []
    for level in LEVELS:
        ratio = shadow_ratios.get(level, 0)
        lc = lc_professional_scores.get(level, 1)
        priority_score = round(ratio * lc, 3)
        priorities.append((level, priority_score))

    priorities.sort(key=lambda x: x[1], reverse=True)
    return priorities


def compute_epi(acceptance_scores, lc_professional_scores):
    """
    Environmental Pressure Index = LC_professional - Acceptance per level
    Positive = environment demands more than person has
    Negative = environment demands less than person has
    """
    epi = {}
    for level in LEVELS:
        lc = lc_professional_scores.get(level, 1)
        acc = acceptance_scores.get(level, 2.70)
        epi[level] = round(lc - acc, 3)
    return epi


def compute_rejection_scores(rejection_responses):
    """
    rejection_responses: dict {level: [score1, score2, score3]}
    scores: 1=This drains me significantly, 5=This does not apply
    Invert so higher score = stronger rejection
    Returns: dict {level: mean_rejection_score}
    """
    scores = {}
    for level in LEVELS:
        responses = rejection_responses.get(level, [3, 3, 3])
        inverted = [6 - r for r in responses]
        scores[level] = round(sum(inverted) / len(inverted), 3)
    return scores


def score_all(data):
    """
    Master scoring function. Takes raw response data, returns complete scored profile.
    data keys:
        rank_order, intensities, shadow_responses, frequency_responses,
        recognition_responses, rejection_responses, lc_intensity, lc_quality,
        lc_stability, sc_responses, sm_responses, identity_responses,
        enneagram, about
    """
    # Acceptance
    acceptance_scores = compute_acceptance_scores(
        data.get('rank_order', {}),
        data.get('intensities', {})
    )

    # Shadow
    shadow_scores = compute_shadow_scores(data.get('shadow_responses', {}))
    shadow_ratios = compute_shadow_ratios(acceptance_scores, shadow_scores)
    net_cog = compute_net_cog_scores(acceptance_scores, shadow_scores)

    # CoG determination
    cog_result = determine_cog(acceptance_scores, shadow_ratios, net_cog)

    # Self/Group
    self_group = compute_self_group(acceptance_scores)

    # LC
    lc_professional = {
        level: data.get('lc_intensity', {}).get(level, {}).get('Professional', 1)
        for level in LEVELS
    }

    # Shadow priority
    shadow_priority = compute_shadow_priority_ranking(shadow_ratios, lc_professional)

    # EPI
    epi = compute_epi(acceptance_scores, lc_professional)

    # Rejection
    rejection_scores = compute_rejection_scores(data.get('rejection_responses', {}))

    return {
        'acceptance_scores': acceptance_scores,
        'shadow_scores': shadow_scores,
        'shadow_ratios': shadow_ratios,
        'net_cog_scores': net_cog,
        'cog_result': cog_result,
        'self_group': self_group,
        'shadow_priority_ranking': shadow_priority,
        'epi': epi,
        'rejection_scores': rejection_scores,
        'frequency_responses': data.get('frequency_responses', {}),
        'recognition_responses': data.get('recognition_responses', {}),
        'lc_intensity': data.get('lc_intensity', {}),
        'lc_quality': data.get('lc_quality', {}),
        'lc_stability': data.get('lc_stability', {}),
        'sc_responses': data.get('sc_responses', {}),
        'sm_responses': data.get('sm_responses', {}),
        'identity_responses': data.get('identity_responses', {}),
        'enneagram': data.get('enneagram', {}),
        'about': data.get('about', {}),
    }
