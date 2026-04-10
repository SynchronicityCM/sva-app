"""
Spiral Values Assessment (SVA) — Version 2
All UX fixes applied: scroll-to-top, inline descriptions, blank defaults,
context always visible, mobile-friendly ranking.
Synchronicity Change Management · April 2026
"""

import streamlit as st
import json
import random
import string
from datetime import datetime

from items import (
    LEVELS, LEVEL_COLORS, DESCRIPTIVE_LABELS,
    ACCEPTANCE_ITEMS, SHADOW_ITEMS,
    FREQUENCY_SCALE, RECOGNITION_SCALE,
    REJECTION_ITEMS, REJECTION_SCALE,
    LC_DESCRIPTORS,
    SM_SCENARIOS, IDENTITY_SCENARIOS, SC_STEMS,
    HEART_TYPES, HEAD_TYPES, GUT_TYPES, SUBTYPES,
    TOP_INTENSITY_OPTIONS, BOTTOM_INTENSITY_OPTIONS,
)
from scoring import score_all
from email_handler import save_local_backup

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
    .item-box {
        background: #FAFAF8;
        border: 1px solid #DDDDDD;
        padding: 14px 16px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 0.95em;
        line-height: 1.6;
    }
    .level-card {
        border-radius: 6px;
        padding: 14px 16px;
        margin: 10px 0;
        border: 1px solid #DDDDDD;
    }
    .level-name {
        font-weight: 700;
        font-size: 1.05em;
        margin-bottom: 4px;
    }
    .level-desc {
        font-size: 0.92em;
        color: #333;
        line-height: 1.5;
        margin-bottom: 8px;
    }
    .context-reminder {
        background: #F0F4FF;
        border-left: 3px solid #4A5568;
        padding: 10px 14px;
        border-radius: 4px;
        margin: 6px 0 12px 0;
        font-size: 0.90em;
        color: #333;
        font-style: italic;
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
    .rank-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #EEE;
    }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        'page': 'welcome',
        'access_code': None,
        'participant_name': '',
        'started_at': None,
        'about': {},
        'enneagram': {},
        'rank_order': {},
        'rank_confirmed': False,
        'intensities': {},
        'shadow_current_level_idx': 0,
        'shadow_responses': {},
        'frequency_responses': {},
        'recognition_responses': {},
        'rejection_responses': {},
        'lc_intensity': {},
        'lc_quality': {},
        'lc_stability': {},
        'sm_responses': {},
        'identity_responses': {},
        'sc_responses': {},
        'sc_current_idx': 0,
        'submitted': False,
        'submission_json': None,
        'submission_error': None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


def generate_access_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=8))


def scroll_top():
    st.markdown(
        '<script>window.parent.document.querySelector("section.main").scrollTo(0,0);</script>',
        unsafe_allow_html=True
    )


def nav_to(page):
    st.session_state.page = page
    st.rerun()


def get_progress():
    page_weights = {
        'welcome': 0, 'access': 2, 'about': 5, 'enneagram': 8,
        'acceptance_rank': 15, 'acceptance_intensity': 25,
        'shadow': 55, 'shadow_close': 57, 'lc': 65,
        'sm': 75, 'identity': 82, 'sc': 92,
        'review': 97, 'submitting': 99, 'complete': 100,
    }
    return page_weights.get(st.session_state.page, 0)


def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def instruction_box(text):
    st.markdown(f'<div class="instruction-box">{text}</div>', unsafe_allow_html=True)


def item_box(text):
    st.markdown(f'<div class="item-box">{text}</div>', unsafe_allow_html=True)


def context_reminder(text):
    st.markdown(f'<div class="context-reminder">{text}</div>', unsafe_allow_html=True)


def closing_note(text):
    st.markdown(f'<div class="closing-note">{text}</div>', unsafe_allow_html=True)


def level_color(level):
    return LEVEL_COLORS.get(level, '#1B2A4A')


def show_level_card(level, show_descriptor=True):
    """Show a level name and descriptor as a coloured card."""
    color = level_color(level)
    label = DESCRIPTIVE_LABELS[level]
    desc = f'<div class="level-desc">{label["descriptor"]}</div>' if show_descriptor else ''
    st.markdown(
        f'<div class="level-card" style="border-left:5px solid {color}; background:#FAFAF8;">'
        f'<div class="level-name" style="color:{color};">{label["name"]}</div>'
        f'{desc}'
        f'</div>',
        unsafe_allow_html=True
    )


