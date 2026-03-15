from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
import os

# ── Output folder ─────────────────────────────────────
OUTPUT_DIR = "documents"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Style Helper ──────────────────────────────────────
def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CompanyTitle",
        fontSize=24,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a237e"),
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name="DocTitle",
        fontSize=16,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#283593"),
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=13,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1565c0"),
        spaceBefore=16,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#212121"),
        spaceAfter=6,
        leading=16
    ))
    styles.add(ParagraphStyle(
        name="BulletText",
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#212121"),
        spaceAfter=4,
        leftIndent=20,
        leading=14
    ))
    return styles


# ── Table Style Helper ────────────────────────────────
def get_table_style():
    return TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),
         colors.HexColor("#1a237e")),
        ("TEXTCOLOR",    (0, 0), (-1, 0),
         colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),
         "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 10),
        ("ALIGN",        (0, 0), (-1, -1),
         "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#e8eaf6"),
          colors.white]),
        ("GRID",         (0, 0), (-1, -1),
         0.5, colors.HexColor("#9fa8da")),
        ("FONTSIZE",     (0, 1), (-1, -1), 9),
        ("PADDING",      (0, 0), (-1, -1), 8),
    ])


# ── Document 1: Annual Report ─────────────────────────
def create_annual_report():
    doc = SimpleDocTemplate(
        f"{OUTPUT_DIR}/01_annual_report_2024.pdf",
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )
    styles = get_styles()
    story  = []

    # Header
    story.append(Paragraph("TechNova Solutions", styles["CompanyTitle"]))
    story.append(Paragraph("Annual Report 2024", styles["DocTitle"]))
    story.append(HRFlowable(width="100%", thickness=2,
                            color=colors.HexColor("#1a237e")))
    story.append(Spacer(1, 16))

    # Company Overview
    story.append(Paragraph("Company Overview", styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova Solutions is a leading technology products company headquartered
in Hyderabad, India. Founded in 2015, TechNova specializes in consumer
electronics including Laptops, Smartphones, Tablets, Headphones, and
Smartwatches. The company operates across four regions: North, South,
East, and West India, serving both retail and enterprise customers.
In 2024, TechNova employed 1,200 professionals across 8 office locations
and served over 10,000 enterprise customers nationwide.
    """, styles["BodyText2"]))

    # Financial Highlights
    story.append(Paragraph("Financial Highlights 2024",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova achieved record revenue of Rs. 508 Crores in FY2024, representing
a 23% year-over-year growth compared to Rs. 413 Crores in FY2023.
Net profit reached Rs. 76 Crores, up from Rs. 58 Crores in the previous
year, reflecting a healthy profit margin of 15%. EBITDA grew by 28% to
Rs. 102 Crores. The company maintained a strong cash position of
Rs. 45 Crores with zero long-term debt.
    """, styles["BodyText2"]))

    fin_data = [
        ["Metric", "FY2024", "FY2023", "Growth"],
        ["Total Revenue", "Rs. 508 Cr", "Rs. 413 Cr", "+23%"],
        ["Net Profit",    "Rs. 76 Cr",  "Rs. 58 Cr",  "+31%"],
        ["EBITDA",        "Rs. 102 Cr", "Rs. 80 Cr",  "+28%"],
        ["Cash Position", "Rs. 45 Cr",  "Rs. 32 Cr",  "+41%"],
        ["Employees",     "1,200",      "980",         "+22%"],
    ]
    t = Table(fin_data, colWidths=[2.2*inch]*4)
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Regional Performance
    story.append(Paragraph("Regional Performance",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
The West region emerged as the top performer in FY2024 with revenue of
Rs. 160 Crores, driven by strong enterprise demand in Mumbai and Pune.
The East region followed with Rs. 139 Crores, showing 31% growth
fueled by expansion in Kolkata and Bhubaneswar. North region contributed
Rs. 125 Crores while South region, despite being home to headquarters,
recorded Rs. 84 Crores due to increased competition in Bangalore market.
    """, styles["BodyText2"]))

    reg_data = [
        ["Region", "Revenue FY2024", "Revenue FY2023", "Growth"],
        ["West",   "Rs. 160 Cr",     "Rs. 118 Cr",     "+36%"],
        ["East",   "Rs. 139 Cr",     "Rs. 106 Cr",     "+31%"],
        ["North",  "Rs. 125 Cr",     "Rs. 104 Cr",     "+20%"],
        ["South",  "Rs. 84 Cr",      "Rs. 85 Cr",      "-1%"],
    ]
    t = Table(reg_data, colWidths=[2.2*inch]*4)
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Product Performance
    story.append(Paragraph("Product Line Performance",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
Laptops remained the highest revenue generating product category
contributing 38% of total revenue at Rs. 193 Crores, driven by
enterprise bulk purchases and work-from-home demand. Smartphones
contributed 24% at Rs. 122 Crores showing strong retail growth.
Tablets grew 45% YoY to Rs. 91 Crores as education sector adoption
increased significantly. Headphones and Smartwatches combined
contributed Rs. 102 Crores representing the fastest growing
accessories segment at 52% YoY growth.
    """, styles["BodyText2"]))

    prod_data = [
        ["Product",      "Revenue",     "% Share", "YoY Growth"],
        ["Laptop",       "Rs. 193 Cr",  "38%",     "+18%"],
        ["Smartphone",   "Rs. 122 Cr",  "24%",     "+21%"],
        ["Tablet",       "Rs. 91 Cr",   "18%",     "+45%"],
        ["Headphones",   "Rs. 61 Cr",   "12%",     "+48%"],
        ["Smartwatch",   "Rs. 41 Cr",   "8%",      "+58%"],
    ]
    t = Table(prod_data, colWidths=[2.2*inch]*4)
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Future Outlook
    story.append(Paragraph("Future Outlook 2025",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova targets revenue of Rs. 650 Crores in FY2025, representing
28% growth. Key strategic initiatives include:
    """, styles["BodyText2"]))

    bullets = [
        "Launch of TechNova AI-powered Laptop series in Q1 2025",
        "Expansion into Tier-2 cities across all four regions",
        "New enterprise partnership program targeting 500 new accounts",
        "Investment of Rs. 25 Crores in R&D for next generation products",
        "International expansion to Southeast Asian markets by Q3 2025",
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", styles["BulletText"]))

    doc.build(story)
    print("✅ Created: 01_annual_report_2024.pdf")


# ── Document 2: HR Policy ─────────────────────────────
def create_hr_policy():
    doc = SimpleDocTemplate(
        f"{OUTPUT_DIR}/02_hr_policy_2024.pdf",
        pagesize=letter,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch,   bottomMargin=inch
    )
    styles = get_styles()
    story  = []

    story.append(Paragraph("TechNova Solutions",
                            styles["CompanyTitle"]))
    story.append(Paragraph("HR Policy Document 2024",
                            styles["DocTitle"]))
    story.append(HRFlowable(width="100%", thickness=2,
                            color=colors.HexColor("#1a237e")))
    story.append(Spacer(1, 16))

    # Leave Policy
    story.append(Paragraph("Leave Policy", styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova provides comprehensive leave benefits to all full-time employees.
The leave year runs from January 1st to December 31st. All leaves must
be applied through the HR portal with minimum 2 days advance notice
except for sick leave.
    """, styles["BodyText2"]))

    leave_data = [
        ["Leave Type",       "Days/Year", "Carry Forward", "Encashment"],
        ["Annual Leave",     "18 days",   "Max 9 days",    "Yes"],
        ["Sick Leave",       "12 days",   "No",            "No"],
        ["Casual Leave",     "6 days",    "No",            "No"],
        ["Maternity Leave",  "180 days",  "N/A",           "No"],
        ["Paternity Leave",  "15 days",   "No",            "No"],
        ["Marriage Leave",   "5 days",    "No",            "No"],
        ["Bereavement Leave","3 days",    "No",            "No"],
    ]
    t = Table(leave_data, colWidths=[2*inch, 1.2*inch, 1.5*inch, 1.5*inch])
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # WFH Policy
    story.append(Paragraph("Work From Home Policy",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova follows a hybrid work model effective from January 2024.
Employees are required to work from office minimum 3 days per week
(Tuesday, Wednesday, Thursday mandatory). Monday and Friday are
flexible WFH days. Employees must be available on calls and respond
to messages within 2 hours during WFH days. WFH is not applicable
during probation period of 6 months.
    """, styles["BodyText2"]))

    wfh_data = [
        ["Day",       "Policy",           "Notes"],
        ["Monday",    "WFH Flexible",     "Optional office"],
        ["Tuesday",   "Mandatory Office", "No exceptions"],
        ["Wednesday", "Mandatory Office", "No exceptions"],
        ["Thursday",  "Mandatory Office", "No exceptions"],
        ["Friday",    "WFH Flexible",     "Optional office"],
    ]
    t = Table(wfh_data, colWidths=[1.5*inch, 2*inch, 2.7*inch])
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Performance Review
    story.append(Paragraph("Performance Review Process",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova conducts bi-annual performance reviews in June and December.
The performance rating system uses a 5-point scale:
5 - Exceptional, 4 - Exceeds Expectations, 3 - Meets Expectations,
2 - Needs Improvement, 1 - Unsatisfactory.
Employees rated 4 or above are eligible for fast-track promotion.
Employees rated 2 or below for two consecutive reviews are placed
on a Performance Improvement Plan (PIP) for 90 days.
    """, styles["BodyText2"]))

    # Salary Increment
    story.append(Paragraph("Salary Increment Policy",
                            styles["SectionHeader"]))
    increment_data = [
        ["Performance Rating", "Increment Range", "Bonus"],
        ["5 - Exceptional",    "18% - 25%",       "20% of CTC"],
        ["4 - Exceeds Exp.",   "12% - 18%",       "12% of CTC"],
        ["3 - Meets Exp.",     "7% - 12%",        "5% of CTC"],
        ["2 - Needs Imp.",     "0% - 5%",         "No Bonus"],
        ["1 - Unsatisfactory", "0%",               "No Bonus"],
    ]
    t = Table(increment_data,
              colWidths=[2.2*inch, 1.8*inch, 2.2*inch])
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Benefits
    story.append(Paragraph("Employee Benefits",
                            styles["SectionHeader"]))
    benefits = [
        "Health Insurance: Rs. 5 Lakhs coverage for employee and family",
        "Term Life Insurance: 3x annual CTC coverage",
        "Provident Fund: 12% employer contribution",
        "Gratuity: As per Payment of Gratuity Act",
        "Internet Allowance: Rs. 1,500 per month for WFH days",
        "Learning Budget: Rs. 25,000 per year for courses and certifications",
        "Meal Card: Rs. 2,200 per month loaded on Sodexo card",
        "Cab Facility: Available for office shifts beyond 8 PM",
    ]
    for b in benefits:
        story.append(Paragraph(f"• {b}", styles["BulletText"]))

    doc.build(story)
    print("✅ Created: 02_hr_policy_2024.pdf")


