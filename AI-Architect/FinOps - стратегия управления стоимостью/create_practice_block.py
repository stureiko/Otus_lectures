from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

COLORS = {
    "navy":         RGBColor(0x0D, 0x2B, 0x45),
    "blue":         RGBColor(0x1E, 0x5B, 0x9B),
    "blue_light":   RGBColor(0xD6, 0xE8, 0xF7),
    "red":          RGBColor(0xC0, 0x39, 0x2B),
    "red_light":    RGBColor(0xFD, 0xED, 0xEB),
    "green":        RGBColor(0x1A, 0x7A, 0x45),
    "green_light":  RGBColor(0xD5, 0xF5, 0xE3),
    "amber":        RGBColor(0xD4, 0x7B, 0x0D),
    "amber_light":  RGBColor(0xFD, 0xF3, 0xD0),
    "purple":       RGBColor(0x6A, 0x3B, 0x9E),
    "purple_light": RGBColor(0xF0, 0xE6, 0xFF),
    "teal":         RGBColor(0x00, 0x7A, 0x7A),
    "teal_light":   RGBColor(0xD0, 0xF4, 0xF4),
    "slate":        RGBColor(0x3D, 0x5A, 0x80),
    "gold":         RGBColor(0xF3, 0x9C, 0x12),
    "white":        RGBColor(0xFF, 0xFF, 0xFF),
    "black":        RGBColor(0x1A, 0x1A, 0x1A),
    "gray":         RGBColor(0x55, 0x65, 0x70),
    "gray_light":   RGBColor(0xF4, 0xF6, 0xF8),
    "orange":       RGBColor(0xE6, 0x7E, 0x22),
}

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

# ────────────────────── helpers ──────────────────────

def rect(slide, x, y, w, h, fill, line=None, line_w=1):
    s = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    else:
        s.line.fill.background()
    return s


def tb(slide, text, x, y, w, h, size=14, bold=False, color=None,
       align=PP_ALIGN.LEFT, italic=False, wrap=True):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    box.word_wrap = wrap
    tf = box.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return box


def bullets(slide, items, x, y, w, h, size=14, color=None,
            header=None, header_size=16, header_color=None,
            bullet="•", indent=0.0, line_gap=0.55):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    box.word_wrap = True
    tf = box.text_frame
    tf.word_wrap = True
    first = True
    if header:
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = header
        run.font.size = Pt(header_size)
        run.font.bold = True
        run.font.color.rgb = header_color or color or COLORS["black"]
        first = False
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = f"{'  ' * int(indent)}{bullet}  {item}"
        run.font.size = Pt(size)
        if color:
            run.font.color.rgb = color
    return box


def code_block(slide, code_text, x, y, w, h, bg=None):
    bg = bg or RGBColor(0x1E, 0x1E, 0x1E)
    rect(slide, x, y, w, h, bg)
    box = slide.shapes.add_textbox(Inches(x + 0.12), Inches(y + 0.1),
                                    Inches(w - 0.24), Inches(h - 0.2))
    box.word_wrap = True
    tf = box.text_frame
    tf.word_wrap = True
    lines = code_text.strip().split("\n")
    first = True
    for line in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        run = p.add_run()
        run.text = line
        run.font.size = Pt(11)
        run.font.name = "Courier New"
        run.font.color.rgb = RGBColor(0xD4, 0xD4, 0xD4)
    return box


def table(slide, headers, rows, x, y, w, h,
          hdr_fill, hdr_color, alt_fill=None, base_fill=None, size=13):
    alt_fill = alt_fill or COLORS["gray_light"]
    base_fill = base_fill or COLORS["white"]
    cols = len(headers)
    t = slide.shapes.add_table(1 + len(rows), cols,
                                Inches(x), Inches(y),
                                Inches(w), Inches(h)).table
    cw = Inches(w / cols)
    for i in range(cols):
        t.columns[i].width = cw

    def _set(cell, text, fill, color, bold=False):
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.clear()
        r = p.add_run()
        r.text = text
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color

    for j, h in enumerate(headers):
        _set(t.cell(0, j), h, hdr_fill, hdr_color, bold=True)
    for i, row in enumerate(rows):
        fill = base_fill if i % 2 == 0 else alt_fill
        for j, v in enumerate(row):
            _set(t.cell(i + 1, j), str(v), fill, COLORS["black"])
    return t


def section_header(slide, title, accent, subtitle=None):
    rect(slide, 0, 0, 13.33, 1.45, accent)
    tb(slide, title, 0.35, 0.1, 12.6, 0.95,
       size=28, bold=True, color=COLORS["white"])
    if subtitle:
        rect(slide, 0, 1.45, 13.33, 6.05, COLORS["gray_light"])
        tb(slide, subtitle, 0.35, 1.05, 12.6, 0.38,
           size=13, italic=True, color=RGBColor(0xCC, 0xDD, 0xFF))
    else:
        rect(slide, 0, 1.45, 13.33, 6.05, COLORS["gray_light"])


def badge(slide, text, x, y, w, h, fill, text_color=None):
    rect(slide, x, y, w, h, fill)
    tb(slide, text, x, y + 0.05, w, h - 0.05,
       size=12, bold=True,
       color=text_color or COLORS["white"],
       align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
# SLIDE 1 — Title (Practice block)
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["navy"])
rect(s, 0, 0, 0.35, 7.5, COLORS["gold"])
rect(s, 0, 5.5, 13.33, 2.0, RGBColor(0x07, 0x1A, 0x2E))

tb(s, "ПРАКТИЧЕСКИЙ БЛОК", 0.6, 0.5, 12.5, 0.7,
   size=16, bold=True, color=RGBColor(0x80, 0xB0, 0xD8), italic=True)
tb(s, "Анализ Cloud Bill\nAI-системы", 0.6, 1.2, 12.5, 2.2,
   size=48, bold=True, color=COLORS["white"])
tb(s, "Полный разбор: диагностика → причины → решения → расчёт экономии",
   0.6, 3.4, 12.5, 0.7, size=20, color=RGBColor(0x90, 0xC8, 0xFF), italic=True)

items_overview = [
    "Входные данные и контекст системы",
    "5 архитектурных проблем — детальный разбор",
    "Конкретные решения с примерами конфигурации",
    "Расчёт экономии по каждому пункту",
    "Итоговый результат и план внедрения",
]
y = 4.1
for item in items_overview:
    rect(s, 0.6, y, 0.08, 0.38, COLORS["gold"])
    tb(s, item, 0.85, y - 0.03, 11.5, 0.45, size=15,
       color=RGBColor(0xC0, 0xD8, 0xF0))
    y += 0.48

