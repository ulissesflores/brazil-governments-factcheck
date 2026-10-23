"""UI strings of the figures in the five languages of the repository.

Hebrew is a machine translation with no human right-to-left review (stated in the figure
notes and in ``docs/*/METHODOLOGY.md``); every Hebrew string is checked by the bidi rule in
:func:`govfc.svg.proteger_rtl`. Numbers are never written here: they come from ``results.json``.
"""

LINGUAS = ["pt-BR", "en", "es", "it", "he"]
DECIMAL = {"pt-BR": ",", "en": ".", "es": ",", "it": ",", "he": "."}

COLUNAS = {  # slug -> {lang: (name, years)}
    "ditadura": {
        "pt-BR": ("Ditadura", "1967–74"),
        "en": ("Dictatorship", "1967–74"),
        "es": ("Dictadura", "1967–74"),
        "it": ("Dittatura", "1967–74"),
        "he": ("הדיקטטורה", "1967–74"),
    },
    "itamar": {k: ("Itamar", "1992–94") for k in LINGUAS} | {"he": ("איטמר", "1992–94")},
    "fhc": {k: ("FHC", "1995–2002") for k in LINGUAS} | {"he": ("קרדוזו", "1995–2002")},
    "lula12": {k: ("Lula 1–2", "2003–10") for k in LINGUAS} | {"he": ("לולה 1–2", "2003–10")},
    "dilma": {k: ("Dilma", "2011–16") for k in LINGUAS} | {"he": ("דילמה", "2011–16")},
    "temer": {k: ("Temer", "2016–18") for k in LINGUAS} | {"he": ("טמר", "2016–18")},
    "bolsonaro": {k: ("Bolsonaro", "2019–22") for k in LINGUAS} | {"he": ("בולסונרו", "2019–22")},
    "lula3": {k: ("Lula 3", "2023–25*") for k in LINGUAS} | {"he": ("לולה 3", "2023–25*")},
}

INDICADORES = {  # slug -> {lang: (name, hint)}
    "pib": {
        "pt-BR": ("PIB", "média anual (IBGE)"),
        "en": ("GDP", "annual average (IBGE)"),
        "es": ("PIB", "media anual (IBGE)"),
        "it": ("PIL", "media annua (IBGE)"),
        "he": ("תוצר", "ממוצע שנתי (IBGE)"),
    },
    "inflacao": {
        "pt-BR": ("Inflação", "média anual (IPCA)"),
        "en": ("Inflation", "annual average (IPCA)"),
        "es": ("Inflación", "media anual (IPCA)"),
        "it": ("Inflazione", "media annua (IPCA)"),
        "he": ("אינפלציה", "ממוצע שנתי (IPCA)"),
    },
    "desemprego": {
        "pt-BR": ("Desemprego", "taxa média (PME ou PNAD-C)"),
        "en": ("Unemployment", "average rate (PME or PNAD-C)"),
        "es": ("Desempleo", "tasa media (PME o PNAD-C)"),
        "it": ("Disoccupazione", "tasso medio (PME o PNAD-C)"),
        "he": ("אבטלה", "שיעור ממוצע (PME או PNAD-C)"),
    },
    "salmin": {
        "pt-BR": ("Salário mínimo", "variação real, dez a dez"),
        "en": ("Minimum wage", "real change, Dec to Dec"),
        "es": ("Salario mínimo", "variación real, dic a dic"),
        "it": ("Salario minimo", "variazione reale, dic su dic"),
        "he": ("שכר מינימום", "שינוי ריאלי, דצמבר לדצמבר"),
    },
    "pobreza": {
        "pt-BR": ("Pobreza", "% da pop., US$ 6,85/dia"),
        "en": ("Poverty", "% of pop., US$ 6.85/day"),
        "es": ("Pobreza", "% de la pob., US$ 6,85/día"),
        "it": ("Povertà", "% della pop., US$ 6,85/giorno"),
        "he": ("עוני", "% מהאוכלוסייה, 6.85$ ליום"),
    },
    "gini": {
        "pt-BR": ("Desigualdade", "índice de Gini (PIP)"),
        "en": ("Inequality", "Gini index (PIP)"),
        "es": ("Desigualdad", "índice de Gini (PIP)"),
        "it": ("Disuguaglianza", "indice di Gini (PIP)"),
        "he": ("אי־שוויון", "מדד ג׳יני (PIP)"),
    },
    "expvida": {
        "pt-BR": ("Expectativa de vida", "anos (ONU/Banco Mundial)"),
        "en": ("Life expectancy", "years (UN/World Bank)"),
        "es": ("Esperanza de vida", "años (ONU/Banco Mundial)"),
        "it": ("Aspettativa di vita", "anni (ONU/Banca Mondiale)"),
        "he": ("תוחלת חיים", "שנים (או״ם/הבנק העולמי)"),
    },
}

