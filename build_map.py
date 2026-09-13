#!/usr/bin/env python3
"""上野動物園 ベースマップSVG生成スクリプト

方針:
  - 文字は一切入れない。多言語ラベルはHTML側のマーカーで描画する。
  - 公式マップの「俯瞰イラスト」ではなく、真上から見た平面図として描く。
  - パレットはセージ〜土色の落ち着いた測量図寄り。
"""
import math
import random

W, H = 1600, 1300
random.seed(4)

C = {
    'outside':   '#C9D5BB',
    'outtree':   '#B2C29E',
    'ground':    '#EEF2E6',
    'path':      '#FBF8F0',
    'path_edge': '#DCD3BE',
    'road':      '#C4BFB2',
    'road_line': '#EFECE2',
    'water':     '#AFD0DB',
    'water_edge':'#7FADBC',
    'wood':      '#B2C994',
    'wood_dark': '#94AF77',
    'grass':     '#D6E3BD',
    'rock':      '#D2CEC0',
    'rock_dark': '#BAB5A4',
    'polar':     '#BCD8E4',
    'savanna':   '#E4D8AF',
    'forest_ex': '#A8C387',
    'bldg':      '#EBE0CA',
    'bldg_edge': '#AC9B7C',
    'roof':      '#D8C9A9',
    'bridge':    '#C6B999',
    'gate':      '#7E8F60',
    'line':      '#8FA277',
    'fence':     '#A99C80',
}

P = []
A = P.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
A('<desc>Ueno Zoo base map, plan view. Labels are rendered separately as HTML markers.</desc>')

# ================================================================== 園外
A(f'<rect width="{W}" height="{H}" fill="{C["outside"]}"/>')
for _ in range(90):
    x, y = random.uniform(0, W), random.uniform(0, H)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(12,28):.0f}" '
      f'fill="{C["outtree"]}" opacity="0.45"/>')

# ================================================================== 敷地
EAST = ('M 900,90 C 1020,62 1250,58 1410,88 C 1510,108 1548,190 1544,310 '
        'C 1552,470 1532,640 1494,780 C 1454,890 1330,922 1180,900 '
        'C 1040,880 936,826 890,716 C 852,616 844,458 858,300 '
        'C 866,200 878,112 900,90 Z')
WEST = ('M 756,500 C 770,610 772,760 764,880 C 756,1000 728,1118 666,1188 '
        'C 600,1260 470,1268 350,1238 C 220,1206 110,1138 76,1018 '
        'C 44,902 70,772 138,686 C 212,592 340,530 470,500 '
        'C 570,478 700,470 756,500 Z')
A(f'<path d="{EAST}" fill="{C["ground"]}"/>')
A(f'<path d="{WEST}" fill="{C["ground"]}"/>')

# ================================================================== 動物園通り(公道)
ROAD = ('M 806,50 C 796,260 802,460 810,640 C 818,830 834,1020 852,1180 '
        'C 860,1250 866,1290 870,1305')
A(f'<path d="{ROAD}" stroke="{C["road"]}" stroke-width="44" fill="none" stroke-linecap="butt"/>')
A(f'<path d="{ROAD}" stroke="{C["road_line"]}" stroke-width="2.5" stroke-dasharray="16 18" fill="none"/>')

# ================================================================== 不忍池
A(f'<ellipse cx="580" cy="1080" rx="152" ry="90" transform="rotate(-16 580 1080)" '
  f'fill="{C["water"]}" stroke="{C["water_edge"]}" stroke-width="3"/>')
for _ in range(34):
    a = random.uniform(0, 2 * math.pi); r = math.sqrt(random.random())
    px, py = r * 130 * math.cos(a), r * 72 * math.sin(a)
    th = math.radians(-16)
    x = 580 + px * math.cos(th) - py * math.sin(th)
    y = 1080 + px * math.sin(th) + py * math.cos(th)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(5,11):.0f}" fill="#93BFA8" opacity="0.55"/>')
A(f'<ellipse cx="628" cy="1108" rx="30" ry="19" fill="{C["wood"]}" '
  f'stroke="{C["water_edge"]}" stroke-width="2"/>')

# ================================================================== 園内樹林
def grove(cx, cy, rx, ry, n=12):
    A(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{C["wood"]}" opacity="0.9"/>')
    for _ in range(n):
        x = cx + random.uniform(-rx, rx) * 0.85
        y = cy + random.uniform(-ry, ry) * 0.85
        A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(10,20):.0f}" '
          f'fill="{C["wood_dark"]}" opacity="0.8"/>')

for g in [(960, 170, 76, 64, 11), (1500, 160, 52, 74, 9), (1496, 500, 50, 86, 10),
          (920, 620, 62, 84, 11), (1110, 840, 104, 54, 11), (1330, 290, 46, 42, 7),
          (1470, 660, 54, 52, 8), (980, 330, 44, 46, 7)]:
    grove(*g)