tb(s, "⏱  ~45 минут · Работа в группах · Разбор преподавателем",
   0.6, 6.6, 12.5, 0.65, size=14, color=RGBColor(0x60, 0x80, 0xA0),
   align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# SLIDE 2 — Контекст: система и бизнес-требования
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Контекст: что за система?", COLORS["slate"])

tb(s, "E-commerce рекомендательная система на ML", 0.5, 1.6, 12.3, 0.6,
   size=20, bold=True, color=COLORS["slate"])

# Left: system description
rect(s, 0.5, 2.3, 6.0, 4.5, COLORS["white"])
rect(s, 0.5, 2.3, 6.0, 0.5, COLORS["slate"])
tb(s, "Что делает система", 0.65, 2.35, 5.7, 0.4,
   size=14, bold=True, color=COLORS["white"])
desc_items = [
    "Рекомендует товары пользователям (ML-модель)",
    "Обучение на данных о покупках и кликах",
    "Обслуживает 50,000 запросов/день",
    "Пиковая нагрузка: 09:00–11:00 (×3 от среднего)",
    "Данные за 3 года: 5 TB исторических логов",
    "Команда: 3 ML-инженера, 1 DevOps",
]
bullets(s, desc_items, 0.65, 2.9, 5.7, 3.8, size=14, color=COLORS["black"])

# Right: SLA / constraints
rect(s, 6.8, 2.3, 6.0, 4.5, COLORS["white"])
rect(s, 6.8, 2.3, 6.0, 0.5, COLORS["teal"])
tb(s, "Бизнес-требования и SLA", 6.95, 2.35, 5.7, 0.4,
   size=14, bold=True, color=COLORS["white"])
sla_items = [
    "Latency inference: < 500ms (p99)",
    "Availability: 99.5% (не 99.99%)",
    "Модель: обновляется не реже раза в неделю",
    "Данные старше 6 мес — только для аудита",
    "Бюджет: хотят снизить, не критично мгновенно",
    "Downtime inference: до 30 мин/неделю OK",
]
bullets(s, sla_items, 6.95, 2.9, 5.7, 3.8, size=14, color=COLORS["black"])

rect(s, 0.5, 6.95, 12.3, 0.38, COLORS["amber_light"])
tb(s, "Ключевой вывод: SLA допускает batch inference и еженедельный training — это открывает большие возможности",
   0.65, 6.98, 12.0, 0.32, size=13, bold=True, color=COLORS["amber"],
   align=PP_ALIGN.LEFT)

# ══════════════════════════════════════════════════════════════════
# SLIDE 3 — Cloud Bill (детальный)
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Cloud Bill: что платим и за что", COLORS["red"])

headers = ["Сервис", "Тип ресурса", "Кол-во", "Цена/ед", "Итого/мес", "Доля"]
rows = [
    ["EC2 GPU", "p3.2xlarge (1× V100)", "4 инстанса", "$2.48/час × 24 × 30", "$7,142", "31%"],
    ["EC2 GPU (dev)", "p3.2xlarge", "1 инстанс", "$2.48/час × 24 × 30", "$1,786", "8%"],
    ["EC2 Spot (нет)", "—", "—", "—", "$0", "—"],
    ["S3 Standard", "5 TB × 3 года данных", "15 TB", "$0.023/GB", "$354", "1.5%"],
    ["S3 Standard (копии)", "Backup + dev копии", "5 TB", "$0.023/GB", "$118", "0.5%"],
    ["S3 итого выставлено", "включая PUT/GET запросы", "—", "—", "$3,500", "15%"],
    ["K8s nodes (EKS)", "m5.2xlarge × 8 нод", "8 нод", "$0.384/час × 24 × 30", "$2,212", "9.6%"],
    ["K8s nodes (fixed)", "r5.xlarge × 4 нод", "4 нод", "$0.252/час × 24 × 30", "$726", "3.1%"],
    ["K8s overhead (EKS)", "Control plane + LB", "—", "—", "$1,062", "4.6%"],
    ["Data Transfer", "Cross-region replication", "~25 TB/мес", "$0.08/GB", "$2,000", "8.7%"],
    ["CloudWatch Logs", "90 дней retention, все сервисы", "~500 GB/мес", "$0.03/GB", "$1,500", "6.5%"],
    ["Прочее (Route53, NAT)", "—", "—", "—", "$900", "3.9%"],
]
# Use a condensed table for this amount of data
t = table(s, headers, rows, 0.3, 1.55, 12.73, 5.15,
          COLORS["red"], COLORS["white"],
          alt_fill=RGBColor(0xFD, 0xF0, 0xF0),
          size=11)

rect(s, 0.3, 6.75, 12.73, 0.55, COLORS["red"])
tb(s, "ИТОГО: $23,046/мес  ·  $276,552/год  ·  GPU = 39% расходов",
   0.5, 6.82, 12.3, 0.4, size=15, bold=True, color=COLORS["white"],
   align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# SLIDE 4 — Архитектура "как есть"
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Архитектура «как есть» (AS-IS)", COLORS["slate"])

# Pipeline flow
stages = [
    ("S3\n(все данные\nhot tier)", COLORS["blue"]),
    ("Feature\nPipeline\n(ежедневно)", COLORS["orange"]),
    ("Training\n(GPU 24/7\nежедневно)", COLORS["red"]),
    ("Model\nRegistry\n(MLflow)", COLORS["teal"]),
    ("Realtime\nInference\n(K8s fixed)", COLORS["purple"]),
]
x = 0.4
for i, (label, color) in enumerate(stages):
    rect(s, x, 1.65, 2.15, 1.5, color)
    tb(s, label, x, 1.75, 2.15, 1.3,
       size=12, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER)
    if i < 4:
        tb(s, "→", x + 2.15, 2.2, 0.3, 0.6,
           size=22, bold=True, color=COLORS["slate"], align=PP_ALIGN.CENTER)
    x += 2.45

# Problem annotations
problems = [
    (0.4, 3.3, 2.15, "❌ Нет lifecycle\n5 TB в hot tier\nДанные за 3 года", COLORS["red_light"]),
    (2.85, 3.3, 2.15, "❌ CPU-only\nФиксированный\nрасклад ежедневно", COLORS["red_light"]),
    (5.3, 3.3, 2.15, "❌ GPU простаивает\n80% времени\nЕжедневный запуск", COLORS["red_light"]),
    (7.75, 3.3, 2.15, "❌ Нет versioning\nВсе в один S3\nкопируется 3×", COLORS["red_light"]),
    (10.2, 3.3, 2.15, "❌ Fixed 8 нод\nПик 2ч/день\nНет autoscaling", COLORS["red_light"]),
]
for x, y, w, text, fill in problems:
    rect(s, x, y, w, 1.8, fill, line=COLORS["red"], line_w=1)
    tb(s, text, x + 0.1, y + 0.08, w - 0.2, 1.6, size=11, color=COLORS["red"])

# Monitoring and logging row
rect(s, 0.4, 5.3, 12.5, 0.7, RGBColor(0xFF, 0xEB, 0xEB))
tb(s, "📊 Monitoring / Logging (CloudWatch): всё логируется, retention 90 дней, нет фильтрации → $1,500/мес",
   0.6, 5.42, 12.1, 0.45, size=13, color=COLORS["red"], bold=True)

# Key metrics
rect(s, 0.4, 6.1, 12.5, 1.15, COLORS["white"])
metrics = [
    ("GPU utilization", "~15%", COLORS["red"]),
    ("K8s node utilization", "~25%", COLORS["red"]),
    ("S3 read (данные >6 мес)", "~0.1%", COLORS["red"]),
    ("Training необходимость", "1×/неделю", COLORS["amber"]),
    ("Реальный realtime %", "~5%", COLORS["amber"]),
]
x = 0.6
for label, val, col in metrics:
    tb(s, label, x, 6.15, 2.2, 0.4, size=11, color=COLORS["gray"])
    tb(s, val, x, 6.55, 2.2, 0.45, size=18, bold=True, color=col)
    x += 2.5

# ══════════════════════════════════════════════════════════════════
# SLIDE 5 — Задание для групп
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Задание: найдите точки оптимизации", COLORS["blue"])

tb(s, "У вас есть 15 минут. Работайте в группах по 3–4 человека.", 0.5, 1.6, 12.3, 0.5,
   size=16, italic=True, color=COLORS["blue"])

tasks_detail = [
    ("1", "Диагностика", COLORS["blue"],
     ["Выпишите 3–5 крупнейших источников затрат",
      "Посчитайте долю каждого в общем bill",
      "Определите — это архитектурная или операционная проблема?"]),
    ("2", "Анализ причин", COLORS["amber"],
     ["Для каждой проблемы: почему так получилось?",
      "Какое архитектурное решение привело к этому?",
      "Было ли это сознательное решение или «по умолчанию»?"]),
    ("3", "Решения", COLORS["green"],
     ["Предложите конкретное архитектурное изменение",
      "Оцените сложность внедрения (легко/средне/сложно)",
      "Оцените потенциальную экономию в $ и %"]),
]

y = 2.2
for num, title, color, items in tasks_detail:
    rect(s, 0.5, y, 0.65, 1.45, color)
    tb(s, num, 0.5, y + 0.3, 0.65, 0.8,
       size=32, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER)
    rect(s, 1.2, y, 11.6, 1.45, COLORS["white"])
    tb(s, title, 1.4, y + 0.06, 11.2, 0.45, size=16, bold=True, color=color)
    x_item = 1.45
    for i, item in enumerate(items):
        tb(s, f"→  {item}", 1.45, y + 0.52 + i * 0.32, 11.1, 0.3,
           size=13, color=COLORS["black"])
    y += 1.6

rect(s, 0.5, 7.05, 12.3, 0.3, COLORS["blue"])
tb(s, "Цель: найти суммарную экономию ≥20% от $23,000 = минимум $4,600/мес",
   0.6, 7.07, 12.1, 0.25, size=13, bold=True, color=COLORS["white"])

# ══════════════════════════════════════════════════════════════════
# SLIDE 6 — Подсказки
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Подсказки (открыть, если группа застряла)", COLORS["teal"])

hints = [
    ("🖥  GPU utilization = 15%", COLORS["red"],
     [
         "Сколько часов в сутки реально идёт training?",
         "Что происходит в остальное время?",
         "Можно ли запускать только по расписанию?",
         "Spot instances — что это и когда применимо?",
     ]),
    ("📅  Training ежедневно", COLORS["amber"],
     [
         "Данные о покупках — как часто реально меняются паттерны?",
         "Есть ли смысл переобучать ежедневно?",
         "Что произойдёт, если обучать раз в неделю?",
         "Как бизнес заметит разницу?",
     ]),
    ("💾  S3 без lifecycle", COLORS["blue"],
     [
         "Когда последний раз читали данные 2-летней давности?",
         "Нужен ли мгновенный доступ к архиву?",
         "Какие S3 storage классы существуют?",
         "Что такое lifecycle policy?",
     ]),
    ("⚡  K8s без autoscaling", COLORS["purple"],
     [
         "График нагрузки: пик 09–11, потом падение в 3–4 раза",
         "Сколько нод реально нужно в ночное время?",
         "Что такое HPA и Cluster Autoscaler?",
         "Каков trade-off: экономия vs холодный старт?",
     ]),
    ("📋  Логирование $1,500", COLORS["teal"],
     [
         "Что именно логируется? Все уровни?",
         "Нужны ли DEBUG-логи в production?",
         "Через 90 дней логи реально читают?",
         "Sampling: нужно ли логировать каждый запрос?",
     ]),
]

x_pos = 0.35
y_pos = 1.6
for i, (title, color, items) in enumerate(hints):
    if i == 3:
        x_pos = 0.35
        y_pos = 4.45
    rect(s, x_pos, y_pos, 4.1, 2.6, COLORS["white"])
    rect(s, x_pos, y_pos, 4.1, 0.52, color)
    tb(s, title, x_pos + 0.1, y_pos + 0.08, 3.9, 0.38,
       size=13, bold=True, color=COLORS["white"])
    for j, item in enumerate(items):
        tb(s, f"→  {item}", x_pos + 0.15, y_pos + 0.65 + j * 0.45, 3.8, 0.42,
           size=12, color=COLORS["black"])
    x_pos += 4.35
    if i == 1:
        x_pos = 0.35 + 4.35 * 2  # start third col at same row

rect(s, 9.15, 4.45, 4.1, 2.6, COLORS["white"])
rect(s, 9.15, 4.45, 4.1, 0.52, COLORS["teal"])
tb(s, "📋  Логирование $1,500", 9.25, 4.53, 3.9, 0.38,
   size=13, bold=True, color=COLORS["white"])
for j, item in enumerate(hints[4][2]):
    tb(s, f"→  {item}", 9.3, 5.1 + j * 0.45, 3.8, 0.42,
       size=12, color=COLORS["black"])

tb(s, "Общее правило: если ресурс используется менее 30% — это сигнал к оптимизации",
   0.35, 7.15, 12.6, 0.28, size=13, bold=True, color=COLORS["teal"],
   align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# SLIDE 7 — Separator: Разбор решений
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["navy"])
rect(s, 0, 0, 13.33, 0.2, COLORS["gold"])
rect(s, 0, 7.3, 13.33, 0.2, COLORS["gold"])

tb(s, "РАЗБОР РЕШЕНИЙ", 0.5, 2.0, 12.3, 0.8,
   size=18, bold=True, color=RGBColor(0x80, 0xB0, 0xD8),
   align=PP_ALIGN.CENTER, italic=True)
tb(s, "5 архитектурных\nоптимизаций", 0.5, 2.7, 12.3, 2.0,
   size=52, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER)
tb(s, "с конкретными решениями, конфигурацией и расчётом экономии",
   0.5, 4.65, 12.3, 0.6, size=19, italic=True,
   color=RGBColor(0x90, 0xC8, 0xFF), align=PP_ALIGN.CENTER)

opt_labels = [
    ("1", "GPU Spot + Scheduling", COLORS["red"]),
    ("2", "Training Frequency", COLORS["amber"]),
    ("3", "S3 Lifecycle", COLORS["blue"]),
    ("4", "K8s Autoscaling", COLORS["purple"]),
    ("5", "Log Optimization", COLORS["teal"]),
]
x = 0.75
for num, label, color in opt_labels:
    rect(s, x, 5.5, 2.2, 0.8, color)
    tb(s, f"{num}. {label}", x + 0.1, 5.58, 2.0, 0.62,
       size=11, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER)
    x += 2.45

# ══════════════════════════════════════════════════════════════════
# SLIDE 8 — Оптимизация 1: GPU → Spot + Scheduling
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["gray_light"])
rect(s, 0, 0, 13.33, 1.5, COLORS["red"])
rect(s, 0, 0, 0.25, 7.5, COLORS["red"])
badge(s, "01", 0.35, 0.45, 0.85, 0.7, COLORS["white"],
      text_color=COLORS["red"])
tb(s, "GPU: Spot Instances + Job Scheduling", 1.3, 0.1, 11.7, 0.75,
   size=26, bold=True, color=COLORS["white"])
tb(s, "Экономия: $7,200–$8,500/мес · Сложность: средняя · Срок внедрения: 2–3 недели",
   1.3, 0.85, 11.7, 0.5, size=13, italic=True, color=RGBColor(0xFF, 0xCC, 0xCC))

# Problem analysis
rect(s, 0.5, 1.65, 5.8, 2.5, COLORS["white"])
tb(s, "🔍 Диагностика проблемы", 0.65, 1.72, 5.5, 0.45,
   size=14, bold=True, color=COLORS["red"])
diag = [
    "4× p3.2xlarge работают 24/7 = 2,976 часов/мес",
    "Training занимает ~3–4 часа в сутки = 12.5% времени",
    "Остальные 87.5% — GPU просто ждут",
    "Dev-инстанс работает даже в выходные",
    "Нет механизма авто-выключения после training",
]
bullets(s, diag, 0.65, 2.2, 5.6, 1.9, size=12, color=COLORS["black"])

# Solution
rect(s, 6.5, 1.65, 6.5, 2.5, COLORS["white"])
tb(s, "✅ Решение", 6.65, 1.72, 6.2, 0.45,
   size=14, bold=True, color=COLORS["green"])
sol = [
    "Spot instances вместо On-Demand (экономия 60–70%)",
    "Training запускается по cron → авто-завершение",
    "Dev-инстанс: lifecycle schedule (только рабочие часы)",
    "Fallback: On-Demand при недоступности Spot",
    "Saving Plans для baseline serving нагрузки",
]
bullets(s, sol, 6.65, 2.2, 6.2, 1.9, size=12, color=COLORS["black"])

# Config example
code_block(s, """# AWS Batch Job Definition (training)
{
  "jobDefinition": "ml-training",
  "instanceTypes": ["p3.2xlarge"],
  "allocationStrategy": "SPOT_CAPACITY_OPTIMIZED",
  "bidPercentage": 60,
  "retryStrategy": { "attempts": 3 }
}

# Cron schedule (CloudWatch Events)
cron(0 2 ? * SUN *)   # Воскресенье 02:00 UTC (еженедельно)

# Auto-shutdown после завершения training job
aws ec2 terminate-instances --instance-ids $TRAINING_INSTANCE_ID""",
            0.5, 4.3, 8.0, 2.85, bg=RGBColor(0x1A, 0x1A, 0x2E))

# Cost calculation
rect(s, 8.65, 4.3, 4.3, 2.85, COLORS["white"])
tb(s, "💰 Расчёт экономии", 8.8, 4.38, 4.0, 0.4,
   size=14, bold=True, color=COLORS["green"])
calc_items = [
    "On-Demand: $2.48/час × 5 инст = $12.4/час",
    "Spot (~40%): ~$1.0/час × 5 инст = $5/час",
    "Training: 4ч/нед × 4 = 16ч × $5 = $80",
    "Serving spot: $5/час × 24 × 30 = $3,600",
    "Dev schedule: 8ч × 5д × $2.48 = $496",
    "───────────────────────────────────",
    "БЫЛО:  $8,928/мес",
    "СТАЛО: $4,176/мес",
    "Экономия: $4,752/мес (53%)",
]
y = 4.8
for item in calc_items:
    bold = item.startswith("Экономия") or item.startswith("БЫЛО") or item.startswith("СТАЛО")
    color = COLORS["green"] if item.startswith("Экономия") else (
        COLORS["red"] if item.startswith("БЫЛО") else COLORS["black"])
    tb(s, item, 8.8, y, 4.05, 0.28, size=11, bold=bold, color=color)
    y += 0.29

# ══════════════════════════════════════════════════════════════════
# SLIDE 9 — Оптимизация 2: Training Frequency
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["gray_light"])
rect(s, 0, 0, 13.33, 1.5, COLORS["amber"])
rect(s, 0, 0, 0.25, 7.5, COLORS["amber"])
badge(s, "02", 0.35, 0.45, 0.85, 0.7, COLORS["white"],
      text_color=COLORS["amber"])