def show_level_reminder(level):
    """Show a compact level reminder above a question."""
    color = level_color(level)
    label = DESCRIPTIVE_LABELS[level]
    short_desc = label['descriptor'][:120] + '...' if len(label['descriptor']) > 120 else label['descriptor']
    st.markdown(
        f'<div class="context-reminder" style="border-left-color:{color};">'
        f'<strong>{label["name"]}</strong> — {short_desc}'
        f'</div>',
        unsafe_allow_html=True
    )


# ── PAGES ─────────────────────────────────────────────────────────────────────

def page_welcome():
    scroll_top()
    st.markdown('<h1 style="color:#1B2A4A;">Spiral Values Assessment</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4A5568; font-size:1.1em;">Synchronicity Change Management</p>', unsafe_allow_html=True)
    st.divider()

    instruction_box(
        'This assessment has been designed to give you a precise and honest picture of how you operate — '
        'what you value, how you navigate challenge, and where your greatest opportunities for growth lie.'
        '<br><br>'
        'There are no right or wrong answers. The quality of what you receive depends entirely on the honesty of what you give.'
    )

    st.markdown("""
**Before you begin:**
- Find a quiet space where you will not be interrupted
- The assessment takes approximately **45–55 minutes**
- You can save your progress and return using your access code
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
    scroll_top()
    st.markdown('<h2 style="color:#1B2A4A;">Return to your assessment</h2>', unsafe_allow_html=True)
    instruction_box('Enter your 8-character access code to continue.')
    code = st.text_input('Access code', max_chars=8, placeholder='e.g. ABC12345').strip().upper()
    if st.button('Continue', type='primary'):
        if len(code) == 8:
            st.session_state.access_code = code
            nav_to('about')
        else:
            st.error('Please enter your complete 8-character access code.')
    if st.button('← Back'):
        nav_to('welcome')


def page_about():
    scroll_top()
    st.progress(get_progress() / 100)
    st.markdown('<p class="progress-text">Section 1 of 7 — About you</p>', unsafe_allow_html=True)
    section_header('Section 1: About you')

    instruction_box('Before we begin, tell us a little about yourself.')

    st.markdown(
        f'<div class="access-code">{st.session_state.access_code}</div>',
        unsafe_allow_html=True
    )
    st.caption('Save this code — you will need it to return to your assessment if interrupted.')
    st.divider()

    name = st.text_input('Full name *', value=st.session_state.about.get('name', ''),
                         placeholder='Your name as it should appear on your report')
    role = st.text_input('Role / title', value=st.session_state.about.get('role', ''))
    organisation = st.text_input('Organisation', value=st.session_state.about.get('organisation', ''))

    col1, col2 = st.columns(2)
    with col1:
        age_opts = ['Prefer not to say', 'Under 30', '30–39', '40–49', '50–59', '60+']
        age_range = st.selectbox('Age range', age_opts,
            index=age_opts.index(st.session_state.about.get('age_range', 'Prefer not to say')))
    with col2:
        exp_opts = ['Prefer not to say', 'Under 5', '5–10', '10–15', '15–20', '20+']
        years_exp = st.selectbox('Years in leadership', exp_opts,
            index=exp_opts.index(st.session_state.about.get('years_exp', 'Prefer not to say')))

    st.divider()
    if st.button('Next →', type='primary', disabled=not name.strip()):
        st.session_state.about = {
            'name': name.strip(), 'role': role.strip(),
            'organisation': organisation.strip(),
            'age_range': age_range, 'years_exp': years_exp,
        }
        st.session_state.participant_name = name.strip()
        nav_to('enneagram')
    if not name.strip():
        st.caption('Please enter your name to continue.')


def page_enneagram():
    scroll_top()
    st.progress(get_progress() / 100)
    section_header('Your Enneagram Tritype')

    instruction_box(
        'Select your primary Enneagram type from each of the three centres. '
        'If you are unsure, select "Unsure" — this can be confirmed before your debrief.'
    )

    heart = st.selectbox('Heart centre (types 2, 3, 4)', HEART_TYPES,
        index=HEART_TYPES.index(st.session_state.enneagram.get('heart', HEART_TYPES[-1])))
    head = st.selectbox('Head centre (types 5, 6, 7)', HEAD_TYPES,
        index=HEAD_TYPES.index(st.session_state.enneagram.get('head', HEAD_TYPES[-1])))
    gut = st.selectbox('Gut centre (types 8, 9, 1)', GUT_TYPES,
        index=GUT_TYPES.index(st.session_state.enneagram.get('gut', GUT_TYPES[-1])))
    subtype = st.selectbox('Dominant instinctual subtype', SUBTYPES,
        index=SUBTYPES.index(st.session_state.enneagram.get('subtype', SUBTYPES[-1])))

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            nav_to('about')
    with col2:
        if st.button('Next →', type='primary'):
            st.session_state.enneagram = {'heart': heart, 'head': head, 'gut': gut, 'subtype': subtype}
            nav_to('acceptance_rank')


def page_acceptance_rank():
    scroll_top()
    st.progress(get_progress() / 100)
    st.markdown('<p class="progress-text">Section 2 of 7 — Your value orientations (Step 1: Ranking)</p>', unsafe_allow_html=True)
    section_header('Section 2: Your value orientations — Step 1 of 2')

    instruction_box(
        'Below are seven descriptions of different value orientations — different ways people '
        'make sense of the world and decide what matters. Each is a genuine and legitimate way of operating.'
        '<br><br>'
        '<strong>Read each description carefully, then assign it a rank from 1 to 7.</strong>'
        '<br>'
        'Rank 1 = most like how you actually operate. Rank 7 = least like how you actually operate.'
        '<br><br>'
        'Rank how you genuinely <em>are</em> — not how you aspire to be. Each rank number can only be used once.'
    )

    st.divider()

    rank_options = list(range(1, 8))
    current_ranks = {}

    for level in LEVELS:
        label = DESCRIPTIVE_LABELS[level]
        color = level_color(level)
        current_val = st.session_state.rank_order.get(level, None)

        st.markdown(
            f'<div class="level-card" style="border-left:5px solid {color}; background:#FAFAF8;">'
            f'<div class="level-name" style="color:{color};">{label["name"]}</div>'
            f'<div class="level-desc">{label["descriptor"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        rank = st.selectbox(
            f'Rank for {label["name"]}',
            options=[None] + rank_options,
            index=(rank_options.index(current_val) + 1) if current_val in rank_options else 0,
            format_func=lambda x: 'Select a rank (1–7)' if x is None else f'Rank {x}',
            key=f'rank_{level}',
            label_visibility='collapsed'
        )
        current_ranks[level] = rank
        st.markdown('')

    # Validate
    assigned = [r for r in current_ranks.values() if r is not None]
    duplicates = len(assigned) != len(set(assigned))
    all_assigned = len(assigned) == 7

    if duplicates:
        st.error('Each rank number can only be used once. Please check your rankings.')
    elif all_assigned:
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
            st.session_state.intensities = {}
            nav_to('acceptance_intensity')


def page_acceptance_intensity():
    scroll_top()
    st.progress(get_progress() / 100)
    st.markdown('<p class="progress-text">Section 2 of 7 — Your value orientations (Step 2: Intensity)</p>', unsafe_allow_html=True)
    section_header('Section 2: Your value orientations — Step 2 of 2')

    instruction_box(
        'You have completed your ranking. Now indicate the <strong>strength</strong> of your '
        'relationship with your top three and bottom three orientations.'
    )

    rank_order = st.session_state.rank_order
    intensities = dict(st.session_state.intensities)
    sorted_levels = sorted(LEVELS, key=lambda l: rank_order.get(l, 4))

    top_3 = [l for l in sorted_levels if rank_order.get(l, 4) in [1, 2, 3]]
    bottom_3 = [l for l in sorted_levels if rank_order.get(l, 4) in [5, 6, 7]]
    middle = [l for l in sorted_levels if rank_order.get(l, 4) == 4]

    st.subheader('Your top three — how strongly does each describe you?')

    for level in top_3:
        rank = rank_order[level]
        label = DESCRIPTIVE_LABELS[level]
        color = level_color(level)

        st.markdown(
            f'<div class="level-card" style="border-left:5px solid {color}; background:#FAFAF8;">'
            f'<div class="level-name" style="color:{color};">Rank {rank}: {label["name"]}</div>'
            f'<div class="level-desc">{label["descriptor"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        current = intensities.get(level)
        # No default — must actively select
        idx = TOP_INTENSITY_OPTIONS.index(current) if current in TOP_INTENSITY_OPTIONS else None

        intensity = st.radio(
            'How strongly does this describe you?',
            options=TOP_INTENSITY_OPTIONS,
            index=idx,
            horizontal=True,
            key=f'int_top_{level}'
        )
        intensities[level] = intensity
        st.markdown('')

    st.divider()
    st.subheader('Your bottom three — how unlike you is each?')

    for level in bottom_3:
        rank = rank_order[level]
        label = DESCRIPTIVE_LABELS[level]
        color = level_color(level)

        st.markdown(
            f'<div class="level-card" style="border-left:5px solid {color}; background:#FAFAF8;">'
            f'<div class="level-name" style="color:{color};">Rank {rank}: {label["name"]}</div>'
            f'<div class="level-desc">{label["descriptor"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        current = intensities.get(level)
        idx = BOTTOM_INTENSITY_OPTIONS.index(current) if current in BOTTOM_INTENSITY_OPTIONS else None

        intensity = st.radio(
            'How unlike you is this?',
            options=BOTTOM_INTENSITY_OPTIONS,
            index=idx,
            horizontal=True,
            key=f'int_bot_{level}'
        )
        intensities[level] = intensity
        st.markdown('')

    # Middle rank gets no modifier
    for level in middle:
        intensities[level] = None

    # Check all top and bottom have been actively selected
    all_done = all(
        (rank_order.get(l, 4) == 4 or intensities.get(l) is not None)
        for l in LEVELS
    )

    if not all_done:
        st.warning('Please select an option for each orientation above before continuing.')

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
    scroll_top()
    idx = st.session_state.shadow_current_level_idx
    level = LEVELS[idx]
    total_levels = len(LEVELS)
    color = level_color(level)
    label = DESCRIPTIVE_LABELS[level]

    st.progress(get_progress() / 100)
    st.markdown(
        f'<p class="progress-text">Section 4 of 7 — Shadow patterns ({idx + 1} of {total_levels})</p>',
        unsafe_allow_html=True
    )

    if idx == 0:
        section_header('Section 4: How these orientations show up in practice')
        instruction_box(
            'This section looks at how your value orientations show up in practice — including '
            'patterns that may operate below your usual awareness.'
            '<br><br>'
            'Answer as honestly as you can. These are normal human patterns. '
            'There are no wrong answers here.'
        )
        st.divider()

    # Level banner — always visible at top of this level's section
    st.markdown(
        f'<div style="background:{color}; color:white; padding:12px 16px; border-radius:6px; margin:8px 0;">'
        f'<strong style="font-size:1.1em;">{label["name"]}</strong><br>'
        f'<span style="font-size:0.9em; opacity:0.9;">{label["descriptor"]}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # ── Shadow endorsement items ──────────────────────────────────────────────
    st.subheader('Rate each statement')
    instruction_box(
        'Rate how strongly each statement feels true to you — even if you would not say it publicly. '
        'Answer honestly.'
    )

    shadow_scale = ['Strongly agree', 'Agree', 'Somewhat agree', 'Somewhat disagree', 'Disagree']
    shadow_items = SHADOW_ITEMS[level]
    saved_shadow = st.session_state.shadow_responses.get(level, [None, None, None])
    new_shadow = []

    for i, (code, text) in enumerate(shadow_items):
        item_box(text)
        current = saved_shadow[i] if i < len(saved_shadow) else None
        idx_val = (current - 1) if current is not None else None
        val = st.radio(
            'Your response',
            options=[1, 2, 3, 4, 5],
            index=idx_val,
            format_func=lambda x: shadow_scale[x - 1],
            horizontal=True,
            key=f'shadow_{level}_{i}'
        )
        new_shadow.append(val)
        st.markdown('')

    st.divider()

    # ── Frequency ─────────────────────────────────────────────────────────────
    st.subheader('How frequently do you notice these patterns?')

    # Show the shadow items as reminders
    st.markdown('**The patterns you just rated:**')
    for _, text in shadow_items:
        context_reminder(text[:130] + '...' if len(text) > 130 else text)

    current_freq = st.session_state.frequency_responses.get(level, None)
    freq_idx = (current_freq - 1) if current_freq is not None else None
    freq = st.radio(
        'In my professional life, I notice these patterns in my behaviour...',
        options=[1, 2, 3, 4, 5],
        index=freq_idx,
        format_func=lambda x: FREQUENCY_SCALE[x - 1],
        key=f'freq_{level}'
    )

    st.divider()

    # ── Recognition honesty ───────────────────────────────────────────────────
    st.subheader('How clearly can you see these patterns in yourself?')
    context_reminder(f'{label["name"]} — {label["descriptor"][:100]}...' if len(label["descriptor"]) > 100 else f'{label["name"]} — {label["descriptor"]}')

    current_recog = st.session_state.recognition_responses.get(level, None)
    recog_idx = (current_recog - 1) if current_recog is not None else None
    recog = st.radio(
        'Recognition',
        options=[1, 2, 3],
        index=recog_idx,
        format_func=lambda x: RECOGNITION_SCALE[x - 1],
        key=f'recog_{level}'
    )

    st.divider()

    # ── Rejection items ───────────────────────────────────────────────────────
    st.subheader('What do you find draining?')
    instruction_box(
        'The following describe things people sometimes find difficult, draining, or genuinely '
        'irritating in their professional environment. Rate how strongly each applies to you.'
    )

    rejection_items = REJECTION_ITEMS[level]
    saved_rej = st.session_state.rejection_responses.get(level, [None, None, None])
    new_rejection = []

    for i, (code, text) in enumerate(rejection_items):
        item_box(text)
        current_rej = saved_rej[i] if i < len(saved_rej) else None
        rej_idx = (current_rej - 1) if current_rej is not None else None
        rej = st.radio(
            'Your response',
            options=[1, 2, 3, 4, 5],
            index=rej_idx,
            format_func=lambda x: REJECTION_SCALE[x - 1],
            horizontal=True,
            key=f'rej_{level}_{i}'
        )
        new_rejection.append(rej)
        st.markdown('')

    # Validate all answered
    shadow_complete = all(v is not None for v in new_shadow)
    freq_complete = freq is not None
    recog_complete = recog is not None
    rej_complete = all(v is not None for v in new_rejection)
    all_complete = shadow_complete and freq_complete and recog_complete and rej_complete

    if not all_complete:
        st.warning('Please answer all questions above before continuing.')

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            if idx == 0:
                nav_to('acceptance_intensity')
            else:
                st.session_state.shadow_current_level_idx = idx - 1
                st.rerun()
    with col2:
        next_label = 'Next orientation →' if idx < total_levels - 1 else 'Next section →'
        if st.button(next_label, type='primary', disabled=not all_complete):
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

            if idx < total_levels - 1:
                st.session_state.shadow_current_level_idx = idx + 1
                st.rerun()
            else:
                st.session_state.page = 'shadow_close'
                st.rerun()


def page_shadow_close():
    scroll_top()
    section_header('Section 4 complete')
    closing_note(
        'Thank you. You have completed the most demanding section of the assessment. '
        'Take a moment before continuing.'
    )
    st.markdown('The next section asks about your professional environment.')
    if st.button('Continue →', type='primary'):
        nav_to('lc')


def page_lc():
    scroll_top()
    st.progress(get_progress() / 100)
    st.markdown('<p class="progress-text">Life conditions — professional environment</p>', unsafe_allow_html=True)
    section_header('Your professional environment')

    instruction_box(
        'For each value orientation, rate how strongly your professional environment demands it '
        '(1 = not at all, 5 = very strongly). '
        'Where the demand is significant (3 or above), select which description best matches your experience.'
    )

    lc_intensity = dict(st.session_state.lc_intensity)
    lc_quality = dict(st.session_state.lc_quality)
    lc_stability = dict(st.session_state.lc_stability)

    for level in LEVELS:
        color = level_color(level)
        label = DESCRIPTIVE_LABELS[level]

        st.markdown(
            f'<div class="level-card" style="border-left:5px solid {color}; background:#FAFAF8;">'
            f'<div class="level-name" style="color:{color};">{label["name"]}</div>'
            f'<div class="level-desc">{label["descriptor"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if level not in lc_intensity:
            lc_intensity[level] = {}
        if level not in lc_quality:
            lc_quality[level] = {}
        if level not in lc_stability:
            lc_stability[level] = {}

        domain = 'Professional'
        current_intensity = lc_intensity[level].get(domain, 1)

        intensity_val = st.slider(
            'Demand intensity in your professional environment',
            min_value=1, max_value=5, value=current_intensity,
            key=f'lc_int_{level}'
        )
        lc_intensity[level][domain] = intensity_val

        if intensity_val >= 3:
            healthy = LC_DESCRIPTORS[level]['healthy']
            unhealthy = LC_DESCRIPTORS[level]['unhealthy']
            current_quality = lc_quality[level].get(domain, None)

            quality = st.radio(
                'Which best describes your experience?',
                options=['healthy', 'unhealthy'],
                index=(['healthy', 'unhealthy'].index(current_quality) if current_quality in ['healthy', 'unhealthy'] else None),
                format_func=lambda x: f'✓ {healthy[:90]}...' if x == 'healthy' else f'✗ {unhealthy[:90]}...',
                key=f'lc_qual_{level}'
            )
            lc_quality[level][domain] = quality

            current_stability = lc_stability[level].get(domain, None)
            stability = st.radio(
                'How consistent is this demand?',
                options=['Consistent', 'Variable', 'Unpredictable'],
                index=(['Consistent', 'Variable', 'Unpredictable'].index(current_stability) if current_stability in ['Consistent', 'Variable', 'Unpredictable'] else None),
                horizontal=True,
                key=f'lc_stab_{level}'
            )
            lc_stability[level][domain] = stability
        else:
            lc_quality[level][domain] = None
            lc_stability[level][domain] = None

        st.markdown('')

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            nav_to('shadow_close')
    with col2:
        if st.button('Next section →', type='primary'):
            st.session_state.lc_intensity = lc_intensity
            st.session_state.lc_quality = lc_quality
            st.session_state.lc_stability = lc_stability
            nav_to('sm')


def page_sm():
    scroll_top()
    st.progress(get_progress() / 100)
    st.markdown('<p class="progress-text">Section 5 of 7 — How you read situations</p>', unsafe_allow_html=True)
    section_header('Section 5: How you read situations')

    instruction_box(
        'The following situations present challenges that leaders commonly face. '
        'Choose the response that most honestly reflects how you would actually approach each one. '
        'There are no right or wrong answers.'
    )

    sm_responses = dict(st.session_state.sm_responses)
    all_answered = True

    for scenario in SM_SCENARIOS:
        st.divider()
        st.subheader(scenario['title'])
        item_box(scenario['stem'])

        options = [f'{opt[0]}. {opt[1]}' for opt in scenario['options']]
        current = sm_responses.get(scenario['code'], None)
        current_idx = None
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
        if choice:
            sm_responses[scenario['code']] = choice[0]
        else:
            all_answered = False

    if not all_answered:
        st.warning('Please answer all scenarios above before continuing.')

    st.divider()
    closing_note('These situations give us a picture of how you naturally read and diagnose complex challenges.')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            nav_to('lc')
    with col2:
        if st.button('Next section →', type='primary', disabled=not all_answered):
            st.session_state.sm_responses = sm_responses
            nav_to('identity')


def page_identity():
    scroll_top()
    st.progress(get_progress() / 100)
    st.markdown('<p class="progress-text">Section 6 of 7 — Significant experiences</p>', unsafe_allow_html=True)
    section_header('Section 6: Significant experiences')

    instruction_box(
        'The following two situations invite genuine reflection on your experience of change and challenge. '
        'There is no time pressure.'
    )

    identity_responses = dict(st.session_state.identity_responses)
    all_answered = True

    for scenario in IDENTITY_SCENARIOS:
        st.divider()
        st.subheader(scenario['title'])
        st.caption(f'*{scenario["instruction"]}*')
        item_box(scenario['stem'])

        options = [f'{opt[0]}. {opt[1]}' for opt in scenario['options']]
        current = identity_responses.get(scenario['code'], None)
        current_idx = None
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
        if choice:
            identity_responses[scenario['code']] = choice[0]
        else:
            all_answered = False

    if not all_answered:
        st.warning('Please answer both scenarios above before continuing.')

    st.divider()
    closing_note('These reflections are among the most valuable data in the entire assessment.')

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
    scroll_top()
    idx = st.session_state.sc_current_idx
    sc = SC_STEMS[idx]
    total = len(SC_STEMS)

    st.progress(get_progress() / 100)
    st.markdown(
        f'<p class="progress-text">Section 7 of 7 — In your own words ({idx + 1} of {total})</p>',
        unsafe_allow_html=True
    )

    if idx == 0:
        section_header('Section 7: In your own words')
        instruction_box(
            'The final section asks you to complete four sentences in your own words. '
            'These are the most important responses in the entire assessment — they will be read carefully '
            'and directly shape the conversation that follows.'
            '<br><br>'
            '<strong>Please write at least 3–4 sentences for each response.</strong>'
        )
        st.divider()

    st.subheader(f'Sentence {idx + 1} of {total}')
    st.caption(sc['instruction'])
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
    st.caption(f'{word_count} words written')

    if 0 < word_count < 15:
        st.warning('Please write a little more — at least 3–4 sentences gives us enough to work with.')

    brief_confirmed = False
    if 0 < word_count < 15:
        brief_confirmed = st.checkbox(
            'I understand this is brief and want to proceed anyway.',
            key=f'sc_confirm_{sc["code"]}'
        )

    can_proceed = response.strip() and (word_count >= 15 or brief_confirmed)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button('← Back'):
            sc_responses[sc['code']] = response
            st.session_state.sc_responses = sc_responses
            if idx == 0:
                nav_to('identity')
            else:
                st.session_state.sc_current_idx = idx - 1
                st.rerun()
    with col2:
        next_label = 'Next →' if idx < total - 1 else 'Review and submit →'
        if st.button(next_label, type='primary', disabled=not can_proceed):
            sc_responses[sc['code']] = response
            st.session_state.sc_responses = sc_responses
            if idx < total - 1:
                st.session_state.sc_current_idx = idx + 1
                st.rerun()
            else:
                nav_to('review')


def page_review():
    scroll_top()
    st.progress(0.97)
    section_header('Review and submit')

    instruction_box(
        'Your assessment is complete. Review the summary below before submitting.'
    )

    st.subheader('Your ranking')
    sorted_levels = sorted(LEVELS, key=lambda l: st.session_state.rank_order.get(l, 4))
    for level in sorted_levels:
        rank = st.session_state.rank_order.get(level, '?')
        intensity = st.session_state.intensities.get(level, '')
        intensity_str = f' — {intensity}' if intensity else ''
        color = level_color(level)
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
        st.caption(f'{words} words')

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
    scroll_top()
    st.progress(0.99)
    section_header('Processing your assessment...')

    with st.spinner('Processing your responses...'):
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

        scored = score_all(raw_data)
        name = st.session_state.about.get('name', 'Unknown')
        code = st.session_state.access_code
        success, json_str = save_local_backup(name, code, scored, raw_data)
        st.session_state.submitted = True
        st.session_state.submission_json = json_str if success else None
        st.session_state.submission_error = None if success else json_str

    nav_to('complete')


def page_complete():
    scroll_top()
    st.progress(1.0)

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
        'debrief session is scheduled. Thank you for the care and honesty you have brought to this.'
    )

    name = st.session_state.about.get('name', '')
    org = st.session_state.about.get('organisation', '')
    safe_name = name.replace(' ', '_')
    code = st.session_state.access_code

    if name:
        st.markdown(f'**Participant:** {name}')
    if org:
        st.markdown(f'**Organisation:** {org}')
    st.markdown(f'**Submitted:** {datetime.utcnow().strftime("%d %B %Y")}')

    st.divider()

    if st.session_state.get('submission_json'):
        filename = f'SVA_{safe_name}_{code}.json'
        st.markdown('### Download your submission file')
        st.markdown(
            'Please download this file and email it to **info@synchronicity.co.za** '
            'with the subject line: **SVA Submission — ' + name + '**'
        )
        st.download_button(
            label='⬇  Download submission file',
            data=st.session_state.submission_json,
            file_name=filename,
            mime='application/json',
            type='primary',
            use_container_width=True,
        )
    else:
        st.error('There was an issue preparing your file. Please contact info@synchronicity.co.za with your access code.')


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

scroll_top()
current_page = PAGE_MAP.get(st.session_state.page, page_welcome)
current_page()
