"""A unique art direction for every client version: palette, typography, hero concept and section mix.
V1 keeps each client's original world; V2 and V3 each get their own concept (no two pages share a recipe)."""

# font families loaded from Google Fonts per page
GF = {
    'Oswald': 'Oswald:wght@400;600;700', 'Source Serif 4': 'Source+Serif+4:ital,wght@0,400;0,700;1,400',
    'Unbounded': 'Unbounded:wght@400;700;900', 'DM Serif Display': 'DM+Serif+Display:ital@0;1', 'Inter': 'Inter:wght@400;500;700',
    'JetBrains Mono': 'JetBrains+Mono:wght@400;700', 'Space Grotesk': 'Space+Grotesk:wght@400;500;700',
    'Big Shoulders Display': 'Big+Shoulders+Display:wght@500;800;900', 'Space Mono': 'Space+Mono:wght@400;700',
    'Syne': 'Syne:wght@500;700;800', 'Playfair Display': 'Playfair+Display:ital,wght@0,700;0,900;1,700',
    'IBM Plex Mono': 'IBM+Plex+Mono:wght@400;600', 'Bodoni Moda': 'Bodoni+Moda:ital,wght@0,700;0,900;1,700',
    'Anton': 'Anton', 'Archivo Black': 'Archivo+Black', 'Barlow Condensed': 'Barlow+Condensed:wght@500;700;800',
    'Fraunces': 'Fraunces:ital,wght@0,600;0,900;1,600', 'Instrument Serif': 'Instrument+Serif:ital@0;1',
    'Bebas Neue': 'Bebas+Neue', 'Manrope': 'Manrope:wght@400;600;800', 'Sora': 'Sora:wght@400;600;800',
    'Cormorant Garamond': 'Cormorant+Garamond:ital,wght@0,600;0,700;1,600', 'Chivo Mono': 'Chivo+Mono:wght@400;700',
    'Libre Franklin': 'Libre+Franklin:wght@400;600;900', 'Rubik': 'Rubik:wght@400;600;900', 'Outfit': 'Outfit:wght@400;600;900',
    'Work Sans': 'Work+Sans:wght@400;600;800', 'Karla': 'Karla:wght@400;600;800', 'Lora': 'Lora:ital,wght@0,400;0,600;1,400',
    'Cinzel': 'Cinzel:wght@500;700;900', 'Figtree': 'Figtree:wght@400;600;800',
}


def P(bg, fg, a, a2, ink, hf, bf, radius=0, name=''):
    return dict(bg=bg, fg=fg, a=a, a2=a2, ink=ink, hf=hf, bf=bf, r=radius, name=name)


