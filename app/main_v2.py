from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')

app, rt = fast_app(hdrs=Theme.orange.headers(mode='light', apex_charts=True, daisy=True), 
                   static_dir=static_dir,  # Serve static files from the static directory
                   live=True)

def BrainIcon(tooltip_text):
    """Brain icon with tooltip for AI transparency"""
    return Span(
        UkIcon("brain", height=16, width=16, cls="text-orange-500 cursor-help"),
        uk_tooltip=f"title: AI Decision: {tooltip_text}; pos: top-left"
    )

def FormSectionDiv(*c, cls='space-y-3', **kwargs): 
    return Div(*c, cls=cls, **kwargs)

def HelpText(c): 
    return P(c, cls=TextPresets.muted_sm)

def LoadingOverlay():
    """Full-screen loading overlay with blur effect"""
    return Div(
        Div(
            Card(
                DivCentered(
                    Loading((LoadingT.spinner, LoadingT.lg)),
                    H3("AI is analyzing and generating your brief...", cls="mt-4"),
                    P("This may take a few moments", cls=TextPresets.muted_sm)
                ),
                cls="p-8"
            ),
            cls="flex items-center justify-center min-h-screen"
        ),
        id="loading-overlay",
        cls="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 hidden",
        style="backdrop-filter: blur(4px);"
    ), Script("""
    function startBriefGeneration() {
        // Show loading overlay
        document.getElementById('loading-overlay').classList.remove('hidden');
        
        // After 10 seconds, redirect to step 4
        setTimeout(function() {
            window.location.href = '/campaign/step4';
        }, 10000);
    }
    """)

def AppHeader():
    """Main application header with navigation"""
    return NavBar(
        Input(placeholder='Search campaigns...', cls="w-64"),
        A('Dashboard', href='/', cls="text-white hover:text-orange-200"),
        A("New Campaign", href='/campaign/new', cls="text-white hover:text-orange-200"),
        A("My Campaigns", href='/campaigns', cls="text-white hover:text-orange-200"),
        A("Settings", href='/settings', cls="text-white hover:text-orange-200"),
        brand=DivLAligned(
            Img(src='logo.png', height=60, width=60),  # Fixed: removed leading slash
            Div(
                H3("ING Content Studio", cls="text-white"),
                P("SEO Brief Generator", cls="text-orange-200 text-sm")
            )
        ),
        cls="bg-gradient-to-r from-orange-600 to-orange-500 shadow-lg"
    )

