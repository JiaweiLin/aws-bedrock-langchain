import streamlit as st

def load_config():
    """Load access keys from secrets file"""
    
    return {
        "aws_service_name": "bedrock-runtime",
        "aws_region_name": "us-east-1",
        "aws_access_key_id": st.secrets["AWS_ACCESS_KEY_ID"],
        "aws_secret_access_key": st.secrets["AWS_SECRET_ACCESS_KEY"],
    }