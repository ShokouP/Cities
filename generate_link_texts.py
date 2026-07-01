import re
import json
import random
from pathlib import Path

html_path = Path("invisible-cities/index.html")
html = html_path.read_text(encoding="utf-8")

# Extract the cities array: find the block starting with "const cities = [" and ending with "];"
match = re.search(r"const cities = (\[.*?\]);", html, re.DOTALL)
if not match:
    raise RuntimeError("Could not find cities array")

# The array contains JS object literals; convert to JSON-safe form.
js_array = match.group(1)
# Replace single-quoted strings inside (rare) with double quotes.
# More robust: use a simple regex to grab id/name/category/excerpt fields.
city_blocks = re.findall(
    r"\{\s*id:\s*\"([^\"]+)\",\s*name:\s*\"([^\"]+)\",\s*category:\s*\"([^\"]+)\"",
    js_array,
)

cities = [
    {"id": cid, "name": cname, "category": cat}
    for cid, cname, cat in city_blocks
]

print(f"Loaded {len(cities)} cities")

verses = {
    "recombine": [
        "两座城市的影子在星光中重叠，诞生出一种尚未命名的颜色。",
        "一条新的丝线穿过夜空，把两处的低语缝进同一首诗。",
        "它们彼此靠近，像两页书在风中偶然合拢。",
        "远方的钟声与近处的潮汐在此刻同时响起。",
        "两颗星辰交换了秘密，星座的形状因此改变。",
        "一座城的记忆落在另一座城的屋顶，像一场温柔的入侵。",
        "它们之间亮起一盏灯，照亮了彼此从未见过的走廊。",
        "两个名字在黑暗中轻轻触碰，发出玻璃般的轻响。",
        "河流在此改道，把一座城的故事带向另一座城。",
        "它们的连接是一枚新的印章，盖在夜空的信封上。",
        "当第一座城的风吹进第二座城，所有的门都开始轻轻颤动。",
        "它们共享同一片夜色，从此分不清谁是谁的倒影。",
        "一座城的黎明被另一座城借走，归还时沾满了陌生的花香。",
        "两座城的轮廓在雾中相拥，合成一个更辽阔的梦。",
        "它们的相遇让时间拐了个弯，留下一串发光的足迹。",
        "一条路从一座城出发，在另一座城找到了它的终点与起点。",
        "它们的呼吸叠在一起，夜空因此多了一颗温热的星。",
        "一座城的秘密住进了另一座城的窗户，偶尔在深夜被月光翻开。",
        "两座城之间长出一座看不见的花园，只在无风的夜晚开放。",
        "它们的名字被同一次潮汐打湿，从此有了相同的光泽。",
    ],
    "break": [
        "两根琴弦同时松开，余音各自飘向不同的山谷。",
        "它们之间的桥沉入水中，只留下一圈圈散开的涟漪。",
        "一页纸被风撕成两半，分别落在两个季节里。",
        "星光在此分岔，各自寻找归途。",
        "一声低语消失在走廊尽头，门轻轻合上。",
        "两条路重新分开，像从未交汇过一样。",
        "一座城的倒影从另一座城的湖面退去。",
        "它们之间的丝线断了，线头在夜风中微微颤抖。",
        "两个名字被重新放回各自的抽屉，锁咔哒一声合上。",
        "回声渐行渐远，终于听不见了。",
        "一盏灯灭了，两扇窗同时暗了下去。",
        "它们之间的风突然转向，把熟悉的气息吹向远方。",
        "一座城的钟声不再被另一座城听见，像从不曾存在过。",
        "它们的影子从同一片墙上滑落，各奔东西。",
        "一条河在此处改了名字，从此两座城各说各的语言。",
        "夜的斗篷把两座城分开，各自沉入各自的梦境。",
        "它们之间那道看不见的桥，被一粒尘埃压垮了。",
        "一个故事的结尾被留在第一座城，开头被遗忘在第二座城。",
        "两颗星各自熄灭了自己的光，不再互相辨认。",
        "它们的离别轻得像一片羽毛，落地时却惊动了整个星空。",
    ],
}

random.seed(42)

link_texts = {"recombine": {}, "break": {}}

for a in cities:
    for b in cities:
        if a["id"] == b["id"]:
            continue
        key = f"{a['id']}:{b['id']}"
        for action in ("recombine", "break"):
            verse = random.choice(verses[action])
            link_texts[action][key] = f"{a['name']} 与 {b['name']}：{verse}"

out_path = Path("link-texts.json")
out_path.write_text(json.dumps(link_texts, ensure_ascii=False, indent=2), encoding="utf-8")

total = len(cities) * (len(cities) - 1) * 2
print(f"Generated {total} link texts -> {out_path}")
print(f"File size: {out_path.stat().st_size / 1024:.1f} KB")