tb(s, "Training: оптимизация частоты и pipeline", 1.3, 0.1, 11.7, 0.75,
   size=26, bold=True, color=COLORS["white"])
tb(s, "Экономия: $800–1,500/мес (входит в GPU-бюджет) · Сложность: низкая · Срок: 1 неделя",
   1.3, 0.85, 11.7, 0.5, size=13, italic=True, color=RGBColor(0xFF, 0xF0, 0xCC))

# Analysis columns
rect(s, 0.5, 1.65, 3.8, 5.0, COLORS["white"])
tb(s, "🔍 Анализ", 0.65, 1.72, 3.5, 0.42, size=14, bold=True, color=COLORS["amber"])
analysis = [
    "Training ежедневно в 00:00",
    "Данные: покупки + клики",
    "Паттерны поведения меняются медленно",
    "Нет A/B теста между моделями",
    "Метрики качества не отслеживаются",
    "Ежедневный training = 7× GPU-часов",
    "vs еженедельный = 1× GPU-часов",
]
bullets(s, analysis, 0.65, 2.2, 3.6, 4.3, size=12, color=COLORS["black"])

rect(s, 4.5, 1.65, 4.0, 5.0, COLORS["white"])
tb(s, "✅ Решение", 4.65, 1.72, 3.7, 0.42, size=14, bold=True, color=COLORS["green"])
solution = [
    "Еженедельный training (воскр. ночью)",
    "Мониторинг data drift (Evidently AI)",
    "Trigger на переобучение при drift",
    "A/B testing: старая vs новая модель",
    "Champion-Challenger deployment",
    "Online learning для быстрых сигналов",
]
bullets(s, solution, 4.65, 2.2, 3.7, 4.3, size=12, color=COLORS["black"])