PLACAR = {
    "titulo": {
        "pt-BR": "O infográfico do WhatsApp contra os dados públicos",
        "en": "The WhatsApp infographic against public data",
        "es": "El infográfico de WhatsApp frente a los datos públicos",
        "it": "L’infografica di WhatsApp messa alla prova dei dati pubblici",
        "he": "האינפוגרפיקה מוואטסאפ מול הנתונים הציבוריים",
    },
    "contagem": {  # n, r, a, x, u
        "pt-BR": "{n} números conferidos: {r} reproduzem, {a} aproximam, {x} não reproduzem, {u} sem verificação",
        "en": "{n} numbers checked: {r} reproduce, {a} approximate, {x} do not reproduce, {u} unverified",
        "es": "{n} números comprobados: {r} se reproducen, {a} se aproximan, {x} no se reproducen, {u} sin verificar",
        "it": "{n} numeri verificati: {r} riprodotti, {a} approssimati, {x} non riprodotti, {u} non verificabili",
        "he": "{n} מספרים נבדקו: {r} משוחזרים, {a} מקורבים, {x} לא משוחזרים, {u} לא ניתנים לבדיקה",
    },
    "celula": {
        "pt-BR": "Em cada célula: em cima, o número impresso no infográfico; embaixo, o que sai dos dados públicos.",
        "en": "In each cell: on top, the number printed on the infographic; below, what public data give.",
        "es": "En cada celda: arriba, el número impreso en el infográfico; abajo, el que dan los datos públicos.",
        "it": "In ogni cella: sopra il numero stampato nell’infografica; sotto quello che danno i dati pubblici.",
        "he": "בכל תא: למעלה המספר שמודפס באינפוגרפיקה; למטה מה שעולה מהנתונים הציבוריים.",
    },
    "legenda": {  # order: reproduz, aproxima, nao reproduz, sem verificacao
        "pt-BR": [
            "reproduz (arredonda ao impresso)",
            "aproxima (até 0,3 p.p. ou 5%)",
            "não reproduz",
            "sem série para conferir",
        ],
        "en": [
            "reproduces (rounds to the printed value)",
            "approximates (within 0.3 pp or 5%)",
            "does not reproduce",
            "no series to check",
        ],
        "es": [
            "se reproduce (redondea a lo impreso)",
            "se aproxima (hasta 0,3 p.p. o 5%)",
            "no se reproduce",
            "sin serie para comprobar",
        ],
        "it": [
            "riprodotto (arrotonda allo stampato)",
            "approssimato (entro 0,3 p.p. o 5%)",
            "non riprodotto",
            "nessuna serie da verificare",
        ],
        "he": [
            "משוחזר (מתעגל לערך המודפס)",
            "מקורב (עד 0.3 נק׳ אחוז או 5%)",
            "לא משוחזר",
            "אין סדרה לבדיקה",
        ],
    },
    "rodape_regra": {
        "pt-BR": "Regra de veredito fixa em código; uma especificação primária por indicador; alternativas só como sensibilidade.",
        "en": "Verdict rule fixed in code; one primary specification per indicator; alternatives only as sensitivity.",
        "es": "Regla de veredicto fija en código; una especificación primaria por indicador; alternativas solo como sensibilidad.",
        "it": "Regola di verdetto fissata nel codice; una specifica primaria per indicatore; le alternative solo come sensibilità.",
        "he": "כלל ההכרעה קבוע בקוד; מפרט ראשי אחד לכל מדד; חלופות רק כניתוח רגישות.",
    },
    "rodape_fonte": {
        "pt-BR": "Fontes: Banco Central (SGS), IBGE, Ipea, Banco Mundial. Asterisco: mandato em curso, dado parcial.",
        "en": "Sources: Central Bank of Brazil (SGS), IBGE, Ipea, World Bank. Asterisk: ongoing term, partial data.",
        "es": "Fuentes: Banco Central de Brasil (SGS), IBGE, Ipea, Banco Mundial. Asterisco: mandato en curso, dato parcial.",
        "it": "Fonti: Banca centrale del Brasile (SGS), IBGE, Ipea, Banca Mondiale. Asterisco: mandato in corso, dato parziale.",
        "he": "מקורות: הבנק המרכזי של ברזיל (SGS), IBGE, Ipea, הבנק העולמי. כוכבית: כהונה מתמשכת, נתון חלקי.",
    },
    "impresso": {
        "pt-BR": "infográfico",
        "en": "infographic",
        "es": "infográfico",
        "it": "infografica",
        "he": "אינפוגרפיקה",
    },
    "dados": {"pt-BR": "dados", "en": "data", "es": "datos", "it": "dati", "he": "נתונים"},
    "traducao_he": "תרגום מכונה, ללא סקירה אנושית של כיווניות הטקסט.",
}
