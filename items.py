"""
SVA Item Bank — Complete and Locked
Synchronicity Change Management · April 2026
All items authored by Wayne Kruger. Do not modify without explicit sign-off.
"""

# ── DESCRIPTIVE LABELS ───────────────────────────────────────────────────────

LEVELS = ['Purple', 'Red', 'Blue', 'Orange', 'Green', 'Yellow', 'Turquoise']

LEVEL_COLORS = {
    'Purple': '#6B3FA0',
    'Red': '#C04828',
    'Blue': '#1F4E79',
    'Orange': '#C8860A',
    'Green': '#2E8B57',
    'Yellow': '#D4A017',
    'Turquoise': '#00897B',
}

DESCRIPTIVE_LABELS = {
    'Purple': {
        'name': 'Reverence and Wisdom',
        'descriptor': (
            'We are held by something larger than ourselves — by the wisdom of those who came before, '
            'by our attunement to the living world, and by the ceremonies and rhythms that ground and '
            'connect us to each other and to what endures.'
        ),
    },
    'Red': {
        'name': 'Decisive Force',
        'descriptor': (
            'I act on my own judgement without hesitation when the moment requires it, and I respect '
            'the directness and strength it takes to hold your ground under pressure.'
        ),
    },
    'Blue': {
        'name': 'Order and Integrity',
        'descriptor': (
            'We build trustworthy organisations through clear standards, defined roles, and genuine '
            'accountability — and we honour our obligations to each other and to the institution, '
            'whether or not anyone is watching.'
        ),
    },
    'Orange': {
        'name': 'Achievement and Mastery',
        'descriptor': (
            'I am motivated by results, by finding smarter ways to get things done, and by the '
            'satisfaction of knowing that what I have built reflects real skill and sustained effort.'
        ),
    },
    'Green': {
        'name': 'People and Conscience',
        'descriptor': (
            'We believe that how decisions are made matters as much as what is decided, and that the '
            'relational and human dimensions of our life together are not secondary to the real work — '
            'they often are the real work.'
        ),
    },
    'Yellow': {
        'name': 'Systemic Intelligence',
        'descriptor': (
            'I see the world through the structures and patterns that produce its behaviour — and I '
            'know that lasting change requires working with those structures, not just managing the '
            'symptoms they generate.'
        ),
    },
    'Turquoise': {
        'name': 'Living Wholeness',
        'descriptor': (
            'We do not stand apart from the world observing it — we are expressions of it, permeable '
            'to its patterns, and responsible to the health of the living whole in ways that go beyond '
            'what can be fully reasoned or explained.'
        ),
    },
}

# ── ACCEPTANCE ITEMS ─────────────────────────────────────────────────────────