def keyword_yoy_chart():
    """SEMRush-style Year-over-Year comparison for 'bedrijfsaansprakelijkheidsverzekering' keyword"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data_2023 = [2100, 2200, 2300, 2400, 2500, 2450, 2600, 2550, 2700, 2650, 2800, 2750]
    data_2024 = [2300, 2400, 2600, 2700, 2800, 2540, 2900, 2850, 3000, 2950, 3100, 3050]
    
    return ApexChart(
        opts={
            "chart": {
                "height": 400,
                "type": "line",
                "dropShadow": {
                    "enabled": True,
                    "color": "#000",
                    "top": 18,
                    "left": 7,
                    "blur": 10,
                    "opacity": 0.2
                },
                "zoom": {"enabled": True},
                "toolbar": {"show": True}
            },
            "series": [
                {"name": "2023", "data": data_2023},
                {"name": "2024", "data": data_2024}
            ],
            "colors": ['#FF6200', '#545454'],
            "dataLabels": {"enabled": False},
            "stroke": {"curve": "smooth", "width": 3},
            "title": {
                "align": "left",
                "style": {"fontSize": "18px", "fontWeight": "600"}
            },
            "grid": {
                "borderColor": "#e7e7e7",
                "row": {"colors": ["#f3f3f3", "transparent"], "opacity": 0.3}
            },
            "markers": {"size": 6, "hover": {"size": 8}},
            "xaxis": {"categories": months, "title": {"text": "Month"}},
            "yaxis": {"title": {"text": "Monthly Search Volume"}, "min": 2000, "max": 3200},
            "legend": {
                "position": "top", "horizontalAlign": "right", 
                "floating": True, "offsetY": -25, "offsetX": -5
            },
            "tooltip": {
                "y": {"formatter": "function(value) { return value.toLocaleString() + ' searches' }"}
            }
        },
        cls='w-full'
    )

def CampaignSteps(current_step=1):
    """Progressive step indicator"""
    steps = [
        ("Mode Selection", "📝", 1),
        ("Research Setup", "🔍", 2), 
        ("AI Analysis", "🧠", 3),
        ("Brief Review", "📄", 4),
        ("Export", "📤", 5)
    ]
    
    step_items = []
    for title, icon, step_num in steps:
        if step_num < current_step:
            cls = StepT.success
        elif step_num == current_step:
            cls = StepT.primary
        else:
            cls = StepT.neutral
            
        step_items.append(
            LiStep(title, cls=cls, data_content=icon)
        )
    
    return Steps(*step_items, cls=(StepsT.horizonal, "mb-8"))

# Step 1: Mode Selection
def step1_mode_selection():
    return Container(
        CampaignSteps(1),
        
        Card(
            H2("Choose Your Campaign Mode"),
            P("Select how you want to create your content brief", cls=TextPresets.muted_sm),
            
            Grid(
                Card(
                    DivCentered(
                        UkIcon("edit", height=48, width=48, cls="text-orange-500 mb-4"),
                        H3("Optimize Existing Page"),
                        P("Improve an existing ING webpage's SEO performance", cls=TextPresets.muted_sm),
                        P("Start with: URL + Keywords", cls="text-orange-600 font-medium")
                    ),
                    A(
                        Button("Select Optimize Mode", 
                               cls=ButtonT.primary + " w-full mt-4"),
                        href="/campaign/step2?mode=optimize"
                    ),
                    cls="p-6 hover:shadow-lg transition-shadow"
                ),
                
                Card(
                    DivCentered(
                        UkIcon("plus-circle", height=48, width=48, cls="text-green-500 mb-4"),
                        H3("Create New Brief"),
                        P("Generate a brief for a completely new page", cls=TextPresets.muted_sm),
                        P("Start with: Keywords + Content Ideas", cls="text-green-600 font-medium")
                    ),
                    A(
                        Button("Select Create Mode", 
                               cls=ButtonT.primary + " w-full mt-4"),
                        href="/campaign/step2?mode=create"
                    ),
                    cls="p-6 hover:shadow-lg transition-shadow"
                ),
                cols=2, gap=6
            )
        ),
        
        cls="max-w-4xl mx-auto"
    )

# Step 2: Research Setup
def step2_research_setup(mode="optimize"):
    settings_card = Card(
        DivLAligned(
            H3("Optional Settings"),
            Switch(id="show-advanced", label="Show Advanced Options")
        ),
        
        Div(
            Grid(
                FormSectionDiv(
                    DivLAligned(
                        FormLabel("Market/Locale"),
                        BrainIcon("Auto-detected based on keywords and domain")
                    ),
                    Select(
                        Option("Netherlands (NL)", selected=True),
                        Option("Belgium (BE)"),
                        Option("Germany (DE)"),
                        id="market"
                    )
                ),
                
                FormSectionDiv(
                    DivLAligned(
                        FormLabel("Product Group"),
                        BrainIcon("Determines legal pack and SharePoint folder")
                    ),
                    Select(
                        Option("Zakelijke Verzekeringen", selected=True),
                        Option("Zakelijke Rekeningen"),
                        Option("Zakelijke Leningen"),
                        Option("Beleggen"),
                        id="product-group"
                    )
                ),
                cols=2, gap=4
            ),
            
            # Advanced options (initially hidden)
            Div(
                H4("Advanced Settings", cls="mt-6 mb-4"),
                Grid(
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Research Depth"),
                            BrainIcon("Affects competitor analysis depth and keyword expansion")
                        ),
                        LabelRange("Standard", value="2", min=1, max=3, id="research-depth")
                    ),
                    
                    FormSectionDiv(
                        FormLabel("Include Sections"),
                        DivVStacked(
                            LabelCheckboxX("Legal/Compliance blocks", checked=True, id="legal-blocks"),
                            LabelCheckboxX("FAQ from PAA", checked=True, id="faq-blocks"),
                            LabelCheckboxX("Competitor analysis", checked=True, id="competitor-analysis"),
                            LabelCheckboxX("Internal linking suggestions", id="internal-links")
                        )
                    ),
                    cols=2, gap=4
                ),
                
                id="advanced-settings",
                cls="hidden"
            )
        )
    )
    
    if mode == "optimize":
        main_inputs = Card(
            H2("Optimize Existing Page"),
            P("Let's analyze and improve your current ING page", cls=TextPresets.muted_sm),
            
            FormSectionDiv(
                DivLAligned(
                    FormLabel("ING Page URL"),
                    BrainIcon("We'll crawl this page to understand current content structure")
                ),
                Input(placeholder="https://www.ing.nl/zakelijk/verzekeringen/...", id="page-url"),
                Button("Analyze URL", cls=ButtonT.default)
            ),
            
            FormSectionDiv(
                DivLAligned(
                    FormLabel("Target Keywords"),
                    BrainIcon("Primary keywords this page should rank for")
                ),
                Input(placeholder="bedrijfsaansprakelijkheidsverzekering, avb", id="keywords"),
                UploadZone(
                    DivCentered(
                        UkIcon("upload", height=24, width=24, cls="text-muted-foreground"),
                        P("Drop keyword file here", cls="text-sm mt-2"),
                        P("Supports .txt, .csv, .xlsx", cls=TextPresets.muted_sm)
                    ),
                    id='keyword-upload',
                    cls="border-2 border-dashed border-muted rounded-lg p-4 mt-3 hover:border-orange-400 transition-colors"
                )
            )
        )
    else:
        main_inputs = Card(
            H2("Create New Brief"),
            P("Let's create a brief for your new content", cls=TextPresets.muted_sm),
            
            FormSectionDiv(
                DivLAligned(
                    FormLabel("Focus Keywords"),
                    BrainIcon("Primary keywords for the new page to target")
                ),
                Input(placeholder="bedrijfsaansprakelijkheidsverzekering, avb", id="keywords"),
                UploadZone(
                    DivCentered(
                        UkIcon("upload", height=24, width=24, cls="text-muted-foreground"),
                        P("Drop keyword file here", cls="text-sm mt-2"),
                        P("Supports .txt, .csv, .xlsx", cls=TextPresets.muted_sm)
                    ),
                    id='keyword-upload',
                    cls="border-2 border-dashed border-muted rounded-lg p-4 mt-3 hover:border-orange-400 transition-colors"
                )
            ),
            
            FormSectionDiv(
                DivLAligned(
                    FormLabel("Content Source (Optional)"),
                    BrainIcon("Reference content to extract insights from")
                ),
                TextArea(placeholder="Paste existing content or competitor insights here...", rows=4, id="content-source")
            )
        )
    
    return Container(
        CampaignSteps(2),
        
        main_inputs,
        settings_card,
        
        DivFullySpaced(
            A(Button("← Back", cls=ButtonT.ghost), href=f"/campaign/step1"),
            A(Button("Start AI Analysis →", 
                   cls=ButtonT.primary + " px-8"),
              href="/campaign/step3")
        ),
        
        cls="max-w-4xl mx-auto space-y-6"
    )

# Step 3: AI Analysis Results (Gate #1)
def step3_analysis():
    return Container(
        LoadingOverlay(),
        CampaignSteps(3),
        
        Card(
            H2("AI Analysis Complete"),
            P("Review the research findings and confirm your preferences", cls=TextPresets.muted_sm)
        ),
        
        Grid(
            # SERP Analysis
            Card(
                DivLAligned(
                    H3("SERP Analysis"),
                    BrainIcon("Top competitors found in Google search results")
                ),
                
                Div(
                    H4("Top Competitors Found", cls="mb-3"),
                    *[
                        Div(
                            DivFullySpaced(
                                Div(
                                    Strong(f"{i+1}. {comp['title']}"),
                                    P(comp['url'], cls=TextPresets.muted_sm)
                                ),
                                Button("Remove", cls=ButtonT.ghost + " text-sm")
                            ),
                            cls="border-b pb-2 mb-2"
                        ) 
                        for i, comp in enumerate([
                            {"title": "KVK - Bedrijfsaansprakelijkheidsverzekering", "url": "kvk.nl/verzekeringen/..."},
                            {"title": "Zilveren Kruis - AVB Zakelijk", "url": "zilverenkruis.nl/zakelijk/..."},
                            {"title": "Nationale Nederlanden - Aansprakelijkheidsverzekering", "url": "nn.nl/zakelijk/..."}
                        ])
                    ],
                    Button("+ Add Competitor", cls=ButtonT.default + " mt-2")
                )
            ),
            
            # Intent & Page Type
            Card(
                DivLAligned(
                    H3("Page Recommendations"),
                    BrainIcon("Analyzed from search intent and competitor patterns")
                ),
                
                FormSectionDiv(
                    FormLabel("Funnel Stage"),
                    Select(
                        Option("Think - Consideration", selected=True),
                        Option("See - Awareness"),
                        Option("Do - Decision"),
                        Option("Care - Retention"),
                        id="funnel-stage"
                    )
                ),
                
                FormSectionDiv(
                    FormLabel("Page Type"), 
                    Select(
                        Option("Product Page", selected=True),
                        Option("Content Page"),
                        Option("Blog Article"),
                        id="page-type"
                    )
                )
            ),
            cols=2, gap=6
        ),
        
        # Keyword Expansion
        Card(
            DivLAligned(
                H3("Keyword Expansion"),
                BrainIcon("Additional keywords found through SEMrush analysis")
            ),
            
            Grid(
                Div(
                    H4("Focus Keyword", cls="mb-2"),
                    P("bedrijfsaansprakelijkheidsverzekering", cls="font-mono bg-orange-50 p-2 rounded"),
                    P("2,540 monthly searches", cls=TextPresets.muted_sm)
                ),
                
                Div(
                    H4("Secondary Keywords", cls="mb-2"),
                    *[
                        DivFullySpaced(
                            Span(kw['term'], cls="font-mono text-sm"),
                            Span(f"{kw['vol']}/mo", cls=TextPresets.muted_sm)
                        )
                        for kw in [
                            {"term": "avb", "vol": "2,200"},
                            {"term": "aansprakelijkheidsverzekering voor bedrijven", "vol": "100"},
                            {"term": "aansprakelijkheid bedrijven", "vol": "60"},
                            {"term": "werkgeversaansprakelijkheidsverzekering", "vol": "60"}
                        ]
                    ]
                ),
                cols=2, gap=6
            )
        ),
        
        DivFullySpaced(
            A(Button("← Back to Setup", cls=ButtonT.ghost), href="/campaign/step2"),
            Button("Generate Brief →", 
                   cls=ButtonT.primary + " px-8",
                   onclick="startBriefGeneration()")
        ),
        
        cls="max-w-6xl mx-auto space-y-6"
    )

# Step 4: Brief Review & Edit (Collapsible Cards)
def step4_brief_edit():
    return Container(
        CampaignSteps(4),
        
        DivFullySpaced(
            Div(
                H2("Content Brief Generated"),
                P("Review and edit your AI-generated brief", cls=TextPresets.muted_sm)
            )
        ),
        
        # Collapsible sections using Accordion
        Accordion(
            # Basic Information
            AccordionItem(
                "Basic Information & Strategy",
                Grid(
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Suggested URL"),
                            BrainIcon("SEO-optimized URL structure recommendation")
                        ),
                        Input(value="https://www.ing.nl/zakelijk/verzekeringen/bedrijfsaansprakelijkheid", id="url-suggestion")
                    ),
                    
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Page Type"),
                            BrainIcon("Recommended based on search intent analysis")
                        ),
                        Select(
                            Option("Product Page", selected=True),
                            Option("Content Page"),
                            Option("Landing Page"),
                            id="page-type-final"
                        )
                    ),
                    
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Funnel Stage"),
                            BrainIcon("Customer journey phase this content addresses")
                        ),
                        Select(
                            Option("Think - Consideration", selected=True),
                            Option("See - Awareness"),
                            Option("Do - Decision"),
                            Option("Care - Retention"),
                            id="funnel-final"
                        )
                    ),
                    
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Target Audience"),
                            BrainIcon("Primary audience identified from keyword analysis")
                        ),
                        Input(value="MKB ondernemers, ZZP'ers", id="target-audience")
                    ),
                    cols=2, gap=4
                )
            ),
            
            # SEO Elements
            AccordionItem(
                "SEO Elements",
                Grid(
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Page Title (60 chars max)"),
                            BrainIcon("Optimized for click-through rate and keyword relevance")
                        ),
                        Input(value="Bedrijfsaansprakelijkheidsverzekering | ING Zakelijk", id="page-title"),
                        P("48/60 characters", cls="text-green-600 text-sm")
                    ),
                    
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Meta Description (155 chars max)"),
                            BrainIcon("Compelling snippet to improve search click-through rates")
                        ),
                        TextArea(
                            "Bescherm je bedrijf met bedrijfsaansprakelijkheidsverzekering van ING. Vergelijk AVB opties en regel direct online. Ontdek jouw mogelijkheden.",
                            rows=3,
                            id="meta-description"
                        ),
                        P("148/155 characters", cls="text-green-600 text-sm")
                    ),
                    cols=2, gap=4
                ),
                
                FormSectionDiv(
                    DivLAligned(
                        FormLabel("Focus Keyword Density"),
                        BrainIcon("Recommended 3-5 natural mentions throughout content")
                    ),
                    P("bedrijfsaansprakelijkheidsverzekering", cls="font-mono bg-orange-50 p-2 rounded"),
                    P("Target: 3-5 mentions (currently 0)", cls=TextPresets.muted_sm)
                )
            ),
            
            # Content Structure
            AccordionItem(
                "Content Structure & Headers",
                FormSectionDiv(
                    DivLAligned(
                        FormLabel("H1 Heading"),
                        BrainIcon("Primary heading incorporating focus keyword")
                    ),
                    Input(value="Bedrijfsaansprakelijkheidsverzekering: Bescherm je bedrijf tegen claims", id="h1-heading")
                ),
                
                FormSectionDiv(
                    DivLAligned(
                        FormLabel("H2 Section Headers"),
                        BrainIcon("Main content sections based on user search intent")
                    ),
                    TextArea(
                        """Wat is een bedrijfsaansprakelijkheidsverzekering?
