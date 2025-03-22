#def render_sidebar():
    # Display the Additional URLs section on the sidebar.
    #st.sidebar.header("Additional URLs")
    
    # Load the additional URLs (one per line) from environment variable or configuration
    #additional_urls = os.getenv("ADDITIONAL_URLS", "")
    #if additional_urls:
        #url_list = additional_urls.splitlines()
        #for url in url_list:
            #st.sidebar.write(url)
    #else:
        #st.sidebar.write("No additional URLs provided.") 
        
   #app.py     
        #from dotenv import load_dotenv

# Load environment variables from .env
#load_dotenv()

# Now import other modules that make use of API keys
#from backend import api  # as an example

#def main():
    # Start the application without needing to manually input any API keys.
    # All API key values are now automatically read from the .env file.
    #pass

#if __name__ == "__main__":
    #main()
    
   
   #api.py 
    #from utils.api_keys import API_KEY

#def perform_api_call(endpoint, params=None):
    #headers = {
        #"Authorization": f"Bearer {API_KEY}"
    #}
    # Perform the API call using the auto-loaded API key in the headers
    # Replace any code prompting the user for API key input with the above
    # Example:
    # response = requests.get(endpoint, headers=headers, params=params)
    # return response.json()
    #pass

# Other functions that use API_KEY should follow the same pattern.