ACCEPTANCE_ITEMS = {
    'Purple': [
        ('BO-01', 'I pay attention to signals that arrive before the data does — in how a room feels, in recurring patterns I notice across situations, in the quiet sense that something is shifting before anyone has named it. I trust this attunement as real information, not as imagination, and it shapes how I read situations and make decisions.'),
        ('BO-02', 'I believe that how a group begins and ends things, how it marks what matters, and how it holds its people through difficulty is not peripheral to the way — it is the way. The consistent rhythms and shared practices that a group creates together access something that individual reasoning and strategic planning cannot reach alone.'),
        ('BO-05', 'My identity is inseparable from the living lineage I come from — not just as biography but as a living inheritance. The wisdom and mistakes of those who came before me are present in how I am, and I take that inheritance seriously.'),
    ],
    'Red': [
        ('CP-01', 'I act decisively when I see what needs to be done. I do not wait for consensus or permission when I am confident in my own judgement — delay is its own kind of failure.'),
        ('CP-02', 'I say what I see, even when it is not what people want to hear. Softening a position to manage how others feel about it is not diplomacy — it is a failure of honesty, and I would rather be direct and respected than agreeable and ignored.'),
        ('CP-03', 'I believe that bringing your full force to what you care about — your full intensity, your full commitment, without apology — is one of the most honest things a person can do. I have more respect for someone who commits completely and is wrong than for someone who hedges everything and is never accountable for anything.'),
    ],
    'Blue': [
        ('DQ-01', 'I believe there are standards worth upholding regardless of whether doing so is convenient or even effective in the short term. The value of a code is precisely that it holds when circumstances make it difficult — the moment you make exceptions, it is no longer a code.'),
        ('DQ-02', 'I take my obligations seriously — not because I chose all of them but because accepting a role or a position means accepting what comes with it. Honour is not about grand gestures. It is about doing what you said you would do, especially when no one would know if you did not.'),
        ('DQ-03', 'I am willing to accept personal cost — of comfort, of recognition, sometimes of advantage — when doing so serves something I believe will matter beyond my own tenure. What I build should be able to stand without me. That is the standard I hold myself to.'),
    ],
    'Orange': [
        ('ER-01', 'I believe the scoreboard matters. Results are not the only thing but they are the honest thing — they tell you whether what you are doing is actually working, regardless of how much effort went in or how good the intentions were. I would rather know the truth of the score than be comfortable with a story about it.'),
        ('ER-02', 'I take responsibility for my own performance and I am genuinely interested in getting better. If something is not working I want to understand why and fix it. I do not find this pressure — I find it clarifying. The gap between where I am and where I could be is something I close through work, not through waiting.'),
        ('ER-03', 'I pay attention to how things actually work — the incentives, the patterns, the points where the system can be influenced. Understanding the game at that level is not cynicism. It is the difference between playing well and playing to win.'),
    ],
    'Green': [
        ('FS-01', 'The most important things in any organisation — the trust between people, the culture that holds them, the conditions that allow good work — belong to everyone and must be stewarded by everyone. These are not soft concerns. They are the shared foundation that everything else depends on, and they are destroyed faster than they are built.'),
        ('FS-02', 'We make better decisions when the people closest to a problem have a real voice in solving it — not as a gesture toward inclusion but because what they see from where they stand is information that is simply not available from the centre. Excluding those voices does not make decisions faster. It makes them worse.'),
        ('FS-03', 'We hold ourselves accountable not just to outcomes but to the health of what we all share. Individual success that comes at the cost of the collective — the team, the culture, the environment we all depend on — is not success. It is extraction. And extraction always costs more than it returns.'),
    ],
    'Yellow': [
        ('GT-01', 'I find myself looking past the presenting problem to what is producing it. Behaviour in a team or organisation is almost always the symptom of something structural — a misaligned incentive, a broken feedback loop, a design that makes the wrong thing easier than the right thing. That is where I focus, because that is where lasting change is actually available.'),
        ('GT-02', 'I am more interested in creating the conditions for something to thrive than in managing whether it does. The most powerful interventions I know are not direct — they change what the system makes possible, and then get out of the way. Trying to control outcomes directly is usually a sign that something upstream has not been understood yet.'),
        ('GT-03', 'I see organisations as living systems where the health of each part depends on the health of the whole. Optimising one part at the expense of another does not produce overall health — it produces a system that is strong in one place and depleted everywhere else. I design for mutual flourishing, not competitive advantage within the system.'),
    ],
    'Turquoise': [
        ('HU-01', 'We are not separate from the systems we are part of — we are expressions of them, shaped by them, and responsible to them in ways that go beyond what can be fully articulated. I find that I can feel what a system needs before the data confirms it, and I have learned to trust that sensing as a genuine form of intelligence rather than as something to be explained away.'),
        ('HU-02', 'We do not locate wisdom in any single perspective, including our own. The intelligence that matters most in any living system is distributed across it — held in relationships, in the margins, in what is not being said as much as what is. My role is to listen to the whole, not to direct it.'),
        ('HU-03', 'We carry responsibility for what has no voice in the room — future generations, the living systems we depend on, the people and communities that will inherit what we build or deplete. This is not an abstract commitment. It is a felt reality that shapes what we do and what we refuse to do, even when the short-term costs are real.'),
    ],
}

# ── SHADOW ITEMS ─────────────────────────────────────────────────────────────

