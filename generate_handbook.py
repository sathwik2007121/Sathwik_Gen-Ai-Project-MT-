"""
generate_handbook.py — Generate the full 50-page Mirai Academic & Hostel Handbook PDF.

This creates a comprehensive, realistic university handbook covering:
- Academic policies (attendance, grading, integrity, leaves)
- Hostel policies (fees, facilities, sports, Wi-Fi)
- Student clubs and activities

Run once: python generate_handbook.py
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    )
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
except ImportError:
    print("Installing reportlab...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "reportlab", "-q"])
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    )
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "mirai_academic_and_hostel_handbook_50p.pdf"

# ─── Styles ───────────────────────────────────────────────────────────────────

def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["title"] = ParagraphStyle(
        "title", parent=base["Title"],
        fontSize=22, leading=28, spaceAfter=16, alignment=TA_CENTER,
        textColor=colors.HexColor("#1a237e"),
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle", parent=base["Normal"],
        fontSize=13, leading=16, spaceAfter=8, alignment=TA_CENTER,
        textColor=colors.HexColor("#283593"),
    )
    styles["h1"] = ParagraphStyle(
        "h1", parent=base["Heading1"],
        fontSize=16, leading=20, spaceBefore=18, spaceAfter=10,
        textColor=colors.HexColor("#1a237e"), borderPad=4,
    )
    styles["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"],
        fontSize=13, leading=17, spaceBefore=12, spaceAfter=6,
        textColor=colors.HexColor("#283593"),
    )
    styles["h3"] = ParagraphStyle(
        "h3", parent=base["Heading3"],
        fontSize=11, leading=15, spaceBefore=8, spaceAfter=4,
        textColor=colors.HexColor("#37474f"),
    )
    styles["body"] = ParagraphStyle(
        "body", parent=base["BodyText"],
        fontSize=10, leading=14, spaceAfter=6, alignment=TA_JUSTIFY,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", parent=base["BodyText"],
        fontSize=10, leading=14, spaceAfter=4,
        leftIndent=16, bulletIndent=4,
    )
    styles["note"] = ParagraphStyle(
        "note", parent=base["BodyText"],
        fontSize=9, leading=13, spaceAfter=4,
        textColor=colors.HexColor("#555555"), leftIndent=12,
    )
    styles["center"] = ParagraphStyle(
        "center", parent=base["Normal"],
        fontSize=10, leading=14, alignment=TA_CENTER,
    )
    return styles

S = build_styles()

def p(text, style="body"):      return Paragraph(text, S[style])
def h1(text):                    return Paragraph(text, S["h1"])
def h2(text):                    return Paragraph(text, S["h2"])
def h3(text):                    return Paragraph(text, S["h3"])
def sp(n=8):                     return Spacer(1, n)
def pb():                        return PageBreak()

# ─── Content ──────────────────────────────────────────────────────────────────

def build_story():
    story = []

    # ── COVER PAGE ─────────────────────────────────────────────────────────────
    story += [
        sp(60), 
        p("🎓", "center"),
        p("MIRAI INSTITUTE OF TECHNOLOGY", "title"),
        p("Official Academic &amp; Hostel Policy Handbook", "subtitle"),
        p("Academic Year 2025 – 2026", "subtitle"),
        sp(20),
        p("Prepared by the Office of the Registrar &amp; Dean of Student Affairs", "center"),
        p("Version 3.2 | Effective: August 2025", "center"),
        sp(40),
        p(
            "This handbook is the authoritative reference for all academic regulations, "
            "hostel rules, facilities usage, and student activity guidelines at Mirai "
            "Institute of Technology. All students are expected to read this document "
            "in full and abide by the policies herein.",
            "note"
        ),
        pb(),
    ]

    # ── TABLE OF CONTENTS ──────────────────────────────────────────────────────
    story += [
        h1("Table of Contents"),
        sp(6),
    ]
    toc = [
        ("Section 1", "Academic Standing &amp; Grading System", "3"),
        ("Section 2", "Attendance &amp; Leave of Absence Policy", "6"),
        ("Section 3", "Academic Integrity &amp; Anti-Plagiarism Policy", "10"),
        ("Section 4", "Degree Requirements &amp; Tuition Fees", "13"),
        ("Section 5", "Examination Rules &amp; Procedures", "16"),
        ("Section 6", "Student Conduct &amp; Disciplinary Policy", "19"),
        ("Section 7", "Hostel Accommodation Policy", "22"),
        ("Section 8", "Hostel Facilities &amp; Fee Schedule", "26"),
        ("Section 9", "Sports &amp; Recreation Facilities", "30"),
        ("Section 10", "Campus IT &amp; Network Policy", "34"),
        ("Section 11", "Student Clubs &amp; Extracurricular Activities", "38"),
        ("Section 12", "Health, Safety &amp; Welfare", "43"),
        ("Section 13", "Grievance &amp; Appeal Procedures", "47"),
        ("Appendix A", "Important Contact Directory", "50"),
    ]
    for sec, title, pg in toc:
        story.append(
            p(f"<b>{sec}</b> — {title} <font color='grey'>..........{pg}</font>", "body")
        )
    story.append(pb())

    # ── SECTION 1: Academic Standing & Grading ─────────────────────────────────
    story += [
        h1("Section 1: Academic Standing &amp; Grading System"),
        sp(4),
        p(
            "The grading and academic standing policies at Mirai Institute of Technology "
            "are designed to maintain rigorous academic standards while supporting student "
            "success. All grades are awarded on a 10-point scale, converted to GPA for "
            "cumulative calculations.",
            "body"
        ),
        sp(6),
        h2("1.1 Grading Scale"),
        p(
            "Marks are assigned on a 10-point scale. The following table shows the "
            "grade, mark range, grade points, and corresponding letter grade:",
            "body"
        ),
        sp(4),
    ]
    grade_table = [
        ["Marks Range (%)", "Letter Grade", "Grade Points", "Classification"],
        ["90 – 100", "O (Outstanding)", "10", "Distinction"],
        ["80 – 89", "A+", "9", "First Class"],
        ["70 – 79", "A", "8", "First Class"],
        ["60 – 69", "B+", "7", "Second Class (Upper)"],
        ["55 – 59", "B", "6", "Second Class (Upper)"],
        ["50 – 54", "C", "5", "Second Class (Lower)"],
        ["45 – 49", "D", "4", "Pass"],
        ["Below 45", "F", "0", "Fail"],
        ["Absent", "Ab", "0", "Fail (Treated as F)"],
    ]
    t = Table(grade_table, colWidths=[3.5*cm, 4*cm, 3.5*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f5f5f5"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (2,0), (2,-1), "CENTER"),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story += [t, sp(8)]

    story += [
        h2("1.2 Attendance Marks"),
        p(
            "Attendance is considered a component of internal assessment and is awarded "
            "marks as follows, based on the percentage of classes attended in the semester:",
            "body"
        ),
        sp(4),
    ]
    att_table = [
        ["Attendance Percentage", "Attendance Marks Awarded"],
        ["90% and above", "5 marks"],
        ["85% to below 90%", "4 marks"],
        ["80% to below 85%", "3 marks"],
        ["75% to below 80%", "2 marks"],
        ["Below 75%", "0 marks (and examination eligibility forfeited)"],
    ]
    t2 = Table(att_table, colWidths=[8*cm, 8*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#283593")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#e8eaf6"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story += [t2, sp(8)]

    story += [
        p(
            "<b>Note:</b> A student with 72% attendance falls in the range of "
            "75% to below 80%; however, 72% is strictly below 75%. Therefore, "
            "72% attendance results in <b>0 attendance marks</b> and the student "
            "<b>is NOT eligible to appear for the final examination</b>. "
            "Students with below 75% attendance are barred from final examinations "
            "unless a formal exemption is granted by the Dean of Academics.",
            "note"
        ),
        sp(6),
        h2("1.3 GPA and Cumulative GPA (CGPA)"),
        p(
            "The Semester GPA (SGPA) is calculated by dividing the sum of "
            "(grade points × credit hours) by the total credit hours in the semester. "
            "The Cumulative GPA (CGPA) aggregates all semesters to date.",
            "body"
        ),
        h2("1.4 Good Standing"),
        p(
            "Students must maintain a minimum CGPA of 5.0 (on a 10-point scale) "
            "to remain in Good Academic Standing.",
            "body"
        ),
        h2("1.5 Academic Probation"),
        p(
            "A student whose CGPA falls below 5.0 for one semester is placed on "
            "Academic Probation. If the CGPA remains below 5.0 for two consecutive "
            "semesters, the student may be asked to withdraw from the program.",
            "body"
        ),
        h2("1.6 Dean's List"),
        p(
            "To qualify for the Dean's List, a student must achieve a semester GPA "
            "of 8.5 or higher while completing at least 18 graded credit hours with "
            "no active disciplinary notation on record.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 2: Attendance & Leave ─────────────────────────────────────────
    story += [
        h1("Section 2: Attendance &amp; Leave of Absence Policy"),
        sp(4),
        p(
            "Regular attendance is a fundamental expectation at Mirai Institute of "
            "Technology. It is the student's responsibility to attend all scheduled "
            "classes, laboratory sessions, tutorials, and seminars.",
            "body"
        ),
        h2("2.1 Mandatory Attendance Requirement"),
        p(
            "Students are required to maintain a minimum of 75% attendance in all "
            "registered courses to be eligible to sit for final examinations. "
            "Attendance is calculated per course independently.",
            "body"
        ),
        h2("2.2 Attendance Marks Award"),
        p(
            "Attendance marks form part of the internal assessment marks as described "
            "in Section 1.2. Only students who maintain 75% or above attendance are "
            "eligible to receive attendance marks.",
            "body"
        ),
        h2("2.3 Examination Eligibility"),
        p(
            "A student who fails to maintain 75% attendance in any course will be "
            "automatically <b>detained</b> from that course's final examination. "
            "Detention is applied course-by-course. A student with 72% attendance "
            "will receive 0 attendance marks and will not be eligible to appear for "
            "the final examination in that course.",
            "body"
        ),
        h2("2.4 Medical Leave Policy"),
        p(
            "Medical Leave is granted to students who are unable to attend classes "
            "due to illness or medical emergencies. The following rules apply:",
            "body"
        ),
        p("• Medical leave must be formally applied through the Student Affairs Portal.", "bullet"),
        p(
            "• The student must submit a Medical Leave Application Form along with "
            "an official medical certificate (issued by a registered medical practitioner "
            "or government hospital) to the Student Affairs Office.",
            "bullet"
        ),
        p(
            "• <b>Supporting documents must be submitted within 7 calendar days of "
            "the student's recovery and return to campus.</b>",
            "bullet"
        ),
        p(
            "• If documents are submitted after the 7-day deadline, the leave will "
            "be treated as an Unauthorized Absence and the absent days will be counted "
            "against the student's attendance record without any exemption.",
            "bullet"
        ),
        p(
            "• Medical Leave, once approved, is excluded from the total class count "
            "for calculating the attendance percentage, up to a maximum of 10 working days "
            "per semester.",
            "bullet"
        ),
        sp(6),
        h2("2.5 Short-term Absence"),
        p(
            "Absences of fewer than 2 consecutive days must be notified to course "
            "instructors via the student portal prior to the class whenever possible. "
            "These absences are counted in the attendance calculation unless covered "
            "by approved Medical or Official Leave.",
            "body"
        ),
        h2("2.6 Official/Duty Leave"),
        p(
            "Official Leave (for inter-collegiate competitions, conferences, or "
            "institute-approved events) must be pre-approved by the Head of Department "
            "and Dean of Student Affairs. Approved duty leave days are excluded from "
            "attendance calculations. Students must submit the duty leave form at least "
            "3 working days before the event.",
            "body"
        ),
        h2("2.7 Long-term Leave of Absence"),
        p(
            "Students requiring leave for more than 10 consecutive working days must "
            "apply for a formal Leave of Absence (LoA) to the Registrar's Office. "
            "LoA is granted only under exceptional circumstances (serious illness, "
            "family emergency, or personal hardship). Tuition fees are not refunded "
            "during an LoA unless waived by the Financial Aid committee.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 3: Academic Integrity ─────────────────────────────────────────
    story += [
        h1("Section 3: Academic Integrity &amp; Anti-Plagiarism Policy"),
        sp(4),
        p(
            "Mirai Institute of Technology is committed to maintaining the highest "
            "standards of academic honesty and intellectual integrity in all academic "
            "endeavors.",
            "body"
        ),
        h2("3.1 Standards of Integrity"),
        p(
            "The Institute maintains zero tolerance for academic dishonesty, including "
            "cheating, collusion, fabrication of data, unauthorized use of AI writing "
            "tools in assessments, and plagiarism.",
            "body"
        ),
        h2("3.2 Definition of Plagiarism"),
        p(
            "Plagiarism includes, but is not limited to: submitting another person's "
            "work, code, or ideas as one's own without appropriate citation; copying "
            "from the internet without attribution; self-plagiarism (reusing one's own "
            "previously submitted work without disclosure); and contract cheating.",
            "body"
        ),
        h2("3.3 Plagiarism Detection"),
        p(
            "All written submissions are processed through the Institute's licensed "
            "plagiarism detection platform. Similarity index thresholds: "
            "0–20% acceptable; 21–40% requires revision; above 40% triggers a "
            "formal integrity review.",
            "body"
        ),
        h2("3.4 First Offense Penalty"),
        p(
            "A first offense of plagiarism or academic dishonesty results in an "
            "automatic zero (0) on the assignment or examination and a formal written "
            "reprimand placed in the student's academic record.",
            "body"
        ),
        h2("3.5 Second Offense Penalty"),
        p(
            "A second offense results in an immediate failure grade ('F') in the "
            "course and mandatory referral to the University Disciplinary Committee "
            "for suspension or expulsion review.",
            "body"
        ),
        h2("3.6 AI-Generated Content Policy"),
        p(
            "Submitting AI-generated text as one's own work is treated as a form of "
            "academic dishonesty. Students may use AI tools only as research aids, "
            "and must disclose usage in a mandatory AI-Use Declaration appendix.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 4: Degree Requirements & Tuition ───────────────────────────────
    story += [
        h1("Section 4: Degree Requirements &amp; Tuition Fees"),
        h2("4.1 Graduation Requirement"),
        p(
            "Candidates for a Bachelor of Technology (B.Tech) degree must successfully "
            "complete 160 credit hours with a minimum CGPA of 5.0 on the 10-point scale.",
            "body"
        ),
        h2("4.2 Tuition Fee Schedule"),
        p(
            "Semester tuition fees must be paid in full within 14 calendar days of "
            "the start of the semester. The fee structure is as follows:",
            "body"
        ),
        sp(4),
    ]
    fee_table = [
        ["Program", "Annual Tuition (INR)", "Per Semester (INR)"],
        ["B.Tech (all branches)", "1,80,000", "90,000"],
        ["M.Tech", "1,50,000", "75,000"],
        ["MBA", "2,40,000", "1,20,000"],
        ["Ph.D (Subsidized)", "60,000", "30,000"],
    ]
    tf = Table(fee_table, colWidths=[6*cm, 5*cm, 5*cm])
    tf.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f5f5f5"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (1,0), (-1,-1), "RIGHT"),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story += [tf, sp(8)]

    story += [
        h2("4.3 Late Fee Penalty"),
        p(
            "A late fee of ₹500 per week is applied to outstanding tuition balances "
            "past the 14-day deadline. After 60 days of non-payment, the student's "
            "examination hall ticket will be withheld.",
            "body"
        ),
        h2("4.4 Scholarship Deductions"),
        p(
            "Students receiving merit-based or need-based scholarships will have the "
            "scholarship amount automatically deducted from the tuition invoice before "
            "the payment deadline.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 5: Examinations ────────────────────────────────────────────────
    story += [
        h1("Section 5: Examination Rules &amp; Procedures"),
        h2("5.1 Types of Examinations"),
        p(
            "The Institute conducts the following examinations each semester: "
            "(a) Continuous Assessment Tests (CAT-1 and CAT-2), "
            "(b) Model Examinations, and "
            "(c) End-Semester Examinations (ESE).",
            "body"
        ),
        h2("5.2 Hall Ticket Issuance"),
        p(
            "Hall tickets for End-Semester Examinations are issued only to students who: "
            "(a) have met the 75% minimum attendance requirement in all courses, "
            "(b) have no outstanding tuition dues, and "
            "(c) have no pending disciplinary action.",
            "body"
        ),
        h2("5.3 Malpractice"),
        p(
            "Any student found engaging in malpractice during examinations will have "
            "the entire semester's results cancelled and will be barred from the next "
            "semester's examinations pending a disciplinary hearing.",
            "body"
        ),
        h2("5.4 Re-Examination"),
        p(
            "Students who fail a course (grade F) may re-appear in the supplementary "
            "examination conducted within 60 days of the main examination. A re-exam "
            "fee of ₹1,500 per subject applies.",
            "body"
        ),
        h2("5.5 Revaluation"),
        p(
            "Students dissatisfied with their results may apply for revaluation within "
            "10 working days of the result declaration. A revaluation fee of ₹800 "
            "per paper applies. Revaluation results are final.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 6: Student Conduct ─────────────────────────────────────────────
    story += [
        h1("Section 6: Student Conduct &amp; Disciplinary Policy"),
        h2("6.1 Code of Conduct"),
        p(
            "All students are expected to maintain respectful, professional, and ethical "
            "behavior in all campus spaces, online platforms, and official events. "
            "Disruptive, discriminatory, or violent behavior is subject to disciplinary action.",
            "body"
        ),
        h2("6.2 Disciplinary Committee"),
        p(
            "The Student Disciplinary Committee (SDC) comprises the Dean of Student "
            "Affairs (Chair), two faculty representatives, and one student body "
            "representative. The SDC investigates all reported misconduct cases.",
            "body"
        ),
        h2("6.3 Sanctions"),
        p(
            "Depending on the severity, sanctions range from written warning and "
            "community service to suspension (1–3 semesters) or permanent expulsion.",
            "body"
        ),
        h2("6.4 Anti-Ragging Policy"),
        p(
            "The Institute has zero tolerance for ragging in any form. Any student "
            "found guilty of ragging will be expelled immediately and the matter "
            "referred to law enforcement, in compliance with UGC Anti-Ragging "
            "Regulations 2009.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 7: Hostel Accommodation ───────────────────────────────────────
    story += [
        h1("Section 7: Hostel Accommodation Policy"),
        sp(4),
        p(
            "Mirai Institute of Technology provides on-campus hostel accommodation "
            "for outstation students. Accommodation is subject to availability and "
            "governed by the rules set forth in this section.",
            "body"
        ),
        h2("7.1 Eligibility"),
        p(
            "Only full-time enrolled students residing more than 50 km from campus "
            "are eligible to apply for hostel accommodation. Priority is given to "
            "first-year students and those receiving need-based financial aid.",
            "body"
        ),
        h2("7.2 Hostel Blocks"),
        p("The campus has the following hostel blocks:", "body"),
        p("• Vega Block (Boys) — 300 rooms, standard and deluxe options", "bullet"),
        p("• Orion Block (Boys) — 250 rooms, single-occupancy only", "bullet"),
        p("• Aurora Block (Girls) — 350 rooms, standard and deluxe options", "bullet"),
        p("• Zenith Block (Girls) — 200 rooms, single-occupancy only", "bullet"),
        h2("7.3 Hostel Fees"),
        p(
            "Annual hostel fees (covering accommodation for 10 months, August–May) "
            "are as follows:",
            "body"
        ),
        sp(4),
    ]
    hostel_fee_table = [
        ["Room Type", "Annual Fee (INR)", "Security Deposit (INR)"],
        ["Standard (3-sharing)", "48,000", "10,000"],
        ["Double-sharing", "64,000", "10,000"],
        ["Deluxe (single-occupancy)", "96,000", "15,000"],
        ["Orion/Zenith Single (premium)", "1,20,000", "20,000"],
    ]
    hft = Table(hostel_fee_table, colWidths=[6.5*cm, 5*cm, 4.5*cm])
    hft.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#e8eaf6"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (1,0), (-1,-1), "RIGHT"),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story += [hft, sp(8)]

    story += [
        h2("7.4 Mess (Dining) Facilities"),
        p(
            "Three vegetarian meals (breakfast, lunch, and dinner) are provided in "
            "the central dining hall. The mess fee of ₹3,500 per month is mandatory "
            "for all hostel residents and is included in the hostel bill.",
            "body"
        ),
        h2("7.5 Hostel Rules"),
        p("• Curfew timings: 10:00 PM on weekdays; 11:00 PM on weekends.", "bullet"),
        p("• Visitors of the opposite gender are not permitted beyond the common room.", "bullet"),
        p("• Alcohol, tobacco, and narcotics are strictly prohibited.", "bullet"),
        p("• Personal electrical appliances above 500W are not permitted.", "bullet"),
        p("• Room inspections may be conducted by the Hostel Warden with prior notice.", "bullet"),
        pb(),
    ]

    # ── SECTION 8: Hostel Facilities & Fee Schedule ────────────────────────────
    story += [
        h1("Section 8: Hostel Facilities &amp; Fee Schedule"),
        sp(4),
        p(
            "Mirai Institute provides a range of supplementary facilities to hostel "
            "residents and day scholars. The following table lists the monthly "
            "subscription fees for each facility:",
            "body"
        ),
        sp(6),
    ]
    facilities_table = [
        ["Facility", "Eligibility", "Monthly Subscription Fee (INR)"],
        ["Laundry Service", "Hostel residents only", "₹350"],
        ["High-Speed Wi-Fi (10 Mbps add-on)", "All students", "₹200"],
        ["Campus Gymnasium", "All students", "₹500"],
        ["Swimming Pool", "All students", "₹750"],
        ["Indoor Squash Court", "All students", "₹400"],
        ["Badminton Court (indoor)", "All students", "₹300"],
        ["Table Tennis Room", "All students", "₹150"],
        ["Music & Performing Arts Room", "All students", "₹250"],
        ["Cycling Track (annual)", "All students", "₹600 per year"],
        ["Yoga & Meditation Room", "All students", "₹200"],
        ["Library Extended Hours (10 PM–12 AM)", "All students", "₹100"],
    ]
    ft = Table(facilities_table, colWidths=[5.5*cm, 4.5*cm, 6*cm])
    ft.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#283593")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#e8eaf6"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story += [ft, sp(8)]

    story += [
        p(
            "<b>Note:</b> Subscriptions are billed on the 1st of each month and must "
            "be paid by the 10th. Late payment attracts a penalty of ₹50. Subscriptions "
            "can be initiated or cancelled with one month's written notice to the "
            "Facilities Management Office.",
            "note"
        ),
        h2("8.1 Facility Booking"),
        p(
            "Shared facilities (squash court, swimming pool) can be booked through "
            "the MirAI Student App up to 48 hours in advance. Each student is "
            "entitled to a maximum of 2 bookings per week per facility.",
            "body"
        ),
        h2("8.2 Facility Usage Rules"),
        p("• Appropriate sports attire must be worn in all sports facilities.", "bullet"),
        p("• The swimming pool is supervised by a certified lifeguard at all times.", "bullet"),
        p("• Food and beverages are not permitted inside the pool or squash court area.", "bullet"),
        p("• All users must sign in and sign out at the facility reception.", "bullet"),
        h2("8.3 Maintenance Closures"),
        p(
            "Facilities may be closed for up to 2 days per month for routine maintenance. "
            "Advance notice of at least 48 hours will be provided via the Student App. "
            "Pro-rated refunds are credited to the student's account for planned closures "
            "exceeding 2 days.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 9: Sports & Recreation ────────────────────────────────────────
    story += [
        h1("Section 9: Sports &amp; Recreation Facilities"),
        sp(4),
        p(
            "Mirai Institute is committed to holistic student development through "
            "a broad range of sports and recreational activities. The campus sports "
            "infrastructure includes:",
            "body"
        ),
        h2("9.1 Outdoor Facilities"),
        p("• Full-size football ground (FIFA standard artificial turf)", "bullet"),
        p("• Cricket ground with covered practice nets (4 lanes)", "bullet"),
        p("• 400-metre athletic track (8 lanes, synthetic surface)", "bullet"),
        p("• Tennis courts ×4 (floodlit, available until 10:00 PM)", "bullet"),
        p("• Basketball courts ×3 (floodlit)", "bullet"),
        p("• Volleyball courts ×2", "bullet"),
        p("• Cycling track (3 km loop, available free of charge to all students)", "bullet"),
        h2("9.2 Indoor Facilities"),
        p("• Swimming pool (Olympic, 50 m, 8 lanes, heated)", "bullet"),
        p("• Indoor squash courts ×3", "bullet"),
        p("• Badminton courts ×6 (double-court hall)", "bullet"),
        p("• Table tennis room (12 tables)", "bullet"),
        p("• State-of-the-art gymnasium (200+ equipment units)", "bullet"),
        p("• Yoga and meditation studio (daily supervised sessions)", "bullet"),
        h2("9.3 Subscription Fees"),
        p(
            "As listed in Section 8, students who wish to use the Swimming Pool pay "
            "a monthly subscription fee of ₹750. Students who wish to use the Indoor "
            "Squash Court pay a monthly subscription fee of ₹400. Students may subscribe "
            "to multiple facilities simultaneously.",
            "body"
        ),
        h2("9.4 Sports Excellence Program"),
        p(
            "Students who represent the Institute at national or international competitions "
            "may apply for the Sports Excellence Scholarship, which covers up to 50% of "
            "tuition fees. Applications must be supported by a recommendation from the "
            "Chief Sports Officer.",
            "body"
        ),
        h2("9.5 Sports Events Calendar"),
        p(
            "The Institute hosts annual inter-department and inter-collegiate tournaments "
            "in all major sports. The MirAI Sports Week is held every February. "
            "Participation in inter-collegiate events earns Extracurricular Activity (ECA) "
            "credit points toward graduation.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 10: Campus IT & Network ───────────────────────────────────────
    story += [
        h1("Section 10: Campus IT &amp; Network Policy"),
        sp(4),
        p(
            "Mirai Institute provides comprehensive IT infrastructure to support "
            "academic and administrative activities. All students are provided "
            "institutional email accounts and access to campus network services "
            "upon enrollment.",
            "body"
        ),
        h2("10.1 Campus Wi-Fi Networks"),
        p("The Institute operates the following Wi-Fi networks:", "body"),
        sp(4),
    ]
    wifi_table = [
        ["Network SSID", "Protocol", "Coverage", "Default Password", "Notes"],
        ["Mirai_Student_2.4G", "WPA2", "Hostel rooms + classrooms", "MiraiStudent@2024", "2.4 GHz band; suitable for general browsing"],
        ["Mirai_Student_5G", "WPA2", "Library, labs, dining hall", "Change upon first login", "5 GHz band; high-speed; personal credentials"],
        ["Mirai_Faculty", "WPA3", "Faculty offices + conference rooms", "Faculty-issued credentials", "Faculty and staff only; not for students"],
        ["Mirai_Guest", "Open (captive portal)", "Main lobby, cafeteria", "No password (register email)", "2-hour session limit; 2 Mbps cap"],
        ["Mirai_IoT", "WPA2-Enterprise", "Lab equipment networks", "Device-specific certificates", "Restricted; lab coordinators only"],
    ]
    wt = Table(wifi_table, colWidths=[3.5*cm, 2.2*cm, 4.2*cm, 4.5*cm, 4.5*cm])
    wt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 7.5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#e8eaf6"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("PADDING", (0,0), (-1,-1), 4),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("WORDWRAP", (0,0), (-1,-1), "CJK"),
    ]))
    story += [wt, sp(8)]

    story += [
        p(
            "<b>Important:</b> Students connecting to Mirai_Student_5G are required "
            "to change the default password upon first login. The network uses personal "
            "institutional credentials (student ID + self-set password) after the first "
            "login. The initial default setup password is used only for the first "
            "connection and onboarding.",
            "note"
        ),
        h2("10.2 Acceptable Use Policy"),
        p("• The campus network must not be used for illegal downloads or streaming.", "bullet"),
        p("• Bandwidth-intensive personal activities are restricted during peak hours (9 AM–6 PM).", "bullet"),
        p("• VPN usage for personal privacy is permitted; using VPNs to bypass security filters is prohibited.", "bullet"),
        p("• Any attempt to compromise network security or access restricted systems is a disciplinary offence.", "bullet"),
        h2("10.3 Data and Privacy"),
        p(
            "Network usage is logged for security purposes. Logs are retained for "
            "90 days and may be reviewed in the event of a security incident or "
            "disciplinary investigation, subject to the Institute's Privacy Policy.",
            "body"
        ),
        h2("10.4 Personal Device Registration"),
        p(
            "Students may register up to 5 personal devices (laptops, smartphones, "
            "tablets) on the campus network via the IT Help Desk portal. Unregistered "
            "devices will be assigned limited-bandwidth guest access.",
            "body"
        ),
        h2("10.5 Support"),
        p(
            "IT support is available 24/7 at the IT Help Desk (Room T-01, Technology "
            "Block). For Wi-Fi connectivity issues, students can also raise a ticket "
            "through the MirAI Student App.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 11: Student Clubs ──────────────────────────────────────────────
    story += [
        h1("Section 11: Student Clubs &amp; Extracurricular Activities"),
        sp(4),
        p(
            "Mirai Institute of Technology encourages active student participation "
            "in extracurricular activities. The Institute recognizes over 40 student "
            "clubs across academic, cultural, sports, and social welfare categories.",
            "body"
        ),
        h2("11.1 Recognized Student Clubs"),
        p("Current recognized clubs include:", "body"),
        p("• MirAI Robotics Club", "bullet"),
        p("• Coding and Competitive Programming Society (CCPS)", "bullet"),
        p("• MirAI Entrepreneurship Cell (E-Cell)", "bullet"),
        p("• Photography and Filmmaking Club", "bullet"),
        p("• MirAI Cultural Arts Society", "bullet"),
        p("• Community Service and NSS Chapter", "bullet"),
        p("• Debate and Public Speaking Club", "bullet"),
        p("• Music and Fine Arts Society", "bullet"),
        sp(4),
        h2("11.2 Proposing a New Student Club"),
        p(
            "Any student wishing to establish a new club must follow the formal "
            "club registration process:",
            "body"
        ),
        p(
            "• <b>Student Support Requirement:</b> The proposal must be supported "
            "by at least <b>15% of the students in the proposer's batch</b>. "
            "Supporting students must co-sign the proposal form.",
            "bullet"
        ),
        p(
            "• <b>Faculty Advisor:</b> A faculty member willing to serve as the "
            "club's Faculty Advisor must be identified and their consent letter attached.",
            "bullet"
        ),
        p(
            "• <b>Proposal Contents:</b> The proposal must include the club's "
            "mission statement, planned activities, proposed budget, and a list of "
            "founding members (minimum 20 students).",
            "bullet"
        ),
        p(
            "• <b>First Review — Student Affairs Committee (SAC):</b> The completed "
            "proposal is submitted to the Student Affairs Committee (SAC), which "
            "conducts the first-level review within 15 working days. The SAC evaluates "
            "relevance, feasibility, and alignment with institutional values.",
            "bullet"
        ),
        p(
            "• <b>Second Review — Dean of Student Affairs:</b> If the SAC approves, "
            "the proposal proceeds to the Dean of Student Affairs for final ratification.",
            "bullet"
        ),
        p(
            "• <b>Approval Timeline:</b> The full approval process, from submission "
            "to final ratification, takes approximately 30–45 working days.",
            "bullet"
        ),
        sp(6),
        h2("11.3 Annual Club Registration Renewal"),
        p(
            "All clubs must renew their registration annually at the beginning of "
            "each academic year. Clubs that fail to renew or fail to demonstrate "
            "minimum activity (at least 3 events per semester) will be de-recognized.",
            "body"
        ),
        h2("11.4 Club Funding"),
        p(
            "Recognized clubs receive an annual base grant of ₹20,000 from the "
            "Student Activity Fund. Additional funds may be applied for through "
            "the Student Affairs Committee for specific events.",
            "body"
        ),
        h2("11.5 ECA Credit Points"),
        p(
            "Active participation in recognized clubs earns ECA credit points: "
            "2 points per semester for active membership, 4 points for leadership "
            "positions (President, Secretary, Treasurer). A minimum of 10 ECA "
            "points is required for graduation.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 12: Health, Safety & Welfare ───────────────────────────────────
    story += [
        h1("Section 12: Health, Safety &amp; Welfare"),
        h2("12.1 Campus Health Centre"),
        p(
            "The Mirai Campus Health Centre (CHC) operates 24 hours, 7 days a week. "
            "It is staffed by 2 full-time physicians, 4 nurses, and a part-time "
            "psychiatrist. Basic outpatient consultations are free for all enrolled "
            "students.",
            "body"
        ),
        h2("12.2 Emergency Procedures"),
        p(
            "In case of medical emergencies, call the Campus Emergency Line: "
            "1800-MIT-HELP (toll-free). The CHC maintains a 24/7 ambulance service "
            "in partnership with the nearest district hospital.",
            "body"
        ),
        h2("12.3 Mental Health Services"),
        p(
            "The Institute provides free, confidential counselling sessions through "
            "the Student Wellness Centre. Students are encouraged to seek support "
            "without stigma. Counselling sessions are held on appointment; "
            "walk-in slots are available on Tuesdays and Thursdays, 2–5 PM.",
            "body"
        ),
        h2("12.4 Student Insurance"),
        p(
            "All enrolled students are covered under the Group Student Accident "
            "Insurance Policy with a sum assured of ₹5,00,000 per student per "
            "academic year. Claims must be submitted within 30 days of the incident.",
            "body"
        ),
        h2("12.5 Fire Safety"),
        p(
            "All students must attend the mandatory fire safety induction at the "
            "start of each academic year. Fire exits must be kept clear at all times. "
            "Tampering with fire safety equipment is a disciplinary offence.",
            "body"
        ),
        pb(),
    ]

    # ── SECTION 13: Grievance & Appeal ────────────────────────────────────────
    story += [
        h1("Section 13: Grievance &amp; Appeal Procedures"),
        h2("13.1 Academic Grievances"),
        p(
            "Students who believe their academic assessment or grade is incorrect "
            "must first attempt to resolve the matter informally with the concerned "
            "faculty member. If unresolved, a formal grievance may be filed with the "
            "Head of Department within 10 working days of the result.",
            "body"
        ),
        h2("13.2 Non-Academic Grievances"),
        p(
            "Complaints related to hostel management, facilities, or administrative "
            "services should be submitted via the Student Grievance Portal. The Student "
            "Affairs Office will acknowledge receipt within 2 working days and resolve "
            "within 15 working days.",
            "body"
        ),
        h2("13.3 Anti-Sexual Harassment Cell"),
        p(
            "The Institute has a duly constituted Internal Complaints Committee (ICC) "
            "in accordance with the Prevention, Protection and Redressal of Sexual "
            "Harassment of Women at Workplace Act, 2013. All complaints are handled "
            "with strict confidentiality.",
            "body"
        ),
        h2("13.4 Appeal Against Disciplinary Action"),
        p(
            "A student wishing to appeal a disciplinary decision must submit a written "
            "appeal to the Vice-Chancellor's office within 15 working days of receiving "
            "the decision. The appeal will be heard by an independent Appeal Committee.",
            "body"
        ),
        pb(),
    ]

    # ── APPENDIX A: Contacts ───────────────────────────────────────────────────
    story += [
        h1("Appendix A: Important Contact Directory"),
        sp(4),
    ]
    contacts = [
        ["Office", "Contact Person", "Email", "Extension"],
        ["Registrar's Office", "Mr. Rajan Pillai", "registrar@mirai.edu.in", "Ext. 1001"],
        ["Dean of Academics", "Dr. Priya Nair", "dean.academics@mirai.edu.in", "Ext. 1010"],
        ["Dean of Student Affairs", "Dr. Suresh Menon", "dean.studentaffairs@mirai.edu.in", "Ext. 1020"],
        ["Student Affairs Committee", "Ms. Ananya Krishnan", "sac@mirai.edu.in", "Ext. 1021"],
        ["Hostel Administration", "Mr. Ramesh Kumar", "hostel@mirai.edu.in", "Ext. 2001"],
        ["Facilities Management", "Ms. Leela Varma", "facilities@mirai.edu.in", "Ext. 2010"],
        ["IT Help Desk", "Mr. Arun Dev", "itsupport@mirai.edu.in", "Ext. 3001"],
        ["Campus Health Centre", "Dr. Meera Iyer", "chc@mirai.edu.in", "Ext. 4001"],
        ["Student Wellness Centre", "Dr. Kavitha Mohan", "wellness@mirai.edu.in", "Ext. 4010"],
        ["Library", "Ms. Saritha Nambiar", "library@mirai.edu.in", "Ext. 5001"],
        ["Finance Office", "Mr. George Thomas", "finance@mirai.edu.in", "Ext. 6001"],
        ["Sports Office", "Mr. Vijay Prakash", "sports@mirai.edu.in", "Ext. 7001"],
    ]
    ct = Table(contacts, colWidths=[4.5*cm, 4*cm, 5.5*cm, 2.5*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f5f5f5"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("PADDING", (0,0), (-1,-1), 4),
    ]))
    story += [ct, sp(12)]

    story += [
        sp(20),
        p("— End of Handbook —", "center"),
        sp(8),
        p(
            "This handbook supersedes all previous versions. Last updated: August 2025. "
            "For the most current policies, refer to the official student portal at "
            "portal.mirai.edu.in. The Institute reserves the right to amend policies "
            "with due notice to students.",
            "note"
        ),
    ]

    return story


# ─── Build PDF ────────────────────────────────────────────────────────────────

def main():
    story = build_story()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Mirai Academic & Hostel Policy Handbook",
        author="Office of the Registrar, Mirai Institute of Technology",
    )
    doc.build(story)
    import os
    size_kb = os.path.getsize(OUTPUT) // 1024
    print(f"[handbook] Generated '{OUTPUT}' ({size_kb} KB)")

    # Verify page count
    try:
        import fitz
        d = fitz.open(OUTPUT)
        print(f"[handbook] Pages: {len(d)}")
        d.close()
    except Exception:
        pass


if __name__ == "__main__":
    main()
