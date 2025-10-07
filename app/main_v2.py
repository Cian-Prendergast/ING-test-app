from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *
import os
from pathlib import Path
import uuid
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
APP_PASSWORD = os.getenv("APP_PASSWORD", "change-this-password-123")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-to-random-string-in-production")

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
session_key_path = "/tmp/.sesskey"

# Initialize app with session middleware
app, rt = fast_app(
    hdrs=Theme.orange.headers(mode='light', apex_charts=True, daisy=True),
    static_dir=static_dir,
    live=False,
    key_fname=session_key_path,
    middleware=[
        Middleware(SessionMiddleware, secret_key=SECRET_KEY)
    ]
)

# ===== AUTHENTICATION HELPERS =====

def is_authenticated(request):
    """Check if user is authenticated via session"""
    return request.session.get("authenticated", False)

def require_auth(func):
    """Decorator to require authentication for routes"""
    async def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'session'):
            return RedirectResponse('/login', status_code=302)
        
        if is_authenticated(request):
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            
            func_kwargs = {}
            if 'request' in params:
                func_kwargs['request'] = request
            
            for i, param_name in enumerate(params[1:], 1):
                if i <= len(args):
                    func_kwargs[param_name] = args[i-1]
            
            for key, value in kwargs.items():
                if key in params:
                    func_kwargs[key] = value
            
            return await func(**func_kwargs)
        
        return RedirectResponse('/login', status_code=302)
    return wrapper

def get_or_create_session_id(request):
    """Get existing session ID or create new one"""
    if not request.session.get("session_id"):
        request.session["session_id"] = str(uuid.uuid4())
    return request.session["session_id"]

def get_short_session_id(session_id):
    """Get shortened version of session ID for display"""
    return session_id[:8].upper()

def create_session_banner(session_id):
    """Create copyable session ID banner"""
    short_id = get_short_session_id(session_id)
    
    return Div(
        DivFullySpaced(
            Div(
                Strong("📋 Session ID: "),
                Code(short_id, cls="bg-orange-100 px-3 py-1 rounded font-mono"),
                cls="flex items-center gap-2"
            ),
            Button(
                "📋 Copy Full ID",
                cls=ButtonT.ghost + " text-sm",
                onclick=f"navigator.clipboard.writeText('{session_id}'); this.textContent='✅ Copied!'; setTimeout(() => this.textContent='📋 Copy Full ID', 2000);"
            )
        ),
        P("Save this ID to reference your session later", cls=TextPresets.muted_sm),
        cls="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6"
    )

# ===== VERIFICATION & LEGAL PAGES (NO AUTH REQUIRED) =====

@rt('/google52b7c19ec95a274e.html')
def google_verification():
    """Serve Google verification file"""
    verification_file = Path('google52b7c19ec95a274e.html')
    if verification_file.exists():
        return open(verification_file, 'r').read()
    return "google-site-verification: google52b7c19ec95a274e.html"

@rt('/privacy-policy')
def privacy_policy():
    """Privacy Policy page for OAuth consent"""
    return (
        Title("Privacy Policy - ING Content Studio"),
        Container(
            Card(
                H1("Privacy Policy"),
                P("Last updated: December 2024", cls=TextPresets.muted_sm),
                
                Div(
                    H2("Information We Collect"),
                    P("This application collects and processes the following information:"),
                    Ul(
                        Li("Account email address and basic profile information"),
                        Li("Campaign and content brief data you create within the application"),
                        Li("Usage data for improving the service")
                    ),
                    
                    H2("How We Use Your Information", cls="mt-6"),
                    P("We use the collected information to:"),
                    Ul(
                        Li("Authenticate your identity"),
                        Li("Provide SEO content brief generation services"),
                        Li("Store your campaign data securely"),
                        Li("Improve our services and user experience")
                    ),
                    
                    H2("Data Storage and Security", cls="mt-6"),
                    P("Your data is stored securely on Google Cloud Platform infrastructure. We implement appropriate technical and organizational measures to protect your personal information."),
                    
                    H2("Data Sharing", cls="mt-6"),
                    P("We do not sell or share your personal information with third parties except:"),
                    Ul(
                        Li("When required by law"),
                        Li("To protect our rights and safety"),
                        Li("With your explicit consent")
                    ),
                    
                    H2("Your Rights", cls="mt-6"),
                    P("You have the right to:"),
                    Ul(
                        Li("Access your personal data"),
                        Li("Request correction of your data"),
                        Li("Request deletion of your data"),
                        Li("Withdraw consent at any time")
                    ),
                    
                    H2("Contact Us", cls="mt-6"),
                    P("For privacy-related questions, contact the app admin at: cian.prendergast@deptagency.com"),
                    
                    cls="space-y-4"
                ),
                cls="prose max-w-4xl"
            ),
            A(Button("← Back to App", cls=ButtonT.primary), href="/")
        )
    )