# ── Document 3: Market Research ───────────────────────
def create_market_research():
    doc = SimpleDocTemplate(
        f"{OUTPUT_DIR}/03_market_research_2024.pdf",
        pagesize=letter,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch,   bottomMargin=inch
    )
    styles = get_styles()
    story  = []

    story.append(Paragraph("TechNova Solutions",
                            styles["CompanyTitle"]))
    story.append(Paragraph("Market Research Report 2024",
                            styles["DocTitle"]))
    story.append(HRFlowable(width="100%", thickness=2,
                            color=colors.HexColor("#1a237e")))
    story.append(Spacer(1, 16))

    # Market Overview
    story.append(Paragraph("Industry Market Overview",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
The Indian consumer electronics market reached Rs. 4,200 Crores in 2024,
growing at 18% CAGR. The market is expected to reach Rs. 8,500 Crores
by 2028. Key growth drivers include increasing digitization, government
initiatives like Digital India, rising disposable income in Tier-2 cities,
and rapid adoption of remote work culture post-pandemic. TechNova holds
a 12.1% market share, making it the third largest player in the industry.
    """, styles["BodyText2"]))

    # Competitor Analysis
    story.append(Paragraph("Competitor Analysis",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova operates in a competitive landscape dominated by global and
domestic players. Key competitors include DigiMax (market leader with
18% share), ByteForce (second at 15% share), and several international
brands. TechNova differentiates through superior after-sales service,
competitive pricing, and strong enterprise relationships.
    """, styles["BodyText2"]))

    comp_data = [
        ["Company",    "Market Share", "Revenue",      "Strength"],
        ["DigiMax",    "18%",          "Rs. 756 Cr",   "Brand recall"],
        ["ByteForce",  "15%",          "Rs. 630 Cr",   "Price leader"],
        ["TechNova",   "12.1%",        "Rs. 508 Cr",   "Enterprise"],
        ["GlobalTech", "10%",          "Rs. 420 Cr",   "Innovation"],
        ["Others",     "44.9%",        "Rs. 1,886 Cr", "Regional"],
    ]
    t = Table(comp_data,
              colWidths=[1.5*inch, 1.3*inch, 1.5*inch, 2*inch])
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Market Trends
    story.append(Paragraph("Key Market Trends 2024-2025",
                            styles["SectionHeader"]))
    trends = [
        "AI Integration: 67% of enterprise buyers prefer AI-enabled devices",
        "Tier-2 Expansion: 45% of new demand coming from non-metro cities",
        "Subscription Model: SaaS-style hardware subscriptions growing 78%",
        "Sustainability: 52% of buyers consider eco-friendly manufacturing",
        "5G Adoption: Smartphone upgrade cycle accelerating due to 5G rollout",
        "Work From Home: Sustained demand for home office equipment",
    ]
    for t in trends:
        story.append(Paragraph(f"• {t}", styles["BulletText"]))
    story.append(Spacer(1, 8))

    # Customer Segments
    story.append(Paragraph("Customer Segments",
                            styles["SectionHeader"]))
    seg_data = [
        ["Segment",    "% Revenue", "Growth", "Key Products"],
        ["Enterprise", "58%",       "+28%",   "Laptop, Tablet"],
        ["SMB",        "24%",       "+19%",   "All products"],
        ["Retail",     "18%",       "+15%",   "Phone, Headphones"],
    ]
    t = Table(seg_data, colWidths=[1.5*inch, 1.3*inch, 1.2*inch, 2.2*inch])
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Risks
    story.append(Paragraph("Key Risks and Challenges",
                            styles["SectionHeader"]))
    risks = [
        "Supply Chain: Global chip shortage impacting product availability",
        "Competition: Aggressive pricing by Chinese OEM brands",
        "Currency Risk: INR depreciation increasing import costs by 8%",
        "Talent: High attrition (22%) in engineering and sales teams",
        "Regulation: New BIS certification requirements adding compliance cost",
        "Economic: Slowdown in IT sector affecting enterprise spending",
    ]
    for r in risks:
        story.append(Paragraph(f"• {r}", styles["BulletText"]))

    doc.build(story)
    print("✅ Created: 03_market_research_2024.pdf")


