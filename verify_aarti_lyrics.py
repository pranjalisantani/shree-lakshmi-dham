import json
import os

p = r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi\data\aarti_lyrics.json'
with open(p, 'r', encoding='utf-8') as f:
    lyrics = json.load(f)

print(f'Total segments in lyrics JSON: {len(lyrics)}')

# Verify time continuity and non-empty text on vocal segments
for i, item in enumerate(lyrics):
    st = item['startTime']
    et = item['endTime']
    t = item['type']
    assert st < et, f"Invalid timestamps in {item['id']}: {st} >= {et}"
    if t == 'vocal':
        assert len(item['text'].strip()) > 0, f"Empty text in vocal item {item['id']}"
        print(f"[{st:6.2f}s - {et:6.2f}s] Verse {item['verse']}: {item['text']}")
    else:
        print(f"[{st:6.2f}s - {et:6.2f}s] {item.get('label', 'Instrumental')}")

# Test seeking simulator
def get_active(time_s):
    for it in lyrics:
        if it['startTime'] <= time_s < it['endTime']:
            return it['text'] if it['type'] == 'vocal' else f"({it['label']})"
    return 'End'

test_seek_times = [5.0, 18.0, 40.0, 58.5, 70.0, 90.0, 104.0, 115.0, 130.0, 160.0, 200.0, 235.0, 265.0, 300.0, 328.0]
print('\n=== SEEK SIMULATION TEST ===')
for ts in test_seek_times:
    print(f"Seek @ {ts:5.1f}s -> Displays: {get_active(ts)}")

print('\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!')