rect(s, 8.7, 1.65, 4.3, 5.0, COLORS["white"])
tb(s, "📐 Архитектура", 8.85, 1.72, 4.0, 0.42, size=14, bold=True, color=COLORS["blue"])

code_block(s, """# MLflow + Airflow DAG
@dag(schedule="0 2 * * 0")  # Каждое воскресенье
def weekly_training_pipeline():

    check_drift = DataDriftSensor(
        threshold=0.15,  # Если drift > 15%
        trigger_immediate=True  # → внеплановый run
    )

    train = TrainingOperator(
        instance_type="p3.2xlarge",
        use_spot=True,
        max_runtime=14400  # 4 часа max
    )

    evaluate = ModelEvaluationOperator(
        min_auc=0.82,
        compare_to_champion=True
    )

    deploy_if_better >> champion_challenger""",
            8.85, 2.2, 4.1, 4.35, bg=RGBColor(0x1A, 0x1A, 0x2E))

rect(s, 0.5, 6.8, 12.3, 0.55, COLORS["amber_light"])
tb(s, "Результат: экономия вычислений в 6–7× + лучший контроль качества модели",
   0.65, 6.88, 12.0, 0.38, size=14, bold=True, color=COLORS["amber"])

# ══════════════════════════════════════════════════════════════════
# SLIDE 10 — Оптимизация 3: S3 Lifecycle
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["gray_light"])
rect(s, 0, 0, 13.33, 1.5, COLORS["blue"])
rect(s, 0, 0, 0.25, 7.5, COLORS["blue"])
badge(s, "03", 0.35, 0.45, 0.85, 0.7, COLORS["white"],
      text_color=COLORS["blue"])
tb(s, "S3: Lifecycle Policy — горячее/холодное хранение", 1.3, 0.1, 11.7, 0.75,
   size=26, bold=True, color=COLORS["white"])
tb(s, "Экономия: $2,450–$2,800/мес · Сложность: низкая · Срок: 2–3 дня",
   1.3, 0.85, 11.7, 0.5, size=13, italic=True, color=RGBColor(0xCC, 0xDD, 0xFF))

# Storage tiers diagram
tiers = [
    ("S3 Standard\n(HOT)", "Активные данные\n≤ 30 дней", "$0.023/GB", "$354/мес", COLORS["red"]),
    ("S3 Infrequent\nAccess", "Данные 30–90 дней\nРедкий доступ", "$0.0125/GB", "$94/мес", COLORS["amber"]),
    ("S3 Glacier\nInstant", "Данные 90–365 дней\nДоступ за сек", "$0.004/GB", "$30/мес", COLORS["blue"]),
    ("S3 Glacier\nDeep Archive", "Данные > 1 года\nТолько аудит", "$0.00099/GB", "$7/мес", COLORS["teal"]),
]
x = 0.5
for tier_name, desc, price, cost, color in tiers:
    rect(s, x, 1.65, 2.95, 3.4, color)
    tb(s, tier_name, x + 0.1, 1.75, 2.75, 0.75,
       size=16, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER)
    tb(s, desc, x + 0.1, 2.55, 2.75, 0.75,
       size=12, color=COLORS["white"], align=PP_ALIGN.CENTER)
    rect(s, x, 3.4, 2.95, 0.5, RGBColor(0xFF, 0xFF, 0xFF))
    tb(s, price, x + 0.1, 3.45, 2.75, 0.4,
       size=14, bold=True, color=color, align=PP_ALIGN.CENTER)
    tb(s, cost, x + 0.1, 3.9, 2.75, 0.7,
       size=13, bold=True, color=color, align=PP_ALIGN.CENTER)
    if x < 11:
        tb(s, "→", x + 2.95, 2.9, 0.3, 0.5,
           size=22, bold=True, color=COLORS["slate"], align=PP_ALIGN.CENTER)
    x += 3.25

# Lifecycle config
code_block(s, """# S3 Lifecycle Configuration (JSON)
{
  "Rules": [{
    "ID": "ml-data-tiering",
    "Filter": { "Prefix": "datasets/" },
    "Status": "Enabled",
    "Transitions": [
      { "Days": 30,  "StorageClass": "STANDARD_IA" },
      { "Days": 90,  "StorageClass": "GLACIER_IR" },
      { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
    ],
    "NoncurrentVersionExpiration": { "NoncurrentDays": 30 },
    "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 }
  }]
}""",
            0.5, 5.2, 7.5, 2.05, bg=RGBColor(0x0A, 0x1A, 0x2E))