for g in [(150, 620, 68, 62, 9), (140, 1000, 64, 58, 9), (640, 660, 58, 54, 8),
          (420, 1180, 62, 44, 8), (250, 560, 56, 42, 7), (700, 1020, 44, 40, 6),
          (430, 542, 70, 40, 8), (712, 596, 42, 46, 7), (196, 800, 44, 48, 7)]:
    grove(*g)

# ================================================================== 園路
PATHS = [
    # --- 東園 ---
    'M 1512,522 C 1440,520 1400,486 1384,436',                      # 正門 → サル山
    'M 1384,436 C 1366,376 1310,336 1230,326',                      # サル山 → ゾウ
    'M 1230,326 C 1150,314 1092,286 1060,232',                      # ゾウ → 五重塔
    'M 1060,232 C 1024,182 980,164 934,172',                        # 五重塔 → ツル
    'M 1230,326 C 1268,250 1302,192 1324,152',                      # → 日本の動物
    'M 1384,436 C 1430,398 1456,326 1452,246',                      # → バードハウス
    'M 1384,436 C 1376,516 1330,570 1258,596',                      # サル山 → 南へ
    'M 1258,596 C 1180,624 1114,664 1080,718',                      # → クマ → 夜の森
    'M 1258,596 C 1320,650 1372,700 1408,742',                      # → ホッキョクグマ
    'M 1060,232 C 1054,320 1038,408 1020,478 C 1004,542 1030,606 1080,718',
    'M 1020,478 C 1098,466 1176,468 1244,482',                      # ゴリラ ↔ プレーリー
    'M 1080,718 C 1030,768 962,786 916,778',                        # → キジ・カワウソ
    'M 916,778 C 890,724 852,676 830,626',                          # → いそっぷ橋
    # --- いそっぷ橋の西側 ---
    'M 830,626 C 792,614 748,620 722,650 C 690,686 692,730 704,766',
    'M 722,650 C 674,608 626,566 618,540',                          # → パンダのもり
    'M 722,650 C 640,684 540,690 452,678 C 366,666 288,682 236,722',
    'M 236,722 C 192,782 190,856 222,898',                          # → アイアイ
    'M 222,898 C 288,936 366,926 434,894',                          # → 小獣館
    'M 434,894 C 494,932 534,952 570,950',                          # → 両生爬虫類館
    'M 570,950 C 636,988 700,972 742,942',                          # → 弁天門
    'M 704,766 C 686,842 640,900 570,950',                          # 鳥エリア → 南
    'M 434,894 C 404,962 366,1020 342,1064',                        # → すてっぷ
    'M 342,1064 C 258,1058 158,1026 104,982',                       # → 池之端門
    'M 452,678 C 470,738 476,790 470,822',                          # 西園中央の短絡
]
for d in PATHS:
    A(f'<path d="{d}" stroke="{C["path_edge"]}" stroke-width="23" fill="none" '
      f'stroke-linecap="round" stroke-linejoin="round"/>')
for d in PATHS:
    A(f'<path d="{d}" stroke="{C["path"]}" stroke-width="17" fill="none" '
      f'stroke-linecap="round" stroke-linejoin="round"/>')

# ================================================================== 部品
def blob(d, fill, sw=3):
    A(f'<path d="{d}" fill="{fill}" stroke="{C["line"]}" stroke-width="{sw}" stroke-linejoin="round"/>')

def bldg(x, y, w, h, rot=0, r=9):
    t = f' transform="rotate({rot} {x+w/2:.0f} {y+h/2:.0f})"' if rot else ''
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"{t} '
      f'fill="{C["bldg"]}" stroke="{C["bldg_edge"]}" stroke-width="3"/>')
    A(f'<rect x="{x+7}" y="{y+7}" width="{max(w-14,4)}" height="{max(h-14,4)}" rx="{max(r-4,2)}"{t} '
      f'fill="none" stroke="{C["bldg_edge"]}" stroke-width="1.4" opacity="0.55"/>')

def pond(cx, cy, rx, ry, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    A(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"{t} fill="{C["water"]}" '
      f'stroke="{C["water_edge"]}" stroke-width="2.5"/>')

def cage(cx, cy, r):
    A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{C["grass"]}" stroke="{C["fence"]}" '
      f'stroke-width="2.5" stroke-dasharray="6 5"/>')
    A(f'<circle cx="{cx}" cy="{cy}" r="{r-7}" fill="none" stroke="{C["fence"]}" '
      f'stroke-width="1.2" opacity="0.5"/>')

def rocks(pts):
    A(f'<path d="M {pts}" fill="{C["rock_dark"]}" opacity="0.85"/>')

