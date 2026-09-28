"""
Scansiona music-assets/, genera music-assets/tracks.json dai filename.

Naming convention:
  MIX__[TITOLO]__[ARTISTA]__[DURATA]__[A|B].m4a
  PROD__[TITOLO]__[ARTISTA]__[DURATA]__[A|B].m4a

Esempio:
  MIX__Coffin Dance__Francesco Riolo__1m27s__A.m4a
"""
import os, json, re

MUSIC_DIR = 'music-assets'

def dur_display(s):
    m = re.match(r'(?:(\d+)m)?(\d+)s', s)
    if not m: return s
    return f'{int(m.group(1) or 0)}:{int(m.group(2)):02d}'

pairs = {}
for fname in os.listdir(MUSIC_DIR):
    if not fname.lower().endswith('.m4a'):
        continue
    parts = fname[:-4].split('__')
    if len(parts) != 5:
        print(f'  skip (formato errato): {fname}')
        continue
    player_raw, title, artist, duration, side = parts
    key = (player_raw.lower(), title, artist, duration)
    pairs.setdefault(key, {})[side.upper()] = f'/{MUSIC_DIR}/{fname}'

out = []
for (player, title, artist, duration), sides in pairs.items():
    if 'A' not in sides or 'B' not in sides:
        print(f'  skip (manca lato A o B): {title} — {artist}')
        continue
    out.append({'player': player, 'title': title, 'artist': artist,
                'dur': dur_display(duration), 'a': sides['A'], 'b': sides['B']})

out.sort(key=lambda t: (t['player'], t['title']))

dest = os.path.join(MUSIC_DIR, 'tracks.js')
with open(dest, 'w', encoding='utf-8') as f:
    f.write('window.ABC_TRACKS = ')
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f'tracks.js aggiornato: {len(out)} brani.')
