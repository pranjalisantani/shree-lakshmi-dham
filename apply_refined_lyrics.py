import json

refined_lyrics = [
    {
        "id": "intro",
        "verse": 0,
        "type": "instrumental",
        "label": "🪔 ॥ शंखनाद एवं मंदिर घंटानाद (Instrumental Prelude) ॥ 🪔",
        "text": "",
        "startTime": 0.00,
        "endTime": 13.40,
        "verified": True
    },
    {
        "id": "v1_l1",
        "verse": 1,
        "type": "vocal",
        "text": "ॐ जय लक्ष्मी माता, मैया जय लक्ष्मी माता।",
        "startTime": 13.40,
        "endTime": 33.80,
        "verified": True
    },
    {
        "id": "v1_l2",
        "verse": 1,
        "type": "vocal",
        "text": "तुमको निशिदिन सेवत, हरि विष्णु विधाता॥ ॐ जय लक्ष्मी माता॥",
        "startTime": 33.80,
        "endTime": 56.80,
        "verified": True
    },
    {
        "id": "interlude_1",
        "verse": 1,
        "type": "instrumental",
        "label": "🪔 ॥ संगीत अन्तराल (Flute & Sitar Interlude) ॥ 🪔",
        "text": "",
        "startTime": 56.80,
        "endTime": 60.40,
        "verified": True
    },
    {
        "id": "v2_l1",
        "verse": 2,
        "type": "vocal",
        "text": "उमा, रमा, ब्रह्माणी, तुम ही जग-माता।",
        "startTime": 60.40,
        "endTime": 82.20,
        "verified": True
    },
    {
        "id": "v2_l2",
        "verse": 2,
        "type": "vocal",
        "text": "सूर्य-चन्द्रमा ध्यावत, नारद ऋषि गाता॥ ॐ जय लक्ष्मी माता॥",
        "startTime": 82.20,
        "endTime": 102.50,
        "verified": True
    },
    {
        "id": "interlude_2",
        "verse": 2,
        "type": "instrumental",
        "label": "🪔 ॥ संगीत अन्तराल (Dholak & Shenhai Interlude) ॥ 🪔",
        "text": "",
        "startTime": 102.50,
        "endTime": 104.80,
        "verified": True
    },
    {
        "id": "v3_l1",
        "verse": 3,
        "type": "vocal",
        "text": "दुर्गा रुप निरंजनी, सुख सम्पत्ति दाता।",
        "startTime": 104.80,
        "endTime": 125.30,
        "verified": True
    },
    {
        "id": "v3_l2",
        "verse": 3,
        "type": "vocal",
        "text": "जो कोई तुमको ध्यावत, ऋद्धि-सिद्धि धन पाता॥ ॐ जय लक्ष्मी माता॥",
        "startTime": 125.30,
        "endTime": 149.00,
        "verified": True
    },
    {
        "id": "interlude_3",
        "verse": 3,
        "type": "instrumental",
        "label": "🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔",
        "text": "",
        "startTime": 149.00,
        "endTime": 152.50,
        "verified": True
    },
    {
        "id": "v4_l1",
        "verse": 4,
        "type": "vocal",
        "text": "तुम पाताल-निवासिनि, तुम ही शुभदाता।",
        "startTime": 152.50,
        "endTime": 172.60,
        "verified": True
    },
    {
        "id": "v4_l2",
        "verse": 4,
        "type": "vocal",
        "text": "कर्म-प्रभाव-प्रकाशिनी, भवनिधि की त्राता॥ ॐ जय लक्ष्मी माता॥",
        "startTime": 172.60,
        "endTime": 192.50,
        "verified": True
    },
    {
        "id": "interlude_4",
        "verse": 4,
        "type": "instrumental",
        "label": "🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔",
        "text": "",
        "startTime": 192.50,
        "endTime": 195.00,
        "verified": True
    },
    {
        "id": "v5_l1",
        "verse": 5,
        "type": "vocal",
        "text": "जिस घर में तुम रहतीं, सब सद्गुण आता।",
        "startTime": 195.00,
        "endTime": 203.80,
        "verified": True
    },
    {
        "id": "v5_l2",
        "verse": 5,
        "type": "vocal",
        "text": "सब सम्भव हो जाता, मन नहीं घबराता॥ ॐ जय लक्ष्मी माता॥",
        "startTime": 203.80,
        "endTime": 225.50,
        "verified": True
    },
    {
        "id": "interlude_5",
        "verse": 5,
        "type": "instrumental",
        "label": "🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔",
        "text": "",
        "startTime": 225.50,
        "endTime": 227.20,
        "verified": True
    },
    {
        "id": "v6_l1",
        "verse": 6,
        "type": "vocal",
        "text": "तुम बिन यज्ञ न होते, वस्त्र न कोई पाता।",
        "startTime": 227.20,
        "endTime": 239.70,
        "verified": True
    },
    {
        "id": "v6_l2",
        "verse": 6,
        "type": "vocal",
        "text": "खान-पान का वैभव, सब तुमसे आता॥",
        "startTime": 239.70,
        "endTime": 254.50,
        "verified": True
    },
    {
        "id": "interlude_6",
        "verse": 6,
        "type": "instrumental",
        "label": "🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔",
        "text": "",
        "startTime": 254.50,
        "endTime": 257.50,
        "verified": True
    },
    {
        "id": "v7_l1",
        "verse": 7,
        "type": "vocal",
        "text": "शुभ-गुण मन्दिर सुन्दर, क्षीरोदधि-जाता।",
        "startTime": 257.50,
        "endTime": 274.20,
        "verified": True
    },
    {
        "id": "v7_l2",
        "verse": 7,
        "type": "vocal",
        "text": "रत्न चतुर्दश तुमहीं, कोई नहीं पाता॥",
        "startTime": 274.20,
        "endTime": 288.80,
        "verified": True
    },
    {
        "id": "interlude_7",
        "verse": 7,
        "type": "instrumental",
        "label": "🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔",
        "text": "",
        "startTime": 288.80,
        "endTime": 293.50,
        "verified": True
    },
    {
        "id": "v8_l1",
        "verse": 8,
        "type": "vocal",
        "text": "महा लक्ष्मीजी की आरती, जो कोई जन गाता।",
        "startTime": 293.50,
        "endTime": 305.50,
        "verified": True
    },
    {
        "id": "v8_l2",
        "verse": 8,
        "type": "vocal",
        "text": "उर आनन्द समाता, पाप उतर जाता॥ ॐ जय लक्ष्मी माता॥",
        "startTime": 305.50,
        "endTime": 327.20,
        "verified": True
    },
    {
        "id": "outro",
        "verse": 9,
        "type": "instrumental",
        "label": "🪔 ॥ महाआरती पूर्णम् एवं घंटानाद (Crescendo & Temple Bells) ॥ 🪔",
        "text": "",
        "startTime": 327.20,
        "endTime": 331.02,
        "verified": True
    }
]

p1 = r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi\data\aarti_lyrics.json'
p2 = r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi\media\audio\maa-lakshmi-aarti-lyrics.json'

with open(p1, 'w', encoding='utf-8') as f:
    json.dump(refined_lyrics, f, ensure_ascii=False, indent=2)

with open(p2, 'w', encoding='utf-8') as f:
    json.dump(refined_lyrics, f, ensure_ascii=False, indent=2)

print('Updated both JSON files with refined empirical timestamps.')