Waarom heb je een AVB nodig als ondernemer?
Wat dekt een bedrijfsaansprakelijkheidsverzekering?
Hoe kies je de juiste dekking voor jouw bedrijf?
ING AVB: jouw voordelen op een rij
Aanvragen in 3 eenvoudige stappen""",
                        rows=6,
                        id="h2-headers"
                    )
                ),
                
                FormSectionDiv(
                    DivLAligned(
                        FormLabel("Content Guidelines"),
                        BrainIcon("Writing instructions following ING tone of voice")
                    ),
                    TextArea(
                        """Schrijf persoonlijk en begrijpelijk. Gebruik 'je'-vorm en vermijd jargon.

Focus keyword 'bedrijfsaansprakelijkheidsverzekering' minimaal 3x natuurlijk verwerken.
Secundaire keywords: avb, aansprakelijkheid bedrijven, werkgeversaansprakelijkheid.

Structuur per sectie:
- Duidelijke koppen met keywords
- Korte alinea's (max 4 regels)
- Praktische voorbeelden voor MKB
- Call-to-action per sectie""",
                        rows=8,
                        id="content-guidelines"
                    )
                )
            ),
            
            # Competitor Insights
            AccordionItem(
                "Competitor Analysis & Opportunities",
                Grid(
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Content Gaps"),
                            BrainIcon("Opportunities where competitors are weak")
                        ),
                        TextArea(
                            """Concurrenten missen:
