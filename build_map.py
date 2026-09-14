#!/usr/bin/env python3
"""上野動物園 ベースマップSVG生成スクリプト

方針:
  - 文字は一切入れない。多言語ラベルはHTML側のマーカーで描画する。
  - 配置は公式ガイドマップ(tokyo-zoo.net の guide_brochure_ueno.pdf)に合わせる。
  - パレットはセージ〜土色の落ち着いた測量図寄り。

座標系:
  図形は「ガイド座標」(公式マップを 2000x1414 に正規化した空間)で記述し、
  出力時に <g transform> でキャンバス(1600x1200)へ写す。
  ガイド座標 (gx, gy) → 画像ピクセル (x, y) は次式。index.html の
  AREAS / CALIBRATION の x, y はこの変換後の値を使う。
      x = SCALE * (gx - GX0) + OX
      y = SCALE * (gy - GY0) + OY

向き:
  公式マップに合わせているため真北は上ではない。北は画面上方向から
  時計回りに約52度(公式マップの方位記号を実測)。GPS換算は index.html 側で
  3点アフィン変換を使うこと。
"""
import math
import random
import os

W, H = 1600, 1200
SCALE, GX0, GY0, OX, OY = 0.83, 30, 25, 20, 60
NORTH_DEG = 52  # 画面上方向から時計回りの北の向き

random.seed(7)

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
    'lake':      '#9CC2D2',
    'islet':     '#D6C9A8',
    'wood':      '#B2C994',
    'wood_dark': '#94AF77',
    'grass':     '#D6E3BD',
    'rock':      '#D2CEC0',
    'rock_dark': '#BAB5A4',
    'plot':      '#CFD2C8',
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


def poly(pts, close=True):
    d = 'M ' + ' L '.join(f'{x},{y}' for x, y in pts)
    return d + (' Z' if close else '')


A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
A('<desc>Ueno Zoo base map, plan view, laid out after the official guide map. '
  'Labels are rendered separately as HTML markers.</desc>')

# ================================================================== 園外
A(f'<rect width="{W}" height="{H}" fill="{C["outside"]}"/>')

A(f'<g transform="translate({OX},{OY}) scale({SCALE}) translate({-GX0},{-GY0})">')

for _ in range(110):
    x, y = random.uniform(10, 1960), random.uniform(10, 1400)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(14,32):.0f}" '
      f'fill="{C["outtree"]}" opacity="0.4"/>')

# ================================================================== 敷地
# 西園: 北西に池之端門、北にアフリカの動物、南半分を不忍池が占める
WEST = poly([
    (648, 68), (790, 150), (858, 300), (862, 470), (838, 640), (800, 760),
    (775, 900), (752, 1040), (722, 1180), (650, 1290), (430, 1300),
    (250, 1235), (120, 1100), (52, 900), (42, 700), (78, 520),
    (160, 370), (268, 245), (420, 135),
])
# 東園: 北東にゴリラ・トラのすむ森、南端に正門、南西へ細い首がのびて いそっぷ橋 へ
EAST = poly([
    (925, 430), (955, 330), (1010, 240), (1105, 150), (1240, 80), (1420, 40),
    (1620, 35), (1790, 60), (1885, 140), (1905, 260), (1893, 390), (1855, 495),
    (1785, 578), (1688, 648), (1594, 698), (1546, 768), (1536, 898),
    (1514, 1028), (1448, 1114), (1352, 1120), (1284, 1058), (1240, 980),
    (1186, 1005), (1132, 950), (1122, 850), (1150, 740), (1150, 660),
    (1070, 646), (992, 664), (938, 698), (904, 700), (898, 672), (936, 646),
    (996, 612), (1012, 566), (988, 524), (952, 470),
])
A(f'<path d="{WEST}" fill="{C["ground"]}"/>')
A(f'<path d="{EAST}" fill="{C["ground"]}"/>')

