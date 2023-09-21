from streamlit_authenticator import Authenticate
import streamlit as st
import traceback
import yaml

def read_configs(file):
    try:
        with open(file, 'r') as file:
            config = yaml.safe_load(file)

        return config
    except Exception as e:
        stacktrace = traceback.format_exc()

        print(stacktrace)

        raise e

config = read_configs("./configs.yaml")

## Check auth enabled
#
authenticator = authenticator = Authenticate(
    config['auth']['credentials'],
    config['auth']['cookie']['name'],
    config['auth']['cookie']['key'],
    config['auth']['cookie']['expiry_days'],
)

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    ## Render frontend
    #
    authenticator.logout('Logout', 'main')
    url = "https://ddna-amazon-web-services--stellaautoexpert.soului.dh.soulmachines.cloud/?sig=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODY3Njc4NTcsImlzcyI6InNpZ25lZF91cmwtM2U2YmMwZjMtNjE2Zi00YWVmLWI1YzAtMDMzY2QzZWE1YWZiIiwiZXhwIjoxNzczMDgxNDU3LCJlbWFpbCI6ImFtYXpvbi13ZWItc2VydmljZXMtLXN0ZWxsYWF1dG9leHBlcnRAZGRuYS5zdHVkaW8iLCJzb3VsSWQiOiJkZG5hLWFtYXpvbi13ZWItc2VydmljZXMtLXN0ZWxsYWF1dG9leHBlcnQifQ.X1EpnYkFm5HFn3OcsNxzaV461T2WI3rUNeNS-subozM"
    st.markdown("[Talk with Stella](%s)" % url)
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
