from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# Color palette
COLORS = {
    "blue_dark":    RGBColor(0x1A, 0x3A, 0x5C),   # title bg
    "blue_mid":     RGBColor(0x1E, 0x5B, 0x9B),   # blue slides accent
    "blue_light":   RGBColor(0xD6, 0xE8, 0xF7),   # blue slide bg
    "red_mid":      RGBColor(0xC0, 0x39, 0x2B),   # red slides accent
    "red_light":    RGBColor(0xFD, 0xED, 0xEB),   # red slide bg
    "green_mid":    RGBColor(0x1E, 0x8B, 0x4C),   # green slides accent
    "green_light":  RGBColor(0xD5, 0xF5, 0xE3),   # green slide bg
    "yellow_mid":   RGBColor(0xD4, 0xAC, 0x0D),   # yellow slides accent
    "yellow_light": RGBColor(0xFD, 0xF9, 0xE3),   # yellow slide bg
    "purple_mid":   RGBColor(0x76, 0x44, 0xAB),   # purple slides accent
    "purple_light": RGBColor(0xF4, 0xEC, 0xFC),   # purple slide bg
    "brown_mid":    RGBColor(0x79, 0x55, 0x48),   # brown slides accent
    "brown_light":  RGBColor(0xEF, 0xEB, 0xE9),   # brown slide bg
    "white":        RGBColor(0xFF, 0xFF, 0xFF),
    "black":        RGBColor(0x1A, 0x1A, 0x1A),
    "gray_light":   RGBColor(0xF2, 0xF2, 0xF2),
    "accent_gold":  RGBColor(0xF3, 0x9C, 0x12),
}

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]  # blank