@rt('/terms-of-service')
def terms_of_service():
    """Terms of Service page"""
    return (
        Title("Terms of Service - ING Content Studio"),
        Container(
            Card(
                H1("Terms of Service"),
                P("Last updated: December 2024", cls=TextPresets.muted_sm),
                
                Div(
                    H2("Acceptance of Terms"),
                    P("By accessing and using this service, you accept and agree to be bound by the terms and provision of this agreement."),
                    
                    H2("Use License", cls="mt-6"),
                    P("This application is provided for internal ING business use only. Unauthorized use is prohibited."),
                    
                    H2("Service Availability", cls="mt-6"),
                    P("We strive to provide reliable service but do not guarantee uninterrupted access. The service is provided 'as is' without warranties."),
                    
                    H2("User Responsibilities", cls="mt-6"),
                    P("You agree to:"),
                    Ul(
                        Li("Use the service in compliance with applicable laws"),
                        Li("Not misuse or attempt to compromise the service"),
                        Li("Keep your account credentials secure")
                    ),
                    
                    H2("Contact", cls="mt-6"),
                    P("For questions about these terms, contact: cian.prendergast@deptagency.com"),
                    
                    cls="space-y-4"
                ),
                cls="prose max-w-4xl"
            ),
            A(Button("← Back to App", cls=ButtonT.primary), href="/")
        )
    )

# ===== LOGIN/LOGOUT ROUTES =====

@rt("/login")
async def get(request):
    """Display login form"""
    if is_authenticated(request):
        return RedirectResponse('/', status_code=302)
    
    error_msg = request.query_params.get("error")
    
    return (
        Title("Login - ING Content Studio"),
        Container(
            DivCentered(
                Card(
                    DivCentered(
                        Img(src='/static/logo.png', height=80, width=80, cls="mb-4"),
                        H2("ING Content Studio"),
                        P("SEO Brief Generator", cls=TextPresets.muted_lg + " mb-6")
                    ),
                    
                    Form(
                        FormSectionDiv(
                            Input(
                                type="password",
                                name="password",
                                placeholder="Enter password",
                                cls="w-full",
                                required=True,
                                autofocus=True
                            )
                        ),
                        Button(
                            "🔓 Login",
                            type="submit",
                            cls=ButtonT.primary + " w-full"
                        ),
                        method="post",
                        action="/login"
                    ),
                    
                    Alert(
                        "❌ Incorrect password. Please try again.",
                        cls=AlertT.error + " mt-4"
                    ) if error_msg else "",
                    
                    Div(
                        P("Need help? Contact: ", A("cian.prendergast@deptagency.com", href="mailto:cian.prendergast@deptagency.com")),
                        cls=TextPresets.muted_sm + " text-center mt-4"
                    ),
                    
                    cls="max-w-md p-8"
                ),
                cls="min-h-screen"
            )
        )
    )

@rt("/login")
async def post(request, password: str):
    """Handle login form submission"""
    if password == APP_PASSWORD:
        request.session["authenticated"] = True
        print(f"✅ User authenticated successfully")
        return RedirectResponse('/', status_code=302)
    else:
        print(f"❌ Failed login attempt")
        return RedirectResponse('/login?error=1', status_code=302)

@rt("/logout")
async def get(request):
    """Handle logout"""
    request.session.clear()
    print("🚪 User logged out")
    return RedirectResponse('/login', status_code=302)

# ===== UI COMPONENTS =====

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
        A("Privacy", href='/privacy-policy', cls="text-white hover:text-orange-200 text-sm"),  
        A("Terms", href='/terms-of-service', cls="text-white hover:text-orange-200 text-sm"),
        A(
            Button("🚪 Logout", cls=ButtonT.ghost + " text-white hover:text-orange-200"),
            href='/logout'
        ),

        brand=DivLAligned(
            Img(src='/static/logo.png', height=60, width=60),
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

# ===== CAMPAIGN STEP FUNCTIONS =====

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

def step3_analysis():
    return Container(
        LoadingOverlay(),
        CampaignSteps(3),
        
        Card(
            H2("AI Analysis Complete"),
            P("Review the research findings and confirm your preferences", cls=TextPresets.muted_sm)
        ),
        
        Grid(
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

def step4_brief_edit():
    return Container(
        CampaignSteps(4),
        
        DivFullySpaced(
            Div(
                H2("Content Brief Generated"),
                P("Review and edit your AI-generated brief", cls=TextPresets.muted_sm)
            )
        ),
        
        Accordion(
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
        
        DivFullySpaced(
            A(Button("← Back to Analysis", cls=ButtonT.ghost), href="/campaign/step3"),
            DivLAligned(
                Button("Save Draft", cls=ButtonT.default),
                A(Button("Export & Finish →", cls=ButtonT.primary), href="/campaign/step5")
            )
        ),
        
        cls="max-w-6xl mx-auto space-y-6"
    )

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

# ===== PROTECTED ROUTES =====

@rt("/")
@require_auth
async def get(request):
    """Dashboard - Landing page (protected)"""
    session_id = get_or_create_session_id(request)
    
    return (
        AppHeader(),
        Container(
            create_session_banner(session_id),
            
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

@rt('/campaign/new')
@require_auth
async def get(request):
    return AppHeader(), step1_mode_selection()

@rt('/campaign/step1')
@require_auth  
async def get(request):
    return AppHeader(), step1_mode_selection()

@rt('/campaign/step2')
@require_auth
async def get(request, mode: str = "optimize"):
    return AppHeader(), step2_research_setup(mode)

@rt('/campaign/step3')
@require_auth
async def get(request):
    return AppHeader(), step3_analysis()

@rt('/campaign/step4')
@require_auth 
async def get(request):
    return AppHeader(), step4_brief_edit()

@rt('/campaign/step5')
@require_auth
async def get(request):
    return AppHeader(), step5_complete()

@rt('/campaigns')
@require_auth
async def get(request):
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
@require_auth
async def get(request):
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
