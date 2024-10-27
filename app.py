import streamlit as st
import re
import requests
import whois
from bs4 import BeautifulSoup
import socket
import ssl
from datetime import datetime, timedelta

def extract_features(url):
    features = {}
    
    # Check if the URL has an IP address
    features['having_IP_Address'] = 1 if re.search(r'(\d{1,3}\.){3}\d{1,3}', url) else -1
    
    # URL Length
    features['URL_Length'] = 1 if len(url) < 54 else -1
    
    # Shortening Service
    shorteners = ["bit.ly", "tinyurl", "goo.gl", "ow.ly", "t.co", "is.gd", "buff.ly"]
    features['Shortening_Service'] = -1 if any(short in url for short in shorteners) else 1
    
    # Check if "@" symbol is in the URL
    features['having_At_Symbol'] = -1 if "@" in url else 1
    
    # Prefix/Suffix in domain
    features['Prefix_Suffix'] = -1 if '-' in url.split('/')[2] else 1
    
    # SSL Certificate
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=url) as s:
            s.connect((url, 443))
            cert = s.getpeercert()
            expiry_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            features['SSLfinal_State'] = 1 if expiry_date > datetime.now() + timedelta(days=365) else -1
    except:
        features['SSLfinal_State'] = -1
    
    # Domain registration length
    try:
        domain_info = whois.whois(url)
        expiry_date = domain_info.expiration_date if isinstance(domain_info.expiration_date, datetime) else domain_info.expiration_date[0]
        features['Domain_registration_length'] = 1 if (expiry_date - domain_info.creation_date).days > 365 else -1
    except:
        features['Domain_registration_length'] = -1
    
    # Age of domain
    try:
        creation_date = domain_info.creation_date if isinstance(domain_info.creation_date, datetime) else domain_info.creation_date[0]
        age_days = (datetime.now() - creation_date).days
        features['age_of_domain'] = 1 if age_days > 180 else -1
    except:
        features['age_of_domain'] = -1
    
    # Check for Request URL
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        total_links = len(soup.find_all(['img', 'video', 'audio']))
        external_links = sum(1 for link in soup.find_all(['img', 'video', 'audio']) if url not in link.get('src', ''))
        features['Request_URL'] = 1 if external_links < total_links * 0.5 else -1
        
        # URL of Anchor
        total_anchors = len(soup.find_all('a'))
        external_anchors = sum(1 for anchor in soup.find_all('a') if url not in anchor.get('href', ''))
        features['URL_of_Anchor'] = 1 if external_anchors < total_anchors * 0.5 else -1
        
        # Links in tags
        features['Links_in_tags'] = 1 if sum(1 for tag in ['meta', 'script', 'link'] if url not in soup.get(tag, '')) == 0 else -1
        
        # Submitting_to_email
        features['Submitting_to_email'] = -1 if soup.find('form', action=re.compile("mailto:")) else 1
        
        # Abnormal_URL
        features['Abnormal_URL'] = -1 if " " in url else 1
        
        # Redirect
        features['Redirect'] = -1 if len(soup.find_all('meta', attrs={"http-equiv": "refresh"})) > 0 else 1
    except:
        features.update({
            'Request_URL': -1, 'URL_of_Anchor': -1, 'Links_in_tags': -1,
            'Submitting_to_email': -1, 'Abnormal_URL': -1, 'Redirect': -1
        })
    
    # Check for onMouseOver event
    features['on_mouseover'] = -1 if "onmouseover" in response.text else 1
    
    # RightClick
    features['RightClick'] = -1 if "contextmenu" in response.text else 1
    
    # Iframe
    features['Iframe'] = -1 if len(soup.find_all('iframe')) > 0 else 1

    # Web Traffic
    try:
        alexa_url = f"http://data.alexa.com/data?cli=10&url={url}"
        alexa_response = requests.get(alexa_url)
        features['web_traffic'] = 1 if '<REACH RANK="' in alexa_response.text else -1
    except:
        features['web_traffic'] = -1

    # Google Index
    try:
        google_response = requests.get(f"https://www.google.com/search?q=site:{url}")
        features['Google_Index'] = 1 if google_response.status_code == 200 and "did not match any documents" not in google_response.text else -1
    except:
        features['Google_Index'] = -1
    
    # Statistical Report
    features['Statistical_report'] = -1 if suspicious_pattern_check(url) else 1
    
    # Check for login keywords
    features['login_keyword'] = -1 if 'login' in url else 1
    
    # Check for security keywords
    features['security_keywords'] = -1 if any(keyword in url for keyword in ['secure', 'login', 'signin']) else 1

    # Check for special characters
    features['special_characters'] = 1 if re.search(r'[!@#$%^&*(),.?":{}|<>]', url) else -1

    # Number of dots in URL
    features['number_of_dots'] = url.count('.')
    
    # Check for suspicious top-level domain
    suspicious_tlds = ['.cn', '.xyz', '.info', '.top', '.click', '.date']
    features['suspicious_TLD'] = -1 if any(url.endswith(tld) for tld in suspicious_tlds) else 1

    # Check for numeric values in URL
    features['numeric_in_URL'] = 1 if any(char.isdigit() for char in url) else -1

    # Check for redirection chains
    features['Redirection_Chain'] = 1 if url.startswith('http://') else -1

    # Subdomain count
    subdomains = url.split('.')
    features['subdomain_count'] = len(subdomains) - 2 if len(subdomains) > 2 else 0

    # Check for valid IP address format in URL
    features['valid_IP_format'] = 1 if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', url) else -1

    # Check if the URL is in a known phishing database
    features['phishing_database_check'] = -1 if phishing_database_check(url) else 1

    # Determine if the website is phishing or legitimate
    prediction = 1 if all(value == 1 for value in features.values()) else -1
    features['Prediction'] = prediction
    
    return features

def suspicious_pattern_check(url):
    suspicious_patterns = ["login", "signin", "bank", "account", "update"]
    return any(pattern in url.lower() for pattern in suspicious_patterns)

def phishing_database_check(url):
    return False  # Placeholder function; integrate with actual database check if available

# Streamlit App Interface
st.title("URL Phishing Detection App")
st.write("Enter a URL to check if it's phishing or legitimate.")

url_input = st.text_input("URL")

if st.button("Check"):
    if url_input:
        features = extract_features(url_input)
        st.subheader("Extracted Features")
        st.write(features)
        
        # Display prediction
        prediction = "Phishing" if features['Prediction'] == -1 else "Legitimate"
        st.write(f"**Prediction:** {prediction}")
    else:
        st.error("Please enter a URL.")

# Run this app using the command: streamlit run <script_name>.py