SHADOW_ITEMS = {
    'Purple': [
        ('BO-S01', 'When something goes wrong in a group I am part of, my honest first response is to look for what has been broken in the relationships — who stopped honouring their obligations, who betrayed the trust that held things together. Cause and effect explanations feel like they miss what actually matters.'),
        ('BO-S02', 'I am aware that I extend a different quality of trust to people who are genuinely part of my inner circle than to those who are not — and that this difference is not primarily about competence or track record. Some people are simply inside and others are simply outside, and I respond to them differently without always being able to explain why.'),
        ('BO-S03', 'When trust is broken in a group I am part of, my first response is to identify who is responsible for the disruption and ensure they understand the cost of what they have done. Belonging has conditions, and people who violate those conditions — even unknowingly — need to feel the consequence.'),
    ],
    'Red': [
        ('CP-S02', 'People who consistently defer to others, seek consensus before acting, or avoid confrontation are not being collaborative — they are being weak. Strength requires the willingness to act unilaterally when the situation demands it.'),
        ('CP-S03', 'Consequences — real ones, delivered swiftly — are the only reliable mechanism for changing behaviour in organisations. Appeals to understanding or dialogue work with people who are already aligned; they are insufficient for everyone else.'),
        ('CP-S04', 'The instinct to protect your territory, your people, and your position is healthy and should not be suppressed in the name of values that often turn out to be rationalised weakness. Self-interest, honestly pursued, is not a character flaw.'),
    ],
    'Blue': [
        ('DQ-S01', 'People who constantly question or reinterpret established standards to suit their own situation are not thinking independently — they are avoiding the discipline that genuine commitment requires. Standards that can always be reconsidered are not really standards.'),
        ('DQ-S02', 'There are roles and functions that are not interchangeable, and organisations that pretend otherwise — in the name of equality or flexibility — produce confusion about accountability and erosion of the competence that comes from genuine specialisation.'),
        ('DQ-S03', 'Consistency is an undervalued virtue in leadership. Leaders who adjust their principles to fit circumstances — who always have a reason why this situation is different — are not being sophisticated; they are being unreliable.'),
    ],
    'Orange': [
        ('ER-S01', 'The people who rise to the top of competitive environments generally deserve to be there. Outcomes are not random — they reflect real differences in capability, effort, and willingness to do what it takes.'),
        ('ER-S03', 'In organisations, the people who are most resistant to change are usually the ones with the most to lose if performance is actually measured. Comfort with ambiguity and commitment to results tend to sort people into useful and not useful fairly quickly.'),
        ('ER-S04', 'Strategic thinking and execution capability are more important leadership qualities than empathy or emotional attunement. A leader who understands the dynamics of their market but has limited personal warmth will outperform a caring leader who lacks strategic acuity.'),
    ],
    'Green': [
        ('FS-S03', 'I find it genuinely difficult to make a decision that I know will disappoint or exclude someone who has a legitimate stake in the outcome. I am aware that this sometimes means decisions take longer than they should — but moving forward without genuine consensus feels like a betrayal of the people who trusted the process.'),
        ('FS-S04', 'I find it very difficult to say something directly critical to someone I care about or work closely with. I am aware that I sometimes soften feedback to the point where the real message does not land — and that I tell myself this is kindness when it may actually be self-protection.'),
        ('FS-S05', 'I find myself judging a meeting or a decision process by how well everyone was heard and how safe people felt — more than by what it actually produced. A process that felt good but reached no useful conclusion still feels like a partial success to me.'),
    ],
    'Yellow': [
        ('GT-S01', 'The gap between people who can genuinely think in systems and those who cannot is the most practically significant difference in any leadership team. Other differences — experience, technical skill, emotional intelligence — matter less than whether someone can hold the complexity of what is actually happening.'),
        ('GT-S02', 'I am aware that I sometimes hold back from committing to a direction because I can see more complexity in the situation than the people around me are ready to engage with. I tell myself I am being thorough. I am not always sure I am not also avoiding the discomfort of acting on an incomplete picture.'),
        ('GT-S03', 'I feel a genuine responsibility to name the complexity that others are glossing over — even when it slows things down or makes people uncomfortable. Leaving important things unsaid because the room is not ready to hear them feels like a failure of intellectual honesty, not a social skill.'),
    ],
    'Turquoise': [
        ('HU-S03', 'I sometimes find that the boundary between what I am feeling and what the people around me are feeling becomes unclear. I absorb the emotional and relational field of a group so completely that I lose track of where my own experience ends and theirs begins.'),
        ('HU-S04', 'I find it genuinely painful to make decisions that I know will benefit some at the cost of others. The harm to the part I am deprioritising feels as real and present to me as the benefit to the part I am serving — and that felt reality makes it very difficult to act with the partiality the situation requires.'),
        ('HU-S05', 'I notice that I resist being the sole author of any conclusion. Decisions feel most true to me when they emerge from the whole rather than from any single perspective — including my own. I am aware that this can make it difficult for others to know where I actually stand.'),
    ],
}