- Specifieke voorbeelden voor verschillende sectoren
- Kostenrekentool of premium calculator  
- Video uitleg van complexe verzekeringssituaties
- Vergelijkingstabel met andere verzekeringen""",
                            rows=4,
                            id="content-gaps"
                        )
                    ),
                    
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Differentiation Strategy"),
                            BrainIcon("How to stand out from competitor content")
                        ),
                        TextArea(
                            """ING differentiatie:
- Focus op digitale ondernemers en moderne werkvormen
- Integratie met zakelijke bankproducten
- Persoonlijke adviseur via video call
- Snelle online afhandeling (24u)""",
                            rows=4,
                            id="differentiation"
                        )
                    ),
                    cols=2, gap=4
                )
            ),
            
            # FAQ & Internal Links
            AccordionItem(
                "FAQ & Internal Linking",
                Grid(
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("FAQ from PAA"),
                            BrainIcon("Questions extracted from Google's People Also Ask")
                        ),
                        TextArea(
                            """Wat kost een bedrijfsaansprakelijkheidsverzekering?
Hoe hoog moet mijn AVB dekking zijn?
Kan ik mijn AVB tussentijds opzeggen?
Wat is het verschil tussen AVB en beroepsaansprakelijkheid?
Dekt AVB ook schade aan eigen personeel?
Welke bedrijven hebben een AVB verplicht?""",
                            rows=6,
                            id="faq-questions"
                        )
                    ),
                    
                    FormSectionDiv(
                        DivLAligned(
                            FormLabel("Internal Links"),
                            BrainIcon("Relevant ING pages to link to for SEO and user journey")
                        ),
                        TextArea(
                            """/zakelijk/verzekeringen → Overzicht zakelijke verzekeringen