# ================================================================== 公道
# 動物園通り(東園と西園のあいだ)
ROAD = 'M 878,40 C 890,260 872,430 838,620 C 806,800 778,980 752,1200 C 744,1270 740,1330 738,1380'
A(f'<path d="{ROAD}" stroke="{C["road"]}" stroke-width="62" fill="none" stroke-linecap="butt"/>')
A(f'<path d="{ROAD}" stroke="{C["road_line"]}" stroke-width="3" stroke-dasharray="20 22" fill="none"/>')
# 不忍通り(西園の北西側)
SHINOBAZU_ST = 'M 600,20 C 470,90 330,180 210,300 C 120,392 60,470 20,540'
A(f'<path d="{SHINOBAZU_ST}" stroke="{C["road"]}" stroke-width="54" fill="none" stroke-linecap="butt"/>')
A(f'<path d="{SHINOBAZU_ST}" stroke="{C["road_line"]}" stroke-width="3" stroke-dasharray="20 22" fill="none"/>')

# ================================================================== 不忍池
LAKE = ('M 274,720 C 388,750 496,784 572,830 C 626,864 632,940 612,1024 '
        'C 590,1110 546,1176 458,1198 C 370,1220 286,1186 238,1110 '
        'C 194,1042 206,938 216,852 C 224,782 242,730 274,720 Z')
A(f'<path d="{LAKE}" fill="{C["lake"]}" stroke="{C["water_edge"]}" stroke-width="4"/>')
for cx, cy, rx, ry, rot in [(392, 946, 46, 30, 18), (466, 1036, 38, 24, -12),
                            (330, 1080, 30, 20, 26), (298, 862, 26, 17, -8)]:
    A(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" '
      f'fill="{C["islet"]}"/>')
# 蓮の茂み
for _ in range(26):
    a = random.uniform(0, 2 * math.pi)
    r = math.sqrt(random.random())
    x = 420 + r * 190 * math.cos(a)
    y = 960 + r * 230 * math.sin(a)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(6,13):.0f}" '
      f'fill="#8FB79C" opacity="0.45"/>')

# ================================================================== 園内樹林
def grove(cx, cy, rx, ry, n=12):
    A(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{C["wood"]}" opacity="0.9"/>')
    for _ in range(n):
        x = cx + random.uniform(-rx, rx) * 0.85
        y = cy + random.uniform(-ry, ry) * 0.85
        A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(11,22):.0f}" '
          f'fill="{C["wood_dark"]}" opacity="0.8"/>')


for g in [  # 東園
    (1180, 120, 70, 50, 9), (1470, 80, 70, 46, 8), (1878, 250, 36, 80, 7),
    (1700, 560, 66, 52, 9), (1300, 220, 56, 46, 8), (1460, 560, 54, 44, 8),
    (1230, 520, 48, 46, 7), (1000, 470, 56, 70, 9), (1300, 700, 62, 50, 8),
    (1180, 900, 50, 60, 8), (1450, 900, 60, 52, 8), (1600, 800, 52, 44, 7),
]:
    grove(*g)
for g in [  # 西園
    (700, 120, 64, 46, 8), (110, 640, 56, 70, 9), (96, 980, 54, 64, 9),
    (300, 400, 58, 44, 8), (610, 400, 40, 38, 6), (770, 500, 44, 56, 7),
    (640, 690, 46, 40, 7), (300, 1200, 62, 42, 8), (620, 1230, 54, 40, 7),
    (170, 1120, 44, 40, 6), (540, 640, 34, 32, 5),
]:
    grove(*g)

