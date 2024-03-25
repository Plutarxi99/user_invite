# from backend.src.core.config import settings
#
# irl = "https://app.hubspot.com/oauth/authorize?client_id=231d3627-3410-4f9d-bcf0-3f60f552021c&scope=contacts%20automation&redirect_uri=http://127.0.0.1:8000/docs#"
#
# from hubspot3 import Hubspot3
#
# API_KEY = settings.HUBSPOT_CLIENT_SECRET
#
# client = Hubspot3(api_key=API_KEY)
#
# # all of the clients are accessible as attributes of the main Hubspot3 Client
# contact = client.contacts.get_contact_by_email('shievanov@bk.ru')
# contact_id = contact['vid']
#
# all_companies = client.companies.get_all()
#
# # new usage limit functionality - keep track of your API calls
# client.usage_limits
# # <Hubspot3UsageLimits: 28937/1000000 (0.028937%) [reset in 22157s, cached for 299s]>
#
# client.usage_limits.calls_remaining
#
# url_all_users = "https://api.hubapi.com/crm/v3/objects/contacts/" # получить все контакты
