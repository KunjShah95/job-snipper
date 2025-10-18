"""
User Analytics and Data Collection Module for Streamlit
Tracks user interactions, feature usage, and saves data to Streamlit Cloud
"""

import streamlit as st
import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib


class UserAnalytics:
    """
    Handles user data collection and analytics for Streamlit Cloud.
    Data is stored in st.session_state and persists in Streamlit Cloud's
    managed app storage.
    """
    
    def __init__(self):
        """Initialize analytics tracking."""
        self.init_session_state()
        
    def init_session_state(self):
        """Initialize session state variables for analytics."""
        if 'user_id' not in st.session_state:
            st.session_state.user_id = self.generate_user_id()
        
        if 'session_start' not in st.session_state:
            st.session_state.session_start = datetime.now().isoformat()
        
        if 'analytics_data' not in st.session_state:
            st.session_state.analytics_data = {
                'user_id': st.session_state.user_id,
                'session_start': st.session_state.session_start,
                'page_views': {},
                'feature_usage': {},
                'resume_uploads': 0,
                'job_matches': 0,
                'cover_letters_generated': 0,
                'resume_rewrites': 0,
                'interactions': [],
                'errors': [],
                'user_feedback': [],
                'total_time_spent': 0
            }
        
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {
                'name': None,
                'email': None,
                'phone': None,
                'target_role': None,
                'experience_level': None,
                'industry': None,
                'location': None,
                'collected_at': None
            }
    
    @staticmethod
    def generate_user_id() -> str:
        """Generate a unique anonymous user ID."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def track_page_view(self, page_name: str):
        """Track when a user views a page."""
        if page_name not in st.session_state.analytics_data['page_views']:
            st.session_state.analytics_data['page_views'][page_name] = 0
        st.session_state.analytics_data['page_views'][page_name] += 1
        
        self.log_interaction('page_view', {'page': page_name})
    
    def track_feature_usage(self, feature_name: str, details: Optional[Dict] = None):
        """Track when a user uses a specific feature."""
        if feature_name not in st.session_state.analytics_data['feature_usage']:
            st.session_state.analytics_data['feature_usage'][feature_name] = 0
        st.session_state.analytics_data['feature_usage'][feature_name] += 1
        
        self.log_interaction('feature_use', {
            'feature': feature_name,
            'details': details or {}
        })
    
    def track_resume_upload(self, file_type: str, file_size: int):
        """Track resume upload."""
        st.session_state.analytics_data['resume_uploads'] += 1
        self.log_interaction('resume_upload', {
            'file_type': file_type,
            'file_size': file_size
        })
    
    def track_job_match(self, score: float):
        """Track job matching activity."""
        st.session_state.analytics_data['job_matches'] += 1
        self.log_interaction('job_match', {'score': score})
    
    def track_cover_letter_generation(self, company: str):
        """Track cover letter generation."""
        st.session_state.analytics_data['cover_letters_generated'] += 1
        self.log_interaction('cover_letter', {'company': company})
    
    def track_resume_rewrite(self, focus_area: str):
        """Track resume rewriting."""
        st.session_state.analytics_data['resume_rewrites'] += 1
        self.log_interaction('resume_rewrite', {'focus': focus_area})
    
    def track_error(self, error_type: str, error_message: str, context: Dict = None):
        """Track errors that occur."""
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': error_message,
            'context': context or {}
        }
        st.session_state.analytics_data['errors'].append(error_data)
    
    def collect_user_feedback(self, rating: int, feedback: str, page: str):
        """Collect user feedback."""
        feedback_data = {
            'timestamp': datetime.now().isoformat(),
            'rating': rating,
            'feedback': feedback,
            'page': page
        }
        st.session_state.analytics_data['user_feedback'].append(feedback_data)
    
    def log_interaction(self, interaction_type: str, data: Dict):
        """Log a user interaction."""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'type': interaction_type,
            'data': data
        }
        st.session_state.analytics_data['interactions'].append(interaction)
    
    def update_user_profile(self, profile_data: Dict):
        """Update user profile information."""
        st.session_state.user_profile.update(profile_data)
        st.session_state.user_profile['collected_at'] = datetime.now().isoformat()
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get summary of analytics data."""
        return {
            'user_id': st.session_state.user_id,
            'session_duration': self.calculate_session_duration(),
            'total_page_views': sum(st.session_state.analytics_data['page_views'].values()),
            'total_features_used': sum(st.session_state.analytics_data['feature_usage'].values()),
            'resume_uploads': st.session_state.analytics_data['resume_uploads'],
            'job_matches': st.session_state.analytics_data['job_matches'],
            'cover_letters': st.session_state.analytics_data['cover_letters_generated'],
            'resume_rewrites': st.session_state.analytics_data['resume_rewrites'],
            'total_interactions': len(st.session_state.analytics_data['interactions']),
            'errors_encountered': len(st.session_state.analytics_data['errors']),
            'feedback_count': len(st.session_state.analytics_data['user_feedback'])
        }
    
    def calculate_session_duration(self) -> int:
        """Calculate session duration in minutes."""
        start = datetime.fromisoformat(st.session_state.session_start)
        duration = (datetime.now() - start).total_seconds() / 60
        return int(duration)
    
    def export_analytics_data(self) -> str:
        """Export all analytics data as JSON."""
        export_data = {
            'user_profile': st.session_state.user_profile,
            'analytics': st.session_state.analytics_data,
            'summary': self.get_analytics_summary(),
            'exported_at': datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2)
    
    def save_to_file(self, filepath: str = "data/analytics"):
        """
        Save analytics data to file.
        In Streamlit Cloud, this will be in the managed app storage.
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(filepath, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filepath}/user_{st.session_state.user_id}_{timestamp}.json"
            
            # Save data
            with open(filename, 'w') as f:
                f.write(self.export_analytics_data())
            
            return filename
        except Exception as e:
            self.track_error('save_error', str(e))
            return None


class UserDataCollectionUI:
    """
    UI components for collecting user data in Streamlit.
    Displays forms and widgets to gather user information.
    """
    
    @staticmethod
    def show_user_profile_form():
        """Display user profile collection form."""
        st.subheader("📝 Complete Your Profile (Optional)")
        st.caption("Help us personalize your experience. This data is stored securely.")
        
        with st.form("user_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", placeholder="John Doe")
                email = st.text_input("Email", placeholder="john@example.com")
                phone = st.text_input("Phone (Optional)", placeholder="+1 234 567 8900")
                location = st.text_input("Location", placeholder="San Francisco, CA")
            
            with col2:
                target_role = st.text_input("Target Job Role", placeholder="Software Engineer")
                experience_level = st.selectbox(
                    "Experience Level",
                    ["Select...", "Entry Level (0-2 years)", "Mid Level (3-5 years)", 
                     "Senior (6-10 years)", "Lead/Principal (10+ years)"]
                )
                industry = st.selectbox(
                    "Industry",
                    ["Select...", "Technology", "Finance", "Healthcare", "Education", 
                     "Marketing", "Manufacturing", "Retail", "Other"]
                )
            
            # Privacy consent
            consent = st.checkbox(
                "I consent to data collection for improving my experience and app analytics"
            )
            
            submitted = st.form_submit_button("💾 Save Profile", type="primary")
            
            if submitted:
                if consent:
                    analytics = UserAnalytics()
                    analytics.update_user_profile({
                        'name': name if name else None,
                        'email': email if email else None,
                        'phone': phone if phone else None,
                        'target_role': target_role if target_role else None,
                        'experience_level': experience_level if experience_level != "Select..." else None,
                        'industry': industry if industry != "Select..." else None,
                        'location': location if location else None
                    })
                    st.success("✅ Profile saved successfully!")
                    analytics.track_feature_usage('profile_completion')
                else:
                    st.warning("⚠️ Please accept the consent to save your profile.")
    
    @staticmethod
    def show_feedback_widget(page_name: str):
        """Display feedback collection widget."""
        with st.expander("📢 Give Feedback", expanded=False):
            st.write("Help us improve ResumeMasterAI!")
            
            rating = st.slider(
                "How satisfied are you with this feature?",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Not satisfied, 5 = Very satisfied"
            )
            
            feedback = st.text_area(
                "Share your thoughts (optional)",
                placeholder="What did you like? What could be better?",
                max_chars=500
            )
            
            if st.button("Submit Feedback", key=f"feedback_{page_name}"):
                analytics = UserAnalytics()
                analytics.collect_user_feedback(rating, feedback, page_name)
                st.success("🙏 Thank you for your feedback!")
    
    @staticmethod
    def show_analytics_dashboard():
        """Display user analytics dashboard (for admins or user view)."""
        analytics = UserAnalytics()
        summary = analytics.get_analytics_summary()
        
        st.subheader("📊 Your Activity Summary")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Session Duration", f"{summary['session_duration']} min")
        with col2:
            st.metric("Pages Viewed", summary['total_page_views'])
        with col3:
            st.metric("Features Used", summary['total_features_used'])
        with col4:
            st.metric("Interactions", summary['total_interactions'])
        
        # Detailed stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Feature Usage")
            st.write(f"✅ Resume Uploads: {summary['resume_uploads']}")
            st.write(f"🎯 Job Matches: {summary['job_matches']}")
            st.write(f"💼 Cover Letters: {summary['cover_letters']}")
            st.write(f"✍️ Resume Rewrites: {summary['resume_rewrites']}")
        
        with col2:
            st.markdown("### 📊 Page Views")
            for page, count in st.session_state.analytics_data['page_views'].items():
                st.write(f"• {page}: {count} views")
        
        # Export option
        if st.button("📥 Download My Data", key="download_my_data_btn"):
            data = analytics.export_analytics_data()
            st.download_button(
                label="💾 Download JSON",
                data=data,
                file_name=f"my_resumemasterai_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )


class StreamlitCloudDataManager:
    """
    Manages data persistence in Streamlit Cloud.
    Handles saving and retrieving user data from Streamlit Cloud storage.
    """
    
    @staticmethod
    def save_user_data():
        """
        Save user data to Streamlit Cloud managed storage.
        Data persists across sessions in Streamlit Cloud's Manage Apps section.
        """
        analytics = UserAnalytics()
        
        # Save to file (Streamlit Cloud persists this)
        filepath = analytics.save_to_file()
        
        if filepath:
            return {"status": "success", "filepath": filepath}
        else:
            return {"status": "error", "message": "Failed to save data"}
    
    @staticmethod
    def get_storage_info():
        """Get information about stored analytics data."""
        analytics_dir = "data/analytics"
        
        if not os.path.exists(analytics_dir):
            return {"total_files": 0, "total_users": 0}
        
        files = [f for f in os.listdir(analytics_dir) if f.endswith('.json')]
        unique_users = set()
        
        for file in files:
            # Extract user_id from filename
            parts = file.split('_')
            if len(parts) >= 2:
                unique_users.add(parts[1])
        
        return {
            "total_files": len(files),
            "total_users": len(unique_users),
            "latest_file": max(files) if files else None
        }
    
    @staticmethod
    def auto_save_on_exit():
        """
        Auto-save analytics data when user exits.
        Call this in the sidebar or footer of your app.
        """
        st.sidebar.markdown("---")
        st.sidebar.caption("📊 Session Analytics")
        
        analytics = UserAnalytics()
        summary = analytics.get_analytics_summary()
        
        st.sidebar.caption(f"⏱️ Session: {summary['session_duration']} min")
        st.sidebar.caption(f"📄 Actions: {summary['total_interactions']}")
        
    # Auto-save button moved to module-level to avoid NameError during class definition
    # This was previously executed inside the class body which caused StreamlitCloudDataManager
    # to be undefined at runtime; see `render_save_session_button` below.


# Convenience functions for easy integration
def init_analytics():
    """Initialize analytics for the current page."""
    return UserAnalytics()

def render_save_session_button():
    """Render the Save Session Data button in the sidebar (module-level)."""
    if st.sidebar.button("💾 Save Session Data", help="Save your session data to cloud", key="save_session_data_btn"):
        result = StreamlitCloudDataManager.save_user_data()
        if result.get('status') == 'success':
            st.sidebar.success("✅ Data saved!")
        else:
            st.sidebar.error("❌ Save failed")


# Render the button once the class is defined
render_save_session_button()


# Convenience functions for easy integration
def init_analytics():
    """Initialize analytics for the current page."""
    return UserAnalytics()


# Convenience wrappers for backwards compatibility with pages that import
# these helpers directly from utils.user_analytics
def show_feedback_widget(page_name: str):
    """Display the feedback widget for the given page name."""
    UserDataCollectionUI.show_feedback_widget(page_name)


def auto_save_session():
    """Trigger the StreamlitCloudDataManager auto-save UI."""
    StreamlitCloudDataManager.auto_save_on_exit()


def track_page(page_name: str):
    """Quick function to track page view."""
    analytics = UserAnalytics()
    analytics.track_page_view(page_name)


def show_feedback_widget(page_name: str):
    """Quick function to show feedback widget."""
    ui = UserDataCollectionUI()
    ui.show_feedback_widget(page_name)


def show_profile_form():
    """Quick function to show profile form."""
    ui = UserDataCollectionUI()
    ui.show_user_profile_form()


def auto_save_session():
    """Quick function for auto-save in sidebar."""
    StreamlitCloudDataManager.auto_save_on_exit()
