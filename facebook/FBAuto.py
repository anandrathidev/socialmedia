# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 21:16:00 2023

@author: arathi
"""


import json
import os

from pyfacebook import GraphAPI
# PAGEID = 106825752298751
#{
#  "name": "Ex-Muslim Murtad Apostate India",
#  "id": "106825752298751"
#}
704236071444139
USER_ID = "704236071444139"  # Your App ID
PAGE_ID = "106825752298751" # Test app
APP_ID = "551781136898046" # Test app
APP_SECRET = "3c2b38b140d3483c03d7bb5d9acdb8fe"  # Your App secret



# Your Access Token EAAH1146olZC4BAM23tbtvwI8vCOFAJZBsfDRfZAq6bJGMhDY4wrxflf4eeLVATUBlKtOxmnGkZAaacDwzAoR6MddXi9jjjYq83N91kfUEZCdjTHNus8JaBL62M7fhIX9r3wKB51VGmdWkLSH7hRrtDh0UuEO1upVsmtIzoinwIarKg9ZC3XVXosfvT69fhrYfj2G4VKhnGFJltvTpW0QQBlZCnxbTom2imMmeV6IZApIcHfmLsIFHIJb
USER_ACCESS_TOKEN = "EAAH1146olZC4BAFh70ZBZAvXDM9BdMKLzsIAGO05UHu6dyCoaTdz8nzt3QdKEFIuM6s430tvvYZAr5aYhHnEagkq0AoCu1AKY6STWJAUlozkjp8ppBPHLMt30AtuiA1TRJkhnIH13GfJiAIAeZBS1pi9cBEcjZCZAr0L1fJL66xxGDkl4U7l8ZAO"
PAGE_ACCESS_TOKEN = "EAAH1146olZC4BALr8BZA3wbSkf9fJjdy0iu03IrAtWAzESkTtvdIR67bdfztX3ggvZAeSTZAtRNZAiaZBZAezuZAOfnVeD6O01kQNP0PTZANdRCjjtmhxisyLtZA8MYkZCB2EDrAslZBRxKG3lNOP9k5ZAmoUipdWthjyuAuIODOTRAMvJLJssU3dE3Vu"
"""
Page ID	106825752298751 : Ex-Muslim Murtad Apostate India
App-Scoped User ID 704236071444139 : Kumar Ameet
"""

ACCESS_TOKEN = PAGE_ACCESS_TOKEN

"""
This new long-lived access token will expire on April 5, 2023:

From Graph Explorer tool, select the relevant permissions and get the short lived page access token.
Go to debugger tool and paste your access token. Then, click on 'Extend Token' button at the bottom of the page.
Copy the the extended token and use it in this API:
https://graph.facebook.com/v2.10/me?fields=access_token&access_token=<extended_access_token>
This should return you the permanent access token. You can verify it in debugger tool, the expires at field should say 'Never'.
"""

def handler(page_id):
    api = GraphAPI(app_id=None, app_secret=None, access_token=ACCESS_TOKEN)
    settings = api.get_object(object_id=f"{page_id}", fields="settings" )
    print(settings)
    post_result = api.post_object(object_id=f"{page_id}", connection="settings?option={USERS_CAN_MESSAGE: true}")
    print( "post_result {post_result} " )
    settings = api.get_object(object_id=f"{page_id}", fields="settings" )
    print(settings)
    post_result = api.post_object(object_id=f"{page_id}", connection="page_about_story?title=My Title &composed_text=[{text:My Story text., type:UNSTYLED, depth:0}]  &is_published=true")
    print( "post_result {post_result} " )
    
    #feed = api.get_full_connections(
    #    object_id=page_id,
    #    connection="groups",
    #    count=50,
    #    limit=25,
    #    fields="id,message,create_time",
    #)
    with open(f"./{page_id}.json", "w+") as f:
        print(settings)
        json.dump(settings, f)


def get_account_info():
    api = GraphAPI(app_id=None, app_secret=None, access_token=USER_ACCESS_TOKEN)
    result = api.get_object(object_id=f"{USER_ID}", fields="accounts" )
    print(result)

def get_page_settings():
    api = GraphAPI(app_id=None, app_secret=None, access_token=PAGE_ACCESS_TOKEN)
    result = api.get_object(object_id=f"{PAGE_ID}", fields="settings" )
    print(result)


if __name__ == "__main__":
    #handler(page_id="106825752298751")
    get_account_info()
    get_page_settings()
    
# Get page access     me?fields=accounts USERID = 704236071444139 PAGE_ID = 106825752298751 


# Code to get accounts 
# curl -i -X GET  "https://graph.facebook.com/v16.0/me/accounts?access_token=EAAH1146olZC4BAFh70ZBZAvXDM9BdMKLzsIAGO05UHu6dyCoaTdz8nzt3QdKEFIuM6s430tvvYZAr5aYhHnEagkq0AoCu1AKY6STWJAUlozkjp8ppBPHLMt30AtuiA1TRJkhnIH13GfJiAIAeZBS1pi9cBEcjZCZAr0L1fJL66xxGDkl4U7l8ZAO"


    