# Savings calculation
rect(s, 8.15, 5.2, 4.85, 2.05, COLORS["white"])
tb(s, "💰 Расчёт", 8.3, 5.28, 4.6, 0.38, size=13, bold=True, color=COLORS["green"])
s3_calc = [
    "Текущее: 15 TB все в Standard",
    "  → $0.023 × 15,360 GB = $353/мес",
    "После lifecycle:",
    "  Hot (30д):    0.5 TB × $0.023 = $12",
    "  IA (30–90д):  1.0 TB × $0.013 = $13",
    "  Glacier:      3.5 TB × $0.004 = $14",
    "  Deep Archive: 10 TB × $0.001 = $10",
    "S3 requests + реплика: ~$15",
    "──────────────────────────────",
    "БЫЛО:  $3,500/мес (вкл копии)",
    "СТАЛО: ~$750/мес",
    "Экономия: $2,750/мес (79%)",
]
y = 5.65
for line in s3_calc:
    bold = line.startswith("Экономия") or line.startswith("БЫЛО") or line.startswith("СТАЛО")
    color = COLORS["green"] if line.startswith("Экономия") else (
        COLORS["red"] if line.startswith("БЫЛО") else COLORS["black"])
    tb(s, line, 8.3, y, 4.55, 0.27, size=11, bold=bold, color=color)
    y += 0.28

# ══════════════════════════════════════════════════════════════════
# SLIDE 11 — Оптимизация 4: Kubernetes Autoscaling
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["gray_light"])
rect(s, 0, 0, 13.33, 1.5, COLORS["purple"])
rect(s, 0, 0, 0.25, 7.5, COLORS["purple"])
badge(s, "04", 0.35, 0.45, 0.85, 0.7, COLORS["white"],
      text_color=COLORS["purple"])
tb(s, "Kubernetes: Horizontal + Cluster Autoscaling", 1.3, 0.1, 11.7, 0.75,
   size=26, bold=True, color=COLORS["white"])
tb(s, "Экономия: $1,500–$2,000/мес · Сложность: средняя · Срок: 1–2 недели",
   1.3, 0.85, 11.7, 0.5, size=13, italic=True, color=RGBColor(0xE8, 0xD8, 0xFF))

# Load profile analysis
rect(s, 0.5, 1.65, 5.5, 3.1, COLORS["white"])
tb(s, "📊 Профиль нагрузки", 0.65, 1.72, 5.2, 0.42,
   size=14, bold=True, color=COLORS["purple"])

# ASCII-style load chart
load_data = [
    ("00:00–06:00", "▂", "~5k req/h",   "1–2 ноды"),
    ("06:00–09:00", "▄", "~15k req/h",  "3–4 ноды"),
    ("09:00–11:00", "█", "~50k req/h",  "8 нод (пик)"),
    ("11:00–18:00", "▅", "~20k req/h",  "4–5 нод"),
    ("18:00–21:00", "▆", "~30k req/h",  "5–6 нод"),
    ("21:00–24:00", "▃", "~8k req/h",   "2–3 ноды"),
]
y = 2.25
for time, bar, req, nodes in load_data:
    tb(s, f"{time}  {bar * 4}  {req:<12}→ {nodes}", 0.65, y, 5.2, 0.38,
       size=12, color=COLORS["black"])
    y += 0.38

tb(s, "Сейчас: 8 нод постоянно = переплата ~70% времени",
   0.65, 4.6, 5.2, 0.38, size=12, bold=True, color=COLORS["red"])

# K8s config
code_block(s, """# HorizontalPodAutoscaler
apiVersion: autoscaling/v2
kind: HPA
metadata: { name: inference-hpa }
spec:
  scaleTargetRef:
    kind: Deployment
    name: ml-inference
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        averageUtilization: 60
  - type: Pods
    pods:
      metric: { name: requests_per_second }
      target: { averageValue: "100" }
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300""",
            6.15, 1.65, 5.0, 5.0, bg=RGBColor(0x1A, 0x0A, 0x2E))

# Cluster autoscaler + savings
rect(s, 11.3, 1.65, 1.7, 5.0, COLORS["white"])
tb(s, "💰", 11.3, 1.75, 1.7, 0.5, size=24, align=PP_ALIGN.CENTER)
tb(s, "БЫЛО\n$4,000", 11.3, 2.3, 1.7, 0.9, size=16, bold=True,
   color=COLORS["red"], align=PP_ALIGN.CENTER)
tb(s, "↓", 11.3, 3.25, 1.7, 0.45, size=22, bold=True,
   color=COLORS["black"], align=PP_ALIGN.CENTER)
tb(s, "СТАЛО\n~$2,200", 11.3, 3.75, 1.7, 0.9, size=16, bold=True,
   color=COLORS["green"], align=PP_ALIGN.CENTER)
tb(s, "-45%\n$1,800", 11.3, 4.75, 1.7, 0.8, size=15, bold=True,
   color=COLORS["purple"], align=PP_ALIGN.CENTER)

rect(s, 0.5, 6.85, 12.3, 0.5, COLORS["purple_light"])
tb(s, "Дополнительно: Spot node groups для non-critical workloads даёт ещё +30–40% экономии на нодах",
   0.65, 6.9, 12.0, 0.38, size=13, color=COLORS["purple"])

# ══════════════════════════════════════════════════════════════════
# SLIDE 12 — Оптимизация 5: Logging
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["gray_light"])
rect(s, 0, 0, 13.33, 1.5, COLORS["teal"])
rect(s, 0, 0, 0.25, 7.5, COLORS["teal"])
badge(s, "05", 0.35, 0.45, 0.85, 0.7, COLORS["white"],
      text_color=COLORS["teal"])
tb(s, "Логирование: сокращение объёма и стоимости", 1.3, 0.1, 11.7, 0.75,
   size=26, bold=True, color=COLORS["white"])
tb(s, "Экономия: $900–$1,200/мес · Сложность: низкая · Срок: 3–5 дней",
   1.3, 0.85, 11.7, 0.5, size=13, italic=True, color=RGBColor(0xCC, 0xFF, 0xFF))

# What's being logged
rect(s, 0.5, 1.65, 5.5, 2.5, COLORS["white"])
tb(s, "❌ Что логируется сейчас", 0.65, 1.72, 5.2, 0.42,
   size=14, bold=True, color=COLORS["red"])
current_log = [
    "DEBUG логи всех сервисов (90% объёма!)",
    "Каждый ML inference запрос (~50k/день)",
    "K8s events (все уровни)",
    "S3 access logs (каждый GET/PUT)",
    "Retention: 90 дней для всего",
    "Нет sampling для однотипных событий",
]
bullets(s, current_log, 0.65, 2.2, 5.2, 1.85, size=12, color=COLORS["red"])

# After
rect(s, 6.3, 1.65, 5.5, 2.5, COLORS["white"])
tb(s, "✅ Как должно быть", 6.45, 1.72, 5.2, 0.42,
   size=14, bold=True, color=COLORS["green"])
after_log = [
    "Production: только INFO + ERROR + WARN",
    "Inference: 1% sampling + все ошибки",
    "K8s: WARNING и выше только",
    "S3: только error events",
    "Retention: 30 дней стандарт, 90 — errors",
    "Structured logging → меньше данных",
]
bullets(s, after_log, 6.45, 2.2, 5.2, 1.85, size=12, color=COLORS["green"])

# Config
code_block(s, """# CloudWatch Log Group settings
aws logs put-retention-policy \\
  --log-group-name /ml/inference \\
  --retention-in-days 30

# Fluentd sampling config (1% inference logs)
<filter ml.inference>
  @type sampling
  sample_unit minute
  sample_threshold 1  # 1 из 100
  sample_rate 0.01
</filter>

# Python logging level
import logging
logging.getLogger("ml_service").setLevel(logging.WARNING)
logging.getLogger("inference").setLevel(
    logging.DEBUG if os.getenv("ENV") == "dev" else logging.INFO
)""",
            0.5, 4.25, 7.8, 2.95, bg=RGBColor(0x00, 0x1A, 0x1A))

