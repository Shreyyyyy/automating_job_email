"""
Generate a sample CV PDF for demonstration purposes.
This creates a simple but professional-looking CV.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

def create_sample_cv(output_path: str = "cv.pdf"):
    """Create a sample CV PDF."""
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=5,
        backColor=colors.HexColor('#ecf0f1')
    )
    
    # Header
    elements.append(Paragraph("JOHN DOE", title_style))
    elements.append(Paragraph("Software Engineer | Full-Stack Developer", subtitle_style))
    elements.append(Paragraph("📧 john.doe@email.com | 📱 +1-234-567-8900 | 🔗 linkedin.com/in/johndoe", 
                             styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Professional Summary
    elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    elements.append(Paragraph(
        "Experienced software engineer with 5+ years of expertise in full-stack development, "
        "cloud architecture, and agile methodologies. Proven track record of delivering "
        "scalable solutions and leading cross-functional teams. Passionate about clean code, "
        "user experience, and continuous learning.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Technical Skills
    elements.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills_data = [
        ["Languages:", "Python, JavaScript, TypeScript, Java, Go"],
        ["Frontend:", "React, Next.js, Vue.js, HTML5, CSS3, Tailwind"],
        ["Backend:", "Node.js, Django, FastAPI, Express, Spring Boot"],
        ["Database:", "PostgreSQL, MongoDB, Redis, MySQL"],
        ["Cloud:", "AWS, Google Cloud, Azure, Docker, Kubernetes"],
        ["Tools:", "Git, CI/CD, Jenkins, GitHub Actions, Terraform"]
    ]
    
    skills_table = Table(skills_data, colWidths=[1.2*inch, 5*inch])
    skills_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(skills_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Work Experience
    elements.append(Paragraph("WORK EXPERIENCE", heading_style))
    
    elements.append(Paragraph("<b>Senior Software Engineer</b> | Tech Corp Inc.", styles['Normal']))
    elements.append(Paragraph("<i>January 2021 - Present</i>", styles['Normal']))
    elements.append(Paragraph(
        "• Led development of microservices architecture serving 1M+ daily users<br/>"
        "• Reduced API response time by 60% through optimization and caching strategies<br/>"
        "• Mentored team of 5 junior developers and conducted code reviews<br/>"
        "• Implemented CI/CD pipeline reducing deployment time by 75%",
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("<b>Software Engineer</b> | StartUp Solutions", styles['Normal']))
    elements.append(Paragraph("<i>June 2019 - December 2020</i>", styles['Normal']))
    elements.append(Paragraph(
        "• Built full-stack web applications using React and Node.js<br/>"
        "• Designed and implemented RESTful APIs and database schemas<br/>"
        "• Collaborated with product team to define technical requirements<br/>"
        "• Achieved 95% test coverage through comprehensive unit and integration testing",
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Education
    elements.append(Paragraph("EDUCATION", heading_style))
    elements.append(Paragraph(
        "<b>Bachelor of Science in Computer Science</b><br/>"
        "University of Technology | Graduated: May 2019 | GPA: 3.8/4.0",
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Certifications
    elements.append(Paragraph("CERTIFICATIONS", heading_style))
    elements.append(Paragraph(
        "• AWS Certified Solutions Architect - Associate<br/>"
        "• Google Cloud Professional Developer<br/>"
        "• Certified Kubernetes Application Developer (CKAD)",
        styles['Normal']
    ))
    
    # Build PDF
    doc.build(elements)
    print(f"✓ Sample CV created: {output_path}")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cv_path = os.path.join(script_dir, "cv.pdf")
    
    create_sample_cv(cv_path)
