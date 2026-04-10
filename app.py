"""
Spiral Values Assessment (SVA) — Version 2
Synchronicity Change Management · April 2026
"""

import streamlit as st
import json
import random
import string
from datetime import datetime

from items import (
    LEVELS, LEVEL_COLORS, DESCRIPTIVE_LABELS,
    ACCEPTANCE_ITEMS, SHADOW_ITEMS, SHADOW_SCALE,
    FREQUENCY_SCALE, RECOGNITION_SCALE,
    REJECTION_ITEMS, REJECTION_SCALE,
    LC_DESCRIPTORS, LC_DOMAINS, LC_STABILITY,
    SM_SCENARIOS, IDENTITY_SCENARIOS, SC_STEMS,
    HEART_TYPES, HEAD_TYPES, GUT_TYPES, SUBTYPES,
    TOP_INTENSITY_OPTIONS, BOTTOM_INTENSITY_OPTIONS,
)
from scoring import score_all
from email_handler import submit_via_sendgrid, save_local_backup

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title='Spiral Values Assessment',
    page_icon='🌀',
    layout='centered',
    initial_sidebar_state='collapsed',
)

# ── STYLING ───────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .main { max-width: 800px; margin: 0 auto; }
    .stProgress > div > div { background-color: #1B2A4A; }
    .section-header {
        background: #1B2A4A;
        color: white;
        padding: 16px 20px;
        border-radius: 6px;
        margin: 20px 0 16px 0;
        font-size: 1.1em;
        font-weight: 600;
    }
    .instruction-box {
        background: #EEF2F7;
        border-left: 4px solid #1B2A4A;
        padding: 14px 16px;
        border-radius: 4px;
        margin: 12px 0;
        font-size: 0.95em;
        line-height: 1.6;
    }
    .item-text {
        background: #FAFAF8;
        border: 1px solid #DDDDDD;
        padding: 14px 16px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 0.95em;
        line-height: 1.6;
    }
    .level-banner {
        padding: 10px 16px;
        border-radius: 6px;
        color: white;
        font-weight: 600;
        margin: 16px 0 8px 0;
        font-size: 1.05em;
    }
    .closing-note {
        background: #FDF6E3;
        border-left: 4px solid #C8860A;
        padding: 14px 16px;
        border-radius: 4px;
        margin: 16px 0;
        font-style: italic;
    }
    .access-code {
        background: #1B2A4A;
        color: white;
        padding: 12px 20px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 1.4em;
        letter-spacing: 4px;
        text-align: center;
        margin: 16px 0;
    }
    .progress-text {
        color: #4A5568;
        font-size: 0.85em;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE INIT ────────────────────────────────────────────────────────

def init_state():
    defaults = {
        'page': 'welcome',
        'access_code': None,
        'participant_name': '',
        'started_at': None,

        # About
        'about': {},

        # Enneagram
        'enneagram': {},

        # Acceptance ranking
        'rank_order': {},      # {level: rank 1-7}
        'rank_step': 1,        # 1=ranking, 2=intensity
        'intensities': {},     # {level: intensity label}

        # Shadow section
        'shadow_current_level_idx': 0,
        'shadow_responses': {},      # {level: [s1, s2, s3]}
        'frequency_responses': {},   # {level: int 1-5}
        'recognition_responses': {}, # {level: int 1-3}
        'rejection_responses': {},   # {level: [r1, r2, r3]}

        # LC
        'lc_intensity': {},   # {level: {domain: 1-5}}
        'lc_quality': {},     # {level: {domain: 'healthy'/'unhealthy'/None}}
        'lc_stability': {},   # {level: {domain: stability}}

        # SM scenarios
        'sm_responses': {},   # {code: option}

        # Identity scenarios
        'identity_responses': {}, # {code: option}

        # SC completions
        'sc_responses': {},   # {code: text}
        'sc_current_idx': 0,

        # Submission
        'submitted': False,
        'submission_error': None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


def generate_access_code():
    """Generate a unique 8-character access code."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=8))


def get_progress():
    """Estimate completion percentage."""
    page_weights = {
        'welcome': 0, 'access': 2, 'about': 5, 'enneagram': 8,
        'acceptance_rank': 15, 'acceptance_intensity': 22,
        'shadow': 55, 'lc': 65, 'sm': 75, 'identity': 82,
        'sc': 92, 'review': 97, 'complete': 100,
    }
    return page_weights.get(st.session_state.page, 0)


def nav_to(page):
    st.session_state.page = page
    st.rerun()


def level_banner(level):
    color = LEVEL_COLORS[level]
    label = DESCRIPTIVE_LABELS[level]['name']
    st.markdown(
        f'<div class="level-banner" style="background:{color};">{level} — {label}</div>',
        unsafe_allow_html=True
    )


def instruction_box(text):
    st.markdown(f'<div class="instruction-box">{text}</div>', unsafe_allow_html=True)


def item_box(text):
    st.markdown(f'<div class="item-text">{text}</div>', unsafe_allow_html=True)


def closing_note(text):
    st.markdown(f'<div class="closing-note">{text}</div>', unsafe_allow_html=True)


# ── PAGES ─────────────────────────────────────────────────────────────────────

def page_welcome():
    st.markdown('<h1 style="color:#1B2A4A;">Spiral Values Assessment</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4A5568; font-size:1.1em;">Synchronicity Change Management</p>', unsafe_allow_html=True)
    st.divider()

    instruction_box(
        'This assessment has been designed to give you a precise and honest picture of how you operate — '
        'what you value, how you navigate challenge, and where your greatest opportunities for growth lie. '
        '<br><br>'
        'There are no right or wrong answers. The quality of what you receive depends entirely on the honesty of what you give.'
    )

    st.markdown("""
    **Before you begin:**
    - Find a quiet space where you will not be interrupted
    - The assessment takes approximately **45–55 minutes**
    - You can save your progress at any point and return using your access code
    - Answer honestly — not how you think you should respond, but how you actually are
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Start new assessment', type='primary', use_container_width=True):
            code = generate_access_code()
            st.session_state.access_code = code
            st.session_state.started_at = datetime.utcnow().isoformat()
            nav_to('about')
    with col2:
        if st.button('Return with access code', use_container_width=True):
            nav_to('access')


def page_access():
    st.markdown('<h2 style="color:#1B2A4A;">Return to your assessment</h2>', unsafe_allow_html=True)
    instruction_box('Enter your 8-character access code to continue where you left off.')

    code = st.text_input('Access code', max_chars=8, placeholder='e.g. ABC12345').strip().upper()

    if st.button('Continue assessment', type='primary'):
        if len(code) == 8:
            # In a full deployment, this would look up saved state from a database
            # For now, accept any 8-char code and begin fresh
            st.session_state.access_code = code
            nav_to('about')
        else:
            st.error('Please enter your complete 8-character access code.')

    if st.button('← Back'):
        nav_to('welcome')


def page_about():
    progress = get_progress()
    st.progress(progress / 100)
    st.markdown(f'<p class="progress-text">Section 1 of 7 — About you</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Section 1: About you</div>', unsafe_allow_html=True)

    instruction_box(
        'Before we begin, we would like to know a little about you. '
        'This information helps personalise how your results are presented and discussed with you.'
    )

    # Show access code
    st.markdown(
        f'<div class="access-code">{st.session_state.access_code}</div>',
        unsafe_allow_html=True
    )
    st.caption('Save this code — you will need it to return to your assessment.')

    st.divider()

    name = st.text_input(
        'Full name *',
        value=st.session_state.about.get('name', ''),
        placeholder='Your name as it should appear on your report'
    )

    role = st.text_input(
        'Role / title',
        value=st.session_state.about.get('role', ''),
        placeholder='e.g. Chief Executive Officer'
    )

    organisation = st.text_input(
        'Organisation',
        value=st.session_state.about.get('organisation', ''),
        placeholder='e.g. Acme Corporation'
    )

    col1, col2 = st.columns(2)
    with col1:
        age_range = st.selectbox(
            'Age range',
            ['Prefer not to say', 'Under 30', '30–39', '40–49', '50–59', '60+'],
            index=['Prefer not to say', 'Under 30', '30–39', '40–49', '50–59', '60+'].index(
                st.session_state.about.get('age_range', 'Prefer not to say')
            )
        )
    with col2:
        years_exp = st.selectbox(
            'Years in leadership',
            ['Prefer not to say', 'Under 5', '5–10', '10–15', '15–20', '20+'],
            index=['Prefer not to say', 'Under 5', '5–10', '10–15', '15–20', '20+'].index(
                st.session_state.about.get('years_exp', 'Prefer not to say')
            )
        )

    st.divider()

    if st.button('Next →', type='primary', disabled=not name.strip()):
        st.session_state.about = {
            'name': name.strip(),
            'role': role.strip(),
            'organisation': organisation.strip(),
            'age_range': age_range,
            'years_exp': years_exp,
        }
        st.session_state.participant_name = name.strip()
        nav_to('enneagram')

    if not name.strip():
        st.caption('Please enter your name to continue.')


def page_enneagram():
    progress = get_progress()
    st.progress(progress / 100)
    st.markdown(f'<p class="progress-text">Section 1 continued — Enneagram Tritype</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Your Enneagram Tritype</div>', unsafe_allow_html=True)

    instruction_box(
        'The Enneagram describes how you make sense of the world and what drives your behaviour. '
        'Select your primary Enneagram type from each of the three centres below. '
        'If you are unsure of your type, select "Unsure" — this can be confirmed before your debrief. '
        'Then select your dominant instinctual subtype.'
    )

    st.subheader('Heart centre (types 2, 3, 4)')
    heart = st.selectbox('Your primary Heart centre type', HEART_TYPES,
        index=HEART_TYPES.index(st.session_state.enneagram.get('heart', HEART_TYPES[-1])))

    st.subheader('Head centre (types 5, 6, 7)')
    head = st.selectbox('Your primary Head centre type', HEAD_TYPES,
        index=HEAD_TYPES.index(st.session_state.enneagram.get('head', HEAD_TYPES[-1])))

    st.subheader('Gut centre (types 8, 9, 1)')
    gut = st.selectbox('Your primary Gut centre type', GUT_TYPES,
        index=GUT_TYPES.index(st.session_state.enneagram.get('gut', GUT_TYPES[-1])))

    st.subheader('Dominant instinctual subtype')
    subtype = st.selectbox('Your dominant subtype', SUBTYPES,
        index=SUBTYPES.index(st.session_state.enneagram.get('subtype', SUBTYPES[-1])))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            nav_to('about')
    with col2:
        if st.button('Next →', type='primary'):
            st.session_state.enneagram = {
                'heart': heart, 'head': head, 'gut': gut, 'subtype': subtype
            }
            nav_to('acceptance_rank')


def page_acceptance_rank():
    progress = get_progress()
    st.progress(progress / 100)
    st.markdown(f'<p class="progress-text">Section 2 of 7 — Your value orientations (Step 1: Ranking)</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Section 2: Your value orientations — Step 1</div>', unsafe_allow_html=True)

    instruction_box(
        'Below you will find seven descriptions of different value orientations — different ways people '
        'make sense of the world and decide what matters. Each describes a genuine and legitimate way '
        'of operating. None is better or worse than any other.'
        '<br><br>'
        '<strong>Read all seven descriptions carefully before making any choices.</strong>'
        '<br><br>'
        'Your task is to rank these seven orientations in order — from the one that <strong>most '
        'describes how you actually operate</strong> (rank 1) to the one that <strong>least describes '
        'how you actually operate</strong> (rank 7).'
        '<br><br>'
        'Rank how you genuinely are, not how you think you should be or aspire to become. '
        'Each rank can only be used once.'
    )

    st.divider()

    # Display all seven descriptions
    st.subheader('The seven orientations')
    for level in LEVELS:
        label = DESCRIPTIVE_LABELS[level]
        color = LEVEL_COLORS[level]
        st.markdown(
            f'<div style="border-left:4px solid {color}; padding:10px 16px; margin:8px 0; background:#FAFAF8;">'
            f'<strong>{label["name"]}</strong><br>'
            f'<span style="font-size:0.95em;">{label["descriptor"]}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()
    st.subheader('Assign your rankings')
    instruction_box(
        'Assign a rank from 1 (most like you) to 7 (least like you) to each orientation. '
        'Each number can only be used once.'
    )

    rank_options = list(range(1, 8))
    current_ranks = {}

    for level in LEVELS:
        label = DESCRIPTIVE_LABELS[level]
        current_val = st.session_state.rank_order.get(level, None)
        default_idx = 0
        if current_val is not None:
            try:
                default_idx = rank_options.index(current_val)
            except ValueError:
                default_idx = 0

        rank = st.selectbox(
            f'{label["name"]}',
            options=[None] + rank_options,
            index=default_idx + 1 if current_val is not None else 0,
            format_func=lambda x: 'Select rank' if x is None else f'Rank {x}',
            key=f'rank_{level}'
        )
        current_ranks[level] = rank

    # Validate
    assigned = [r for r in current_ranks.values() if r is not None]
    duplicates = len(assigned) != len(set(assigned))
    all_assigned = len(assigned) == 7

    if duplicates:
        st.error('Each rank number can only be used once. Please check your rankings.')

    if all_assigned and not duplicates:
        st.success('All seven orientations ranked. Click next to continue.')

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            nav_to('enneagram')
    with col2:
        if st.button('Lock ranking and continue →', type='primary',
                     disabled=(not all_assigned or duplicates)):
            st.session_state.rank_order = current_ranks
            nav_to('acceptance_intensity')


def page_acceptance_intensity():
    progress = get_progress()
    st.progress(progress / 100)
    st.markdown(f'<p class="progress-text">Section 2 of 7 — Your value orientations (Step 2: Intensity)</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Section 2: Your value orientations — Step 2</div>', unsafe_allow_html=True)

    instruction_box(
        'You have completed your ranking. Now we would like to understand the <strong>strength</strong> '
        'of your relationship with your top three and bottom three orientations.'
        '<br><br>'
        'For each orientation below, choose the option that most honestly reflects how strongly '
        'it describes — or does not describe — you.'
    )

    rank_order = st.session_state.rank_order
    intensities = dict(st.session_state.intensities)

    # Sort by rank
    sorted_levels = sorted(LEVELS, key=lambda l: rank_order.get(l, 4))

    top_3 = [l for l in sorted_levels if rank_order.get(l, 4) in [1, 2, 3]]
    bottom_3 = [l for l in sorted_levels if rank_order.get(l, 4) in [5, 6, 7]]

    st.subheader('Your top three orientations')
    instruction_box('How strongly does each of these describe you?')

    for level in top_3:
        rank = rank_order[level]
        label = DESCRIPTIVE_LABELS[level]
        color = LEVEL_COLORS[level]
        st.markdown(
            f'<div style="border-left:4px solid {color}; padding:8px 16px; margin:6px 0; background:#FAFAF8;">'
            f'<strong>Rank {rank}: {label["name"]}</strong>'
            f'</div>',
            unsafe_allow_html=True
        )
        current = intensities.get(level, None)
        intensity = st.radio(
            f'How strongly does this describe you?',
            options=TOP_INTENSITY_OPTIONS,
            index=TOP_INTENSITY_OPTIONS.index(current) if current in TOP_INTENSITY_OPTIONS else 0,
            horizontal=True,
            key=f'int_top_{level}'
        )
        intensities[level] = intensity

    st.divider()
    st.subheader('Your bottom three orientations')
    instruction_box('How unlike you is each of these?')

    for level in bottom_3:
        rank = rank_order[level]
        label = DESCRIPTIVE_LABELS[level]
        color = LEVEL_COLORS[level]
        st.markdown(
            f'<div style="border-left:4px solid {color}; padding:8px 16px; margin:6px 0; background:#FAFAF8;">'
            f'<strong>Rank {rank}: {label["name"]}</strong>'
            f'</div>',
            unsafe_allow_html=True
        )
        current = intensities.get(level, None)
        intensity = st.radio(
            f'How unlike you is this?',
            options=BOTTOM_INTENSITY_OPTIONS,
            index=BOTTOM_INTENSITY_OPTIONS.index(current) if current in BOTTOM_INTENSITY_OPTIONS else 0,
            horizontal=True,
            key=f'int_bot_{level}'
        )
        intensities[level] = intensity

    # Middle rank (rank 4) gets no intensity modifier
    middle = [l for l in sorted_levels if rank_order.get(l, 4) == 4]
    for level in middle:
        intensities[level] = None

    all_done = all(
        (rank_order.get(l, 4) == 4 or intensities.get(l) is not None)
        for l in LEVELS
    )

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            nav_to('acceptance_rank')
    with col2:
        if st.button('Next →', type='primary', disabled=not all_done):
            st.session_state.intensities = intensities
            st.session_state.shadow_current_level_idx = 0
            nav_to('shadow')


def page_shadow():
    progress = get_progress()
    st.progress(progress / 100)

    idx = st.session_state.shadow_current_level_idx
    level = LEVELS[idx]
    total_levels = len(LEVELS)

    st.markdown(
        f'<p class="progress-text">Section 4 of 7 — Shadow patterns ({idx + 1} of {total_levels})</p>',
        unsafe_allow_html=True
    )

    if idx == 0:
        st.markdown('<div class="section-header">Section 4: How these orientations show up in practice</div>', unsafe_allow_html=True)
        instruction_box(
            'The following section looks at how your value orientations show up in practice — including '
            'patterns that may operate below your usual awareness.'
            '<br><br>'
            'This is the most important section of the assessment. Answer as honestly as you can. '
            'These are normal human patterns. There are no wrong answers and no judgement attached '
            'to what you endorse.'
            '<br><br>'
            'For each orientation, you will be asked:'
            '<ul>'
            '<li>Four questions about how it shows up for you</li>'
            '<li>One question about how frequently you notice it</li>'
            '<li>One question about how clearly you can see it</li>'
            '<li>A few questions about what you find draining in others</li>'
            '</ul>'
        )
        st.divider()

    level_banner(level)

    # Shadow items
    st.subheader('How strongly do you agree with each statement?')
    instruction_box(
        'Rate how strongly each statement feels true to you — even if you would not say it publicly. '
        'Answer honestly. These are normal human patterns.'
    )

    shadow_items = SHADOW_ITEMS[level]
    shadow_vals = list(st.session_state.shadow_responses.get(level, [3, 3, 3]))

    shadow_scale_labels = ['Strongly agree', 'Agree', 'Somewhat agree', 'Somewhat disagree', 'Disagree']

    new_shadow = []
    for i, (code, text) in enumerate(shadow_items):
        item_box(text)
        current_val = shadow_vals[i] if i < len(shadow_vals) else 3
        val = st.select_slider(
            f'Your response',
            options=[1, 2, 3, 4, 5],
            value=current_val,
            format_func=lambda x: shadow_scale_labels[x - 1],
            key=f'shadow_{level}_{i}'
        )
        new_shadow.append(val)

    st.divider()

    # Behavioural frequency
    st.subheader('How frequently do you notice this pattern in yourself?')
    freq_items = SHADOW_ITEMS[level]
    freq_item_text = f'In my professional life, I notice these patterns in my behaviour...'
    item_box(freq_item_text)

    current_freq = st.session_state.frequency_responses.get(level, 3)
    freq = st.select_slider(
        'Frequency',
        options=[1, 2, 3, 4, 5],
        value=current_freq,
        format_func=lambda x: FREQUENCY_SCALE[x - 1],
        key=f'freq_{level}'
    )

    st.divider()

    # Recognition honesty
    st.subheader('How clearly can you see this in yourself?')
    current_recog = st.session_state.recognition_responses.get(level, 2)
    recog = st.radio(
        'Recognition',
        options=[1, 2, 3],
        index=current_recog - 1,
        format_func=lambda x: RECOGNITION_SCALE[x - 1],
        key=f'recog_{level}'
    )

    st.divider()

    # Rejection items
    st.subheader('What do you find draining in your professional environment?')
    instruction_box(
        'The following describe things people sometimes find difficult, draining, or genuinely '
        'irritating — in their environment, in others, or in how organisations operate. '
        'Rate how strongly each applies to you. Be honest. There are no wrong answers.'
    )

    rejection_items = REJECTION_ITEMS[level]
    rej_vals = list(st.session_state.rejection_responses.get(level, [3, 3, 3]))

    new_rejection = []
    for i, (code, text) in enumerate(rejection_items):
        item_box(text)
        current_rej = rej_vals[i] if i < len(rej_vals) else 3
        rej = st.select_slider(
            'Your response',
            options=[1, 2, 3, 4, 5],
            value=current_rej,
            format_func=lambda x: REJECTION_SCALE[x - 1],
            key=f'rej_{level}_{i}'
        )
        new_rejection.append(rej)

    st.divider()

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        back_label = '← Back'
        if st.button(back_label):
            if idx == 0:
                nav_to('acceptance_intensity')
            else:
                st.session_state.shadow_current_level_idx = idx - 1
                st.rerun()

    with col2:
        next_label = 'Next orientation →' if idx < total_levels - 1 else 'Next section →'
        if st.button(next_label, type='primary'):
            # Save all responses for this level
            shadow_dict = dict(st.session_state.shadow_responses)
            shadow_dict[level] = new_shadow
            st.session_state.shadow_responses = shadow_dict

            freq_dict = dict(st.session_state.frequency_responses)
            freq_dict[level] = freq
            st.session_state.frequency_responses = freq_dict

            recog_dict = dict(st.session_state.recognition_responses)
            recog_dict[level] = recog
            st.session_state.recognition_responses = recog_dict

            rej_dict = dict(st.session_state.rejection_responses)
            rej_dict[level] = new_rejection
            st.session_state.rejection_responses = rej_dict

            if idx == 0:
                closing_note_shown = True

            if idx < total_levels - 1:
                st.session_state.shadow_current_level_idx = idx + 1
                st.rerun()
            else:
                # Show closing note before moving on
                st.session_state.page = 'shadow_close'
                st.rerun()


def page_shadow_close():
    st.markdown('<div class="section-header">Section 4 complete</div>', unsafe_allow_html=True)
    closing_note(
        'Thank you. You have completed the most demanding section of the assessment. '
        'Take a moment before continuing.'
    )
    st.markdown("""
    The next section asks how you read and diagnose complex situations.
    There are no right or wrong answers — we are interested in how you naturally approach challenges.
    """)
    if st.button('Continue to next section →', type='primary'):
        nav_to('lc')


def page_lc():
    progress = get_progress()
    st.progress(progress / 100)
    st.markdown(f'<p class="progress-text">Life conditions — professional environment</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Your professional environment</div>', unsafe_allow_html=True)

    instruction_box(
        'This section asks about the environment you work in — specifically, what kinds of values '
        'and ways of operating are demanded of you in your professional context.'
        '<br><br>'
        'For each value orientation, rate how strongly your professional environment demands it (1 = not at all, 5 = very strongly). '
        'Where the demand is significant (3 or above), select which description best matches your experience.'
    )

    lc_intensity = dict(st.session_state.lc_intensity)
    lc_quality = dict(st.session_state.lc_quality)
    lc_stability = dict(st.session_state.lc_stability)

    for level in LEVELS:
        level_banner(level)

        if level not in lc_intensity:
            lc_intensity[level] = {}
        if level not in lc_quality:
            lc_quality[level] = {}
        if level not in lc_stability:
            lc_stability[level] = {}

        # Professional domain only
        domain = 'Professional'
        current_intensity = lc_intensity[level].get(domain, 1)

        intensity_val = st.slider(
            f'How strongly does your professional environment demand {DESCRIPTIVE_LABELS[level]["name"]} values?',
            min_value=1, max_value=5, value=current_intensity,
            format='%d',
            key=f'lc_int_{level}'
        )
        lc_intensity[level][domain] = intensity_val

        if intensity_val >= 3:
            st.markdown('**Which description best matches your experience?**')
            healthy = LC_DESCRIPTORS[level]['healthy']
            unhealthy = LC_DESCRIPTORS[level]['unhealthy']

            current_quality = lc_quality[level].get(domain, 'healthy')
            quality = st.radio(
                'Environment quality',
                options=['healthy', 'unhealthy'],
                index=0 if current_quality == 'healthy' else 1,
                format_func=lambda x: f'{"✓ " + healthy[:80] + "..." if x == "healthy" else "✗ " + unhealthy[:80] + "..."}',
                key=f'lc_qual_{level}'
            )
            lc_quality[level][domain] = quality

            current_stability = lc_stability[level].get(domain, 'Consistent')
            stability = st.radio(
                'How consistent is this demand?',
                options=['Consistent', 'Variable', 'Unpredictable'],
                index=['Consistent', 'Variable', 'Unpredictable'].index(current_stability),
                horizontal=True,
                key=f'lc_stab_{level}'
            )
            lc_stability[level][domain] = stability
        else:
            lc_quality[level][domain] = None
            lc_stability[level][domain] = None

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            st.session_state.shadow_current_level_idx = len(LEVELS) - 1
            nav_to('shadow_close')
    with col2:
        if st.button('Next section →', type='primary'):
            st.session_state.lc_intensity = lc_intensity
            st.session_state.lc_quality = lc_quality
            st.session_state.lc_stability = lc_stability
            nav_to('sm')


def page_sm():
    progress = get_progress()
    st.progress(progress / 100)
    st.markdown(f'<p class="progress-text">Section 5 of 7 — How you read situations</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Section 5: How you read situations</div>', unsafe_allow_html=True)

    instruction_box(
        'The next section moves from reflecting on yourself to responding to situations. '
        'There are no right or wrong answers — we are interested in how you naturally approach '
        'challenges, not in what the theoretically correct response might be.'
        '<br><br>'
        'For each situation, choose the response that most honestly reflects how you would '
        'actually approach it.'
    )

    sm_responses = dict(st.session_state.sm_responses)

    for scenario in SM_SCENARIOS:
        st.divider()
        st.subheader(scenario['title'])
        item_box(scenario['stem'])

        options = [f'{opt[0]}. {opt[1]}' for opt in scenario['options']]
        current = sm_responses.get(scenario['code'], None)
        current_idx = 0
        if current:
            for i, opt in enumerate(scenario['options']):
                if opt[0] == current:
                    current_idx = i
                    break

        choice = st.radio(
            'Choose the response that most honestly describes how you would approach this:',
            options=options,
            index=current_idx,
            key=f'sm_{scenario["code"]}'
        )
        selected_letter = choice[0]
        sm_responses[scenario['code']] = selected_letter

    all_answered = all(s['code'] in sm_responses for s in SM_SCENARIOS)

    st.divider()

    closing_note('Thank you. These situations give us a picture of how you naturally read and diagnose complex challenges.')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            nav_to('lc')
    with col2:
        if st.button('Next section →', type='primary', disabled=not all_answered):
            st.session_state.sm_responses = sm_responses
            nav_to('identity')


def page_identity():
    progress = get_progress()
    st.progress(progress / 100)
    st.markdown(f'<p class="progress-text">Section 6 of 7 — Significant experiences</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Section 6: Significant experiences</div>', unsafe_allow_html=True)

    instruction_box(
        'The final scenario section asks you to reflect on experiences of change and challenge — '
        'particularly ones that required more of you than you expected.'
        '<br><br>'
        'The following two situations invite genuine reflection. There is no time pressure.'
    )

    identity_responses = dict(st.session_state.identity_responses)

    for scenario in IDENTITY_SCENARIOS:
        st.divider()
        st.subheader(scenario['title'])
        st.caption(f'*{scenario["instruction"]}*')
        item_box(scenario['stem'])

        options = [f'{opt[0]}. {opt[1]}' for opt in scenario['options']]
        current = identity_responses.get(scenario['code'], None)
        current_idx = 0
        if current:
            for i, opt in enumerate(scenario['options']):
                if opt[0] == current:
                    current_idx = i
                    break

        choice = st.radio(
            'Choose the response that most honestly describes your experience:',
            options=options,
            index=current_idx,
            key=f'id_{scenario["code"]}'
        )
        selected_letter = choice[0]
        identity_responses[scenario['code']] = selected_letter

    all_answered = all(s['code'] in identity_responses for s in IDENTITY_SCENARIOS)

    st.divider()

    closing_note(
        'Thank you. These reflections are among the most valuable data in the entire assessment.'
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            nav_to('sm')
    with col2:
        if st.button('Next section →', type='primary', disabled=not all_answered):
            st.session_state.identity_responses = identity_responses
            st.session_state.sc_current_idx = 0
            nav_to('sc')


def page_sc():
    progress = get_progress()
    st.progress(progress / 100)

    idx = st.session_state.sc_current_idx
    sc = SC_STEMS[idx]
    total = len(SC_STEMS)

    st.markdown(
        f'<p class="progress-text">Section 7 of 7 — In your own words ({idx + 1} of {total})</p>',
        unsafe_allow_html=True
    )

    if idx == 0:
        st.markdown('<div class="section-header">Section 7: In your own words</div>', unsafe_allow_html=True)
        instruction_box(
            'The final section of this assessment asks you to complete four sentences in your own words. '
            'These are the most important responses in the entire assessment — they will be read carefully '
            'and directly shape the conversation that follows.'
            '<br><br>'
            '<strong>Please write at least 3–4 sentences for each response.</strong> '
            'Brief answers significantly reduce the value of what you receive.'
        )
        st.divider()

    st.subheader(f'Sentence {idx + 1} of {total}')
    instruction_box(sc['instruction'])

    st.markdown(f'**{sc["stem"]}**')

    sc_responses = dict(st.session_state.sc_responses)
    current_text = sc_responses.get(sc['code'], '')

    response = st.text_area(
        'Your response',
        value=current_text,
        height=200,
        placeholder='Write honestly — not how you think you should respond, but what is actually true for you right now.',
        key=f'sc_{sc["code"]}'
    )

    word_count = len(response.split()) if response.strip() else 0
    st.caption(f'{word_count} words')

    if word_count < 15 and response.strip():
        st.warning('Please write a little more — at least 3–4 sentences gives us enough to work with.')

    sufficient = word_count >= 15 or not response.strip()

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            if idx == 0:
                nav_to('identity')
            else:
                sc_responses[sc['code']] = response
                st.session_state.sc_responses = sc_responses
                st.session_state.sc_current_idx = idx - 1
                st.rerun()

    with col2:
        next_label = 'Next →' if idx < total - 1 else 'Review and submit →'
        proceed = st.button(next_label, type='primary', disabled=(not response.strip()))

        if proceed:
            if word_count < 15:
                confirmed = st.checkbox(
                    'I understand this response is brief. Proceed anyway.',
                    key=f'sc_confirm_{sc["code"]}'
                )
                if not confirmed:
                    st.warning('Please tick the box to confirm you want to proceed with a brief response.')
                else:
                    sc_responses[sc['code']] = response
                    st.session_state.sc_responses = sc_responses
                    if idx < total - 1:
                        st.session_state.sc_current_idx = idx + 1
                        st.rerun()
                    else:
                        nav_to('review')
            else:
                sc_responses[sc['code']] = response
                st.session_state.sc_responses = sc_responses
                if idx < total - 1:
                    st.session_state.sc_current_idx = idx + 1
                    st.rerun()
                else:
                    nav_to('review')


def page_review():
    st.progress(0.97)
    st.markdown('<div class="section-header">Review and submit</div>', unsafe_allow_html=True)

    instruction_box(
        'Your assessment is complete. Please review the summary below before submitting. '
        'Once submitted, your responses will be reviewed and your debrief will be scheduled.'
    )

    # Summary
    st.subheader('Your ranking')
    sorted_levels = sorted(LEVELS, key=lambda l: st.session_state.rank_order.get(l, 4))
    for level in sorted_levels:
        rank = st.session_state.rank_order.get(level, '?')
        intensity = st.session_state.intensities.get(level, '')
        intensity_str = f' — {intensity}' if intensity else ''
        color = LEVEL_COLORS[level]
        label = DESCRIPTIVE_LABELS[level]['name']
        st.markdown(
            f'<div style="border-left:4px solid {color}; padding:6px 14px; margin:4px 0; background:#FAFAF8;">'
            f'<strong>Rank {rank}</strong> — {label}{intensity_str}'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()
    st.subheader('Your sentence completions')
    for sc in SC_STEMS:
        response = st.session_state.sc_responses.get(sc['code'], '')
        words = len(response.split()) if response.strip() else 0
        st.markdown(f'**{sc["stem"]}**')
        st.markdown(f'*{words} words written*')

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Go back and edit'):
            st.session_state.sc_current_idx = len(SC_STEMS) - 1
            nav_to('sc')
    with col2:
        if st.button('Submit assessment →', type='primary'):
            nav_to('submitting')


def page_submitting():
    st.progress(0.99)
    st.markdown('<div class="section-header">Submitting your assessment...</div>', unsafe_allow_html=True)

    with st.spinner('Processing and submitting your responses...'):
        # Build raw data
        raw_data = {
            'about': st.session_state.about,
            'enneagram': st.session_state.enneagram,
            'rank_order': st.session_state.rank_order,
            'intensities': st.session_state.intensities,
            'shadow_responses': st.session_state.shadow_responses,
            'frequency_responses': st.session_state.frequency_responses,
            'recognition_responses': st.session_state.recognition_responses,
            'rejection_responses': st.session_state.rejection_responses,
            'lc_intensity': st.session_state.lc_intensity,
            'lc_quality': st.session_state.lc_quality,
            'lc_stability': st.session_state.lc_stability,
            'sm_responses': st.session_state.sm_responses,
            'identity_responses': st.session_state.identity_responses,
            'sc_responses': st.session_state.sc_responses,
        }

        # Score
        scored = score_all(raw_data)

        # Submit
        name = st.session_state.about.get('name', 'Unknown')
        code = st.session_state.access_code

        success, message = submit_via_sendgrid(name, code, scored, raw_data)
        if not success:
            # Fall back to local save
            success, message = save_local_backup(name, code, scored, raw_data)

        st.session_state.submitted = True
        st.session_state.submission_error = None if success else message

    nav_to('complete')


def page_complete():
    st.progress(1.0)

    if st.session_state.submission_error:
        st.error(f'There was an issue submitting your assessment: {st.session_state.submission_error}')
        st.markdown('Please contact info@synchronicity.co.za with your access code.')
    else:
        st.markdown(
            '<div style="text-align:center; padding:40px 0;">'
            '<h1 style="color:#1B2A4A;">✓</h1>'
            '<h2 style="color:#1B2A4A;">Assessment complete</h2>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        f'<div class="access-code">{st.session_state.access_code}</div>',
        unsafe_allow_html=True
    )
    st.caption('Your access code — keep this for your records.')

    closing_note(
        'You have completed the Spiral Values Assessment. Your responses will be reviewed before your '
        'debrief session is scheduled. Thank you for the care and honesty you have brought to this. '
        'The quality of what you receive reflects directly what you have given here.'
    )

    name = st.session_state.about.get('name', '')
    org = st.session_state.about.get('organisation', '')
    if name:
        st.markdown(f'**Participant:** {name}')
    if org:
        st.markdown(f'**Organisation:** {org}')
    st.markdown(f'**Submitted:** {datetime.utcnow().strftime("%d %B %Y")}')


# ── ROUTER ────────────────────────────────────────────────────────────────────

PAGE_MAP = {
    'welcome': page_welcome,
    'access': page_access,
    'about': page_about,
    'enneagram': page_enneagram,
    'acceptance_rank': page_acceptance_rank,
    'acceptance_intensity': page_acceptance_intensity,
    'shadow': page_shadow,
    'shadow_close': page_shadow_close,
    'lc': page_lc,
    'sm': page_sm,
    'identity': page_identity,
    'sc': page_sc,
    'review': page_review,
    'submitting': page_submitting,
    'complete': page_complete,
}

current_page = PAGE_MAP.get(st.session_state.page, page_welcome)
current_page()