# Cost breakdown
rect(s, 8.45, 4.25, 4.55, 2.95, COLORS["white"])
tb(s, "💰 Расчёт экономии", 8.6, 4.33, 4.3, 0.4,
   size=13, bold=True, color=COLORS["green"])
log_calc = [
    "Было: 500 GB/мес × $0.03 = $1,500",
    "",
    "После оптимизации:",
    "  Уровни INFO→WARN: -70% объём",
    "  Sampling 1%: -50% inference",
    "  Retention 30д: -67% хранение",
    "",
    "Итого объём: ~80 GB/мес",
    "80 GB × $0.03 = $240/мес",
    "─────────────────────────",
    "БЫЛО:  $1,500/мес",
    "СТАЛО: $240/мес",
    "Экономия: $1,260/мес (84%)",
]
y = 4.72
for line in log_calc:
    if not line:
        y += 0.12
        continue
    bold = "БЫЛО" in line or "СТАЛО" in line or "Экономия" in line
    color = COLORS["green"] if "Экономия" in line else (
        COLORS["red"] if "БЫЛО" in line else COLORS["black"])
    tb(s, line, 8.6, y, 4.3, 0.27, size=11, bold=bold, color=color)
    y += 0.27

# ══════════════════════════════════════════════════════════════════
# SLIDE 13 — Оптимизация 6: Data Transfer (bonus)
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["gray_light"])
rect(s, 0, 0, 13.33, 1.5, COLORS["slate"])
rect(s, 0, 0, 0.25, 7.5, COLORS["slate"])
badge(s, "BONUS", 0.35, 0.5, 1.0, 0.6, COLORS["gold"],
      text_color=COLORS["navy"])
tb(s, "Data Transfer: устранение cross-region репликации", 1.5, 0.1, 11.5, 0.75,
   size=24, bold=True, color=COLORS["white"])
tb(s, "Экономия: $1,500–$1,800/мес · Сложность: средняя · Срок: 1 неделя",
   1.5, 0.85, 11.5, 0.5, size=13, italic=True,
   color=RGBColor(0xCC, 0xDD, 0xFF))

# Problem
rect(s, 0.5, 1.65, 5.8, 4.2, COLORS["white"])
tb(s, "🔍 Проблема: зачем cross-region?", 0.65, 1.72, 5.5, 0.42,
   size=14, bold=True, color=COLORS["red"])
problem_items = [
    "ML данные реплицируются в 3 региона",
    "Исторически: DR требования из 2022 года",
    "Реальность: DR тест не проводился ни разу",
    "Inference сервис читает данные только из us-east-1",
    "Dev-окружение в eu-west-1 — читает из us-east-1",
    "25 TB данных × $0.02–0.08/GB = $2,000+/мес",
    "",
    "Решение:",
    "→ Dev-окружение перенести в us-east-1",
    "→ S3 Replication только для backup (Deep Archive)",
    "→ Использовать S3 Transfer Acceleration только при необходимости",
    "→ Пересмотреть DR стратегию с бизнесом",
]
y = 2.2
for item in problem_items:
    if not item:
        y += 0.15
        continue
    bold = item.startswith("→") or item.startswith("Решение")
    color = COLORS["green"] if item.startswith("→") else (
        COLORS["amber"] if item.startswith("Решение") else COLORS["black"])
    tb(s, item, 0.65, y, 5.5, 0.35, size=12, bold=bold, color=color)
    y += 0.36

# Transfer cost comparison
rect(s, 6.5, 1.65, 6.5, 4.2, COLORS["white"])
tb(s, "💸 Стоимость трафика AWS", 6.65, 1.72, 6.2, 0.42,
   size=14, bold=True, color=COLORS["slate"])

traffic_types = [
    ("Cross-region (us→eu)", "$0.02/GB", "25 TB/мес", "$500", COLORS["red"]),
    ("Cross-region (us→ap)", "$0.08/GB", "10 TB/мес", "$800", COLORS["red"]),
    ("Egress (→ internet)", "$0.09/GB", "~5 TB/мес", "$460", COLORS["red"]),
    ("Cross-AZ (в регионе)", "$0.01/GB", "~10 TB/мес", "$100", COLORS["amber"]),
    ("Intra-AZ", "БЕСПЛАТНО", "—", "$0", COLORS["green"]),
]
headers_tr = ["Тип трафика", "Цена/GB", "Объём", "Стоимость"]
rows_tr = [(t, p, v, c) for t, p, v, c, _ in traffic_types]
table(s, headers_tr, rows_tr, 6.5, 2.2, 6.5, 2.6,
      COLORS["slate"], COLORS["white"],
      alt_fill=RGBColor(0xEE, 0xF3, 0xF8), size=12)

rect(s, 6.5, 4.95, 6.5, 0.75, COLORS["green_light"])
tb(s, "После оптимизации: только intra-AZ + минимальный egress = ~$200/мес",
   6.65, 5.05, 6.2, 0.55, size=13, bold=True, color=COLORS["green"])

# Data locality principle
rect(s, 0.5, 6.0, 12.3, 1.2, COLORS["white"])
tb(s, "📐 Принцип data locality:", 0.65, 6.08, 4.0, 0.38,
   size=14, bold=True, color=COLORS["slate"])
tb(s, "Данные должны находиться там, где их обрабатывают.\n"
       "Перемещение данных между регионами и AZ — это всегда дорого и медленно.",
   0.65, 6.5, 12.0, 0.65, size=13, color=COLORS["black"], italic=True)

# ══════════════════════════════════════════════════════════════════
# SLIDE 14 — Сводная таблица экономии
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Итоговый расчёт: было → стало", COLORS["green"])

headers_sum = ["#", "Оптимизация", "Было, $/мес", "Стало, $/мес", "Экономия, $", "Экономия, %", "Сложность"]
rows_sum = [
    ["1", "GPU: Spot + Scheduling", "$8,928", "$4,176", "$4,752", "53%", "⭐⭐"],
    ["2", "Training: еженедельно", "входит в GPU", "входит в GPU", "~$800", "—", "⭐"],
    ["3", "S3 Lifecycle Policy", "$3,500", "$750", "$2,750", "79%", "⭐"],
    ["4", "K8s Autoscaling", "$4,000", "$2,200", "$1,800", "45%", "⭐⭐"],
    ["5", "Log Optimization", "$1,500", "$240", "$1,260", "84%", "⭐"],
    ["6", "Data Transfer", "$2,000", "$200", "$1,800", "90%", "⭐⭐"],
    ["", "Прочее (без изменений)", "$3,118", "$3,118", "$0", "—", "—"],
    ["", "ИТОГО", "$23,046", "$10,684", "$12,362", "54%", ""],
]
table(s, headers_sum, rows_sum, 0.3, 1.6, 12.73, 4.8,
      COLORS["green"], COLORS["white"],
      alt_fill=COLORS["green_light"],
      size=12)

# Visual result
rect(s, 0.3, 6.5, 5.8, 0.85, COLORS["red_light"])
tb(s, "БЫЛО: $23,046/мес  ($276,552/год)", 0.5, 6.62, 5.5, 0.55,
   size=16, bold=True, color=COLORS["red"], align=PP_ALIGN.CENTER)

tb(s, "→", 6.2, 6.6, 0.9, 0.6, size=32, bold=True,
   color=COLORS["black"], align=PP_ALIGN.CENTER)

