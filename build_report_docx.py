import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text, title="NOTE / OBSERVATION"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="1F4E79"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"{title}: ")
    r1.bold = True
    r1.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    r1.font.size = Pt(10)
    
    r2 = p.add_run(text)
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor(0x2A, 0x3E, 0x50)
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(2)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F7F9FA")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="12" w:space="0" w:color="A0AEC0"/><w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(9.0)
    run.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(2)

def add_screenshot_placeholder(doc, img_name, caption):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "FAFAFA")
    set_cell_margins(cell, top=160, bottom=160, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="dashed" w:sz="12" w:space="0" w:color="CBD5E0"/><w:top w:val="dashed" w:sz="12" w:space="0" w:color="CBD5E0"/><w:right w:val="dashed" w:sz="12" w:space="0" w:color="CBD5E0"/><w:bottom w:val="dashed" w:sz="12" w:space="0" w:color="CBD5E0"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"Figure Evidence: {img_name}\n")
    r1.font.name = "Calibri"
    r1.font.size = Pt(10)
    r1.bold = True
    r1.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    
    r2 = p.add_run(caption)
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(4)

def format_table(doc, tbl, col_widths, headers, data):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    hdr_row = tbl.rows[0]
    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        cell.width = Inches(col_widths[idx])
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(heading)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9.5)
        
    for r_idx, row_data in enumerate(data):
        row = tbl.rows[r_idx + 1]
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(col_widths[c_idx])
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            
            tcPr = cell._tc.get_or_add_tcPr()
            borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/></w:tcBorders>')
            tcPr.append(borders)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(str(val))
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
            
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(4)

