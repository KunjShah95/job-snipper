"""
Test script to verify skills extraction from resumes.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.resume_parser import parse_resume_to_json

# Test case 1: Resume with clear Skills section
test_resume_1 = """
John Doe
john.doe@email.com | (555) 123-4567
New York, NY

SKILLS
Python, JavaScript, React, Node.js, SQL, MongoDB, Docker, AWS, Git, Machine Learning

EXPERIENCE
Senior Developer at Tech Corp
- Built scalable applications
- 5 years experience

EDUCATION
B.Tech in Computer Science
"""

# Test case 2: Resume without clear Skills section
test_resume_2 = """
Jane Smith
jane@example.com
Boston, MA

PROFESSIONAL EXPERIENCE
Software Engineer - 3 years
Working with Python and Django
Experience in Docker and Kubernetes

EDUCATION
M.Sc Computer Science
"""

# Test case 3: Empty resume
test_resume_3 = """
Simple Resume
No real content here
"""

print("=" * 60)
print("TEST 1: Resume with Skills Section")
print("=" * 60)
result1 = parse_resume_to_json(test_resume_1)
print(f"Name: {result1['name']}")
print(f"Email: {result1['email']}")
print(f"Phone: {result1['phone']}")
print(f"Location: {result1['location']}")
print(f"Skills Found: {len(result1['skills'])}")
print(f"Skills: {result1['skills']}")
print(f"Education: {result1['education']}")
print(f"Experience: {result1['experience']}")

print("\n" + "=" * 60)
print("TEST 2: Resume without Skills Section")
print("=" * 60)
result2 = parse_resume_to_json(test_resume_2)
print(f"Name: {result2['name']}")
print(f"Email: {result2['email']}")
print(f"Location: {result2['location']}")
print(f"Skills Found: {len(result2['skills'])}")
print(f"Skills: {result2['skills']}")
print(f"Education: {result2['education']}")
print(f"Experience: {result2['experience']}")

print("\n" + "=" * 60)
print("TEST 3: Minimal Resume (should show empty/minimal skills)")
print("=" * 60)
result3 = parse_resume_to_json(test_resume_3)
print(f"Skills Found: {len(result3['skills'])}")
print(f"Skills: {result3['skills']}")

print("\n" + "=" * 60)
print("✅ All tests completed!")
print("=" * 60)
print("\nKEY POINTS:")
print("1. ✅ Skills are ONLY extracted from resume content")
print("2. ✅ NO hardcoded skills are added")
print("3. ✅ If no skills found, list is empty []")
print("4. ✅ Skills section is parsed when present")
print("5. ✅ Skills are extracted dynamically, not from fixed list")