rect(s, 7.25, 6.5, 5.8, 0.85, COLORS["green_light"])
tb(s, "СТАЛО: $10,684/мес  ($128,208/год)", 7.45, 6.62, 5.5, 0.55,
   size=16, bold=True, color=COLORS["green"], align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# SLIDE 15 — Визуализация до/после
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Визуализация: структура расходов до и после", COLORS["slate"])

# Before chart (stacked bar simulation)
tb(s, "ДО оптимизации", 1.0, 1.6, 5.0, 0.45,
   size=16, bold=True, color=COLORS["red"], align=PP_ALIGN.CENTER)
before_items = [
    ("GPU (EC2)", 39, COLORS["red"]),
    ("Kubernetes", 17, COLORS["purple"]),
    ("S3 Storage", 15, COLORS["blue"]),
    ("Data Transfer", 9, COLORS["orange"]),
    ("Logging", 6, COLORS["teal"]),
    ("Прочее", 14, COLORS["gray"]),
]
y_bar = 2.15
for label, pct, color in before_items:
    bar_w = pct * 0.09
    rect(s, 1.0, y_bar, bar_w, 0.48, color)
    tb(s, f"{label}: {pct}%", 1.0 + bar_w + 0.08, y_bar + 0.08,
       3.5, 0.32, size=12, color=COLORS["black"])
    y_bar += 0.56

# After chart
tb(s, "ПОСЛЕ оптимизации", 7.5, 1.6, 5.0, 0.45,
   size=16, bold=True, color=COLORS["green"], align=PP_ALIGN.CENTER)
after_items = [
    ("GPU (Spot)", 39, RGBColor(0xFF, 0xAA, 0xAA)),
    ("Kubernetes", 21, RGBColor(0xCC, 0xAA, 0xFF)),
    ("S3 Storage", 7, RGBColor(0xAA, 0xCC, 0xFF)),
    ("Data Transfer", 2, RGBColor(0xFF, 0xCC, 0x99)),
    ("Logging", 2, RGBColor(0xAA, 0xEE, 0xEE)),
    ("Прочее", 29, RGBColor(0xCC, 0xCC, 0xCC)),
]
y_bar = 2.15
for label, pct, color in after_items:
    bar_w = pct * 0.09
    rect(s, 7.5, y_bar, bar_w, 0.48, color)
    tb(s, f"{label}: {pct}%", 7.5 + bar_w + 0.08, y_bar + 0.08,
       3.5, 0.32, size=12, color=COLORS["black"])
    y_bar += 0.56

# Big number highlight
rect(s, 4.5, 2.5, 4.3, 2.5, COLORS["navy"])
tb(s, "Экономия\nза год:", 4.5, 2.7, 4.3, 0.8,
   size=16, bold=True, color=RGBColor(0x80, 0xB0, 0xD8),
   align=PP_ALIGN.CENTER)
tb(s, "$148,344", 4.5, 3.45, 4.3, 0.9,
   size=36, bold=True, color=COLORS["gold"], align=PP_ALIGN.CENTER)
tb(s, "54% savings", 4.5, 4.35, 4.3, 0.5,
   size=18, bold=True, color=COLORS["green"], align=PP_ALIGN.CENTER)

rect(s, 0.3, 5.7, 12.73, 1.0, COLORS["white"])
tb(s, "Важно: функциональность системы не изменилась.",
   0.5, 5.78, 12.3, 0.38, size=14, bold=True, color=COLORS["black"])
tb(s, "Все пользователи получают рекомендации с той же точностью и скоростью.",
   0.5, 6.18, 12.3, 0.38, size=14, color=COLORS["gray"], italic=True)

# ══════════════════════════════════════════════════════════════════
# SLIDE 16 — Приоритизация: Quick Wins vs Long-term
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Приоритизация: план внедрения", COLORS["amber"])

# Quadrant matrix: Impact vs Effort
rect(s, 0.5, 1.65, 6.5, 5.1, COLORS["white"])
tb(s, "Матрица: Экономия vs Сложность внедрения", 0.65, 1.72, 6.2, 0.42,
   size=14, bold=True, color=COLORS["amber"])

# Q1: Low effort, High impact = DO FIRST
rect(s, 0.5, 2.25, 3.1, 2.3, RGBColor(0xD5, 0xF5, 0xE3))
tb(s, "СНАЧАЛА", 0.65, 2.3, 2.9, 0.38, size=12, bold=True, color=COLORS["green"])
tb(s, "Низкие усилия\nВысокий эффект", 0.65, 2.68, 2.9, 0.55,
   size=11, italic=True, color=COLORS["green"])
qw = ["S3 Lifecycle", "Log Retention 30д", "Log Levels (INFO)"]
for i, item in enumerate(qw):
    tb(s, f"✓  {item}", 0.65, 3.3 + i * 0.32, 2.9, 0.28, size=11, color=COLORS["green"])

# Q2: High effort, High impact = PLAN
rect(s, 3.65, 2.25, 3.1, 2.3, RGBColor(0xD6, 0xE8, 0xF7))
tb(s, "ПЛАНИРОВАТЬ", 3.8, 2.3, 2.9, 0.38, size=12, bold=True, color=COLORS["blue"])
tb(s, "Средние усилия\nВысокий эффект", 3.8, 2.68, 2.9, 0.55,
   size=11, italic=True, color=COLORS["blue"])
plan_items = ["GPU Spot Instances", "K8s Autoscaling", "Training Schedule"]
for i, item in enumerate(plan_items):
    tb(s, f"→  {item}", 3.8, 3.3 + i * 0.32, 2.9, 0.28, size=11, color=COLORS["blue"])

# Q3: Low effort, Low impact = QUICK FILL
rect(s, 0.5, 4.6, 3.1, 1.5, COLORS["gray_light"])
tb(s, "ПОПУТНО", 0.65, 4.65, 2.9, 0.38, size=12, bold=True, color=COLORS["gray"])
tb(s, "Log Sampling 1%\nS3 Request Opt", 0.65, 5.1, 2.9, 0.55,
   size=11, color=COLORS["gray"])

# Q4: High effort, Low impact = LATER
rect(s, 3.65, 4.6, 3.1, 1.5, RGBColor(0xFF, 0xF9, 0xE6))
tb(s, "ПОТОМ", 3.8, 4.65, 2.9, 0.38, size=12, bold=True, color=COLORS["amber"])
tb(s, "Data Transfer\nDev→us-east-1", 3.8, 5.1, 2.9, 0.55,
   size=11, color=COLORS["amber"])

# Axis labels
tb(s, "← Малый эффект          Большой эффект →", 0.5, 6.3, 6.5, 0.38,
   size=11, color=COLORS["gray"], align=PP_ALIGN.CENTER)

# Timeline
rect(s, 7.2, 1.65, 5.8, 5.1, COLORS["white"])
tb(s, "📅 Timeline внедрения", 7.35, 1.72, 5.5, 0.42,
   size=14, bold=True, color=COLORS["amber"])

timeline = [
    ("Неделя 1–2", COLORS["green"],
     ["S3 Lifecycle Policy (1 день)",
      "Log retention → 30 дней (1 день)",
      "Log levels → INFO (3 дня)",
      "Ожидаемая экономия: +$4,010/мес"]),
    ("Неделя 3–4", COLORS["blue"],
     ["GPU Spot instances (5 дней)",
      "Training cron schedule (2 дня)",
      "K8s HPA настройка (3 дня)",
      "Ожидаемая экономия: +$5,750/мес"]),
    ("Месяц 2", COLORS["amber"],
     ["Cluster Autoscaler (5 дней)",
      "Data Transfer оптимизация",
      "Log sampling (2 дня)",
      "Ожидаемая экономия: +$2,600/мес"]),
]

y_tl = 2.25
for period, color, items in timeline:
    rect(s, 7.35, y_tl, 1.55, len(items) * 0.34 + 0.42, color)
    tb(s, period, 7.35, y_tl + 0.05, 1.55, 0.32,
       size=11, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER)
    for i, item in enumerate(items):
        bold = item.startswith("Ожидаем")
        col = COLORS["green"] if item.startswith("Ожидаем") else COLORS["black"]
        tb(s, item, 9.0, y_tl + 0.1 + i * 0.34, 3.9, 0.32,
           size=11, bold=bold, color=col)
    y_tl += len(items) * 0.34 + 0.55

# ══════════════════════════════════════════════════════════════════
# SLIDE 17 — Архитектура "как должно быть"
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Архитектура «как должно быть» (TO-BE)", COLORS["green"])

# Pipeline TO-BE
stages_tobe = [
    ("S3 Tiered\n(lifecycle\npolicy)", COLORS["green"]),
    ("Feature\nPipeline\n(по расписанию)", COLORS["teal"]),
    ("Training\n(Spot GPU\n1×/неделю)", COLORS["blue"]),
    ("Model\nRegistry\n(A/B testing)", COLORS["slate"]),
    ("Batch/RT\nInference\n(K8s autoscale)", COLORS["purple"]),
]
x = 0.4
for i, (label, color) in enumerate(stages_tobe):
    rect(s, x, 1.75, 2.15, 1.4, color)
    tb(s, label, x, 1.83, 2.15, 1.22,
       size=12, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER)
    if i < 4:
        tb(s, "→", x + 2.15, 2.25, 0.3, 0.55,
           size=22, bold=True, color=COLORS["green"], align=PP_ALIGN.CENTER)
    x += 2.45

# Improvements annotations
improvements = [
    (0.4, 3.3, 2.15,
     "✅ Lifecycle:\nhot→IA→Glacier\nавтоматически", COLORS["green_light"]),
    (2.85, 3.3, 2.15,
     "✅ Запуск\nпо расписанию\n+ data drift", COLORS["green_light"]),
    (5.3, 3.3, 2.15,
     "✅ Spot GPU\n1×/неделю\n+ авто-выкл", COLORS["green_light"]),
    (7.75, 3.3, 2.15,
     "✅ Champion-\nChallenger\nA/B deploy", COLORS["green_light"]),
    (10.2, 3.3, 2.15,
     "✅ HPA + CAS\nSpot node groups\nАвтомасштаб", COLORS["green_light"]),
]
for x, y, w, text, fill in improvements:
    rect(s, x, y, w, 1.7, fill, line=COLORS["green"], line_w=1)
    tb(s, text, x + 0.1, y + 0.08, w - 0.2, 1.5, size=11, color=COLORS["green"])

# Monitoring row
rect(s, 0.4, 5.2, 12.5, 0.7, COLORS["green_light"])
tb(s, "📊 Monitoring / Logging: structured logs · sampling 1% · INFO/WARN/ERROR · retention 30 дней",
   0.6, 5.3, 12.1, 0.45, size=13, color=COLORS["green"], bold=True)

# Key metrics TO-BE
rect(s, 0.4, 6.05, 12.5, 1.2, COLORS["white"])
metrics_tobe = [
    ("GPU utilization", "~80%", COLORS["green"]),
    ("K8s node util.", "~65%", COLORS["green"]),
    ("S3 avg tier cost", "-79%", COLORS["green"]),
    ("Training cadence", "1×/неделю", COLORS["blue"]),
    ("Inference mode", "Batch+RT mix", COLORS["teal"]),
]
x = 0.6
for label, val, col in metrics_tobe:
    tb(s, label, x, 6.1, 2.2, 0.38, size=11, color=COLORS["gray"])
    tb(s, val, x, 6.52, 2.2, 0.6, size=18, bold=True, color=col)
    x += 2.5

# ══════════════════════════════════════════════════════════════════
# SLIDE 18 — Чеклист внедрения
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
section_header(s, "Чеклист внедрения FinOps-практик", COLORS["slate"])

checklist = [
    (COLORS["green"], "Быстрые победы (неделя 1)", [
        ("S3 Lifecycle Policy — настроить правила hot→IA→Glacier", "1 день"),
        ("CloudWatch retention: установить 30 дней для всех лог-групп", "2 часа"),
        ("Log levels: убрать DEBUG из production конфигов", "1 день"),
        ("Теги на все ресурсы: project/env/team/cost-center", "1–2 дня"),
    ]),
    (COLORS["blue"], "Среднесрочные (неделя 2–4)", [
        ("GPU: настроить Spot instance + bid strategy в AWS Batch", "3–5 дней"),
        ("Training cron: перевести на еженедельный schedule + drift monitor", "3 дня"),
        ("K8s HPA: настроить по CPU и RPS метрикам", "2–3 дня"),
        ("Cluster Autoscaler: добавить Spot node group", "3–5 дней"),
    ]),
    (COLORS["amber"], "Долгосрочные (месяц 2–3)", [
        ("Data Transfer: перенести dev окружение в us-east-1", "1 неделя"),
        ("Log sampling: настроить 1% sampling для inference", "2–3 дня"),
        ("MLflow: добавить cost tracking per experiment", "1 неделя"),
        ("Budget alerts: настроить оповещения при отклонении >10%", "1 день"),
    ]),
]

y_pos = 1.65
for color, section_title, items in checklist:
    rect(s, 0.4, y_pos, 12.5, 0.42, color)
    tb(s, section_title, 0.55, y_pos + 0.06, 8.0, 0.3,
       size=13, bold=True, color=COLORS["white"])
    y_pos += 0.42
    for task, duration in items:
        rect(s, 0.4, y_pos, 12.5, 0.4, COLORS["white"])
        rect(s, 0.4, y_pos, 0.08, 0.4, color)
        tb(s, f"☐  {task}", 0.6, y_pos + 0.05, 10.2, 0.3, size=12, color=COLORS["black"])
        tb(s, duration, 11.0, y_pos + 0.06, 1.8, 0.28, size=11,
           color=color, bold=True, align=PP_ALIGN.RIGHT)
        y_pos += 0.4
    y_pos += 0.12

# ══════════════════════════════════════════════════════════════════
# SLIDE 19 — Финальный вывод практики
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
rect(s, 0, 0, 13.33, 7.5, COLORS["navy"])
rect(s, 0, 0, 0.3, 7.5, COLORS["gold"])
rect(s, 0, 7.1, 13.33, 0.4, COLORS["gold"])

tb(s, "Выводы практической работы", 0.6, 0.35, 12.5, 0.6,
   size=18, italic=True, color=RGBColor(0x80, 0xB0, 0xD8))

tb(s, "Что мы сделали:", 0.6, 1.05, 12.5, 0.5,
   size=20, bold=True, color=COLORS["white"])

results = [
    ("$23,046/мес", "$10,684/мес", "54%", "Снизили cloud bill"),
    ("15% GPU util", "80% GPU util", "×5.3", "Улучшили эффективность"),
    ("90д retention", "30д retention", "-67%", "Сократили хранение логов"),
    ("Ежедневно", "1×/неделю", "7×", "Оптимизировали training"),
]

headers_res = ["Метрика", "До", "После", "Изменение", "Что это значит"]
rows_res = [(m, b, a, c) for b, a, c, m in results]
table(s, headers_res, rows_res, 0.5, 1.65, 12.3, 2.5,
      COLORS["blue"], COLORS["white"],
      alt_fill=RGBColor(0x1A, 0x3A, 0x5C),
      size=13)

tb(s, "Главный инсайт:", 0.6, 4.35, 12.5, 0.5,
   size=18, bold=True, color=COLORS["gold"])

insights = [
    "Экономия получена без ухудшения качества сервиса для пользователей",
    "Каждая проблема имела архитектурную причину, а не «плохой DevOps»",
    "Самые дорогие решения были приняты «по умолчанию» — без анализа",
    "FinOps = сделать стоимость явным параметром архитектурных решений",
]
y = 4.9
for insight in insights:
    rect(s, 0.6, y, 0.12, 0.4, COLORS["gold"])
    tb(s, insight, 0.85, y - 0.03, 12.0, 0.45,
       size=15, color=RGBColor(0xCC, 0xDD, 0xFF))
    y += 0.52

rect(s, 0.5, 7.0, 12.3, 0.4, RGBColor(0x1A, 0x3A, 0x5C))
tb(s, "FinOps — это не про экономию.  Это про управляемость системы через стоимость.",
   0.6, 7.05, 12.1, 0.3, size=14, bold=True, color=COLORS["gold"],
   align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# Save
# ══════════════════════════════════════════════════════════════════
output_path = ("/Users/stureiko/Documents/Programming/Otus/AI-Architect/"
               "FinOps - стратегия управления стоимостью/"
               "FinOps_Practice_Block.pptx")
prs.save(output_path)
print(f"Saved: {output_path}")
print(f"Slides: {len(prs.slides)}")