def build_document():
    doc = docx.Document()
    
    # Page setup: Standard Letter, 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    
    # Helper for styled headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x31, 0x82, 0xCE)
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        p.add_run(text)
        return p

    # ==================== COVER / HEADER ====================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(24)
    title_p.paragraph_format.space_after = Pt(4)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_main = title_p.add_run("DEVOPS FOR CLOUD COMPUTING (CSC418)")
    r_main.bold = True
    r_main.font.size = Pt(22)
    r_main.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(2)
    sub_p.paragraph_format.space_after = Pt(18)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("LAB ASSIGNMENT 4: COMPREHENSIVE LABORATORY REPORT\nVersion Control, Git Branching, GitHub Collaboration, CI/CD with GitHub Actions, and Release Management")
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # Metadata Box Table
    meta_tbl = doc.add_table(rows=5, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    widths = [2.2, 4.3]
    meta_data = [
        ["Student Name", "Abdullah Zahid"],
        ["Course Code & Title", "CSC418: DevOps for Cloud Computing"],
        ["Public Repository", "https://github.com/MAbdullahZahid/student-task-manager"],
        ["Application Title", "Student Task Manager (Python CLI)"],
        ["Submission Date", "November 2026"]
    ]
    for idx, (lbl, val) in enumerate(meta_data):
        row = meta_tbl.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(widths[0])
        c1.width = Inches(widths[1])
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 80, 80, 120, 120)
        set_cell_margins(c1, 80, 80, 120, 120)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(lbl)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        
    doc.add_page_break()

    # ==================== EXECUTIVE SUMMARY ====================
    add_h1("1. Executive Summary & Project Overview")
    add_p("This laboratory assignment demonstrates an industry-grade DevOps software development lifecycle utilizing Git distributed version control, GitHub team collaboration features, automated continuous integration (CI) workflows via GitHub Actions, and formalized semantic release packaging. The subject application, Student Task Manager, is a modular Python command-line utility designed for task tracking, input validation, and status lifecycle management.")
    add_p("The project fulfills all requirements specified in CSC418 Lab Assignment 4 across eight distinct parts (A through H), totaling 25 marks. Key engineering practices validated include branch isolation, defensive programming, continuous automated testing using Python's built-in unittest framework, intentional merge conflict resolution, and peer code review through GitHub Pull Requests.")

    add_h2("1.1 Technology Stack & Environment Details")
    tech_table = doc.add_table(rows=7, cols=3)
    t_headers = ["Layer / Tool", "Specification", "Purpose in Project"]
    t_data = [
        ["Host Operating System", "Microsoft Windows 11", "Development and local shell execution environment"],
        ["Programming Language", "Python 3.13 / 3.12", "Core application logic and automated unittest suites"],
        ["Version Control System", "Git 2.45.2.windows.1", "Local commit tracking, branching, rebasing, and merging"],
        ["Cloud Repository Host", "GitHub (Public)", "Remote synchronization, Issue tracking, PR reviews, Releases"],
        ["CI Automation Engine", "GitHub Actions", "Headless Ubuntu runner automated test execution on push/PR"],
        ["Integrated Development", "Visual Studio Code", "Source code authoring, Git staging, and conflict resolution"]
    ]
    format_table(doc, tech_table, [1.8, 1.9, 2.8], t_headers, t_data)

    # ==================== PART A ====================
    add_h1("2. Part A — Repository Initialization & Setup (3 Marks)")
    add_p("The foundational phase established a remote-first Git repository architecture on GitHub and synchronized it to the local workstation.")
    
    add_h2("2.1 Remote Repository Provisioning on GitHub")
    add_p("A public GitHub repository named 'student-task-manager' was provisioned under the GitHub user account MAbdullahZahid with standard initialization assets including a Python .gitignore template, an MIT open-source license, and a preliminary README.md file.")
    add_screenshot_placeholder(doc, "01-repository.png", "Public GitHub repository 'student-task-manager' initialized under user MAbdullahZahid.")

    add_h2("2.2 Local Cloning and Git Identity Configuration")
    add_p("The remote repository was cloned into the local directory E:\\Semester7\\Devops\\Lab\\gitlab\\student-task-manager. Global Git credentials were confirmed to match the GitHub account credentials:")
    add_code_block(doc, 
"""PS E:\\...> git --version
git version 2.45.2.windows.1

PS E:\\...> python --version
Python 3.13.3

PS E:\\...> git config --global user.name "Abdullah Zahid"
PS E:\\...> git config --global user.email "mabdullzahid@gmail.com"
PS E:\\...> git config --global --list
user.name=Abdullah Zahid
user.email=mabdullzahid@gmail.com""")

    add_h2("2.3 Core Modular Architecture & First Meaningful Commit")
    add_p("The project structure separates concerns between stateful task business logic (task_manager.py) and user interaction (main.py):")
    add_code_block(doc,
"""student-task-manager/
├── .github/
│   └── workflows/
│       └── python-tests.yml       # GitHub Actions CI workflow
├── docs/
│   └── user-guide.md              # End-user documentation
├── tests/
│   └── test_task_manager.py       # Unit test suite
├── lab-evidence/                  # Experimental screenshots
├── main.py                        # Console CLI interaction
├── task_manager.py                # Business logic functions
├── README.md                      # Project technical overview
├── LAB-REPORT.md                  # Comprehensive technical lab report
├── LICENSE                        # MIT License
└── .gitignore                     # Python exclusions""")
    add_screenshot_placeholder(doc, "02-project-structure.png", "VS Code Explorer showing clean directory structure and configuration files.")

    add_p("Initial business logic and console menu execution was committed directly to the main branch:")
    add_code_block(doc,
"""git add main.py task_manager.py
git commit -m "Add basic student task manager application"
git push origin main""")
    add_screenshot_placeholder(doc, "03-application.png", "Interactive console execution of Student Task Manager displaying menu and task additions.")

    # ==================== PART B ====================
    add_h1("3. Part B — Git Branching Strategy & Feature Implementation (4 Marks)")
    add_p("In accordance with professional Git workflows, direct commits to the production branch (main) were suspended. Three dedicated feature branches were branched off main to isolate distinct capabilities.")

    add_h2("3.1 Feature Branch Breakdown & Commit Audit")
    add_p("Each feature branch fulfilled the strict assignment requirement of containing at least two granular, meaningful commits pushed to the remote repository:")
    
    branch_tbl = doc.add_table(rows=4, cols=4)
    b_headers = ["Branch Name", "Commit Hash", "Commit Message", "Functional Purpose"]
    b_data = [
        ["feature/add-task", "465fa0c\na8b6980", "Add validation for empty task titles\nDocument task creation behavior", "Enforces whitespace stripping, raises ValueError on empty titles, and provides docstrings."],
        ["feature/complete-task", "13e9dfb\n58dbab3", "Implement task completion functionality\nValidate task identifier before completion", "Searches task list by ID, updates 'completed' to True, and validates ID type."],
        ["feature/delete-task", "4300e61\n9db3ed8", "Implement task deletion functionality\nAdd task identifier validation for deletion", "Locates task by ID, deletes index entry, validates boolean/non-int inputs."]
    ]
    format_table(doc, branch_tbl, [1.5, 0.9, 2.1, 2.0], b_headers, b_data)

    add_h2("3.2 Defensive Programming & Code Validation")
    add_p("The task management functions incorporate defensive checks against invalid user input:")
    add_code_block(doc,
"""# Validation in task_manager.py:
def add_task(title):
    \"\"\"Add a new task after validating its title.\"\"\"
    global next_id
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    task = {"id": next_id, "title": title, "completed": False}
    tasks.append(task)
    next_id += 1
    return task

def complete_task(task_id):
    \"\"\"Mark a task as completed using its ID.\"\"\"
    if not isinstance(task_id, int) or isinstance(task_id, bool):
        return False
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return True
    return False

def delete_task(task_id):
    \"\"\"Delete a task using its ID.\"\"\"
    if not isinstance(task_id, int) or isinstance(task_id, bool):
        return False
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[index]
            return True
    return False""")

    add_h2("3.3 Branch Inspection & Git Graph Visualization")
    add_p("Local and remote branch pointers and topological DAGs were inspected using Git CLI:")
    add_code_block(doc,
"""PS E:\\...> git branch -a
* main
  feature/add-task
  feature/complete-task
  feature/delete-task
  remotes/origin/main
  remotes/origin/feature/add-task
  remotes/origin/feature/complete-task
  remotes/origin/feature/delete-task

PS E:\\...> git log --oneline --graph --all
* 9db3ed8 (origin/feature/delete-task) Add task identifier validation for deletion
* 4300e61 Implement task deletion functionality
| * 58dbab3 (origin/feature/complete-task) Validate task identifier before completion
| * 13e9dfb Implement task completion functionality
|/  
| * a8b6980 (origin/feature/add-task) Document task creation behavior
| * 465fa0c Add validation for empty task titles
|/  
* 0537a64 (HEAD -> main, origin/main) Add basic student task manager application
* 70bcde8 Initial commit""")
    add_screenshot_placeholder(doc, "05-feature-branches.png", "Terminal output showing all local and remote tracking branches and commit graph.")

    # ==================== PART C ====================
    add_h1("4. Part C — GitHub Issues & Pull Requests (4 Marks)")
    add_p("Project management and peer code reviews were executed natively within GitHub's web interface.")

    add_h2("4.1 Issue Tracking Lifecycle")
    add_p("Five GitHub Issues were opened to track development milestones with explicit descriptions and labels:")
    
    issue_tbl = doc.add_table(rows=6, cols=4)
    i_headers = ["Issue #", "Issue Title", "Label", "Associated Pull Request"]
    i_data = [
        ["#1", "Implement task creation", "enhancement", "PR #1 (feature/add-task)"],
        ["#2", "Add task completion feature", "enhancement", "PR #2 (feature/complete-task)"],
        ["#3", "Implement task deletion", "enhancement", "PR #3 (feature/delete-task)"],
        ["#4", "Add input validation and documentation", "documentation", "PR #5 (docs/project-documentation)"],
        ["#5", "Add automated tests and CI workflow", "testing / enhancement", "PR #4 (feature/automated-testing)"]
    ]
    format_table(doc, issue_tbl, [0.8, 2.3, 1.4, 2.0], i_headers, i_data)
    add_screenshot_placeholder(doc, "06-github-issues.png", "GitHub Issues overview showing all 5 tracked milestone issues.")

    add_h2("4.2 Pull Requests & Automated Issue Resolution")
    add_p("Five Pull Requests were submitted targeting the main branch. Every PR underwent code diff inspection, inline review comments, and linked issue closure using GitHub's keyword 'Closes #N':")
    
    pr_tbl = doc.add_table(rows=6, cols=5)
    pr_headers = ["PR #", "Source Branch", "Target", "Linked Issue", "Review Status"]
    pr_data = [
        ["PR #1", "feature/add-task", "main", "Closes #1", "Approved & Merged"],
        ["PR #2", "feature/complete-task", "main", "Closes #2", "Approved & Merged"],
        ["PR #3", "feature/delete-task", "main", "Closes #3", "Rebased, Approved & Merged"],
        ["PR #4", "feature/automated-testing", "main", "Closes #5", "CI Verified, Approved & Merged"],
        ["PR #5", "docs/project-documentation", "main", "Closes #4", "Approved & Merged"]
    ]
    format_table(doc, pr_tbl, [0.7, 1.8, 0.8, 1.2, 2.0], pr_headers, pr_data)
    add_screenshot_placeholder(doc, "07-pull-requests.png", "GitHub Closed Pull Requests view demonstrating five successfully merged pull requests.")

    # ==================== PART D ====================
    add_h1("5. Part D — Deliberate Merge Conflict Creation & Resolution (4 Marks)")
    add_p("A merge conflict was intentionally synthesized to simulate collaborative divergence where two team members modify identical lines in a file asynchronously.")

    add_h2("5.1 Conflict Simulation Steps")
    add_p("1. The main branch established the baseline line: 'Project status: Planning' in README.md.")
    add_p("2. Branch conflict/active-status changed the line to: 'Project status: Active'.")
    add_p("3. Branch conflict/completed-status simultaneously branched from main and modified the identical line to: 'Project status: Completed'.")
    add_p("4. conflict/active-status was merged into main cleanly via fast-forward merge.")
    add_p("5. When attempting to merge conflict/completed-status into main, Git flagged a 3-way content merge collision:")

    add_code_block(doc,
"""PS E:\\...> git checkout main
Switched to branch 'main'

PS E:\\...> git merge conflict/completed-status
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.""")
    add_screenshot_placeholder(doc, "08-merge-conflict.png", "Terminal and VS Code showing active merge conflict and standard Git conflict markers.")

    add_h2("5.2 Manual Conflict Resolution")
    add_p("Git marked the conflict region inside README.md with three standard delimiters:")
    add_code_block(doc,
"""<<<<<<< HEAD
Project status: Active
=======
Project status: Completed
>>>>>>> conflict/completed-status""")
    add_p("The conflict markers were purged, selecting the final production status 'Project status: Completed', followed by staging and finalizing the merge commit:")
    add_code_block(doc,
"""git add README.md
git commit -m "Resolve README merge conflict"
git push origin main""")
    add_screenshot_placeholder(doc, "09-conflict-resolved.png", "VS Code editor showing cleanly resolved README.md without conflict markers.")

    # ==================== PART E ====================
    add_h1("6. Part E — Automated Testing & GitHub Actions CI (4 Marks)")
    add_p("Continuous Integration was established using Python's standard library unittest framework coupled with GitHub Actions automation.")

    add_h2("6.1 Unit Test Implementation")
    add_p("A test suite in tests/test_task_manager.py defines test fixtures and unit assertions to validate all state transitions:")
    add_code_block(doc,
"""import unittest
import task_manager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        task_manager.tasks.clear()
        task_manager.next_id = 1

    def test_add_task(self):
        task = task_manager.add_task("Complete assignment")
        self.assertEqual(task["title"], "Complete assignment")
        self.assertFalse(task["completed"])
        self.assertEqual(len(task_manager.tasks), 1)

    def test_complete_task(self):
        task = task_manager.add_task("Study Git")
        result = task_manager.complete_task(task["id"])
        self.assertTrue(result)
        self.assertTrue(task["completed"])

    def test_delete_task(self):
        task = task_manager.add_task("Submit lab")
        result = task_manager.delete_task(task["id"])
        self.assertTrue(result)
        self.assertEqual(len(task_manager.tasks), 0)

if __name__ == "__main__":
    unittest.main()""")

    add_p("Local execution passed successfully:")
    add_code_block(doc,
"""PS E:\\...> python -m unittest discover -s tests -v
test_add_task (test_task_manager.TestTaskManager.test_add_task) ... ok
test_complete_task (test_task_manager.TestTaskManager.test_complete_task) ... ok
test_delete_task (test_task_manager.TestTaskManager.test_delete_task) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK""")
    add_screenshot_placeholder(doc, "10-tests-passed.png", "Local PowerShell terminal showing three passing unit tests.")

    add_h2("6.2 GitHub Actions Workflow Specification")
    add_p("A workflow was defined in .github/workflows/python-tests.yml to trigger on both direct pushes and pull requests targeting the main branch:")
    add_code_block(doc,
"""name: Python Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Run automated tests
        run: python -m unittest discover -s tests -v""")

    add_h2("6.3 Empirical CI Demonstration: Failure and Recovery")
    add_p("To satisfy the academic requirement of demonstrating failure detection and subsequent recovery:")
    add_p("1. A deliberate failure was pushed by modifying test_delete_task with an impossible assertion: self.assertEqual(len(task_manager.tasks), 5). GitHub Actions flagged this build as Red (Failed).")
    add_screenshot_placeholder(doc, "11-actions-failed.png", "GitHub Actions UI displaying red failed run due to deliberate assertion mismatch.")
    add_p("2. The assertion was restored to 0, committed, and pushed. The subsequent build passed with a Green checkmark.")
    add_screenshot_placeholder(doc, "12-actions-passed.png", "GitHub Actions UI displaying successful green checkmark after assertion correction.")

    # ==================== PART F ====================
    add_h1("7. Part F — Documentation & GitHub Release Management (2 Marks)")
    add_p("To ensure maintainability and production readiness, project documentation and release tags were formalized.")

    add_h2("7.1 Technical README and User Guide")
    add_p("README.md provides architectural overviews, quick-start installation, execution commands, and test steps. A dedicated docs/user-guide.md details step-by-step end-user interaction.")

    add_h2("7.2 GitHub Semantic Release v1.0.0")
    add_p("A semantic release tag v1.0.0 was published from the tip of the verified main branch:")
    add_screenshot_placeholder(doc, "13-release.png", "GitHub Releases page showing published Student Task Manager v1.0.0 release notes and asset downloads.")

    # ==================== PART G ====================
    add_h1("8. Part G — Comprehensive Lab Report Questions & Answers (2 Marks)")
    add_p("Below are detailed academic analyses answering the five required core questions:")

    add_h2("Question 1: Explain the fundamental difference between Git and GitHub. What are the roles of 'git add', 'git commit', and 'git push'?")
    add_p("Git and GitHub serve distinct yet complementary layers of the software engineering ecosystem:", "Answer: ")
    add_p("1. Git is a local, decentralized command-line version control system (VCS). Created by Linus Torvalds, Git tracks deltas across files, computes SHA-1/SHA-256 cryptographic hashes for commit objects, manages branches through direct DAG pointers, and functions completely without internet connectivity.")
    add_p("2. GitHub is an enterprise cloud platform that hosts remote Git repositories. It layers team collaboration infrastructure on top of Git, including graphical diff visualization, Issue management, Pull Requests with branch protection rules, automated CI/CD runners (GitHub Actions), and user access controls.")
    add_p("Roles of the three core commands:")
    add_p("• git add: Moves files from the Working Directory to the Staging Area (the Git Index). It computes the SHA hash of the file contents, stores blob objects in the .git/objects directory, and prepares an explicit snapshot of changes intended for the next commit.")
    add_p("• git commit: Permanently records staged changes into the local repository database. It creates a commit object containing tree pointers, author metadata, timestamp, and a parent commit pointer, advancing the HEAD reference.")
    add_p("• git push: Establishes a secure network session (HTTPS/SSH) with the remote repository (e.g., origin on GitHub) and transfers local commit objects and ref updates to synchronize remote tracking branches.")

    add_h2("Question 2: What is the purpose of Git branches, Pull Requests, and why do merge conflicts occur?")
    add_p("• Git Branches provide lightweight, movable pointers to individual commits in the commit graph. They allow developers to isolate feature development, bug fixes, or experiments from the stable main branch. Because branches only require moving a 41-byte ref pointer, branching is computationally instantaneous.")
    add_p("• Pull Requests (PRs) are collaborative review gates hosted on GitHub. Rather than pushing code directly to shared production branches, a developer opens a PR to declare: 'Please review and pull changes from feature-branch into main.' PRs facilitate automated CI testing, inline peer code reviews, line-by-line discussions, and compliance enforcement.")
    add_p("• Merge Conflicts occur when Git's automated merge algorithms (such as recursive or ort) encounter irreconcilable diffs between two parent commits. Specifically, conflicts arise when: (a) two branches modify the exact same lines of code within a file differently, or (b) one branch edits a file while another branch deletes or renames it. In these cases, Git halts the merge and places conflict markers for human developer resolution.")

    add_h2("Question 3: Compare and contrast 'git fetch', 'git pull', 'git merge', and 'git rebase'.")
    add_p("These four commands manage remote synchronization and historical branch integration:")
    
    comp_tbl = doc.add_table(rows=5, cols=4)
    c_headers = ["Command", "Primary Action", "Branch History Impact", "Risk Profile"]
    c_data = [
        ["git fetch", "Downloads objects and refs from remote repository to remote-tracking branches (origin/main).", "Zero impact on current local branch or working tree.", "Completely safe; non-destructive read operation."],
        ["git pull", "Executes 'git fetch' followed immediately by 'git merge FETCH_HEAD'.", "Modifies working directory and can create an implicit merge commit.", "Moderate; can introduce unexpected merge conflicts in dirty working trees."],
        ["git merge", "Combines two divergent branches by creating a 3-way merge commit with two parent hashes.", "Preserves true historical branching topology and non-linear chronology.", "Low to moderate; non-destructive, historical commits remain unchanged."],
        ["git rebase", "Replays local commits from current branch on top of a new base commit.", "Rewrites commit history into a linear sequence with brand-new commit hashes.", "High if used on shared public branches; rewriting shared history breaks collaborator trees."]
    ]
    format_table(doc, comp_tbl, [1.2, 2.3, 1.8, 1.2], c_headers, c_data)

    add_h2("Question 4: What is the purpose of GitHub Issues and GitHub Actions in a DevOps pipeline?")
    add_p("• GitHub Issues functions as an agile project management and issue-tracking center. It enables development teams to catalog user stories, bug reports, architectural chores, and enhancement requests. Issues incorporate labels, milestones, assignees, and cross-linking to Pull Requests (e.g., 'Closes #3') to enforce automated traceability between business requirements and shipping code.")
    add_p("• GitHub Actions represents Continuous Integration and Continuous Deployment (CI/CD) automation. Defined through declarative YAML files, Actions run headless workflows on cloud virtual machines in response to webhooks (such as code pushes or PR openings). In a DevOps lifecycle, GitHub Actions eliminates human error by running linters, automated unit test suites, security scans, Docker builds, and cloud deployments automatically before code is permitted into production.")

    add_h2("Question 5: Describe a technical difficulty encountered during this lab and the exact steps taken to resolve it.")
    add_p("Technical Problem Encountered: Feature Branch Merge Collision During Sequential PR Merging.", "Difficulty: ")
    add_p("While developing Part B and Part C, both feature/complete-task and feature/delete-task introduced new functions immediately above the display_tasks() declaration in task_manager.py. Because both branches branched off the original main commit (0537a64), merging PR #2 updated main, causing PR #3 to encounter an automatic merge conflict on GitHub because lines in task_manager.py conflicted at the insertion boundary.")
    add_p("Systematic Solution:")
    add_p("1. Switched locally to the feature/delete-task branch and fetched the latest remote state: git checkout feature/delete-task && git fetch origin.")
    add_p("2. Initiated an interactive rebase against updated main: git rebase origin/main.")
    add_p("3. Inspected task_manager.py to order the function definitions cleanly: add_task followed by complete_task, followed by delete_task, and ending with display_tasks.")
    add_p("4. Staged the resolved file and concluded the rebase: git add task_manager.py && git rebase --continue.")
    add_p("5. Pushed the linearized feature branch safely using git push --force-with-lease origin feature/delete-task. GitHub immediately recognized the conflict was cleared, and PR #3 was merged cleanly with zero further conflicts.")

    # ==================== PART H ====================
    add_h1("9. Part H — Evidence Checklist & Viva Voce Preparation Guide (1 Mark)")
    
    add_h2("9.1 Submission Evidence Checklist")
    ev_tbl = doc.add_table(rows=14, cols=3)
    ev_headers = ["File Name", "Required Subject Matter", "Lab Part"]
    ev_data = [
        ["01-repository.png", "Public GitHub repository page showing repo name, visibility, and initial files", "Part A"],
        ["02-project-structure.png", "VS Code Explorer showing clean directory structure and subfolders", "Part A"],
        ["03-application.png", "Interactive terminal execution of python main.py with task operations", "Part A / B"],
        ["04-git-commits.png", "Terminal output of git log --oneline showing meaningful commits", "Part A / B"],
        ["05-feature-branches.png", "Terminal output of git log --graph --all showing three feature branches", "Part B"],
        ["06-github-issues.png", "GitHub Issues tab showing all 5 tracked milestone issues with labels", "Part C"],
        ["07-pull-requests.png", "GitHub Pull Requests tab showing 5 merged PRs with purple merged icons", "Part C / E / F"],
        ["08-merge-conflict.png", "Terminal and VS Code showing active conflict markers in README.md", "Part D"],
        ["09-conflict-resolved.png", "VS Code showing clean README.md after manual conflict resolution", "Part D"],
        ["10-tests-passed.png", "PowerShell terminal showing three passing unit tests in test_task_manager.py", "Part E"],
        ["11-actions-failed.png", "GitHub Actions UI displaying red failed workflow run from bad assertion", "Part E"],
        ["12-actions-passed.png", "GitHub Actions UI displaying green successful workflow run", "Part E"],
        ["13-release.png", "GitHub Releases tab showing published v1.0.0 semantic release tag", "Part F"]
    ]
    format_table(doc, ev_tbl, [1.6, 3.8, 1.1], ev_headers, ev_data)

    add_h2("9.2 Viva Voce High-Yield Questions & Answers")
    viva_qa = [
        ("Q1: What is a detached HEAD state in Git?",
         "A: A detached HEAD state occurs when HEAD points directly to a specific commit hash rather than a named branch reference. Commits made in this state are orphaned and will eventually be garbage-collected unless saved by creating a new branch (git switch -c new-branch)."),
        ("Q2: Why is 'git pull' considered potentially dangerous compared to 'git fetch'?",
         "A: 'git pull' executes a fetch and an immediate merge. If you have uncommitted changes or diverged work in your local branch, it can unexpectedly create messy merge commits or trigger conflicts. 'git fetch' allows you to safely inspect upstream diffs before deciding whether to merge or rebase."),
        ("Q3: When should a developer use 'rebase' instead of 'merge'?",
         "A: Rebase should be used on local, unpushed feature branches to maintain a clean, linear commit history before integrating into main. Rebase should NEVER be used on shared public branches because rewriting public commit hashes disrupts collaborator repositories."),
        ("Q4: What does the '--force-with-lease' flag do?",
         "A: Unlike standard '--force' which blindly overwrites the remote branch regardless of upstream changes, '--force-with-lease' only overwrites if no one else has updated the remote branch since your last fetch. This prevents accidentally overwriting a peer's pushed commits."),
        ("Q5: What is Continuous Integration (CI)?",
         "A: CI is a DevOps practice where developers frequently merge code changes into a shared central repository. Automated builds and automated test suites are executed automatically upon every push to detect defects early and prevent regressions."),
        ("Q6: How does GitHub automatically close an Issue from a Pull Request?",
         "A: By including supported closing keywords in the PR description or commit message, such as 'Closes #1', 'Fixes #2', or 'Resolves #3'. When the PR is merged into the default branch, GitHub automatically marks the referenced Issue as closed."),
        ("Q7: What is the purpose of the setUp() method in Python unittest?",
         "A: setUp() is a test fixture method executed immediately before every individual test method. In our lab, setUp() clears the tasks list and resets next_id to 1 to ensure complete test isolation and zero state pollution between tests."),
        ("Q8: What is Semantic Versioning (SemVer)?",
         "A: Semantic Versioning follows the MAJOR.MINOR.PATCH format (e.g., v1.0.0). MAJOR indicates incompatible API changes, MINOR indicates backward-compatible new functionality, and PATCH indicates backward-compatible bug fixes."),
        ("Q9: What happens under the hood during a 3-way merge in Git?",
         "A: Git locates the nearest common ancestor commit of the two branches, compares the diff of branch A against the ancestor, compares the diff of branch B against the ancestor, and combines non-overlapping diffs into a new merge commit with two parents."),
        ("Q10: What is the function of .gitignore in a Python repository?",
         "A: It specifies intentional patterns of files that Git should never track or commit, such as compiled bytecode (__pycache__/, *.pyc), virtual environments (venv/), system files (.DS_Store), and secret environment variables (.env).")
    ]
    for q, a in viva_qa:
        add_p(q, bold_prefix="")
        add_p(a)

    # Save to disk
    out_path = r"e:\Semester7\Devops\Lab\gitlab\student-task-manager\DevOps_Lab_Assignment_4_Report.docx"
    doc.save(out_path)
    print(f"Report generated successfully at: {out_path}")

if __name__ == "__main__":
    build_document()
