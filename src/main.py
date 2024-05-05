import yaml
import streamlit as st
import streamlit_authenticator as stauth

with open("./.cred.yaml") as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    cookie_key=config["cookie"]["key"],
    cookie_expiry_days=config["cookie"]["expiry_days"],
    pre_authorized=config["pre-authorized"] if "pre-authorized" in config else None,
)


def login():
    authenticator.login()

    # Correct credentials for login
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title("Some content")

    # Incorrect credentials for login
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")

    # No credentials entered
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")


def main():
    login()


if __name__ == "__main__":
    main()