# ================================================================== 園路
PATHS = [
    # --- 西園 ---
    'M 258,300 C 340,300 400,280 452,250',                     # 池之端門 → アフリカの動物
    'M 452,250 C 540,238 620,262 664,300',                     # アフリカの動物 前
    'M 664,300 C 712,330 740,356 772,380',                     # → 小獣館・管理事務所
    'M 452,250 C 430,320 420,380 416,430',                     # → 両生爬虫類館方面
    'M 416,430 C 360,440 310,452 278,470',                     # → 両生爬虫類館
    'M 416,430 C 470,444 520,460 556,486',                     # → フラミンゴ・ペンギン
    'M 556,486 C 600,510 640,540 668,570',                     # → パンダのもり
    'M 668,570 C 700,594 716,640 726,700',                     # → カート乗り場
    'M 726,700 C 736,760 730,840 712,920',                     # → 東岸を南へ
    'M 712,920 C 696,990 664,1060 610,1120',                   # → すてっぷ
    'M 610,1120 C 552,1190 494,1240 452,1266',                 # → 弁天門
    'M 278,470 C 240,510 214,560 204,616',                     # → アイアイのすむ森
    'M 204,616 C 190,690 182,780 190,868',                     # 不忍池 西岸
    'M 190,868 C 198,970 226,1076 284,1152',                   # → 南へ
    'M 284,1152 C 340,1222 400,1258 452,1266',                 # → 弁天門
    'M 556,486 C 540,540 512,590 478,636',                     # 中央の短絡
    'M 478,636 C 440,676 396,700 352,704',                     # → 不忍池 北岸
    'M 352,704 C 290,700 236,672 204,616',
    # --- 東園 ---
    'M 1462,1072 C 1440,1010 1420,940 1408,864',               # 正門 → 総合案内所
    'M 1408,864 C 1396,790 1400,720 1418,660',                 # → リトルトランク
    'M 1408,864 C 1350,910 1300,940 1252,952',                 # → 日本の動物
    'M 1252,952 C 1206,960 1176,930 1168,880',                 # 日本の動物 まわり
    'M 1168,880 C 1160,810 1176,744 1206,700',                 # → 日本の鳥II
    'M 1206,700 C 1240,660 1284,634 1324,620',                 # → リス・プレーリー
    'M 1418,660 C 1400,600 1372,548 1344,510',                 # → 世界のサル
    'M 1344,510 C 1370,470 1400,442 1436,428',                 # → ゾウのすむ森
    'M 1436,428 C 1470,414 1500,420 1522,442',                 # → クマたちの丘
    'M 1522,442 C 1556,470 1586,510 1604,556',                 # → 動物慰霊碑・鳥の列
    'M 1604,556 C 1660,576 1720,586 1790,578',                 # → キジ〜ワシ・タカ
    'M 1790,578 C 1820,520 1826,450 1812,392',                 # → 閑々亭ぞい
    'M 1812,392 C 1780,340 1740,300 1700,276',                 # → ゴリラ・トラのすむ森
    'M 1700,276 C 1650,240 1600,214 1552,204',                 # ゴリラ・トラ 前
    'M 1552,204 C 1500,222 1470,264 1456,312',                 # → 夜の森
    'M 1456,312 C 1430,352 1400,380 1368,398',                 # → フォレストカフェ方面
    'M 1368,398 C 1330,368 1300,326 1286,288',                 # → 藤棚・バードソング
    'M 1286,288 C 1250,254 1210,232 1176,222',                 # → 動物医療センター
    'M 1176,222 C 1120,246 1076,286 1050,332',                 # → ホッキョクグマ
    'M 1050,332 C 1020,380 1006,440 1006,494',                 # 東園 西端
    'M 1006,494 C 1008,540 1000,566 984,592',                  # → いそっぷ橋 へ下る
    'M 984,592 C 962,626 934,662 906,688',                     # → いそっぷ橋 東詰
    'M 1006,494 C 1040,536 1090,586 1136,632',                 # → 日本の鳥II 方面
    'M 1136,632 C 1170,660 1200,676 1230,684',
    'M 1344,510 C 1300,540 1260,570 1230,598',                 # 中央の短絡
]
for d in PATHS:
    A(f'<path d="{d}" stroke="{C["path_edge"]}" stroke-width="26" fill="none" '
      f'stroke-linecap="round" stroke-linejoin="round"/>')
for d in PATHS:
    A(f'<path d="{d}" stroke="{C["path"]}" stroke-width="19" fill="none" '
      f'stroke-linecap="round" stroke-linejoin="round"/>')


# ================================================================== 部品
def blob(d, fill, sw=3):
    A(f'<path d="{d}" fill="{fill}" stroke="{C["line"]}" stroke-width="{sw}" stroke-linejoin="round"/>')


def oval(cx, cy, rx, ry, fill, rot=0, sw=3):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    A(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"{t} fill="{fill}" '
      f'stroke="{C["line"]}" stroke-width="{sw}"/>')


def bldg(x, y, w, h, rot=0, r=9):
    t = f' transform="rotate({rot} {x+w/2:.0f} {y+h/2:.0f})"' if rot else ''
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"{t} '
      f'fill="{C["bldg"]}" stroke="{C["bldg_edge"]}" stroke-width="3"/>')
    A(f'<rect x="{x+7}" y="{y+7}" width="{max(w-14,4)}" height="{max(h-14,4)}" rx="{max(r-4,2)}"{t} '
      f'fill="none" stroke="{C["bldg_edge"]}" stroke-width="1.4" opacity="0.55"/>')


