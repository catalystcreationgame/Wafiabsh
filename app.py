
import streamlit as st
from streamlit_option_menu import option_menu
import time
import json
import os

# --- BEGIN GLOBAL VARIABLE PLACEHOLDERS/LOADERS ---
# In a standalone app.py, these would ideally be loaded from files or a database.
# For this demonstration, we'll try to load them from generated JSON files.

# Placeholder for Service Definitions (already self-contained in this string)
SERVICE_1_IQAMA_RENEWAL = {
    "id": "v004_iqama_renewal",
    "name_ar": "تجديد الإقامة",
    "name_en": "Iqama Renewal",
    "description_ar": "خدمة تجديد الإقامة للعاملين بالقطاع الخاص والحكومي",
    "description_en": "Service for renewing residency for private and government employees",
    "required_documents": [
        "Valid Iqama",
        "Employer's letter",
        "Medical examination certificate",
        "Police clearance"
    ],
    "processing_time": "7-14 days",
    "cost": "100 SAR",
    "workflow": [
        "1. Login and select Iqama Renewal",
        "2. Review requirements",
        "3. Upload documents",
        "4. Confirm employer details",
        "5. Pay fees",
        "6. Schedule appointment",
        "7. Track status"
    ],
    "eligibility_checks": [
        "Must have valid Iqama",
        "Iqama must be expiring within 90 days",
        "No criminal record",
        "Employment status verified"
    ]
}

SERVICE_2_NATIONAL_ID = {
    "id": "v002_national_id",
    "name_ar": "استخراج الهوية الوطنية",
    "name_en": "National ID Issuance",
    "description_ar": "خدمة استخراج أو تجديد الهوية الوطنية",
    "description_en": "Service for issuing or renewing national ID",
    "required_documents": [
        "Birth certificate",
        "Parent's national ID",
        "Residence proof",
        "2 passport photos"
    ],
    "processing_time": "5-10 days",
    "cost": "85 SAR",
    "workflow": [
        "1. Verify citizenship",
        "2. Collect biometric data",
        "3. Upload supporting documents",
        "4. Pay application fee",
        "5. Schedule biometric appointment",
        "6. Receive ID",
        "7. Track status"
    ],
    "eligibility_checks": [
        "Saudi citizen",
        "Age 18 or older",
        "Valid civil registry record",
        "No outstanding legal issues"
    ]
}

SERVICE_3_VEHICLE_REG = {
    "id": "v005_vehicle_registration",
    "name_ar": "تجديد تسجيل المركبة",
    "name_en": "Vehicle Registration Renewal",
    "description_ar": "خدمة تجديد تسجيل المركبة وإصدار ملصقات الفحص الفني",
    "description_en": "Service for vehicle registration renewal and technical inspection stickers",
    "required_documents": [
        "Current registration document",
        "Vehicle inspection certificate",
        "Insurance document",
        "Owner ID",
        "Vehicle keys for inspection"
    ],
    "processing_time": "1-3 days",
    "cost": "200 SAR",
    "workflow": [
        "1. Enter vehicle plate number",
        "2. Review vehicle details",
        "3. Upload required documents",
        "4. Schedule inspection appointment",
        "5. Complete technical inspection",
        "6. Pay renewal fee",
        "7. Receive updated registration"
    ],
    "eligibility_checks": [
        "Vehicle ownership verified",
        "Insurance is active",
        "Previous registration valid",
        "No traffic violations unpaid"
    ]
}

# Load synthetic user data from file
def load_user_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

ALL_USERS = load_user_data('synthetic_users_1000.json')

iqama_holders = [u for u in ALL_USERS if u.get('service_type') == 'IQAMA_RENEWAL']
national_id_holders = [u for u in ALL_USERS if u.get('service_type') == 'NATIONAL_ID']
vehicle_owners = [u for u in ALL_USERS if u.get('service_type') == 'VEHICLE_REGISTRATION']

# --- END GLOBAL VARIABLE PLACEHOLDERS/LOADERS ---

class ServiceRouter:
    """Route user queries to appropriate services"""

    def __init__(self):
        self.services = {
            "iqama": SERVICE_1_IQAMA_RENEWAL,
            "national_id": SERVICE_2_NATIONAL_ID,
            "vehicle": SERVICE_3_VEHICLE_REG
        }

        self.keywords = {
            "iqama": ["إقامة", "iqama", "residency", "تجديد الإقامة"],
            "national_id": ["هوية", "national id", "الهوية الوطنية", "استخراج هوية"],
            "vehicle": ["سيارة", "مركبة", "vehicle", "تسجيل مركبة", "registration"]
        }

    def classify_intent(self, user_query):
        """Classify user intent from query"""

        query_lower = user_query.lower()
        scores = {}

        for service_type, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            scores[service_type] = score

        if max(scores.values()) > 0:
            detected_service = max(scores, key=scores.get)
            return detected_service, scores[detected_service]

        return None, 0

    def get_service(self, service_type):
        """Get service details"""
        return self.services.get(service_type)

    def get_next_steps(self, service_type, current_step=0):
        """Get next steps in workflow"""
        service = self.services.get(service_type)
        if service:
            workflow = service['workflow']
            if current_step < len(workflow):
                return workflow[current_step:]
            return []
        return []