/zakelijk/rekening → Zakelijke rekening openen
/zakelijk/lenen → Zakelijke financiering
/zakelijk/adviseurs → Persoonlijk advies""",
                            rows=4,
                            id="internal-links"
                        )
                    ),
                    cols=2, gap=4
                )
            )
        ),
        
        # Action buttons
        DivFullySpaced(
            A(Button("← Back to Analysis", cls=ButtonT.ghost), href="/campaign/step3"),
            DivLAligned(
                Button("Save Draft", cls=ButtonT.default),
                A(Button("Export & Finish →", cls=ButtonT.primary), href="/campaign/step5")
            )
        ),
        
        cls="max-w-6xl mx-auto space-y-6"
    )

# Step 5: Export Complete
def step5_complete():
    return Container(
        CampaignSteps(5),
        
        DivCentered(
            Card(
                DivCentered(
                    UkIcon("check-circle", height=64, width=64, cls="text-green-500 mb-4"),
                    H2("Brief Generated Successfully!"),
                    P("Your content brief has been created and exported", cls=TextPresets.muted_sm),
                ),
                
                Div(
                    H3("Export Details"),
                    *[
                        DivFullySpaced(
                            P(label, cls="font-medium"),
                            P(value, cls=TextPresets.muted_sm)
                        )
                        for label, value in [
                            ("File Name:", "ZakelijkeVerzekeringen_bedrijfsaansprakelijkheid_20241201.docx"),
                            ("SharePoint Folder:", "/Zakelijke Verzekeringen/Content Briefs/2024"),
                            ("Keywords:", "bedrijfsaansprakelijkheidsverzekering + 8 secondary"),
                            ("Generated:", "December 1, 2024 - 14:32")
                        ]
                    ],
                    cls="space-y-2 mt-6"
                ),
                
                DivCentered(
                    DivLAligned(
                        Button("Download Brief", cls=ButtonT.primary),
                        Button("View in SharePoint", cls=ButtonT.default),
                        A(Button("Create Another", cls=ButtonT.ghost), href="/campaign/new")
                    ),
                    cls="mt-6"
                ),
                
                cls="p-8 max-w-md"
            )
        )
    )

@rt
def index():
    """Dashboard - Landing page"""
    return (
        AppHeader(),
        Container(
            DivFullySpaced(
                Div(
                    H1("SEO Performance Dashboard"),
                    P("Track keyword performance and content opportunities", cls=TextPresets.muted_lg)
                ),
                A(Button("New Campaign", cls=ButtonT.primary), href="/campaign/new")
            ),
            
            Grid(
                Card(
                    CardBody(keyword_yoy_chart()),
                    header=H3("Keyword Trend Analysis")
                ),
                Card(
                    H3("Key Insights"),
                    Ul(cls="space-y-3")(
                        Li(Strong("Top keyword: "), "bedrijfsaansprakelijkheidsverzekering (2,540 searches/month)"),
                        Li(Strong("YoY Growth: "), "↑ 12.4% increase vs 2023"),
                        Li(Strong("Second highest: "), "avb (2,200 searches) - abbreviated form"),
                        Li(Strong("Long-tail opportunity: "), "Several keywords with 60+ monthly searches"),
                        Li(Strong("Total monthly volume: "), "8,180 searches across all tracked keywords"),
                        Li(Strong("Best performing month: "), "November 2024 (3,100 searches)")
                    ),
                    cls="mt-6"
                ),
                cols=2, gap=6, cls="w-full"
            ),
            
            Grid(
                Card(
                    H4("2,540"),
                    P("Monthly searches", cls=TextPresets.muted_sm),
                    P("↑ 12.4% vs last year", cls="text-green-600 text-sm font-medium"),
                    header=H5("Focus Keyword Performance")
                ),
                Card(
                    H4("8,180"),
                    P("Total volume", cls=TextPresets.muted_sm),
                    P("↑ 8.7% vs last year", cls="text-green-600 text-sm font-medium"),
                    header=H5("Portfolio Volume")
                ),
                Card(
                    H4("15"),
                    P("Tracked keywords", cls=TextPresets.muted_sm),
                    P("3 new opportunities", cls="text-blue-600 text-sm font-medium"),
                    header=H5("Keyword Portfolio")
                ),
                Card(
                    H4("68%"),
                    P("Search share", cls=TextPresets.muted_sm),
                    P("↑ 5% vs competition", cls="text-green-600 text-sm font-medium"),
                    header=H5("Market Share")
                ),
                cols=4, gap=4, cls="w-full mt-6"
            ),
            
            cls="space-y-6 max-w-7xl mx-auto"
        ),
        LoadingOverlay()
    )

# Campaign routes
@rt('/campaign/new')
def new_campaign():
    return AppHeader(), step1_mode_selection()

@rt('/campaign/step1')  
def campaign_step1():
    return AppHeader(), step1_mode_selection()

@rt('/campaign/step2')
def campaign_step2(mode: str = "optimize"):
    return AppHeader(), step2_research_setup(mode)

@rt('/campaign/step3')
def campaign_step3():
    return AppHeader(), step3_analysis()

@rt('/campaign/step4') 
def campaign_step4():
    return AppHeader(), step4_brief_edit()

@rt('/campaign/step5')
def campaign_step5():
    return AppHeader(), step5_complete()

@rt('/campaigns')
def campaigns_list():
    return (
        AppHeader(),
        Container(
            H1("My Campaigns"),
            Card(
                P("Campaign history and management coming soon...", cls=TextPresets.muted_lg)
            )
        )
    )

@rt('/settings')
def settings_page():
    return (
        AppHeader(),
        Container(
            H1("Settings"),
            Card(
                P("API settings, templates, and preferences coming soon...", cls=TextPresets.muted_lg)
            )
        )
    )

if __name__ == "__main__":
    # For direct execution - though uvicorn is preferred
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)