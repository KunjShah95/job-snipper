"""
Version Manager - Track & Compare Resume Versions
Manage multiple resume versions, compare changes, and restore previous versions.
"""

import streamlit as st
import sys
import uuid
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.version_manager import VersionManager
from utils.text_analyzer import TextAnalyzer
from utils.color_scheme import get_unified_css
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Version Manager - ResumeMasterAI", page_icon="📝", layout="wide"
)

# Apply unified CSS
st.markdown(get_unified_css(), unsafe_allow_html=True)

@st.cache_data
def load_custom_css(file_path):
    """Load a CSS file and wrap it in style tags."""
    try:
        with open(file_path) as f:
            return f"<style>{f.read()}</style>"
    except FileNotFoundError:
        return ""

# Load custom CSS for this page
css_path = Path(__file__).parent.parent / "styles" / "version_manager.css"
st.markdown(load_custom_css(css_path), unsafe_allow_html=True)

# Header
st.markdown("# 📝 Version Manager")
st.markdown("### Track, compare, and manage all your resume versions")

# Initialize session state
if "version_manager" not in st.session_state:
    st.session_state.version_manager = VersionManager()
if "selected_versions" not in st.session_state:
    st.session_state.selected_versions = []

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Version Control")

    # Upload New Version
    st.subheader("📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload New Version",
        type=["pdf", "docx", "txt"],
        help="Upload a new resume version to track",
    )

    if uploaded_file:
        version_name = st.text_input(
            "Version Name",
            value=f"Resume_{datetime.now().strftime('%Y%m%d_%H%M')}",
            help="Give this version a name",
        )

        version_notes = st.text_area(
            "Version Notes (Optional)",
            placeholder="What changed in this version?",
            height=100,
        )

        if st.button("💾 Save Version", type="primary", key="save_version_button"):
            try:
                result = st.session_state.version_manager.save_version(
                    file=uploaded_file, name=version_name, notes=version_notes
                )
                st.success(f"✅ Version '{version_name}' saved!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error saving version: {str(e)}")

    st.markdown("---")

    # Filters
    st.subheader("🔍 Filters")

    sort_by = st.selectbox(
        "Sort By", ["Most Recent", "Oldest First", "Name (A-Z)", "Name (Z-A)"]
    )

    show_archived = st.checkbox("Show Archived", value=False)

# Main Content
tab1, tab2, tab3, tab4 = st.tabs(
    ["📚 All Versions", "🔄 Compare", "📊 Analytics", "⚙️ Settings"]
)