def scatter(cx, cy, rx, ry, n, fill, rmin=8, rmax=14, op=0.8):
    for _ in range(n):
        x = cx + random.uniform(-rx, rx); y = cy + random.uniform(-ry, ry)
        A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(rmin,rmax):.0f}" '
          f'fill="{fill}" opacity="{op}"/>')

def gate(x, y):
    A(f'<rect x="{x}" y="{y}" width="46" height="50" rx="9" fill="{C["gate"]}"/>')
    A(f'<rect x="{x+13}" y="{y+13}" width="20" height="24" rx="4" fill="{C["ground"]}"/>')

# ================================================================== 東園
# ゾウのすむ森
blob('M 1112,236 C 1188,214 1268,232 1284,282 C 1302,338 1262,392 1196,398 '
     'C 1130,404 1084,376 1078,326 C 1073,280 1086,248 1112,236 Z', C['savanna'])
pond(1254, 366, 28, 15)
scatter(1160, 300, 60, 40, 5, '#CFC08F', 4, 7, 0.7)
bldg(1084, 226, 58, 38, -9)

# サル山
blob('M 1346,392 C 1406,376 1452,402 1452,444 C 1452,488 1406,514 1356,506 '
     'C 1312,499 1292,468 1300,432 C 1306,406 1324,398 1346,392 Z', C['rock'])
rocks('1322,478 L 1348,436 L 1372,470 L 1400,428 L 1424,482 Z')

# ゴリラ・トラのすむ森
blob('M 968,418 C 1042,398 1104,428 1104,480 C 1104,540 1044,576 982,564 '
     'C 928,554 902,516 912,472 C 920,440 942,426 968,418 Z', C['forest_ex'])
scatter(1004, 488, 78, 60, 10, C['wood_dark'], 8, 14)
pond(1008, 548, 30, 12)
A(f'<path d="M 1004,420 C 1006,470 1002,520 1000,562" stroke="{C["fence"]}" '
  f'stroke-width="2" stroke-dasharray="5 5" fill="none"/>')

# プレーリーにすむ動物たち・世界のサル
blob('M 1216,444 C 1278,430 1324,452 1322,488 C 1320,526 1274,544 1230,536 '
     'C 1194,529 1182,502 1192,474 C 1198,456 1204,448 1216,444 Z', C['savanna'])
for _ in range(9):
    x, y = random.uniform(1204, 1306), random.uniform(454, 528)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="#C2B285"/>')

# クマたちの丘
blob('M 1164,574 C 1236,558 1296,586 1296,632 C 1296,682 1238,710 1182,700 '
     'C 1134,691 1110,658 1121,616 C 1130,588 1144,578 1164,574 Z', C['rock'])
rocks('1142,674 L 1176,626 L 1204,662 L 1236,612 L 1268,678 Z')
A(f'<path d="M 1200,576 L 1204,700" stroke="{C["fence"]}" stroke-width="2" '
  f'stroke-dasharray="5 5"/>')

# ホッキョクグマとアザラシの海
blob('M 1348,700 C 1424,684 1482,714 1480,762 C 1478,812 1418,840 1358,830 '
     'C 1308,821 1288,784 1300,742 C 1309,714 1326,704 1348,700 Z', C['polar'])
pond(1398, 786, 46, 21)
pond(1342, 730, 22, 12)
A(f'<path d="M 1352,762 C 1376,748 1404,748 1430,760" stroke="{C["water_edge"]}" '
  f'stroke-width="2" fill="none" opacity="0.7"/>')

# 夜の森 / バク舎
bldg(996, 686, 82, 54, -7, r=11)
blob('M 1094,696 C 1134,686 1166,700 1166,728 C 1166,758 1132,772 1100,766 '
     'C 1074,760 1064,740 1070,720 C 1075,706 1083,699 1094,696 Z', C['forest_ex'])
pond(1130, 754, 20, 9)

# 日本の動物
blob('M 1276,106 C 1346,92 1402,118 1402,162 C 1402,208 1346,232 1292,222 '
     'C 1246,214 1228,180 1239,144 C 1247,120 1258,110 1276,106 Z', C['forest_ex'])
scatter(1316, 164, 68, 46, 7, C['wood_dark'], 7, 12, 0.7)
bldg(1382, 182, 52, 34, 7)

# 旧寛永寺五重塔
A(f'<rect x="1038" y="102" width="66" height="66" rx="4" fill="{C["roof"]}" '
  f'stroke="{C["bldg_edge"]}" stroke-width="3"/>')
A(f'<rect x="1050" y="114" width="42" height="42" rx="3" fill="{C["bldg"]}" '
  f'stroke="{C["bldg_edge"]}" stroke-width="2"/>')
A(f'<rect x="1062" y="126" width="18" height="18" rx="2" fill="{C["bldg_edge"]}"/>')