SHADOW_SCALE = [
    'Strongly agree',
    'Agree',
    'Somewhat agree',
    'Somewhat disagree',
    'Disagree',
]

FREQUENCY_SCALE = [
    'Always',
    'Often',
    'Sometimes',
    'Rarely',
    'Never',
]

RECOGNITION_SCALE = [
    'Clearly — I can see this in myself',
    'With effort — I can see it when I look carefully',
    'I struggle to see this in myself',
]

# ── REJECTION ITEMS ───────────────────────────────────────────────────────────

REJECTION_ITEMS = {
    'Purple': [
        ('RJ-BO-1', 'I find it draining to work with leaders who make decisions based on loyalty rather than what the situation requires.'),
        ('RJ-BO-2', 'I find it depleting to work in cultures where unspoken rules about belonging govern what can be said and by whom.'),
        ('RJ-BO-3', 'I find it exhausting to participate in change processes where the primary resistance is the threat the change poses to existing relationships rather than its merit.'),
    ],
    'Red': [
        ('RJ-CP-1', 'I find it draining to work with leaders who act on impulse and manage the consequences later.'),
        ('RJ-CP-2', 'I find it depleting to work in cultures where the ends justify the means and rules are for other people.'),
        ('RJ-CP-3', 'I find it exhausting to work through change where each function protects its own territory and collaboration requires a negotiation.'),
    ],
    'Blue': [
        ('RJ-DQ-1', 'I find it draining to work with leaders who expect compliance by virtue of their position rather than earning respect through what they produce.'),
        ('RJ-DQ-2', 'I find it depleting to work with people who, by oversimplifying complex problems, solve them precisely — arriving at the right answer to the wrong question.'),
        ('RJ-DQ-3', 'I find it exhausting to work in organisations that cannot reinvent themselves and mistake their own continuity for relevance.'),
    ],
    'Orange': [
        ('RJ-ER-1', 'I find it draining to work with leaders who relate to people as resources.'),
        ('RJ-ER-2', 'I find it depleting to work in cultures where what cannot be measured does not count.'),
        ('RJ-ER-3', 'I find it exhausting to work through change processes that become opportunities to build power bases rather than genuine movement.'),
    ],
    'Green': [
        ('RJ-FS-1', 'I find it draining to work with leaders who cannot decide without consensus.'),
        ('RJ-FS-2', 'I find it depleting to work in cultures where maintaining good relationships has become more important than honest ones.'),
        ('RJ-FS-3', 'I find it exhausting to work through change led by authority that silences rather than listens.'),
    ],
    'Yellow': [
        ('RJ-GT-1', 'I find it draining to work with leaders who can see every angle but cannot commit to a direction.'),
        ('RJ-GT-2', 'I find it depleting to work with people who treat every established structure and authority as something to be questioned.'),
        ('RJ-GT-3', 'I find it exhausting to work with people whose wisdom about long-term conditions comes at the cost of short-term action.'),
    ],
    'Turquoise': [
        ('RJ-HU-1', 'I find it draining to work with leaders who speak in expansive terms about vision and possibility but cannot commit to a specific outcome.'),
        ('RJ-HU-2', 'I find it depleting to work in cultures where talking about complexity and interconnectedness substitutes for deciding and delivering.'),
        ('RJ-HU-3', 'I find it exhausting to work through change where everything is connected to everything else and therefore nothing is specifically anyone\'s responsibility.'),
    ],
}

