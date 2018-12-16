# Basic fb business SDK usage example
# The SKD must be installed first. See: https://github.com/facebook/facebook-python-business-sdk

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign as AdCampaign
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.advideo import AdVideo
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
import config

import pprint

pp = pprint.PrettyPrinter(indent=4)

my_app_id = config.my_app_id
my_app_secret = config.my_app_secret
my_access_token = config.my_access_token
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount(config.my_account)
#print('>>> Reading permissions field of user:')
#pp.pprint(me.remote_read(fields=[AdUser.Field.permissions]))
ads = my_account.get_ads()
print(ads)

creatives = my_account.get_ad_creatives(fields=[AdCreative.Field.video_id])
for creative in creatives:
    video_id = creative[AdCreative.Field.video_id]
    print("video_id:", video_id)

videos = my_account.get_ad_videos(fields=[AdVideo.Field.permalink_url])
print videos
for video in videos:
    print("video_url:", video[AdVideo.Field.permalink_url])


'''
print(">>> Campaign Stats")
for campaign in my_account.get_ad_campaigns(fields=[AdCampaign.Field.name]):
    for stat in campaign.get_stats(fields=[
        'impressions',
        'clicks',
        'spent',
        'unique_clicks',
        'actions',
    ]):
        print(campaign[campaign.Field.name])
        for statfield in stat:
            print("\t%s:\t\t%s" % (statfield, stat[statfield]))
'''