# ツル・ヘビクイワシ・トキ
blob('M 886,146 C 942,134 986,156 984,194 C 982,234 936,252 892,244 '
     'C 858,238 844,210 854,182 C 860,160 872,150 886,146 Z', C['grass'])
pond(928, 224, 28, 12)
cage(900, 186, 24)

# バードハウス / バードケージ
bldg(1414, 208, 78, 58, 9, r=12)
cage(1494, 320, 34)

# キジ類・カワウソ・猛禽類
blob('M 862,748 C 914,736 952,758 950,792 C 948,828 904,844 866,836 '
     'C 836,830 826,804 834,780 C 840,760 850,752 862,748 Z', C['grass'])
pond(892, 820, 24, 10)
cage(930, 768, 20)

# 東園の売店・休憩所
bldg(1440, 546, 56, 38, -6)

# 正門
gate(1500, 496)

# ================================================================== いそっぷ橋
A(f'<path d="M 916,778 C 890,724 852,676 830,626" stroke="{C["bridge"]}" '
  f'stroke-width="27" fill="none" stroke-linecap="round"/>')
A(f'<path d="M 916,778 C 890,724 852,676 830,626" stroke="{C["path"]}" '
  f'stroke-width="16" fill="none" stroke-linecap="round"/>')
for t in range(1, 6):
    A(f'<circle cx="{916 - t*15}" cy="{778 - t*26}" r="3" fill="{C["bldg_edge"]}"/>')

# ================================================================== 西園
# パンダのもり(現在はレッサーパンダ・キジ類)
blob('M 566,486 C 640,470 700,496 698,548 C 696,602 634,630 574,618 '
     'C 524,608 504,572 516,530 C 525,500 544,491 566,486 Z', C['forest_ex'])
scatter(602, 550, 74, 56, 9, C['wood_dark'], 8, 14)
pond(612, 604, 26, 11)

# 西園の鳥たち(ハシビロコウ・ペンギン・フラミンゴ)
blob('M 662,722 C 720,710 760,734 756,770 C 752,808 704,824 666,814 '
     'C 634,806 624,778 634,752 C 641,733 650,725 662,722 Z', C['polar'])
pond(700, 792, 34, 14)
cage(668, 744, 22)
A(f'<path d="M 660,770 C 686,758 716,758 742,768" stroke="{C["water_edge"]}" '
  f'stroke-width="2" fill="none" opacity="0.7"/>')

# アフリカの動物(キリン・カバ・サイ・コビトカバ)
blob('M 234,608 C 348,582 448,616 452,684 C 456,758 358,806 262,790 '
     'C 184,777 150,726 166,666 C 180,624 204,614 234,608 Z', C['savanna'])
pond(392, 754, 42, 19)
pond(238, 690, 26, 13)
bldg(186, 618, 74, 46, -11)
scatter(330, 690, 90, 62, 6, C['wood_dark'], 9, 15, 0.5)
A(f'<path d="M 318,612 C 326,672 322,736 314,788" stroke="{C["fence"]}" '
  f'stroke-width="2" stroke-dasharray="5 5" fill="none"/>')

# アイアイのすむ森
bldg(140, 838, 100, 66, -7, r=13)
blob('M 250,864 C 292,854 324,870 322,898 C 320,928 284,942 252,934 '
     'C 230,928 222,908 230,888 C 235,874 241,867 250,864 Z', C['forest_ex'])

# 小獣館
bldg(362, 848, 108, 74, 4, r=13)

# 両生爬虫類館(ビバリウム)
bldg(500, 906, 112, 78, -5, r=13)
pond(552, 992, 30, 12)

# 子ども動物園すてっぷ
blob('M 282,1016 C 352,1002 406,1028 404,1070 C 402,1116 346,1140 294,1130 '
     'C 250,1121 232,1088 243,1054 C 251,1032 264,1020 282,1016 Z', C['grass'])
bldg(250, 1014, 58, 38, -9)
for _ in range(6):
    x, y = random.uniform(270, 390), random.uniform(1030, 1122)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="#BFCCA0"/>')

# 西園の売店・レストラン
bldg(444, 780, 58, 40, 5)

# 門
gate(726, 918)   # 弁天門
gate(78, 952)    # 池之端門

# ================================================================== 敷地輪郭(最前面)
A(f'<path d="{EAST}" fill="none" stroke="{C["line"]}" stroke-width="4.5" opacity="0.85"/>')
A(f'<path d="{WEST}" fill="none" stroke="{C["line"]}" stroke-width="4.5" opacity="0.85"/>')

A('</svg>')

svg = '\n'.join(P)
with open('/home/claude/prototype/zoo-map.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print('wrote zoo-map.svg', len(svg), 'bytes')