REJECTION_SCALE = [
    'This drains me significantly',
    'This drains me somewhat',
    'This is neutral',
    'This mildly applies',
    'This does not apply to me',
]

# ── LC ENVIRONMENTAL DESCRIPTORS ─────────────────────────────────────────────

LC_DESCRIPTORS = {
    'Purple': {
        'healthy': 'Belonging is genuine. People look out for each other, relationships are trusted, and the group\'s history and identity are a source of strength rather than a reason to exclude.',
        'unhealthy': 'Loyalty is demanded rather than earned. The in-group is protected regardless of performance and outsiders are never fully trusted. Challenging the group\'s direction is treated as betrayal.',
    },
    'Red': {
        'healthy': 'Decisive action is valued and rewarded. People are expected to hold their ground, speak directly, and take responsibility for outcomes. Strength is respected when it is in service of the work.',
        'unhealthy': 'The loudest and most forceful voice wins. Aggression is mistaken for strength, impulse for decisiveness, and compliance is produced through intimidation rather than conviction.',
    },
    'Blue': {
        'healthy': 'Standards are clear, consistently applied, and genuinely serve the work. Authority is earned and trustworthy. Accountability is real and fairly administered.',
        'unhealthy': 'Rules are enforced regardless of outcome. Compliance is demanded. Deviation is punished even when it produces better results. The system protects itself at the cost of the people inside it.',
    },
    'Orange': {
        'healthy': 'Performance is measured honestly and results are recognised. People are trusted to find the best way to deliver and given the autonomy to do so. Competition drives improvement rather than division.',
        'unhealthy': 'Results are demanded at any cost. People are resources to be deployed and replaced. Ethics are negotiable when they get in the way of the numbers.',
    },
    'Green': {
        'healthy': 'People are genuinely heard and their perspectives shape decisions. Relationships are healthy and honest. Difference is welcomed and the culture is strong enough to hold difficult conversations.',
        'unhealthy': 'Harmony is protected at the cost of honesty. Difficult conversations are avoided, performance issues go unaddressed, and consensus becomes a reason to defer every significant decision.',
    },
    'Yellow': {
        'healthy': 'Complexity is engaged with rather than reduced. People are trusted to hold nuance, work across boundaries, and intervene at the level of structure rather than symptom. Learning is genuine and systemic.',
        'unhealthy': 'Complexity is used as a form of status. Over-thinking substitutes for action. The organisation understands its problems with great sophistication and changes very little.',
    },
    'Turquoise': {
        'healthy': 'The organisation takes genuine responsibility for its impact beyond its immediate interests — on people, on systems, on what it leaves behind. Long-term thinking shapes short-term decisions.',
        'unhealthy': 'Expansive language about vision, emergence, and the living whole substitutes for specific accountability. Everything is connected to everything and therefore nothing is specifically anyone\'s responsibility.',
    },
}

LC_DOMAINS = ['Professional', 'Personal', 'Society']

LC_STABILITY = ['Consistent', 'Variable', 'Unpredictable']

# ── SENSEMAKING SCENARIOS ─────────────────────────────────────────────────────