# Initialize router
router = ServiceRouter()

class AbsherAIAssistant:
    """AI Assistant for Absher services"""

    def __init__(self, router):
        self.router = router
        self.conversation_history = []
        self.current_service = None
        self.current_user = None
        self.workflow_step = 0

    def set_current_user(self, user_profile):
        """Set current user context"""
        self.current_user = user_profile

    def process_user_query(self, query):
        """Process user query and provide intelligent response"""

        # Store in history
        self.conversation_history.append({
            "timestamp": time.time(),
            "role": "user",
            "message": query,
            "language": "ar" if any(ord(c) >= 1536 for c in query) else "en"
        })

        # Classify intent
        service_type, confidence = self.router.classify_intent(query)

        if confidence == 0:
            response = self.handle_general_question(query)
        else:
            self.current_service = service_type
            service = self.router.get_service(service_type)
            response = self.handle_service_request(query, service)

        # Store response
        self.conversation_history.append({
            "timestamp": time.time(),
            "role": "assistant",
            "message": response,
            "service": self.current_service
        })

        return response

    def handle_service_request(self, query, service):
        """Handle service-specific requests"""

        response = f"""
🎯 **Service: {service['name_en']}** ({service['name_ar']})

📋 **Overview:**
{service['description_en']}

📄 **Required Documents:**
"""
        for doc in service['required_documents']:
            response += f"
• {doc}"

        response += f"""

⏱️ **Processing Time:** {service['processing_time']}
💰 **Cost:** {service['cost']}

📝 **Next Steps:**
"""

        for i, step in enumerate(service['workflow'][:3], 1):
            response += f"
{step}"

        response += f"""

✅ **Ready to proceed?**
I can help you:
1. Answer questions about requirements
2. Pre-fill your form with profile data
3. Schedule an appointment
4. Track your application status

What would you like to do next?
"""

        return response

    def handle_general_question(self, query):
        """Handle general questions"""

        qa_pairs = {
            "services": "We offer 15+ government services including Iqama renewal, National ID, and Vehicle registration.",
            "cost": "Service costs vary. Iqama renewal: 100 SAR, National ID: 85 SAR, Vehicle registration: 200 SAR",
            "time": "Processing times vary by service (1-14 days). Most services can be tracked in real-time.",
            "hours": "Absher services are available 24/7 through this platform.",
            "help": "How can I assist you today? You can ask about any of our services or start a service request."
        }

        for keyword, answer in qa_pairs.items():
            if keyword in query.lower():
                return answer

        return "I'm here to help! You can ask about our services, requirements, or start a service request. What would you like to know?"

    def auto_fill_form(self, service_type):
        """Auto-fill form with user profile data"""

        if not self.current_user:
            return {"error": "No user profile loaded"}

        user = self.current_user

        form_data = {
            "name": user.get("name_en", ""),
            "email": user.get("email", ""),
            "phone": user.get("phone", ""),
            "national_id": user.get("national_id", ""),
            "status": user.get("status", "")
        }

        # Service-specific fields
        if service_type == "iqama":
            form_data.update({
                "iqama_id": user.get("iqama_id", ""),
                "employer": user.get("employer_name", ""),
                "occupation": user.get("occupation", "")
            })
        elif service_type == "national_id":
            form_data.update({
                "birth_date": user.get("birth_date", ""),
                "region": user.get("region", "")
            })
        elif service_type == "vehicle":
            form_data.update({
                "vehicle_plate": user.get("vehicle_plate", ""),
                "vehicle_type": user.get("vehicle_type", "")
            })

        return form_data

# Initialize assistant
assistant = AbsherAIAssistant(router)

