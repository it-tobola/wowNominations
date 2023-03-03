import backend as b
import streamlit as st

# Set initial page configurations
st.set_page_config(page_title="TOBOLA WOW Nomination Form", layout='wide')

# Page Header
with st.container():
    left, right = st.columns(2)

    with left:
        st.header("WOW Nomination Form")
        st.write("Description")
    with right:
        st.image("images/wow.gif")

# WOW Award Form
st.header("Nominee Info")

# WOW Info Section of the Form
wow_info = st.form("Award Info")
wow_groups = ["teamwork", "humility", "caring", "integrity"]

with wow_info:
    # Filter to limit the employees to those who are based at a specific department
    with st.container():
        program = st.selectbox("Where does the nominee work?", options=b.programs, key="department")
        refreshed = st.form_submit_button(f"Refresh Site", use_container_width=True)

        # Create the dataframe of only the active employees who are based at the selected site
        ee_list = b.active_ee[b.active_ee['Home Base'] == program]

    # Select the specific employee you want to nominate
    with st.container():
        nominee = st.selectbox("Select the team member you want to nominate",
                               options=ee_list["Full Name"],
                               key="nominee")
        refreshed = st.form_submit_button("Refresh Staff", use_container_width=True)

# Submit Employee Selection
    nominee = st.session_state["nominee"]
    department = st.session_state["department"]

    st.subheader(f"WOW Award Submission for {nominee} - {department}")



# Description of how the nominee exemplified each wow group topic
for group in wow_groups:
    with wow_info.container():
        st.subheader(f"{group.upper()}")
        st.text_area(f"Describe how the nominee demonstrates excellence in the area of {group}. "
                     f"Please give examples.", key=group)

with wow_info.container():
    st.subheader("ACCOMPLISHMENTS / OTHER")
wow_info.text_area("List outstanding accomplishments, such as awards, letters of appreciation, etc.",
                     key="accomplishments")

nominator = wow_info.selectbox("Person submitting the form", options=b.active_ee["Full Name"], key="nominator")
ack_button = wow_info.checkbox("By checking this box, you acknowledge that all of the information above is correct to"
                                 " the best of your knowledge.",
                                 key='acknowledgement')

with wow_info:
    nominee = [st.session_state["nominee"]]
    department = [st.session_state["department"]]
    teamwork = [st.session_state['teamwork']]
    humility = [st.session_state['humility']]
    caring = [st.session_state['caring']]
    integrity = [st.session_state['integrity']]
    accomplishments = [st.session_state['accomplishments']]
    nominator = [st.session_state['nominator']]
    acknowledgement = [st.session_state['acknowledgement']]
    final = st.form_submit_button("Submit", use_container_width=True)
    if final and ack_button:
        import pandas as pd

        submission = pd.DataFrame(columns=['nominee',
                                            'department',
                                            'nominee ee',
                                            'teamwork',
                                            'humility',
                                            'caring',
                                            'integrity',
                                            'accomplishments',
                                            'nominator',
                                            'nominator department',
                                            'acknowledgement'])

        submission['nominee'] = nominee
        submission['department'] = department
        submission['teamwork'] = teamwork
        submission['humility'] = humility
        submission['caring'] = caring
        submission['integrity'] = integrity
        submission['accomplishments'] = accomplishments
        submission['nominator'] = nominator
        submission['acknowledgement'] = acknowledgement

        # Automated submission information
        submission['nominee ee'] = b.active_ee["EE Code"][b.active_ee['Full Name'] == format(nominee)[2:-2]].values
        submission['nominator department'] = b.active_ee["Home Base"][b.active_ee['Full Name'] == format(nominator)[2:-2]].values

        try:
            submission.to_notion(b.wow_url, api_key=b.notion_token, title='Test', resolve_relation_values=True)
            with st.sidebar:
                st.success('Request Submitted!', icon="✅")
                st.write("You can now close this screen")
        except:
            st.warning('Please try again', icon="⚠️")

    elif final and (ack_button == False):
        st.warning('Please confirm the checkbox to continue', icon="⚠️")