SM_SCENARIOS = [
    {
        'code': 'SM-01',
        'title': 'The underperforming team',
        'stem': (
            'A team that was performing well six months ago is now consistently missing its targets. '
            'The manager has not changed, the team composition is largely the same, and there have '
            'been no major external disruptions. You have been asked to help diagnose what is happening.'
        ),
        'options': [
            ('A', 'Identify who on the team has changed their behaviour and address it directly with them.'),
            ('B', 'Look at what has changed in how the work is structured, measured, or rewarded — the system may be producing the underperformance.'),
            ('C', 'Facilitate a team conversation to surface what people are experiencing — the real issue is likely relational or motivational.'),
            ('D', 'Examine the assumptions the team and manager are making about what good performance looks like in the current context — the target itself may need revisiting.'),
        ],
        'sm_map': {'A': 'Event', 'B': 'Structural', 'C': 'Technical', 'D': 'Dialogic'},
    },
    {
        'code': 'SM-02',
        'title': 'The failed change initiative',
        'stem': (
            'A significant change initiative was rolled out eighteen months ago. It was well-resourced, '
            'well-communicated, and had genuine leadership support. It has not produced the intended '
            'results and people have largely reverted to previous ways of working. You are asked to '
            'make sense of why.'
        ),
        'options': [
            ('A', 'The people responsible for implementing it did not follow through — accountability needs to be clearer.'),
            ('B', 'The initiative addressed the presenting problem but not the underlying structure that produces it — the same structure is now producing the same behaviour.'),
            ('C', 'People were not genuinely engaged with the change — compliance was mistaken for commitment.'),
            ('D', 'The organisation\'s mental model of what needed to change was incomplete — the initiative solved the problem as it was understood, not as it actually exists.'),
        ],
        'sm_map': {'A': 'Event', 'B': 'Structural', 'C': 'Technical', 'D': 'Dialogic'},
    },
    {
        'code': 'SM-03',
        'title': 'The persistent conflict',
        'stem': (
            'Two senior leaders have been in conflict for over a year. Multiple attempts at mediation '
            'have produced short-term improvement followed by return to the same patterns. The conflict '
            'is affecting team morale and decision-making speed. You are asked how to approach this.'
        ),
        'options': [
            ('A', 'Clarify role boundaries and decision rights — the conflict is likely about unclear territory.'),
            ('B', 'Examine what in the organisational design or incentive structure is producing this dynamic — individual conflict rarely persists without structural fuel.'),
            ('C', 'Create a sustained facilitated process to rebuild the relationship — the interpersonal dimension has not been adequately addressed.'),
            ('D', 'Surface the deeper assumptions each leader holds about what good leadership looks like — the conflict may be a proxy for genuinely different worldviews that have not been named.'),
        ],
        'sm_map': {'A': 'Technical', 'B': 'Structural', 'C': 'Event', 'D': 'Dialogic'},
    },
    {
        'code': 'SM-04',
        'title': 'The strategy that is not landing',
        'stem': (
            'A new strategy has been clearly articulated by the executive team and communicated '
            'throughout the organisation. Middle managers say they understand it. Frontline behaviour '
            'has not changed. The organisation is not moving in the new direction.'
        ),
        'options': [
            ('A', 'Middle managers need to be held more accountable for translating strategy into team behaviour.'),
            ('B', 'The current systems, processes, and incentives are still rewarding the old behaviour — strategy cannot change what the design reinforces.'),
            ('C', 'People need more time and support to genuinely internalise the new direction — understanding is not the same as commitment.'),
            ('D', 'The gap between the stated strategy and the strategy the organisation is actually living may not be visible to the people executing it — this needs to be surfaced explicitly.'),
        ],
        'sm_map': {'A': 'Event', 'B': 'Structural', 'C': 'Technical', 'D': 'Dialogic'},
    },
]

# ── IDENTITY SCENARIOS (CA-08, CA-13) ─────────────────────────────────────────

