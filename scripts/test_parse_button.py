"""
Quick test to verify parse_resume function works
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

print("Testing parse_resume function...")
print("=" * 60)

try:
    from agents.parser_agent import parse_resume
    print("✅ Successfully imported parse_resume from agents.parser_agent")
except Exception as e:
    print(f"❌ Failed to import parse_resume: {e}")
    sys.exit(1)

try:
    from services.docx_parser import parse_document
    print("✅ Successfully imported parse_document from services.docx_parser")
except Exception as e:
    print(f"❌ Failed to import parse_document: {e}")
    sys.exit(1)

try:
    from services.resume_parser import parse_resume_to_json
    print("✅ Successfully imported parse_resume_to_json from services.resume_parser")
except Exception as e:
    print(f"❌ Failed to import parse_resume_to_json: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("Testing with sample text...")
print("=" * 60)

sample_text = """
John Doe
john.doe@email.com | (555) 123-4567
New York, NY

SKILLS
Python, JavaScript, React, SQL, Docker

EXPERIENCE
Senior Developer - 5 years

EDUCATION
B.Tech Computer Science
"""

try:
    result = parse_resume_to_json(sample_text)
    print("✅ parse_resume_to_json works!")
    print(f"   Name: {result.get('name')}")
    print(f"   Email: {result.get('email')}")
    print(f"   Skills: {result.get('skills')}")
except Exception as e:
    print(f"❌ parse_resume_to_json failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("All imports working! Button issue might be:")
print("=" * 60)
print("1. Streamlit session state issue (try refreshing page)")
print("2. File path issue (check if file is saved correctly)")
print("3. Browser cache (try hard refresh: Ctrl+Shift+R)")
print("4. Check browser console for JavaScript errors")