# (slug, version) -> palette + typography + concept
DESIGN = {
    # ------------------------------------------------------------- 01 RIGHT FOR AMERICA
    ('right-for-america', 2): dict(name='NEWS DESK', hero='adwall', sig='mixer', particle=None,
        pal=P('#F3EEE4', '#14161C', '#B22234', '#3C3B6E', '#FFFFFF', 'Oswald', 'Source Serif 4', 0),
        secs=['words', 'hscroll', 'accordion', 'svc_img', 'close_marquee']),
    ('right-for-america', 3): dict(name='CHROME', hero='flag', sig='stars',
        pal=P('#0A0A0B', '#ECEDEF', '#FF2D3D', '#9AA4B2', '#0A0A0B', 'Unbounded', 'Manrope', 18),
        secs=['odometer', 'bento', 'stack', 'close_particles']),
    # ------------------------------------------------------------- 02 LIKUD
    ('netanyahu-likud', 2): dict(name='WHITE PAPER', hero='chatstream', sig='calls',
        pal=P('#FFFFFF', '#0A1A3F', '#0038B8', '#7AA2FF', '#FFFFFF', 'DM Serif Display', 'Inter', 4),
        secs=['brief', 'zigzag', 'odometer', 'close_fill']),
    ('netanyahu-likud', 3): dict(name='SIGNAL', hero='network', sig='donut', particle='ascii',
        pal=P('#030915', '#CFE3FF', '#00D1FF', '#3D7BFF', '#030915', 'Space Grotesk', 'JetBrains Mono', 10),
        secs=['bento', 'path', 'timeline_v', 'close_particles']),
    # ------------------------------------------------------------- 03 NH SENATE
    ('nh-senate-republicans', 2): dict(name='GRANITE', hero='topo', sig='funnel',
        pal=P('#E6E9E3', '#17241B', '#2F6B3A', '#8C9A86', '#FFFFFF', 'Big Shoulders Display', 'Libre Franklin', 0),
        secs=['odometer', 'stack', 'words', 'close_marquee']),
    ('nh-senate-republicans', 3): dict(name='NIGHT VISION', hero='scope', sig='plaque',
        pal=P('#040704', '#B8FFB0', '#7CFF4F', '#2E8B2E', '#040704', 'Space Mono', 'Space Mono', 0),
        secs=['bento', 'path', 'close_particles']),
    # ------------------------------------------------------------- 04 FRANCIS SUAREZ
    ('francis-suarez', 2): dict(name='PASTEL MIAMI', hero='desktop', sig='aichat',
        pal=P('#FFE9DF', '#2A0F3B', '#FF4F8B', '#23C4C8', '#FFFFFF', 'Syne', 'Outfit', 28),
        secs=['hscroll', 'accordion', 'svc_img', 'close_fill']),
    ('francis-suarez', 3): dict(name='DEEP TEAL', hero='ring', sig='confetti',
        pal=P('#031A1F', '#E8FFFB', '#00E5C3', '#FF8A3D', '#031A1F', 'Unbounded', 'Sora', 24),
        secs=['odometer', 'bento', 'stack', 'close_particles']),
    # ------------------------------------------------------------- 05 RAND PAUL
    ('rand-paul', 2): dict(name='LIBERTY GAZETTE', hero='poster', sig='pamphlet',
        pal=P('#F5F1E8', '#1B1B1B', '#B8860B', '#1D3557', '#FFFFFF', 'Playfair Display', 'Source Serif 4', 0),
        secs=['brief', 'zigzag', 'timeline_v', 'close_marquee']),
    ('rand-paul', 3): dict(name='AMBER TERMINAL', hero='army', sig='feed',
        pal=P('#0D0A02', '#FFD27A', '#FFB000', '#FF6A00', '#0D0A02', 'IBM Plex Mono', 'IBM Plex Mono', 0),
        secs=['odometer', 'path', 'bento', 'close_particles']),
    # ------------------------------------------------------------- 06 TED CRUZ
    ('ted-cruz', 2): dict(name='NOIR', hero='pollclimb', sig='meter',
        pal=P('#0B0B0B', '#F2F2F2', '#C8102E', '#8A8A8A', '#FFFFFF', 'Bodoni Moda', 'Inter', 0),
        secs=['words', 'accordion', 'timeline_v', 'close_marquee']),
    ('ted-cruz', 3): dict(name='LONE STAR BLUE', hero='scratch', sig='months',
        pal=P('#F7F6F1', '#0A2342', '#BF0A30', '#0A2342', '#FFFFFF', 'Anton', 'Manrope', 14),
        secs=['bento', 'stack', 'odometer', 'close_particles']),
    # ------------------------------------------------------------- 07 RICK SCOTT
    ('rick-scott', 2): dict(name='SUNSHINE STATE', hero='track', sig='finish',
        pal=P('#FFF3E3', '#12343B', '#FF6B35', '#00A6A6', '#FFFFFF', 'Archivo Black', 'Manrope', 22),
        secs=['zigzag', 'odometer', 'accordion', 'close_fill']),
    ('rick-scott', 3): dict(name='RACE CONTROL', hero='flapboard', sig='press',
        pal=P('#0A120E', '#EAF7EE', '#FFD400', '#18A558', '#0A120E', 'Barlow Condensed', 'Barlow Condensed', 0),
        secs=['hscroll', 'timeline_v', 'path', 'close_particles']),
    # ------------------------------------------------------------- 08 MIKE HUCKABEE
    ('mike-huckabee', 2): dict(name='TYPEWRITER', hero='blog07', sig='micro',
        pal=P('#F4EEDC', '#2B2A26', '#C8102E', '#1A5EA8', '#FFFFFF', 'Chivo Mono', 'Source Serif 4', 0),
        secs=['brief', 'timeline_v', 'words', 'close_marquee']),
    ('mike-huckabee', 3): dict(name='CAUCUS NIGHT', hero='asterisk', sig='book',
        pal=P('#101827', '#F5F1E6', '#E4572E', '#F2C14E', '#101827', 'Fraunces', 'Inter', 16),
        secs=['bento', 'stack', 'odometer', 'close_particles']),
    # ------------------------------------------------------------- 09 MAINE GOP
    ('maine-gop', 2): dict(name='SEA FOG', hero='chart', sig='release',
        pal=P('#DCE6EE', '#0E2235', '#C8102E', '#4F7CA3', '#FFFFFF', 'Cormorant Garamond', 'Inter', 2),
        secs=['brief', 'timeline_v', 'quote_words', 'close_fill']),
    ('maine-gop', 3): dict(name='PINE & BRASS', hero='flagplant', sig='newengland',
        pal=P('#0F1F17', '#F1EAD8', '#D4A84B', '#6E8B5E', '#0F1F17', 'Bebas Neue', 'Manrope', 12),
        secs=['bento', 'stack', 'quote_words', 'close_particles']),
    # ------------------------------------------------------------- 10 LINDA McMAHON
    ('linda-mcmahon', 2): dict(name='GOLD ROOM', hero='curtain', sig='counties',
        pal=P('#120E08', '#F6EEDD', '#E5B547', '#8C6A2A', '#120E08', 'Instrument Serif', 'Inter', 0),
        secs=['words', 'hscroll', 'svc_img', 'close_marquee']),
    ('linda-mcmahon', 3): dict(name='GALLERY', hero='gallery', sig='exhibit',
        pal=P('#F4F4F2', '#111111', '#6B4EFF', '#111111', '#FFFFFF', 'Syne', 'Inter', 20),
        secs=['bento', 'accordion', 'close_particles']),
    # ------------------------------------------------------------- 11 VHHA
    ('vhha', 2): dict(name='CLINICAL', hero='kinetic',
        pal=P('#F7FBFC', '#0F2F35', '#00808A', '#E5484D', '#FFFFFF', 'Manrope', 'Manrope', 16),
        secs=['odometer', 'zigzag', 'accordion', 'close_fill']),
    ('vhha', 3): dict(name='PULSE', hero='particles', particle='dots',
        pal=P('#071316', '#E3F7F5', '#FF4D6D', '#3DDBD9', '#071316', 'Sora', 'Sora', 22),
        secs=['bento', 'path', 'close_particles']),
    # ------------------------------------------------------------- 12 TXOGA
    ('txoga', 2): dict(name='STEEL', hero='tiles',
        pal=P('#E9E7E2', '#1C1C1C', '#E36414', '#5F6B73', '#FFFFFF', 'Bebas Neue', 'Libre Franklin', 0),
        secs=['odometer', 'hscroll', 'svc_img', 'close_marquee']),
    ('txoga', 3): dict(name='CONTROL ROOM', hero='scramble',
        pal=P('#0B0E10', '#D9E2E8', '#FFB000', '#4CC9F0', '#0B0E10', 'Chivo Mono', 'Inter', 6),
        secs=['bento', 'path', 'stack', 'close_particles']),
    # ------------------------------------------------------------- 13 DAN PATRICK
    ('dan-patrick', 2): dict(name='CAPITOL', hero='imgtext',
        pal=P('#F4EFE6', '#1E1A16', '#9E1B32', '#C2A878', '#FFFFFF', 'Fraunces', 'Libre Franklin', 0),
        secs=['brief', 'timeline_v', 'svc_img', 'close_fill']),
    ('dan-patrick', 3): dict(name='HIGH NOON', hero='broadcast',
        pal=P('#140C07', '#F6E7D0', '#FF7A1A', '#3E7CB1', '#140C07', 'Rubik', 'Rubik', 10),
        secs=['odometer', 'bento', 'timeline_v', 'close_particles']),
    # ------------------------------------------------------------- 14 SARAH PALIN
    ('sarah-palin', 2): dict(name='WHITEOUT', hero='particles', particle='snow',
        pal=P('#EEF4F7', '#0B2233', '#0077B6', '#90E0EF', '#FFFFFF', 'Outfit', 'Outfit', 30),
        secs=['words', 'stack', 'close_marquee']),
    ('sarah-palin', 3): dict(name='MIDNIGHT SUN', hero='blob',
        pal=P('#0A0614', '#F3EDFF', '#B39CFF', '#2EFFAA', '#0A0614', 'Big Shoulders Display', 'Sora', 26),
        secs=['bento', 'accordion', 'close_particles']),
    # ------------------------------------------------------------- 15 DOUG COLLINS
    ('doug-collins', 2): dict(name='PEACH STATE FILM', hero='cinematic',
        pal=P('#1A1310', '#F7EFE6', '#FF9E5E', '#E25D3A', '#1A1310', 'Bebas Neue', 'Inter', 0),
        secs=['brief', 'hscroll', 'accordion', 'close_marquee']),
    ('doug-collins', 3): dict(name='DARKROOM', hero='spotlight',
        pal=P('#0A0A0A', '#F2E6DA', '#FF3B30', '#FF9E5E', '#0A0A0A', 'Anton', 'Space Grotesk', 0),
        secs=['bento', 'stack', 'close_particles']),
}