IDENTITY_SCENARIOS = [
    {
        'code': 'CA-08',
        'title': 'Genuinely changing how you operate',
        'instruction': 'Choose the response that most honestly describes your experience — not the response that sounds most capable or sophisticated.',
        'stem': (
            'Think of a time when you genuinely changed how you operate — not just what you did, '
            'but how you thought about a situation or your role in it. What was most true about '
            'that experience?'
        ),
        'options': [
            ('A', 'Something external made the old approach clearly untenable and I adapted pragmatically.'),
            ('B', 'I recognised that my way of seeing the situation was part of the problem, not just the situation itself.'),
            ('C', 'Someone I trusted gave me feedback that genuinely shifted how I understood myself.'),
            ('D', 'I went through a period of genuine uncertainty about what I knew before something new became available.'),
        ],
    },
    {
        'code': 'CA-13',
        'title': 'Coming through a difficult period',
        'instruction': 'Choose the response that most honestly describes your experience — not the response that sounds most capable or sophisticated.',
        'stem': (
            'Think of a genuinely difficult period you have been through — one that tested you '
            'significantly. When you reflect on what happened as you came out the other side, '
            'which is most honest?'
        ),
        'options': [
            ('A', 'I recovered my footing and returned to functioning at my previous level.'),
            ('B', 'I emerged with specific new capacities or perspectives that the difficulty produced.'),
            ('C', 'I am still in the process of making sense of it — I have not fully resolved what it means.'),
            ('D', 'I carry something from that period that I cannot fully articulate but that shapes how I operate now.'),
        ],
    },
]

# ── SENTENCE COMPLETIONS ──────────────────────────────────────────────────────

SC_STEMS = [
    {
        'code': 'SC-01',
        'stem': 'When someone questions my judgement or challenges my effectiveness, my honest first response is...',
        'instruction': 'Complete this sentence with whatever comes to mind first. Write at least 3–4 sentences. Write honestly — not how you think you should respond, but what is actually true for you right now.',
    },
    {
        'code': 'SC-03',
        'stem': 'When I face a situation where I genuinely do not know what the right answer is...',
        'instruction': 'Complete this sentence with whatever comes to mind first. Write at least 3–4 sentences.',
    },
    {
        'code': 'SC-04',
        'stem': 'The experience that has most shaped how I lead is...',
        'instruction': 'Complete this sentence with whatever comes to mind first. Write at least 3–4 sentences.',
    },
    {
        'code': 'SC-05',
        'stem': 'When something I was certain about turns out to be wrong, what I notice in myself is...',
        'instruction': 'Complete this sentence with whatever comes to mind first. Write at least 3–4 sentences.',
    },
]

# ── ACCEPTANCE RANK CONVERSION TABLE ─────────────────────────────────────────

RANK_CONVERSION = {
    (1, 'Strong'): 4.80,
    (1, 'Moderate'): 4.50,
    (1, 'Weak'): 4.20,
    (2, 'Strong'): 4.10,
    (2, 'Moderate'): 3.80,
    (2, 'Weak'): 3.50,
    (3, 'Strong'): 3.40,
    (3, 'Moderate'): 3.20,
    (3, 'Weak'): 3.00,
    (4, None): 2.70,
    (5, 'Very unlike me'): 1.60,
    (5, 'Somewhat unlike me'): 1.80,
    (5, 'Slightly unlike me'): 2.00,
    (6, 'Very unlike me'): 1.10,
    (6, 'Somewhat unlike me'): 1.30,
    (6, 'Slightly unlike me'): 1.50,
    (7, 'Very unlike me'): 0.80,
    (7, 'Somewhat unlike me'): 1.00,
    (7, 'Slightly unlike me'): 1.20,
}

TOP_INTENSITY_OPTIONS = ['Strong', 'Moderate', 'Weak']
BOTTOM_INTENSITY_OPTIONS = ['Very unlike me', 'Somewhat unlike me', 'Slightly unlike me']

# ── ENNEAGRAM ─────────────────────────────────────────────────────────────────

HEART_TYPES = ['2 — The Supportive Helper', '3 — The Ambitious Achiever', '4 — The Sensitive Individualist', 'Unsure']
HEAD_TYPES = ['5 — The Analytical Observer', '6 — The Loyal Questioner', '7 — The Enthusiastic Optimist', 'Unsure']
GUT_TYPES = ['8 — The Decisive Challenger', '9 — The Adaptive Peacemaker', '1 — The Principled Reformer', 'Unsure']
SUBTYPES = ['Self-preservation', 'Social', 'Sexual / One-to-one', 'Unsure']

DOMAINS = ['Professional', 'Personal', 'Society']
