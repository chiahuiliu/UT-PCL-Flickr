##############################################
# This is the python file for Flickr crawling
# Author @ Chia-Hui Liu (GitHub: chiahuiliu)
# the Flickr we are interested: 146634855@N06
##############################################

# import packages
import flickrapi
import json
import pandas as pd
import urllib.request
from progressbar import ProgressBar


def build_connection():
	# This function is used to build the connection and authorization from Flickr
	api_key = ### your api key here ###
	api_secret = ### your api secret here ###
	flickr = flickrapi.FlickrAPI(api_key,api_secret,cache=True)
	return flickr

def check_num_records(flickr, user_accont):
	# check how many records
	page_obj = flickr.photos.search(user_id=user_accont,
                           format='json',
                           extras='url_c',
                           per_page=1)
	page_obj = page_obj.decode('utf8').replace("'", '"')
	page_json = json.loads(page_obj)
	pages = json.dumps(page_json, indent=4, sort_keys=True)
	pages = json.loads(pages)
	total_records = pages['photos']['pages']
	return total_records

def get_record_info(flickr, user_accont, total_records):
	'''
	This is used to get all record information
	'''
	id_list=[]
	pbar = ProgressBar()
	for i in pbar(range(total_records)):
		obj = flickr.photos.search(user_id=user_accont,
	                           format='json',
	                           extras='url_c',
	                           per_page=1,
	                           page=1)
		obj = obj.decode('utf8').replace("'", '"')
		data = json.loads(obj)
		res = json.dumps(data, indent=4, sort_keys=True)
		res = json.loads(res)
		photo_dict = dict(res['photos']['photo'][0])
		id_list.append([photo_dict.get('id'), photo_dict.get('title'), photo_dict.get('url_c')])
	return id_list



if __name__ == "__main__":
	print("Building and asking authorization...")
	flickr = build_connection()
	print("Getting record counts....")
	records = check_num_records(flickr, '146634855@N06')
	print("Getting record information...")
	# Here, the variable record_info contains the id, title, and the link
	record_info = get_record_info(flickr, '146634855@N06', records)
	# convert the results into DataFrame
	record_info_df = pd.DataFrame(record_info, columns=['id', 'title', 'url'])
	# save the resutls to csv file
	record_info_df.to_csv('flickr_brief_record.csv', index=False)