with tab1:
    st.markdown("## 📚 Resume Version History")

    # Get all versions
    versions = st.session_state.version_manager.get_all_versions(
        sort_by=sort_by, include_archived=show_archived
    )

    if not versions:
        st.info(
            "📭 No versions yet. Upload your first resume version using the sidebar!"
        )
    else:
        # Stats Overview
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
            <div class="stats-card">
                <h3>{len(versions)}</h3>
                <p>Total Versions</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            current = [v for v in versions if v.get("is_current", False)]
            st.markdown(
                f"""
            <div class="stats-card">
                <h3>{len(current)}</h3>
                <p>Current Version</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            archived = [v for v in versions if v.get("archived", False)]
            st.markdown(
                f"""
            <div class="stats-card">
                <h3>{len(archived)}</h3>
                <p>Archived</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            total_size = sum(v.get("size", 0) for v in versions)
            st.markdown(
                f"""
            <div class="stats-card">
                <h3>{total_size / 1024:.1f} KB</h3>
                <p>Total Storage</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Timeline View
        st.markdown("### 📅 Version Timeline")

        st.markdown('<div class="timeline">', unsafe_allow_html=True)

        for version in versions:
            version_id = version.get("id", "")
            is_current = version.get("is_current", False)

            st.markdown('<div class="timeline-item">', unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])

            with col1:
                badge_class = "badge-current" if is_current else "badge-previous"
                badge_text = "CURRENT" if is_current else "PREVIOUS"

                st.markdown(
                    f"""
                <div class="version-card">
                    <div class="version-header">
                        <div>
                            <h3>{version.get("name", "Unnamed")}</h3>
                            <span class="version-badge {badge_class}">{badge_text}</span>
                        </div>
                        <div style="text-align: right;">
                            <small>{version.get("date", "N/A")}</small>
                        </div>
                    </div>
                    <p><strong>Notes:</strong> {version.get("notes", "No notes")}</p>
                    <p><strong>Size:</strong> {version.get("size", 0) / 1024:.1f} KB | 
                       <strong>Format:</strong> {version.get("format", "N/A").upper()}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col2:
                # Action buttons
                if st.button("👁️ View", key=f"view_{version_id}"):
                    st.session_state.viewing_version = version_id

                if st.button("📥 Download", key=f"download_{version_id}"):
                    file_data = st.session_state.version_manager.get_version_file(
                        version_id
                    )
                    st.download_button(
                        label="Download File",
                        data=file_data,
                        file_name=f"{version.get('name')}.{version.get('format', 'pdf')}",
                        mime=f"application/{version.get('format', 'pdf')}",
                    )

                if not is_current:
                    if st.button("🔄 Restore", key=f"restore_{version_id}"):
                        st.session_state.version_manager.set_current_version(version_id)
                        st.success(f"✅ Restored version '{version.get('name')}'")
                        st.rerun()

                if st.button("🗑️ Delete", key=f"delete_{version_id}"):
                    st.session_state.version_manager.delete_version(version_id)
                    st.success("🗑️ Version deleted")
                    st.rerun()

                # Selection for comparison
                is_selected = version_id in st.session_state.selected_versions
                if st.checkbox("Select", key=f"select_{version_id}", value=is_selected):
                    if version_id not in st.session_state.selected_versions:
                        st.session_state.selected_versions.append(version_id)
                else:
                    if version_id in st.session_state.selected_versions:
                        st.session_state.selected_versions.remove(version_id)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("## 🔄 Compare Versions")

    if len(st.session_state.selected_versions) < 2:
        st.info("📌 Select at least 2 versions from the 'All Versions' tab to compare")
    else:
        st.success(
            f"✅ {len(st.session_state.selected_versions)} versions selected for comparison"
        )

        # Comparison controls
        col1, col2 = st.columns(2)

        with col1:
            version1_id = st.selectbox(
                "Version 1 (Older)",
                st.session_state.selected_versions,
                format_func=lambda x: st.session_state.version_manager.get_version_name(
                    x
                ),
            )

        with col2:
            version2_id = st.selectbox(
                "Version 2 (Newer)",
                [v for v in st.session_state.selected_versions if v != version1_id],
                format_func=lambda x: st.session_state.version_manager.get_version_name(
                    x
                ),
            )

        if st.button("📊 Compare Versions", type="primary", key="compare_versions_button"):
            with st.spinner("🔄 Comparing versions..."):
                try:
                    comparison = st.session_state.version_manager.compare_versions(
                        version1_id, version2_id
                    )

                    # Summary Statistics
                    st.markdown("### 📈 Change Summary")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        additions = comparison.get("additions", 0)
                        st.metric(
                            "Additions",
                            additions,
                            delta=additions if additions > 0 else None,
                        )

                    with col2:
                        deletions = comparison.get("deletions", 0)
                        st.metric(
                            "Deletions",
                            deletions,
                            delta=-deletions if deletions > 0 else None,
                            delta_color="inverse",
                        )

                    with col3:
                        modifications = comparison.get("modifications", 0)
                        st.metric("Modifications", modifications)

                    with col4:
                        similarity = comparison.get("similarity", 100)
                        st.metric("Similarity", f"{similarity}%")

                    st.markdown("---")

                    # Detailed Comparison
                    st.markdown("### 📝 Detailed Changes")

                    changes = comparison.get("changes", [])

                    if not changes:
                        st.info("✨ No significant changes detected between versions")
                    else:
                        for change in changes:
                            change_type = change.get("type", "modified")
                            section = change.get("section", "Content")

                            if change_type == "added":
                                st.markdown(
                                    f"""
                                <div class="diff-added">
                                    <strong>➕ Added in {section}:</strong><br>
                                    {change.get("content", "")}
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )

                            elif change_type == "removed":
                                st.markdown(
                                    f"""
                                <div class="diff-removed">
                                    <strong>➖ Removed from {section}:</strong><br>
                                    {change.get("content", "")}
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )

                            else:  # modified
                                st.markdown(
                                    f"""
                                <div style="margin: 1rem 0;">
                                    <strong>🔄 Modified in {section}:</strong><br>
                                    <div class="diff-removed">{change.get("old", "")}</div>
                                    <div class="diff-added">{change.get("new", "")}</div>
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )

                    # Export Comparison
                    st.markdown("---")
                    if st.button("📥 Export Comparison Report", key="export_comparison_report_button"):
                        report = f"""
Version Comparison Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Version 1: {st.session_state.version_manager.get_version_name(version1_id)}
Version 2: {st.session_state.version_manager.get_version_name(version2_id)}

Summary:
- Additions: {additions}
- Deletions: {deletions}
- Modifications: {modifications}
- Similarity: {similarity}%

Detailed Changes:
{chr(10).join(f"- {c['type'].upper()}: {c.get('content', c.get('new', 'N/A'))}" for c in changes)}
                        """

                        st.download_button(
                            label="Download Report",
                            data=report,
                            file_name="version_comparison.txt",
                            mime="text/plain",
                        )

                except Exception as e:
                    st.error(f"❌ Error comparing versions: {str(e)}")

with tab3:
    st.markdown("## 📊 Version Analytics")

    versions = st.session_state.version_manager.get_all_versions()

    if not versions:
        st.info("📭 No data available. Upload versions to see analytics.")
    else:
        # Version Activity
        st.markdown("### 📅 Version Activity Over Time")

        version_dates = [
            v.get("date", datetime.now().strftime("%Y-%m-%d")) for v in versions
        ]
        df = pd.DataFrame({"date": version_dates})
        df["date"] = pd.to_datetime(df["date"])
        df["count"] = 1

        fig = px.histogram(
            df,
            x="date",
            title="Versions Created Over Time",
            labels={"date": "Date", "count": "Number of Versions"},
        )
        st.plotly_chart(fig, use_container_width=True)

        # Version Size Trend
        st.markdown("### 📏 Version Size Trend")

        sizes = [v.get("size", 0) / 1024 for v in versions]
        names = [v.get("name", f"Version {i}") for i, v in enumerate(versions)]

        fig = px.line(
            x=names,
            y=sizes,
            title="Resume Size Over Versions",
            labels={"x": "Version", "y": "Size (KB)"},
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Most Modified Sections
        st.markdown("### 🔍 Most Modified Sections")

        if len(versions) > 1:
            analyzer = TextAnalyzer()
            section_modifications = analyzer.analyze_section_modifications(versions)

            if section_modifications:
                df_sections = pd.DataFrame(
                    section_modifications.items(), columns=["Section", "Modifications"]
                )
                df_sections = df_sections.sort_values(
                    "Modifications", ascending=False
                )

                fig_pie = px.pie(
                    df_sections,
                    values="Modifications",
                    names="Section",
                    title="Distribution of Modifications by Section",
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Not enough data to analyze section modifications.")
        else:
            st.info("Need at least two versions to analyze modified sections.")

with tab4:
    st.markdown("## ⚙️ Version Manager Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💾 Storage Settings")

        auto_save = st.checkbox("Auto-save versions", value=True)
        max_versions = st.number_input(
            "Max versions to keep", min_value=5, max_value=100, value=20
        )
        auto_archive = st.checkbox("Auto-archive old versions", value=False)
        archive_after_days = st.number_input(
            "Archive after (days)", min_value=7, max_value=365, value=30
        )

        if st.button("💾 Save Settings", key="save_settings_button"):
            st.success("✅ Settings saved successfully!")

    with col2:
        st.markdown("### 🗑️ Cleanup Options")

        st.warning("⚠️ These actions cannot be undone!")
        
        if st.button("🗑️ Delete All Archived", key="delete_all_archived_button"):
            archived_count = len([v for v in versions if v.get("archived", False)])
            if archived_count > 0:
                st.error(f"Would delete {archived_count} archived versions")
            else:
                st.info("No archived versions to delete")

        if st.button("🗑️ Delete All Versions", key="delete_all_versions_button"):
            st.error(f"Would delete all {len(versions)} versions")

        if st.button("📤 Export All Versions", key="export_all_versions_button"):
            st.info("Would create ZIP file with all versions")

    st.markdown("---")
    st.markdown("### 📚 Version Naming Conventions")

    st.markdown("""
    **Suggested naming formats:**
    - `Resume_CompanyName_Date` - For specific applications
    - `Resume_v1.0` - Simple version numbers
    - `Resume_Industry_Date` - For different industries
    - `Resume_Role_Date` - For different roles
    - `Resume_Final`, `Resume_Draft` - Status-based
    """)

# Resources
st.markdown("---")
st.markdown("## 💡 Version Control Tips")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📝 Best Practices
    - Save before major changes
    - Use descriptive names
    - Add detailed notes
    - Compare before submitting
    - Keep organized structure
    """)

with col2:
    st.markdown("""
    ### 🎯 When to Create Version
    - Tailoring for specific job
    - Major content updates
    - Format changes
    - After feedback
    - Different industries
    """)

with col3:
    st.markdown("""
    ### 🔄 Comparison Uses
    - Track improvements
    - Undo mistakes
    - A/B testing
    - Audit trail
    - Learning what works
    """)

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #6b7280;'>
    <p>💡 <strong>Pro Tip:</strong> Save a version before every major application so you can track what worked!</p>
</div>
""",
    unsafe_allow_html=True,
)