# ── Document 4: Product Catalog ───────────────────────
def create_product_catalog():
    doc = SimpleDocTemplate(
        f"{OUTPUT_DIR}/04_product_catalog_2024.pdf",
        pagesize=letter,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch,   bottomMargin=inch
    )
    styles = get_styles()
    story  = []

    story.append(Paragraph("TechNova Solutions",
                            styles["CompanyTitle"]))
    story.append(Paragraph("Product Catalog 2024",
                            styles["DocTitle"]))
    story.append(HRFlowable(width="100%", thickness=2,
                            color=colors.HexColor("#1a237e")))
    story.append(Spacer(1, 16))

    # Laptop
    story.append(Paragraph("1. TechNova Laptop Series",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova offers three laptop tiers targeting different customer segments.
The ProBook series targets enterprise customers with high performance
specs, the WorkBook series targets SMB customers with balanced
performance, and the EduBook series targets education sector with
affordable pricing. Total laptop sales in 2024 were 19,350 units.
    """, styles["BodyText2"]))

    lap_data = [
        ["Model",     "Price",        "Target",    "Units Sold"],
        ["ProBook X1","Rs. 85,000",   "Enterprise","6,200"],
        ["WorkBook S3","Rs. 65,000",  "SMB",       "8,750"],
        ["EduBook E1", "Rs. 35,000",  "Education", "4,400"],
    ]
    t = Table(lap_data, colWidths=[1.8*inch]*4)
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Smartphone
    story.append(Paragraph("2. TechNova Smartphone Series",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova smartphones focus on the mid-premium segment with strong
camera capabilities and long battery life. The Nova X series targets
premium users while Nova Y series targets mass market. 5G enabled
models launched in Q2 2024 received exceptional market response
with 15,000 units sold in first month alone.
    """, styles["BodyText2"]))

    phone_data = [
        ["Model",    "Price",       "Key Feature",   "Units Sold"],
        ["Nova X5",  "Rs. 45,000",  "108MP Camera",  "12,400"],
        ["Nova Y3",  "Rs. 22,000",  "5G + 6000mAh",  "28,600"],
        ["Nova Y1",  "Rs. 12,000",  "Budget 5G",     "18,200"],
    ]
    t = Table(phone_data, colWidths=[1.5*inch, 1.5*inch, 2*inch, 1.3*inch])
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Tablet
    story.append(Paragraph("3. TechNova Tablet Series",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
Tablets emerged as the fastest growing product category in 2024 with
45% YoY growth. Education sector drove 60% of tablet sales following
government digital education initiatives. Enterprise segment adopted
tablets for field sales and inventory management use cases.
    """, styles["BodyText2"]))

    tab_data = [
        ["Model",      "Price",      "Target",    "Units Sold"],
        ["TabPro T10", "Rs. 35,000", "Enterprise","8,400"],
        ["TabEdu E8",  "Rs. 18,000", "Education", "22,600"],
        ["TabHome H7", "Rs. 25,000", "Consumer",  "7,200"],
    ]
    t = Table(tab_data, colWidths=[1.8*inch]*4)
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Accessories
    story.append(Paragraph("4. Accessories — Headphones and Smartwatches",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
Accessories segment showed strongest growth at 52% YoY in 2024.
TechNova BeatPro headphones won Best Audio Product award at
India Tech Awards 2024. SmartWatch series expanded to 3 models
targeting fitness, professional, and fashion segments.
    """, styles["BodyText2"]))

    acc_data = [
        ["Product",        "Price",      "Category",   "Units Sold"],
        ["BeatPro H1",     "Rs. 8,500",  "Headphones", "42,000"],
        ["BeatBasic H2",   "Rs. 2,500",  "Headphones", "85,000"],
        ["WatchPro W1",    "Rs. 18,000", "Smartwatch", "18,500"],
        ["WatchFit W2",    "Rs. 8,000",  "Smartwatch", "32,000"],
        ["WatchStyle W3",  "Rs. 12,000", "Smartwatch", "14,200"],
    ]
    t = Table(acc_data,
              colWidths=[1.8*inch, 1.3*inch, 1.4*inch, 1.3*inch])
    t.setStyle(get_table_style())
    story.append(t)
    story.append(Spacer(1, 12))

    # Pricing Summary
    story.append(Paragraph("Pricing Strategy",
                            styles["SectionHeader"]))
    story.append(Paragraph("""
TechNova follows a value-based pricing strategy ensuring products
are priced 10-15% below global brands while maintaining 5-8% premium
over domestic competitors. Enterprise customers receive volume discounts
of 8-20% based on order quantity. Channel partners receive margin of
12-18% depending on product category and quarterly targets.
    """, styles["BodyText2"]))

    doc.build(story)
    print("✅ Created: 04_product_catalog_2024.pdf")


# ── Main ──────────────────────────────────────────────
if __name__ == "__main__":
    print("🔄 Generating TechNova documents...")
    print()

    create_annual_report()
    create_hr_policy()
    create_market_research()
    create_product_catalog()

    print()
    print("✅ All 4 documents created in documents/ folder!")
    print()

    # Verify files
    files = os.listdir(OUTPUT_DIR)
    for f in files:
        size = os.path.getsize(f"{OUTPUT_DIR}/{f}")
        print(f"   📄 {f} ({size/1024:.1f} KB)")