def plot(x, y, w, h, rot=0):
    """整備中の区画(公式マップで灰色に塗られている場所)"""
    t = f' transform="rotate({rot} {x+w/2:.0f} {y+h/2:.0f})"' if rot else ''
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"{t} fill="{C["plot"]}" '
      f'stroke="{C["fence"]}" stroke-width="2.5" stroke-dasharray="9 6"/>')


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
        x = cx + random.uniform(-rx, rx)
        y = cy + random.uniform(-ry, ry)
        A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(rmin,rmax):.0f}" '
          f'fill="{fill}" opacity="{op}"/>')


def gate(cx, cy, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    A(f'<g{t}><rect x="{cx-29}" y="{cy-26}" width="58" height="52" rx="10" fill="{C["gate"]}"/>'
      f'<rect x="{cx-11}" y="{cy-12}" width="22" height="26" rx="4" fill="{C["ground"]}"/></g>')


# ================================================================== 東園の展示
# ホッキョクグマとアザラシの海(東園 北西)
blob('M 1186,246 C 1268,226 1372,240 1398,284 C 1424,330 1390,378 1314,388 '
     'C 1240,398 1176,372 1160,330 C 1146,292 1158,254 1186,246 Z', C['polar'])
pond(1226, 316, 44, 22, -8)
pond(1344, 310, 40, 20, 6)
A(f'<path d="M 1200,344 C 1250,326 1320,326 1376,344" stroke="{C["water_edge"]}" '
  f'stroke-width="2" fill="none" opacity="0.7"/>')

# 動物医療センター / バードソング / 藤棚休憩所
bldg(1268, 126, 96, 46, -18)
bldg(1370, 208, 54, 36, -12)
bldg(1440, 284, 52, 34, -6)

# フードショップ さるやまキッチン と、整備中の区画(東園 西側)
bldg(1046, 292, 60, 40, -18)
plot(1000, 368, 96, 68, -14)
plot(1140, 342, 104, 70, -10)
plot(1188, 782, 100, 64, -12)

# ゴリラ・トラのすむ森(東園 北東)
blob('M 1610,116 C 1720,92 1830,130 1852,212 C 1876,300 1820,376 1718,390 '
     'C 1626,402 1560,356 1554,280 C 1548,204 1566,130 1610,116 Z', C['forest_ex'])
scatter(1700, 250, 130, 110, 14, C['wood_dark'], 10, 20)
pond(1774, 330, 34, 16, 12)
A(f'<path d="M 1700,120 C 1690,200 1694,300 1704,388" stroke="{C["fence"]}" '
  f'stroke-width="2" stroke-dasharray="5 5" fill="none"/>')

# 夜の森(バク・コウモリなど)
bldg(1492, 258, 92, 56, -10, r=12)
blob('M 1552,326 C 1596,314 1634,330 1632,360 C 1630,392 1592,406 1556,398 '
     'C 1528,392 1518,368 1526,346 C 1532,332 1540,329 1552,326 Z', C['forest_ex'])
pond(1596, 384, 22, 10)

# フォレストカフェ
bldg(1592, 362, 50, 34, 8)

# クマたちの丘
blob('M 1428,394 C 1498,378 1552,406 1550,452 C 1548,502 1490,528 1436,518 '
     'C 1390,510 1370,476 1382,436 C 1390,408 1408,398 1428,394 Z', C['rock'])
rocks('1404,496 L 1438,448 L 1466,484 L 1498,434 L 1528,500 Z')
A(f'<path d="M 1462,396 L 1466,520" stroke="{C["fence"]}" stroke-width="2" stroke-dasharray="5 5"/>')

# ツル / クロトキ
blob('M 1434,344 C 1478,334 1512,350 1510,376 C 1508,404 1472,418 1440,410 '
     'C 1414,404 1406,384 1414,364 C 1419,352 1425,346 1434,344 Z', C['grass'])
pond(1452, 400, 20, 9)
cage(1568, 444, 26)

# ゾウのすむ森
blob('M 1318,416 C 1394,398 1456,424 1454,476 C 1452,532 1390,560 1330,550 '
     'C 1280,542 1258,506 1270,464 C 1279,434 1296,421 1318,416 Z', C['savanna'])
pond(1420, 516, 30, 15)
scatter(1360, 478, 62, 44, 5, '#CFC08F', 4, 8, 0.7)
bldg(1294, 424, 62, 40, -12)

# 世界のサル
blob('M 1288,492 C 1342,480 1382,500 1380,530 C 1378,562 1336,578 1298,570 '
     'C 1268,564 1258,540 1266,518 C 1271,502 1278,495 1288,492 Z', C['rock'])
rocks('1280,558 L 1304,520 L 1326,550 L 1350,514 L 1370,562 Z')

# バイソン / プレーリードッグ / リス
blob('M 1196,570 C 1262,556 1318,578 1316,614 C 1314,652 1258,670 1210,660 '
     'C 1174,653 1160,626 1170,598 C 1177,580 1185,573 1196,570 Z', C['savanna'])
for _ in range(10):
    x, y = random.uniform(1186, 1304), random.uniform(582, 650)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="#C2B285"/>')
cage(1252, 664, 20)

# 日本の鳥 II
cage(1200, 700, 24)

# リトルトランク(ギフトショップ) / 総合案内所 / サーラータイ
bldg(1400, 600, 54, 38, 6)
bldg(1376, 764, 62, 40, -4)
A(f'<rect x="1494" y="690" width="56" height="50" rx="4" fill="{C["roof"]}" '
  f'stroke="{C["bldg_edge"]}" stroke-width="3"/>')
A(f'<rect x="1506" y="702" width="32" height="26" rx="3" fill="{C["bldg"]}" '
  f'stroke="{C["bldg_edge"]}" stroke-width="2"/>')

# 動物慰霊碑
A(f'<rect x="1578" y="560" width="26" height="30" rx="4" fill="{C["rock_dark"]}" '
  f'stroke="{C["line"]}" stroke-width="2"/>')

# キジ・カワウソ・フクロウ・ワシタカ(東園 東縁の小展示)
blob('M 1630,548 C 1700,534 1800,540 1832,566 C 1862,592 1830,620 1760,624 '
     'C 1690,628 1634,610 1624,584 C 1618,566 1621,553 1630,548 Z', C['grass'])
pond(1706, 590, 30, 12)
cage(1660, 576, 18)
cage(1796, 580, 18)

# 閑々亭
bldg(1822, 436, 52, 36, -14, r=6)

# 旧正門(門柱と柵)
A(f'<path d="M 1596,700 L 1706,646" stroke="{C["fence"]}" stroke-width="4" '
  f'stroke-dasharray="10 7"/>')

# 日本の動物(東園 南西の張り出し)
blob('M 1156,846 C 1214,828 1268,852 1270,902 C 1272,956 1220,990 1172,978 '
     'C 1134,968 1120,932 1128,894 C 1134,866 1142,850 1156,846 Z', C['forest_ex'])
pond(1206, 906, 34, 20, -18)
scatter(1196, 898, 54, 52, 6, C['wood_dark'], 8, 14, 0.7)

# 日本の鳥 I
cage(1322, 962, 22)

# 正門(東園 南端)
gate(1462, 1080, -8)

# ================================================================== いそっぷ橋
BRIDGE = 'M 748,734 C 800,724 856,706 904,692'
A(f'<path d="{BRIDGE}" stroke="{C["bridge"]}" stroke-width="30" fill="none" stroke-linecap="round"/>')
A(f'<path d="{BRIDGE}" stroke="{C["path"]}" stroke-width="18" fill="none" stroke-linecap="round"/>')
for t in range(1, 6):
    A(f'<circle cx="{748 + t*26}" cy="{734 - t*7}" r="3" fill="{C["bldg_edge"]}"/>')

# ================================================================== 西園の展示
# アフリカの動物(西園 北) キリン・サイ・カバ・コビトカバ
blob('M 430,178 C 540,158 654,186 668,248 C 684,318 596,362 498,356 '
     'C 414,350 372,312 380,254 C 386,208 404,183 430,178 Z', C['savanna'])
pond(618, 306, 40, 20, -14)
pond(452, 236, 28, 15, 8)
bldg(486, 176, 86, 42, -14)
scatter(520, 268, 100, 52, 6, C['wood_dark'], 9, 15, 0.5)
A(f'<path d="M 536,180 C 544,238 540,304 528,354" stroke="{C["fence"]}" '
  f'stroke-width="2" stroke-dasharray="5 5" fill="none"/>')

# ハシビロコウ
cage(470, 404, 28)

# フードショップ 西園休憩所 / 小獣館 / 管理事務所 / レッサーパンダ
bldg(596, 328, 58, 40, -8)
bldg(676, 340, 84, 56, -6, r=12)
bldg(782, 362, 56, 40, -10)
cage(732, 466, 22)

# クビワペッカリー
blob('M 542,462 C 584,452 616,468 614,494 C 612,522 578,534 548,526 '
     'C 526,520 518,500 526,482 C 531,470 535,465 542,462 Z', C['savanna'])

# 両生爬虫類館(ビバリウム)
bldg(258, 424, 108, 68, -12, r=13)
pond(300, 500, 26, 12, -12)

# フラミンゴ / ペンギン
pond(444, 482, 30, 16)
pond(548, 542, 34, 17, -8)

# プチカメレオン(ギフトショップ) / カフェカメレオン / 不忍池テラス
bldg(470, 552, 48, 32, 6)
bldg(478, 602, 44, 30, -6)
bldg(438, 648, 56, 26, -14, r=6)

# アイアイのすむ森
bldg(160, 546, 96, 62, -14, r=13)
blob('M 258,596 C 300,586 330,602 328,628 C 326,656 292,668 262,660 '
     'C 240,654 232,636 240,618 C 245,604 250,599 258,596 Z', C['forest_ex'])

# パンダのもり
blob('M 636,538 C 700,524 748,550 746,596 C 744,644 690,666 640,656 '
     'C 600,648 584,618 594,582 C 601,556 616,542 636,538 Z', C['forest_ex'])
scatter(668, 596, 62, 46, 8, C['wood_dark'], 8, 14)
pond(688, 640, 24, 10)

# カート乗り場
bldg(700, 716, 52, 34, -16)

# 子ども動物園すてっぷ
blob('M 668,946 C 722,934 756,958 752,998 C 748,1042 702,1062 664,1052 '
     'C 632,1044 620,1014 630,984 C 637,962 652,950 668,946 Z', C['grass'])
bldg(614, 1070, 56, 36, -18)
for _ in range(7):
    x, y = random.uniform(642, 740), random.uniform(958, 1040)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="#BFCCA0"/>')

# 不忍池浄化施設 / みんなの広場
bldg(560, 1126, 48, 32, -20)
oval(560, 1198, 42, 26, C['grass'], -18, 2.5)

# 門
gate(242, 288, -40)   # 池之端門
gate(432, 1268, -14)  # 弁天門

# ================================================================== 敷地輪郭(最前面)
A(f'<path d="{WEST}" fill="none" stroke="{C["line"]}" stroke-width="5" opacity="0.85"/>')
A(f'<path d="{EAST}" fill="none" stroke="{C["line"]}" stroke-width="5" opacity="0.85"/>')

A('</g>')

# ================================================================== 方位記号
nx, ny, nr = 92, 128, 40
th = math.radians(NORTH_DEG)
ux, uy = math.sin(th), -math.cos(th)          # 北の単位ベクトル
px, py = math.cos(th), math.sin(th)           # 北に直交する単位ベクトル
tipx, tipy = nx + nr * ux, ny + nr * uy
tailx, taily = nx - nr * ux, ny - nr * uy
basex, basey = nx + nr * 0.18 * ux, ny + nr * 0.18 * uy
A(f'<circle cx="{nx}" cy="{ny}" r="{nr+16}" fill="#FFFFFF" opacity="0.7"/>')
A(f'<circle cx="{nx}" cy="{ny}" r="{nr+16}" fill="none" stroke="{C["line"]}" stroke-width="2"/>')
A(f'<path d="M {tailx:.1f},{taily:.1f} L {basex:.1f},{basey:.1f}" '
  f'stroke="{C["line"]}" stroke-width="3.5" stroke-linecap="round"/>')
A(f'<path d="M {tipx:.1f},{tipy:.1f} L {basex + 11*px:.1f},{basey + 11*py:.1f} '
  f'L {basex - 11*px:.1f},{basey - 11*py:.1f} Z" '
  f'fill="{C["gate"]}" stroke="{C["line"]}" stroke-width="1.5" stroke-linejoin="round"/>')

A('</svg>')

svg = '\n'.join(P)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zoo-map.svg')
with open(out, 'w', encoding='utf-8') as f:
    f.write(svg)
print(f'wrote {out} ({len(svg)} bytes)')