# a short word/number for particle moments (V1 signature + particle closings)
SIG = {
    'right-for-america': ('2024', 'Presidential cycle — among the largest spenders on Google & Meta.'),
    'netanyahu-likud': ('16,999', 'Voters mobilized to call by an AI-operated chatbot.'),
    'nh-senate-republicans': ('3×', 'Three cycles — from majority to supermajority.'),
    'francis-suarez': ('#1', 'Digital Campaign of the Year — AAPC 2024.'),
    'rand-paul': ('2016', 'The campaign Politico called an internet army.'),
    'ted-cruz': ('UPSET', 'An underdog Senate win many credit in part to the web.'),
    'rick-scott': ('2010', 'The dark horse who crossed the line first.'),
    'mike-huckabee': ('IOWA', 'From an asterisk in the polls to Caucus winner.'),
    'maine-gop': ('MAINE', 'HMG’s first dedicated New England office: Augusta.'),
    'linda-mcmahon': ('CT', 'Statewide campaigns across Connecticut.'),
    'vhha': ('VA', 'A statewide voice for Virginia healthcare.'),
    'txoga': ('10+', 'Fortune 500 energy companies served.'),
    'dan-patrick': ('TX', 'A Texas client for a firm that grew up in Texas.'),
    'sarah-palin': ('AK', 'Supporters engaged from the Last Frontier and beyond.'),
    'doug-collins': ('ACTION', 'Video-first creative built for the feed.'),
}