def add_rect(slide, x, y, w, h, fill_color, line_color=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape


def add_text_box(slide, text, x, y, w, h,
                 font_size=18, bold=False, color=None,
                 align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return txBox


def add_bullet_text(slide, items, x, y, w, h,
                    font_size=16, color=None, bullet_char="•",
                    title=None, title_size=20, accent_color=None):
    """Add a text box with bullet points"""
    txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    txBox.word_wrap = True
    tf = txBox.text_frame
    tf.word_wrap = True

    first = True
    if title:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = title
        run.font.size = Pt(title_size)
        run.font.bold = True
        if accent_color:
            run.font.color.rgb = accent_color
        elif color:
            run.font.color.rgb = color

    for item in items:
        p = tf.paragraphs[0] if (first and not title) else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = f"{bullet_char}  {item}"
        run.font.size = Pt(font_size)
        if color:
            run.font.color.rgb = color

    return txBox


def add_table(slide, headers, rows, x, y, w, h,
              header_fill, header_text_color, row_fills,
              font_size=14):
    cols = len(headers)
    total_rows = 1 + len(rows)
    table = slide.shapes.add_table(total_rows, cols, Inches(x), Inches(y), Inches(w), Inches(h)).table

    col_width = Inches(w / cols)
    for i in range(cols):
        table.columns[i].width = col_width

    def set_cell(cell, text, fill_rgb, txt_color, bold=False, sz=font_size):
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill_rgb
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.clear()
        run = p.add_run()
        run.text = text
        run.font.size = Pt(sz)
        run.font.bold = bold
        run.font.color.rgb = txt_color

    # Header row
    for j, h_text in enumerate(headers):
        set_cell(table.cell(0, j), h_text, header_fill, header_text_color, bold=True)

    # Data rows
    for i, row in enumerate(rows):
        fill = row_fills[i % len(row_fills)]
        for j, val in enumerate(row):
            set_cell(table.cell(i + 1, j), str(val), fill, COLORS["black"])

    return table


def make_header_bar(slide, title, accent_color, bg_color, subtitle=None):
    """Top bar with title"""
    add_rect(slide, 0, 0, 13.33, 1.4, accent_color)
    add_text_box(slide, title, 0.3, 0.12, 12.5, 0.9,
                 font_size=30, bold=True, color=COLORS["white"],
                 align=PP_ALIGN.LEFT)
    if subtitle:
        add_text_box(slide, subtitle, 0.3, 0.85, 12.5, 0.5,
                     font_size=14, bold=False, color=RGBColor(0xCC, 0xDD, 0xFF),
                     align=PP_ALIGN.LEFT)
    # fill rest of slide
    add_rect(slide, 0, 1.4, 13.33, 6.1, bg_color)


def make_slide(color_key):
    """Create blank slide with color scheme"""
    slide = prs.slides.add_slide(blank_layout)
    accent = COLORS[f"{color_key}_mid"]
    bg = COLORS[f"{color_key}_light"]
    return slide, accent, bg


def make_accent_slide(color_key):
    slide = prs.slides.add_slide(blank_layout)
    return slide, COLORS[f"{color_key}_mid"], COLORS[f"{color_key}_light"]


# ─────────────────────────────────────────────────────────────────
# SLIDE 1 — Title
# ─────────────────────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)

# Background gradient effect using two rects
add_rect(slide, 0, 0, 13.33, 7.5, COLORS["blue_dark"])
add_rect(slide, 0, 5.2, 13.33, 2.3, RGBColor(0x0F, 0x2A, 0x44))

# Gold accent bar
add_rect(slide, 0, 2.55, 0.18, 2.5, COLORS["accent_gold"])

# Main title
add_text_box(slide, "FinOps", 0.5, 0.8, 12, 1.3,
             font_size=60, bold=True, color=COLORS["white"], align=PP_ALIGN.LEFT)
add_text_box(slide, "Архитектура, управляемая стоимостью", 0.5, 2.1, 12, 0.85,
             font_size=28, bold=False, color=RGBColor(0x90, 0xC8, 0xFF),
             align=PP_ALIGN.LEFT)

# Subtitle
add_text_box(slide,
             "Как принимать архитектурные решения с учётом стоимости AI-систем",
             0.5, 2.9, 12, 0.7,
             font_size=18, bold=False, color=RGBColor(0xCC, 0xDD, 0xEE),
             align=PP_ALIGN.LEFT, italic=True)

# Meta info
add_text_box(slide, "OTUS · AI Architect · 2026", 0.5, 6.6, 12, 0.6,
             font_size=14, bold=False, color=RGBColor(0x80, 0xA0, 0xC0),
             align=PP_ALIGN.LEFT)

# decorative element
add_rect(slide, 9.5, 1.2, 3.5, 3.5, RGBColor(0x25, 0x55, 0x90))
add_text_box(slide, "Cost = f(\nArchitecture,\nLoad,\nEfficiency\n)", 9.6, 1.4, 3.3, 3.1,
             font_size=16, bold=True, color=RGBColor(0x70, 0xB8, 0xFF),
             align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 2 — О чём занятие
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("blue")
make_header_bar(slide, "О чём занятие", accent, bg)

items = [
    "Почему cloud bill выходит из-под контроля",
    "Что такое FinOps и зачем он инженеру",
    "Где архитектура влияет на стоимость",
    "Как находить точки оптимизации",
    "Практика: снижение затрат на 20%+",
]
add_bullet_text(slide, items, 0.8, 1.6, 11.5, 5.0,
                font_size=20, color=COLORS["black"],
                title="Программа занятия:", title_size=22,
                accent_color=accent)

add_text_box(slide,
             "⚠  Это не лекция про финансы — это лекция про архитектурное мышление",
             0.5, 6.3, 12.3, 0.8,
             font_size=15, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)
add_rect(slide, 0.3, 6.2, 12.7, 1.0, accent)
add_text_box(slide,
             "⚠  Это не лекция про финансы — это лекция про архитектурное мышление",
             0.5, 6.3, 12.3, 0.8,
             font_size=15, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 3 — Проблема: проекты не учитывают стоимость
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("red")
make_header_bar(slide, "Проблема: проекты не учитывают стоимость", accent, bg)

# Left column
add_rect(slide, 0.5, 1.7, 5.8, 2.6, RGBColor(0xFF, 0xFF, 0xFF))
add_text_box(slide, "Архитектура проектируется под:", 0.7, 1.8, 5.5, 0.5,
             font_size=15, bold=True, color=accent)
items_left = ["Производительность", "Отказоустойчивость", "Масштабируемость"]
add_bullet_text(slide, items_left, 0.7, 2.3, 5.5, 1.8,
                font_size=17, color=COLORS["black"])

# Right column
add_rect(slide, 7.0, 1.7, 5.8, 2.6, RGBColor(0xFF, 0xFF, 0xFF))
add_text_box(slide, "👉  Стоимость — постфактум:", 7.2, 1.8, 5.5, 0.5,
             font_size=15, bold=True, color=accent)
items_right = ["Неожиданные счета", "Бюджетные ограничения", "Переделка архитектуры"]
add_bullet_text(slide, items_right, 7.2, 2.3, 5.5, 1.8,
                font_size=17, color=COLORS["black"])

# Arrow
add_text_box(slide, "→", 6.2, 2.8, 0.8, 0.7, font_size=36, bold=True, color=accent)

# Quote block
add_rect(slide, 0.5, 4.7, 12.3, 1.5, RGBColor(0xC0, 0x39, 0x2B))
add_text_box(slide,
             "\"Самая дорогая архитектура — это та,\nкоторую потом пришлось переделывать\"",
             0.8, 4.8, 11.8, 1.3,
             font_size=20, bold=True, color=COLORS["white"],
             align=PP_ALIGN.CENTER, italic=True)

# ─────────────────────────────────────────────────────────────────
# SLIDE 4 — Почему cloud bill растёт
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("red")
make_header_bar(slide, "Почему cloud bill растёт", accent, bg)

causes = [
    ("Overprovisioning", "Ресурсы выделены «с запасом» и не используются"),
    ("Zombie instances", "Постоянные инстансы, о которых забыли"),
    ("Дублирование данных", "Одни и те же данные хранятся в нескольких местах"),
    ("Неправильные storage-классы", "Все данные в hot storage независимо от частоты доступа"),
    ("Отсутствие lifecycle", "Данные никогда не архивируются и не удаляются"),
]

y_pos = 1.6
for i, (title, desc) in enumerate(causes):
    add_rect(slide, 0.5, y_pos, 12.3, 0.82,
             COLORS["white"] if i % 2 == 0 else RGBColor(0xFB, 0xF0, 0xEF))
    add_text_box(slide, f"🔴  {title}", 0.7, y_pos + 0.05, 3.8, 0.5,
                 font_size=15, bold=True, color=accent)
    add_text_box(slide, desc, 4.7, y_pos + 0.07, 8.0, 0.5,
                 font_size=15, color=COLORS["black"])
    y_pos += 0.9

add_text_box(slide, "Cloud по умолчанию оптимизирован под скорость, а не под стоимость",
             0.5, 6.5, 12.3, 0.7, font_size=16, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 5 — AI/ML специфика
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("red")
make_header_bar(slide, "Особенности AI/ML систем", accent, bg)

items_ai = [
    "GPU простаивают между training-запусками",
    "Training запускается чаще, чем реально нужно",
    "Хранится весь исторический датасет без очистки",
    "Inference всегда realtime — даже там, где не нужно",
    "Избыточное логирование экспериментов",
]
add_bullet_text(slide, items_ai, 0.7, 1.7, 8.5, 4.5,
                font_size=19, color=COLORS["black"])

add_rect(slide, 9.3, 1.7, 3.7, 4.5, RGBColor(0xC0, 0x39, 0x2B))
add_text_box(slide, "Ключевая\nпроблема:", 9.5, 2.0, 3.3, 1.0,
             font_size=16, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER)
add_text_box(slide, "AI-системы\nпо умолчанию\nдорогие", 9.5, 3.0, 3.3, 2.3,
             font_size=22, bold=True, color=COLORS["accent_gold"],
             align=PP_ALIGN.CENTER)

add_text_box(slide,
             "Связь с практикой: Kubeflow / MLflow / pipelines",
             0.5, 6.5, 12.3, 0.7, font_size=14, bold=False,
             color=accent, align=PP_ALIGN.CENTER, italic=True)

# ─────────────────────────────────────────────────────────────────
# SLIDE 6 — Что такое FinOps
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("green")
make_header_bar(slide, "Что такое FinOps", accent, bg)

add_text_box(slide, "FinOps = практика управления облачными затратами",
             0.5, 1.6, 12.3, 0.8, font_size=22, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# NOT block
add_rect(slide, 0.5, 2.6, 5.8, 2.5, RGBColor(0xFF, 0xEB, 0xEB))
add_text_box(slide, "❌  НЕ:", 0.7, 2.7, 5.5, 0.5, font_size=18, bold=True,
             color=COLORS["red_mid"])
add_bullet_text(slide, ["Бухгалтерия", "Контроль бюджета", "Урезание возможностей"],
                0.7, 3.2, 5.5, 1.8, font_size=17, color=COLORS["black"])

# IS block
add_rect(slide, 7.0, 2.6, 5.8, 2.5, RGBColor(0xD5, 0xF5, 0xE3))
add_text_box(slide, "✅  А:", 7.2, 2.7, 5.5, 0.5, font_size=18, bold=True,
             color=accent)
add_bullet_text(slide, ["Часть инженерного процесса",
                         "Continuous optimization",
                         "Метрика качества архитектуры"],
                7.2, 3.2, 5.5, 1.8, font_size=17, color=COLORS["black"])

add_rect(slide, 0.5, 5.4, 12.3, 1.2, accent)
add_text_box(slide, "FinOps = DevOps + Finance + Architecture",
             0.5, 5.6, 12.3, 0.8, font_size=24, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 7 — Принципы FinOps
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("green")
make_header_bar(slide, "Принципы FinOps", accent, bg)

principles = [
    ("1", "Visibility", "Прозрачность затрат — каждая команда видит свой cost"),
    ("2", "Accountability", "Распределённая ответственность за расходы"),
    ("3", "Optimization", "Постоянный поиск и устранение неэффективностей"),
    ("4", "Iteration", "Непрерывные улучшения, а не разовые акции"),
]

y_pos = 1.6
for num, name, desc in principles:
    add_rect(slide, 0.5, y_pos, 0.9, 1.0, accent)
    add_text_box(slide, num, 0.5, y_pos + 0.1, 0.9, 0.8,
                 font_size=32, bold=True, color=COLORS["white"],
                 align=PP_ALIGN.CENTER)
    add_rect(slide, 1.5, y_pos, 11.3, 1.0, COLORS["white"])
    add_text_box(slide, name, 1.7, y_pos + 0.05, 3.0, 0.45,
                 font_size=18, bold=True, color=accent)
    add_text_box(slide, desc, 1.7, y_pos + 0.48, 10.8, 0.45,
                 font_size=15, color=COLORS["black"])
    y_pos += 1.12

# ─────────────────────────────────────────────────────────────────
# SLIDE 8 — Смена мышления
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("green")
make_header_bar(slide, "Смена мышления", accent, bg,
                subtitle="Самый важный слайд — смена парадигмы")

headers = ["Без FinOps", "С FinOps"]
rows = [
    ["Фиксированный бюджет", "Динамическая оптимизация"],
    ["Cost = проблема", "Cost = метрика"],
    ["Централизованный контроль", "Распределённая ответственность"],
    ["Оптимизация раз в квартал", "Continuous improvement"],
    ["Архитектор не думает о cost", "Архитектор = cost owner"],
]
add_table(slide, headers, rows,
          x=1.0, y=1.7, w=11.3, h=4.8,
          header_fill=accent,
          header_text_color=COLORS["white"],
          row_fills=[COLORS["white"], COLORS["green_light"]],
          font_size=15)

add_text_box(slide, "👉  Мы меняем paradigm, не просто добавляем инструменты",
             0.5, 6.55, 12.3, 0.65, font_size=15, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 9 — Стоимость как функция архитектуры
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("green")
make_header_bar(slide, "Стоимость как функция архитектуры", accent, bg)

add_rect(slide, 2.0, 1.7, 9.3, 1.5, accent)
add_text_box(slide, "Cost = f( Architecture,  Load,  Efficiency )",
             2.0, 1.85, 9.3, 1.1,
             font_size=26, bold=True, color=COLORS["white"],
             align=PP_ALIGN.CENTER)

factors = [
    ("Architecture", COLORS["blue_mid"],
     "Как устроена система\nВыбор компонентов, паттернов, интеграций"),
    ("Load", COLORS["red_mid"],
     "Нагрузка от бизнес-требований\n(в основном вне нашего контроля)"),
    ("Efficiency", COLORS["green_mid"],
     "Эффективность использования ресурсов\nRightsizing, batching, caching"),
]

x_pos = 0.5
for name, color, desc in factors:
    add_rect(slide, x_pos, 3.5, 4.0, 2.5, color)
    add_text_box(slide, name, x_pos, 3.6, 4.0, 0.7,
                 font_size=18, bold=True, color=COLORS["white"],
                 align=PP_ALIGN.CENTER)
    add_text_box(slide, desc, x_pos + 0.1, 4.35, 3.8, 1.5,
                 font_size=13, color=COLORS["white"],
                 align=PP_ALIGN.CENTER)
    x_pos += 4.42

add_rect(slide, 0.5, 6.3, 12.3, 0.9, RGBColor(0x2E, 0x7D, 0x32))
add_text_box(slide, "👉  Мы управляем только Architecture и Efficiency",
             0.5, 6.4, 12.3, 0.7, font_size=17, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 10 — Роль архитектора
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("yellow")
make_header_bar(slide, "Роль архитектора", accent, bg)

add_rect(slide, 4.0, 1.7, 5.3, 1.0, accent)
add_text_box(slide, "Архитектор = Cost Owner",
             4.0, 1.8, 5.3, 0.8, font_size=24, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)

areas = [
    ("⚙  Compute", ["CPU vs GPU", "Batch vs realtime", "Autoscaling vs fixed"]),
    ("💾  Storage", ["Hot vs cold", "S3 vs FS vs DB", "Lifecycle policies"]),
    ("🌐  Network", ["Межзонный трафик", "Egress cost", "Data locality"]),
    ("📊  Data patterns", ["Batching", "Caching", "Compression"]),
]

x_positions = [0.4, 3.5, 6.6, 9.7]
for i, ((title, items), x) in enumerate(zip(areas, x_positions)):
    add_rect(slide, x, 3.0, 3.0, 3.5, COLORS["white"])
    add_rect(slide, x, 3.0, 3.0, 0.55, accent)
    add_text_box(slide, title, x + 0.1, 3.05, 2.8, 0.45,
                 font_size=14, bold=True, color=COLORS["white"])
    for j, item in enumerate(items):
        add_text_box(slide, f"• {item}", x + 0.15, 3.6 + j * 0.65, 2.8, 0.6,
                     font_size=13, color=COLORS["black"])

add_text_box(slide,
             "Каждое архитектурное решение имеет ценник — архитектор его видит",
             0.5, 6.6, 12.3, 0.65, font_size=15, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 11 — Compute решения
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("yellow")
make_header_bar(slide, "Compute: архитектурные решения", accent, bg)

decisions = [
    ("CPU vs GPU", "GPU дороже в 5–10x.\nИспользуй только там, где реально нужен параллелизм",
     "💡 Служение LLM inference → GPU,\nBatch ETL → CPU"),
    ("Batch vs Realtime", "Realtime = постоянные ресурсы.\nBatch = ресурсы только во время выполнения",
     "💡 Нужен ли ответ за <100ms?\nЕсли нет — это batch!"),
    ("Autoscaling vs Fixed", "Fixed instances → платишь 24/7.\nAutoscaling → платишь за нагрузку",
     "💡 Типовая экономия:\n30–50% для непостоянной нагрузки"),
]

y_pos = 1.6
for title, desc, tip in decisions:
    add_rect(slide, 0.5, y_pos, 8.2, 1.5, COLORS["white"])
    add_rect(slide, 0.5, y_pos, 0.15, 1.5, accent)
    add_text_box(slide, title, 0.75, y_pos + 0.05, 7.8, 0.5,
                 font_size=16, bold=True, color=accent)
    add_text_box(slide, desc, 0.75, y_pos + 0.55, 7.8, 0.85,
                 font_size=13, color=COLORS["black"])
    add_rect(slide, 8.8, y_pos, 4.0, 1.5, RGBColor(0xFD, 0xF3, 0xD0))
    add_text_box(slide, tip, 8.9, y_pos + 0.1, 3.8, 1.3,
                 font_size=12, color=RGBColor(0x5D, 0x4E, 0x00))
    y_pos += 1.65

# ─────────────────────────────────────────────────────────────────
# SLIDE 12 — Storage решения
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("yellow")
make_header_bar(slide, "Storage: архитектурные решения", accent, bg)

# Storage tier comparison
add_text_box(slide, "Сравнение storage-классов:", 0.5, 1.6, 12.3, 0.5,
             font_size=18, bold=True, color=accent)

headers = ["Класс", "Стоимость", "Доступность", "Использование"]
rows = [
    ["S3 Standard (hot)", "$$$$", "Мгновенно", "Активные данные (<30 дней)"],
    ["S3 Infrequent Access", "$$", "Секунды", "Данные 30–90 дней"],
    ["S3 Glacier", "$", "Минуты", "Архив 90+ дней"],
    ["S3 Deep Archive", "¢", "Часы", "Долгосрочный архив"],
]
add_table(slide, headers, rows,
          x=0.5, y=2.2, w=12.3, h=3.2,
          header_fill=accent,
          header_text_color=COLORS["white"],
          row_fills=[COLORS["white"], COLORS["yellow_light"]],
          font_size=14)

add_rect(slide, 0.5, 5.7, 5.8, 1.2, RGBColor(0xFF, 0xEB, 0xEB))
add_text_box(slide, "💥 Типичная ошибка:", 0.7, 5.8, 5.4, 0.4,
             font_size=14, bold=True, color=COLORS["red_mid"])
add_text_box(slide, "Всё хранится в hot storage\n→ переплата 50–80%",
             0.7, 6.2, 5.4, 0.6, font_size=14, color=COLORS["red_mid"])

add_rect(slide, 7.0, 5.7, 5.8, 1.2, COLORS["green_light"])
add_text_box(slide, "✅ Решение:", 7.2, 5.8, 5.4, 0.4,
             font_size=14, bold=True, color=COLORS["green_mid"])
add_text_box(slide, "S3 Lifecycle policy:\nhot → IA → Glacier автоматически",
             7.2, 6.2, 5.4, 0.6, font_size=14, color=COLORS["green_mid"])

# ─────────────────────────────────────────────────────────────────
# SLIDE 13 — Network cost
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("yellow")
make_header_bar(slide, "Network: скрытые расходы", accent, bg)

network_items = [
    ("Egress traffic", "Самый дорогой тип трафика.\nОблако берёт деньги за исходящий трафик во внешний интернет", "~$0.08–0.09/GB"),
    ("Cross-AZ traffic", "Трафик между зонами доступности внутри одного региона", "~$0.01/GB"),
    ("Cross-region", "Трафик между регионами — очень дорого", "~$0.02–0.08/GB"),
    ("Intra-AZ", "Трафик внутри одной зоны", "Бесплатно"),
]

y_pos = 1.65
for title, desc, cost in network_items:
    add_rect(slide, 0.5, y_pos, 9.5, 1.1, COLORS["white"])
    add_text_box(slide, title, 0.7, y_pos + 0.05, 4.5, 0.45,
                 font_size=15, bold=True, color=accent)
    add_text_box(slide, desc, 0.7, y_pos + 0.52, 9.0, 0.45,
                 font_size=13, color=COLORS["black"])
    add_rect(slide, 10.1, y_pos, 2.7, 1.1, accent if cost != "Бесплатно" else COLORS["green_mid"])
    add_text_box(slide, cost, 10.1, y_pos + 0.25, 2.7, 0.6,
                 font_size=14, bold=True, color=COLORS["white"],
                 align=PP_ALIGN.CENTER)
    y_pos += 1.2

add_text_box(slide, "💥 Типичная ошибка: данные гоняются между регионами без необходимости",
             0.5, 6.55, 12.3, 0.65, font_size=14, bold=True,
             color=COLORS["red_mid"], align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 14 — AI pipeline
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("purple")
make_header_bar(slide, "Стоимость AI/ML Pipeline", accent, bg)

stages = ["Data\nIngestion", "Feature\nEngineering", "Model\nTraining", "Model\nServing", "Monitoring"]
stage_colors = [
    RGBColor(0x5B, 0x9B, 0xD5),
    RGBColor(0x70, 0xAD, 0x47),
    RGBColor(0xFF, 0x75, 0x22),
    RGBColor(0xA5, 0x35, 0xBF),
    RGBColor(0x00, 0x9B, 0x77),
]

x_pos = 0.5
for i, (stage, color) in enumerate(zip(stages, stage_colors)):
    add_rect(slide, x_pos, 1.8, 2.3, 1.6, color)
    add_text_box(slide, stage, x_pos, 2.1, 2.3, 1.0,
                 font_size=16, bold=True, color=COLORS["white"],
                 align=PP_ALIGN.CENTER)
    if i < 4:
        add_text_box(slide, "→", x_pos + 2.3, 2.3, 0.3, 0.8,
                     font_size=24, bold=True, color=accent, align=PP_ALIGN.CENTER)
    x_pos += 2.6

# Cost bars (approximate)
costs = [10, 15, 70, 20, 5]  # relative %
cost_labels = ["$", "$$", "$$$$$", "$$$", "$"]
x_pos = 0.5
for i, (cost_pct, label, color) in enumerate(zip(costs, cost_labels, stage_colors)):
    bar_h = cost_pct * 0.03
    y = 3.6 + (0.8 - bar_h)  # align bottom
    if cost_pct > 0:
        add_rect(slide, x_pos + 0.3, 3.7 + (2.0 - bar_h), 1.7, bar_h + 0.1, color)
    add_text_box(slide, f"{cost_pct}%\n{label}", x_pos, 5.9, 2.3, 0.8,
                 font_size=14, bold=True, color=color, align=PP_ALIGN.CENTER)
    x_pos += 2.6

add_text_box(slide, "Training = до 70% всех затрат на AI/ML систему",
             0.5, 6.7, 12.3, 0.55, font_size=16, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)
add_rect(slide, 0.5, 6.65, 12.3, 0.65, accent)
add_text_box(slide, "Training = до 70% всех затрат на AI/ML систему",
             0.5, 6.7, 12.3, 0.55, font_size=16, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 15 — Типовые утечки стоимости
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("purple")
make_header_bar(slide, "Типовые утечки стоимости в AI/ML", accent, bg)

leaks = [
    ("Training слишком часто", "Запускается ежедневно там, где достаточно еженедельно", "20–40%"),
    ("Realtime вместо batch", "Inference в realtime там, где приемлема задержка", "15–30%"),
    ("Overprovisioned serving", "Слишком большие инстансы для serving-нагрузки", "20–40%"),
    ("Excessive logging", "Логируется всё подряд без retention policy", "20–50%"),
    ("Постоянные GPU-инстансы", "GPU работают 24/7, но используются 10–20% времени", "до 60%"),
]

headers = ["Утечка", "Причина", "Потенциальная экономия"]
rows = [(title, desc, saving) for title, desc, saving in leaks]
add_table(slide, headers, rows,
          x=0.5, y=1.6, w=12.3, h=5.0,
          header_fill=accent,
          header_text_color=COLORS["white"],
          row_fills=[COLORS["white"], COLORS["purple_light"]],
          font_size=13)

add_text_box(slide, "Самые дорогие решения часто принимаются «по умолчанию»",
             0.5, 6.7, 12.3, 0.55, font_size=15, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 16 — Инструменты
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("brown")
make_header_bar(slide, "Инструменты FinOps", accent, bg)

tools = [
    ("AWS Cost Explorer /\nGCP Billing Dashboard",
     "Визуализация расходов по сервисам, регионам, тегам.\nАнализ трендов и аномалий.",
     "Cloud Native"),
    ("Prometheus +\nGrafana",
     "Метрики использования ресурсов Kubernetes.\nRightsizing рекомендации.",
     "Open Source"),
    ("Kubecost",
     "Cost allocation по namespace, team, workload.\nPod-level cost visibility.",
     "K8s Specific"),
    ("MLflow",
     "Tracking экспериментов с привязкой к ресурсам.\nCost per experiment analysis.",
     "ML Specific"),
]

x_positions = [0.3, 3.6, 6.9, 10.2]
for (title, desc, tag), x in zip(tools, x_positions):
    add_rect(slide, x, 1.7, 2.9, 4.5, COLORS["white"])
    add_rect(slide, x, 1.7, 2.9, 0.5, accent)
    add_text_box(slide, tag, x + 0.1, 1.72, 2.7, 0.4,
                 font_size=11, bold=True, color=COLORS["white"])
    add_text_box(slide, title, x + 0.1, 2.3, 2.7, 1.0,
                 font_size=14, bold=True, color=accent)
    add_text_box(slide, desc, x + 0.1, 3.35, 2.7, 2.7,
                 font_size=12, color=COLORS["black"])

add_text_box(slide, "Инструменты дают visibility — но решения принимает архитектор",
             0.5, 6.5, 12.3, 0.7, font_size=15, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 17 — Практики
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("brown")
make_header_bar(slide, "Практики FinOps", accent, bg)

practices = [
    ("🏷  Tagging", "project / team / env / cost-center.\nБез тегов невозможно атрибуция стоимости"),
    ("💰  Budgets + Alerts", "Автоматические оповещения при превышении порогов"),
    ("📐  Rightsizing", "Регулярный анализ использования ресурсов и оптимизация"),
    ("⚡  Spot/Preemptible", "Экономия до 60–90% для fault-tolerant нагрузок"),
    ("♻  Lifecycle policies", "Автоматическое перемещение данных между storage-классами"),
]

y_pos = 1.65
for i, (title, desc) in enumerate(practices):
    color = accent if i % 2 == 0 else RGBColor(0x5D, 0x40, 0x37)
    add_rect(slide, 0.5, y_pos, 12.3, 0.95, COLORS["white"])
    add_rect(slide, 0.5, y_pos, 3.5, 0.95, color)
    add_text_box(slide, title, 0.7, y_pos + 0.2, 3.2, 0.55,
                 font_size=15, bold=True, color=COLORS["white"])
    add_text_box(slide, desc, 4.2, y_pos + 0.1, 8.5, 0.75,
                 font_size=14, color=COLORS["black"])
    y_pos += 1.02

add_rect(slide, 0.5, 6.65, 12.3, 0.65, RGBColor(0x4E, 0x34, 0x2E))
add_text_box(slide, "Золотое правило: нет тегов → нет FinOps",
             0.5, 6.7, 12.3, 0.55, font_size=16, bold=True,
             color=COLORS["accent_gold"], align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 18 — ПРАКТИКА: Постановка задачи
# ─────────────────────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, 13.33, 7.5, RGBColor(0x0D, 0x47, 0xA1))

add_text_box(slide, "🧪 ПРАКТИЧЕСКАЯ ЧАСТЬ", 0.5, 0.5, 12.3, 0.8,
             font_size=20, bold=True, color=RGBColor(0x90, 0xCA, 0xF9),
             align=PP_ALIGN.CENTER)
add_text_box(slide, "Анализ Cloud Bill", 0.5, 1.4, 12.3, 1.2,
             font_size=42, bold=True, color=COLORS["white"],
             align=PP_ALIGN.CENTER)

add_rect(slide, 2.0, 2.9, 9.3, 0.8, RGBColor(0x1E, 0x88, 0xE5))
add_text_box(slide, "Задача: снизить стоимость AI-системы на ≥20%",
             2.0, 2.95, 9.3, 0.65, font_size=18, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)

add_text_box(slide, "Формат:", 1.0, 3.9, 2.0, 0.5,
             font_size=16, bold=True, color=RGBColor(0x90, 0xCA, 0xF9))
add_bullet_text(slide, ["Работа в группах (3–4 человека)", "15 минут на анализ", "5 минут на презентацию решения"],
                1.0, 4.4, 11.3, 2.0, font_size=18, color=COLORS["white"])

add_text_box(slide, "Формат оценки:", 6.5, 3.9, 3.5, 0.5,
             font_size=16, bold=True, color=RGBColor(0x90, 0xCA, 0xF9))
add_bullet_text(slide, ["Найдены ключевые источники", "Корректные причины", "Реалистичные решения"],
                6.5, 4.4, 6.3, 2.0, font_size=18, color=COLORS["white"])

# ─────────────────────────────────────────────────────────────────
# SLIDE 19 — Cloud bill
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("blue")
make_header_bar(slide, "Входные данные: Cloud Bill", accent, bg,
                subtitle="Реальная ситуация — AI-система в продакшене")

headers = ["Сервис", "Стоимость/мес", "Доля", "Примечание"]
rows = [
    ["EC2 GPU (p3.2xlarge × 4)", "$12,000", "52%", "24/7, utilization ~15%"],
    ["Kubernetes nodes", "$4,000", "17%", "Fixed size, нет autoscaling"],
    ["S3 Storage", "$3,500", "15%", "Весь датасет в Standard tier"],
    ["Data transfer", "$2,000", "9%", "Cross-region replication"],
    ["CloudWatch Logging", "$1,500", "7%", "Все логи, 90 дней retention"],
    ["ИТОГО", "$23,000", "100%", ""],
]
add_table(slide, headers, rows,
          x=0.5, y=1.7, w=12.3, h=4.8,
          header_fill=accent,
          header_text_color=COLORS["white"],
          row_fills=[COLORS["white"], COLORS["blue_light"]],
          font_size=14)

add_text_box(slide, "Вопрос к группам: где biggest win?",
             0.5, 6.65, 12.3, 0.6, font_size=16, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 20 — Архитектура системы
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("blue")
make_header_bar(slide, "Архитектура AI-системы (намеренно плохая)", accent, bg)

problems = [
    ("📅 Ежедневный training", "Pipeline запускается каждый день в 00:00\nДанные обновляются раз в неделю"),
    ("⚡ Realtime inference", "Все запросы обрабатываются в realtime\n95% запросов могут ждать до 1 минуты"),
    ("💾 S3 без lifecycle", "Все данные хранятся в Standard tier\nДатасеты за 3 года без архивирования"),
    ("📈 Нет autoscaling", "Kubernetes с фиксированным числом нод\nПик нагрузки — 2 часа в день"),
]

y_pos = 1.7
for i, (title, desc) in enumerate(problems):
    color = COLORS["red_mid"] if i % 2 == 0 else RGBColor(0xC0, 0x39, 0x2B)
    add_rect(slide, 0.5, y_pos, 12.3, 1.15, COLORS["white"])
    add_rect(slide, 0.5, y_pos, 0.18, 1.15, color)
    add_text_box(slide, title, 0.8, y_pos + 0.05, 5.0, 0.5,
                 font_size=16, bold=True, color=color)
    add_text_box(slide, desc, 0.8, y_pos + 0.55, 11.7, 0.5,
                 font_size=14, color=COLORS["black"])
    y_pos += 1.25

add_text_box(slide, "Это намеренно плохая архитектура — найди все проблемы",
             0.5, 6.65, 12.3, 0.6, font_size=14, bold=True,
             color=COLORS["red_mid"], align=PP_ALIGN.CENTER, italic=True)

# ─────────────────────────────────────────────────────────────────
# SLIDE 21 — Задание
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("blue")
make_header_bar(slide, "Задание для групп", accent, bg)

add_text_box(slide, "Проанализируйте архитектуру и cloud bill:", 0.5, 1.6, 12.3, 0.6,
             font_size=18, bold=True, color=accent)

tasks = [
    ("1", "Найти 3–5 главных источников затрат",
     "Какие сервисы/компоненты создают наибольшие расходы?"),
    ("2", "Определить архитектурные причины",
     "Почему так получилось? Какие решения привели к этому?"),
    ("3", "Предложить конкретные изменения",
     "Что именно нужно изменить? Какие паттерны применить?"),
    ("4", "Оценить потенциальную экономию",
     "На сколько % можно снизить bill для каждого решения?"),
]

y_pos = 2.3
for num, task, hint in tasks:
    add_rect(slide, 0.5, y_pos, 0.65, 0.85, accent)
    add_text_box(slide, num, 0.5, y_pos + 0.07, 0.65, 0.7,
                 font_size=28, bold=True, color=COLORS["white"],
                 align=PP_ALIGN.CENTER)
    add_rect(slide, 1.2, y_pos, 11.6, 0.85, COLORS["white"])
    add_text_box(slide, task, 1.4, y_pos + 0.04, 11.2, 0.4,
                 font_size=15, bold=True, color=COLORS["black"])
    add_text_box(slide, hint, 1.4, y_pos + 0.44, 11.2, 0.35,
                 font_size=12, color=RGBColor(0x55, 0x55, 0x55), italic=True)
    y_pos += 1.0

add_rect(slide, 0.5, 6.55, 12.3, 0.7, accent)
add_text_box(slide, "⏱  15 минут на анализ → затем разбор в группах",
             0.5, 6.65, 12.3, 0.55, font_size=16, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 22 — Подсказки
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("blue")
make_header_bar(slide, "Подсказки (если застряли)", accent, bg)

hints = [
    ("🖥  GPU", "GPU используется постоянно?\nКакой реальный utilization? Когда запускается training?"),
    ("⚡ Realtime?", "Действительно нужен ответ за миллисекунды?\nКакова допустимая задержка с точки зрения бизнеса?"),
    ("📦 Batching", "Можно ли объединить запросы?\nЕсть ли периодические паттерны нагрузки?"),
    ("❄  Cold storage", "Когда последний раз читались данные 2-летней давности?\nНужен ли мгновенный доступ к архивным данным?"),
]

x_pos = 0.5
y_pos = 1.75
for i, (icon_title, desc) in enumerate(hints):
    if i == 2:
        x_pos = 0.5
        y_pos = 4.4
    add_rect(slide, x_pos, y_pos, 6.0, 2.2, COLORS["white"])
    add_rect(slide, x_pos, y_pos, 6.0, 0.65, accent)
    add_text_box(slide, icon_title, x_pos + 0.15, y_pos + 0.1, 5.7, 0.5,
                 font_size=17, bold=True, color=COLORS["white"])
    add_text_box(slide, desc, x_pos + 0.15, y_pos + 0.75, 5.7, 1.35,
                 font_size=14, color=COLORS["black"])
    x_pos += 6.65

add_text_box(slide, "Цель: найти решения, дающие в сумме ≥20% экономии",
             0.5, 6.65, 12.3, 0.6, font_size=15, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 23 — Разбор решений
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("green")
make_header_bar(slide, "Разбор решений", accent, bg)

solutions = [
    ("GPU → Spot + Scheduling",
     "Spot instances + запуск только по расписанию",
     "$12,000", "$4,800", "до 60%"),
    ("Training реже",
     "Еженедельный training вместо ежедневного",
     "Входит в GPU", "—", "20–40%"),
    ("S3 Lifecycle policy",
     "hot → IA (30д) → Glacier (90д) автоматически",
     "$3,500", "$700", "до 80%"),
    ("Kubernetes Autoscaling",
     "HPA + Cluster Autoscaler",
     "$4,000", "$2,800", "30%"),
    ("Logging reduction",
     "Sampling + retention 30 дней + log levels",
     "$1,500", "$750", "50%"),
]

headers = ["Оптимизация", "Решение", "До", "После", "Экономия"]
rows = [(opt, sol, before, after, saving) for opt, sol, before, after, saving in solutions]
add_table(slide, headers, rows,
          x=0.5, y=1.7, w=12.3, h=4.5,
          header_fill=accent,
          header_text_color=COLORS["white"],
          row_fills=[COLORS["white"], COLORS["green_light"]],
          font_size=12)

add_text_box(slide, "Итого: экономия $12,950 из $23,000 = -56% 🎯",
             0.5, 6.5, 12.3, 0.75, font_size=18, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 24 — Экономия детально
# ─────────────────────────────────────────────────────────────────
slide, accent, bg = make_slide("green")
make_header_bar(slide, "Результат оптимизации", accent, bg)

add_text_box(slide, "Было: $23,000/мес", 0.5, 1.7, 5.8, 0.9,
             font_size=28, bold=True, color=COLORS["red_mid"], align=PP_ALIGN.CENTER)
add_text_box(slide, "Стало: ~$10,000/мес", 7.0, 1.7, 5.8, 0.9,
             font_size=28, bold=True, color=accent, align=PP_ALIGN.CENTER)
add_text_box(slide, "→", 5.9, 1.85, 1.0, 0.65,
             font_size=32, bold=True, color=COLORS["black"], align=PP_ALIGN.CENTER)

# Savings visualization
savings_data = [
    ("GPU Spot+Sched", 7200, COLORS["red_mid"]),
    ("K8s Autoscaling", 1200, RGBColor(0xE6, 0x7E, 0x22)),
    ("S3 Lifecycle", 2800, COLORS["yellow_mid"]),
    ("Logging", 750, COLORS["green_mid"]),
]
total_saving = sum(s for _, s, _ in savings_data)

x_pos = 0.5
for title, saving, color in savings_data:
    bar_w = (saving / total_saving) * 11.3
    add_rect(slide, x_pos, 3.0, bar_w, 0.6, color)
    x_pos += bar_w + 0.1

x_pos = 0.5
y_pos = 3.7
for title, saving, color in savings_data:
    add_rect(slide, x_pos, y_pos, 0.3, 0.3, color)
    add_text_box(slide, f"{title}: ${saving:,}", x_pos + 0.4, y_pos - 0.05, 2.8, 0.4,
                 font_size=12, color=COLORS["black"])
    x_pos += 3.2

add_rect(slide, 2.0, 4.4, 9.3, 1.5, accent)
add_text_box(slide, f"Экономия: ~$13,000/мес = $156,000/год",
             2.0, 4.55, 9.3, 0.65, font_size=22, bold=True,
             color=COLORS["white"], align=PP_ALIGN.CENTER)
add_text_box(slide, "При этом функциональность системы не изменилась",
             2.0, 5.15, 9.3, 0.65, font_size=15,
             color=RGBColor(0xCC, 0xFF, 0xCC), align=PP_ALIGN.CENTER, italic=True)

add_text_box(slide,
             "Ключевое: все оптимизации — архитектурные решения, а не «урезание»",
             0.5, 6.55, 12.3, 0.65, font_size=14, bold=True,
             color=accent, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# SLIDE 25 — Главный вывод
# ─────────────────────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, 13.33, 7.5, COLORS["blue_dark"])
add_rect(slide, 0, 0, 0.3, 7.5, COLORS["accent_gold"])

add_text_box(slide, "Главный вывод", 0.6, 0.4, 12.0, 0.7,
             font_size=20, color=RGBColor(0x80, 0xA0, 0xC0), italic=True)

add_text_box(slide, "FinOps —\nэто архитектурная\nдисциплина", 0.6, 1.1, 12.0, 2.8,
             font_size=44, bold=True, color=COLORS["white"])

add_text_box(slide, "не бухгалтерия, не контроль расходов", 0.6, 3.8, 12.0, 0.7,
             font_size=20, color=RGBColor(0x80, 0xA0, 0xC0), italic=True)

points = [
    "Стоимость — управляемый параметр системы, как latency или reliability",
    "Каждое решение должно иметь cost-обоснование",
    "Архитектор = cost owner (это ответственность, не наказание)",
]
y_pos = 4.6
for point in points:
    add_rect(slide, 0.6, y_pos, 0.1, 0.45, COLORS["accent_gold"])
    add_text_box(slide, point, 0.85, y_pos - 0.03, 12.0, 0.5,
                 font_size=16, color=RGBColor(0xCC, 0xDD, 0xFF))
    y_pos += 0.6

# ─────────────────────────────────────────────────────────────────
# SLIDE 26 — Архитектурное правило
# ─────────────────────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, 13.33, 7.5, RGBColor(0x1B, 0x5E, 0x20))

add_text_box(slide, "Архитектурное правило", 0.5, 0.4, 12.3, 0.7,
             font_size=22, bold=False, color=RGBColor(0xA5, 0xD6, 0xA7),
             align=PP_ALIGN.CENTER)

add_text_box(slide,
             "Каждое архитектурное решение\nдолжно отвечать на 3 вопроса:",
             0.5, 1.1, 12.3, 1.2,
             font_size=26, bold=True, color=COLORS["white"],
             align=PP_ALIGN.CENTER)

questions = [
    ("💵", "Сколько это стоит?",
     "Конкретные цифры, не «наверное недорого»"),
    ("🤔", "Можно ли дешевле?",
     "Альтернативы всегда существуют — были ли они рассмотрены?"),
    ("📈", "Что будет при росте нагрузки?",
     "Стоимость должна расти линейно, а не экспоненциально"),
]

y_pos = 2.5
for icon, question, desc in questions:
    add_rect(slide, 1.0, y_pos, 11.3, 1.2, RGBColor(0x2E, 0x7D, 0x32))
    add_text_box(slide, icon, 1.2, y_pos + 0.2, 0.8, 0.8, font_size=28)
    add_text_box(slide, question, 2.2, y_pos + 0.1, 9.0, 0.5,
                 font_size=18, bold=True, color=RGBColor(0xA5, 0xD6, 0xA7))
    add_text_box(slide, desc, 2.2, y_pos + 0.6, 9.0, 0.45,
                 font_size=14, color=RGBColor(0xCC, 0xFF, 0xCC), italic=True)
    y_pos += 1.35

add_text_box(slide, "Если нет ответа на эти вопросы — архитектурное решение не принято",
             0.5, 6.6, 12.3, 0.65, font_size=14, bold=True,
             color=RGBColor(0xA5, 0xD6, 0xA7), align=PP_ALIGN.CENTER, italic=True)

# ─────────────────────────────────────────────────────────────────
# SLIDE 27 — Q&A / Thank you
# ─────────────────────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, 13.33, 7.5, COLORS["blue_dark"])
add_rect(slide, 0, 5.8, 13.33, 1.7, RGBColor(0x0F, 0x2A, 0x44))
add_rect(slide, 0, 0, 13.33, 0.15, COLORS["accent_gold"])

add_text_box(slide, "Вопросы?", 0.5, 1.2, 12.3, 1.5,
             font_size=64, bold=True, color=COLORS["white"],
             align=PP_ALIGN.CENTER)

summary_items = [
    "FinOps = часть архитектурного процесса",
    "Cost = f(Architecture, Load, Efficiency)",
    "Каждое решение требует cost-обоснования",
    "Экономия 20–60% достижима без деградации",
]

y_pos = 3.0
for item in summary_items:
    add_rect(slide, 2.5, y_pos, 0.12, 0.42, COLORS["accent_gold"])
    add_text_box(slide, item, 2.8, y_pos - 0.02, 9.8, 0.45,
                 font_size=17, color=RGBColor(0xCC, 0xDD, 0xFF))
    y_pos += 0.55

add_text_box(slide, "OTUS · AI Architect · FinOps: архитектура, управляемая стоимостью",
             0.5, 6.05, 12.3, 0.6, font_size=14, color=RGBColor(0x60, 0x80, 0xA0),
             align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────
output_path = "/Users/stureiko/Documents/Programming/Otus/AI-Architect/FinOps - стратегия управления стоимостью/FinOps_Presentation.pptx"
prs.save(output_path)
print(f"Saved: {output_path}")
print(f"Slides: {len(prs.slides)}")
