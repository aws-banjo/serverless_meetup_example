import streamlit as st
import requests


def call_api(meetup_group):

    data = {"meetup_id": meetup_group}
    api_endpoint = (
        "YOUR ENDPOINT"
    )

    resp = requests.post(api_endpoint, json=data)
    print(resp.json())

    return resp.json()


def main() -> None:
    """
    Purpose:
        Controls the flow of the streamlit app
    Args:
        N/A
    Returns:
        N/A
    """

    # Start the streamlit app
    st.header("Meetup Data")

    meetup_groups = [
        "amazon-web-services-dmv",
        "the-boston-amazon-web-services-meetup-group",
        "AWS-NYC",
    ]

    selected_meetup = st.selectbox("Meetups", meetup_groups)

    if st.button("Get Meetup Data"):
        data = call_api(selected_meetup)
        st.write(data)


if __name__ == "__main__":
    main()