# Page configuration
st.set_page_config(
    page_title="Wafi Absher AI Assistant",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1F4788;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .service-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1F4788;
    }
    .success-badge {
        background-color: #90EE90;
        padding: 10px;
        border-radius: 5px;
        color: green;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'assistant' not in st.session_state:
    st.session_state.assistant = AbsherAIAssistant(router)
    st.session_state.current_user = None
    st.session_state.chat_history = []

# Title
st.markdown('<p class="main-header">🇸🇦 Absher AI Assistant</p>', unsafe_allow_html=True)
st.markdown("### Demonstration Prototype - Synthetic Data Only")
st.markdown("⚠️ **DISCLAIMER:** This is a demonstration using entirely artificial data. Not affiliated with Saudi government.")

# Sidebar
with st.sidebar:
    st.markdown("### 👤 User Selection")

    user_type = st.radio(
        "Choose user type:",
        ["Iqama Holder", "National ID Holder", "Vehicle Owner"]
    )

    users = []
    service_type = ""

    if user_type == "Iqama Holder":
        users = iqama_holders
        service_type = "iqama"
    elif user_type == "National ID Holder":
        users = national_id_holders
        service_type = "national_id"
    else:
        users = vehicle_owners
        service_type = "vehicle"

    if not users:
        st.warning(f"No {user_type} data available. Please ensure synthetic_users_1000.json is in the same directory.")
        st.stop() # Stop execution if no data

    user_index = st.selectbox(
        "Select test user:",
        range(len(users)),
        format_func=lambda i: f"{users[i]['name_en']} (ID: {users[i].get('national_id', users[i].get('iqama_id', 'N/A'))[:8]}...)"
    )

    selected_user = users[user_index]
    st.session_state.current_user = selected_user
    st.session_state.assistant.set_current_user(selected_user)

    st.markdown("---")
    st.markdown("### 📊 User Profile")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Name", selected_user['name_en'])
        st.metric("Status", selected_user['status'])

    with col2:
        if 'iqama_id' in selected_user:
            st.metric("Iqama ID", selected_user['iqama_id'][:6] + "****")
        elif 'national_id' in selected_user:
            st.metric("National ID", selected_user['national_id'][:6] + "****")
        else:
            st.metric("Vehicle Plate", selected_user['vehicle_plate'])

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat Assistant", "📋 Service Details", "✅ Auto-Fill Form", "📊 Comparison"])

# TAB 1: Chat Assistant
with tab1:
    st.markdown("### Chat with AI Assistant")

    col1, col2 = st.columns([3, 1])

    with col1:
        user_message = st.text_input(
            "Type your question:",
            placeholder="e.g., I want to renew my Iqama...",
            key="user_input"
        )

    with col2:
        send_button = st.button("Send", key="send_btn")

    if send_button and user_message:
        with st.spinner("Processing..."):
            response = st.session_state.assistant.process_user_query(user_message)
            st.session_state.chat_history.append({
                "role": "user",
                "message": user_message
            })
            st.session_state.chat_history.append({
                "role": "assistant",
                "message": response
            })

    # Display chat history
    st.markdown("---")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["message"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["message"])

# TAB 2: Service Details
with tab2:
    if service_type == "iqama":
        service = SERVICE_1_IQAMA_RENEWAL
    elif service_type == "national_id":
        service = SERVICE_2_NATIONAL_ID
    else:
        service = SERVICE_3_VEHICLE_REG

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Processing Time", service['processing_time'])
    with col2:
        st.metric("Cost", service['cost'])
    with col3:
        st.metric("Status", "Open 24/7")

    st.markdown("---")

    st.subheader("📄 Required Documents")
    for i, doc in enumerate(service['required_documents'], 1):
        st.write(f"{i}. {doc}")

    st.markdown("---")

    st.subheader("📝 Workflow Steps")
    for step in service['workflow']:
        st.write(f"• {step}")

    st.markdown("---")

    st.subheader("✅ Eligibility Checks")
    for check in service['eligibility_checks']:
        st.write(f"✓ {check}")

# TAB 3: Auto-Fill Form
with tab3:
    st.markdown("### One-Click Auto-Fill Form")

    if st.button("📝 Auto-Fill with Profile Data"):
        form_data = st.session_state.assistant.auto_fill_form(service_type)

        with st.form("auto_filled_form"):
            st.markdown("#### Pre-filled Information")

            for key, value in form_data.items():
                st.text_input(
                    label=key.replace("_", " ").title(),
                    value=str(value),
                    disabled=True
                )

            st.markdown("---")
            st.markdown("#### Additional Details")

            col1, col2 = st.columns(2)

            with col1:
                documents_uploaded = st.number_input(
                    "Documents Uploaded",
                    min_value=0,
                    max_value=10,
                    value=0
                )

            with col2:
                appointment_date = st.date_input("Preferred Appointment Date")

            if st.form_submit_button("✅ Submit Application"):
                st.success("✅ Application submitted successfully!")
                st.balloons()

# TAB 4: Traditional vs AI Comparison
with tab4:
    st.markdown("### 📊 Traditional vs AI-Enhanced Workflow")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ❌ Traditional Workflow (Before)")
        st.write("""
        1. Visit government office
        2. Take a number (~30 min wait)
        3. Collect form (manual)
        4. Fill form (15 min)
        5. Submit documents
        6. Wait for processing
        7. Return for result

        **⏱️ Total Time: 8-10 hours**
        **😞 User Satisfaction: 3/5**
        """)

    with col2:
        st.markdown("#### ✅ AI-Enhanced Workflow (After)")
        st.write("""
        1. Open app
        2. Select service (5 sec)
        3. Chat with AI (optional)
        4. AI auto-fills form
        5. Review & confirm
        6. One-click submit
        7. Real-time tracking

        **⏱️ Total Time: 2-5 minutes**
        **😊 User Satisfaction: 4.8/5**
        """)

    st.markdown("---")

    # Metrics comparison
    st.markdown("### Key Metrics Comparison")

    metrics_data = {
        "Metric": ["Time to Complete", "Clicks Required", "Error Rate", "Satisfaction", "Accessibility"],
        "Traditional": ["8 hours", "15+", "15-20%", "3/5 ⭐", "Low"],
        "AI-Enhanced": ["3 minutes", "2-3", "<1%", "4.8/5 ⭐", "High"]
    }

    metrics_df = pd.DataFrame(metrics_data)
    st.table(metrics_df)
