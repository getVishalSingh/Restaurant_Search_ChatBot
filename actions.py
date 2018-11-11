from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import AllSlotsReset
from rasa_core.events import Restarted
from rasa_core.events import SlotSet
import zomatopy
import json
import smtplib
import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	def run(self, dispatcher, tracker, domain):
		config={ "user_key":"40d3c87042beb41426334eba18090f72"}
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price_lt = tracker.get_slot('price_lt')
		price_ut = tracker.get_slot('price_ut')
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'american':1,'chinese':25,'italian':55,'north indian':50,'south indian':85 ,'mexican':73}
		
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 5,0)
		d = json.loads(results)
		
		response=""
		mail_response = ""
		
		if d['results_found'] == 0:
			response= "no results"			

		elif ((price_lt ==None) & (price_ut==None)):
			response = "Sorry could not extract the price range"
		else:
			index = 0
			if price_lt != None:
				if price_ut != None:
					if price_ut < price_lt:
						price = price_lt
						price_lt = price_ut
						price_ut = price

			
			restaurants = d['restaurants']			
			for loop in [20, 40, 60, 80]:
				r = zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 10,loop)
				temp = json.loads(results)
				if temp['results_found'] > 0:
					restaurants.extend(temp['restaurants'])
			print (len(restaurants))				
			for restaurant in restaurants:
				price = restaurant['restaurant']['average_cost_for_two']
				if (price_lt != None):
					if (price < int(price_lt)):
						continue
				if (price_ut != None):
					if (price > int(price_ut)):
						continue
					
				
				if (index <= 5):
					response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" has been rated"+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
				if (index <= 10):
					mail_response = mail_response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+"with an average budget for two as" + str(restaurant['restaurant']['average_cost_for_two']) + "has been rated"+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
				index = index + 1
				if (index == 10): 
					break
		
		if (index == 0):
			response+="Could not find restaurants in the price range."
			mail_response+="Could not find restaurants in the price range."
		#response+="should I email you the details?"		
		dispatcher.utter_message("-----"+response)
		return [SlotSet('mail_response',mail_response)]
class ActionMailRestaurantDetails(Action):
	def name(self):
		return 'action_mailrestaurantdetails'
		
	def run(self, dispatcher, tracker, domain):
		config={ "user_key":"40d3c87042beb41426334eba18090f72"}
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price_lt = tracker.get_slot('price_lt')
		price_ut = tracker.get_slot('price_ut')
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'american':1,'chinese':25,'italian':55,'north indian':50,'south indian':85 ,'mexican':73}
		
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 20,0)
		d = json.loads(results)
		
		response=""
		mail_details = ""
		
		if d['results_found'] == 0:
			response= "no results"			

		elif ((price_lt ==None) & (price_ut==None)):
			response = "Sorry could not extract the price range"
		else:
			index = 0
			if price_lt != None:
				if price_ut != None:
					if price_ut < price_lt:
						price = price_lt
						price_lt = price_ut
						price_ut = price

			
			restaurants = d['restaurants']			
			for loop in [20, 40, 60, 80]:
				r = zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 20,loop)
				temp = json.loads(results)
				if temp['results_found'] > 0:
					restaurants.extend(temp['restaurants'])
			print (len(restaurants))				
			for restaurant in restaurants:
				price = restaurant['restaurant']['average_cost_for_two']
				if (price_lt != None):
					if (price < int(price_lt)):
						continue
				if (price_ut != None):
					if (price > int(price_ut)):
						continue
					
				
				if (index <= 5):
					response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" has been rated"+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
				if (index <= 10):
					mail_details = mail_details+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+"with an average budget for two as" + str(restaurant['restaurant']['average_cost_for_two']) + "has been rated"+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
				index = index + 1
				if (index == 10): 
					break
		
		if (index == 0):
			response+="Could not find restaurants in the price range."
			mail_details+="Could not find restaurants in the price range."
		#response+="should I email you the details?"		
		dispatcher.utter_message("-----"+response)
		return [SlotSet('mail_details',mail_details)]


class ActionCheckLocation(Action):

    tier1_tier2 = ["ahmedabad","bangalore","chennai","delhi","hyderabad","Kolkata","mumbai","pune",
        "agra","ajmer","aligarh","allahabad","amravati","amritsar","asansol","aurangabad","bareilly",
        "belgaum","bhavnagar","bhiwandi","bhopal","bhubaneswar","bikaner","bokaro steel city","chandigarh",
        "coimbatore","cuttack","dehradun","dhanbad","durg-bhilai nagar","durgapur","erode","faridabad", 
        "firozabad","ghaziabad","gorakhpur","gulbarga","guntur","gurgaon","gwalior","hubli-dharwad", 
        "indore","jabalpur","jaipur","jalandhar","jammu","jamnagar","jamshedpur","jhansi","jodhpur","kannur","kanpur",
        "kakinada","kochi","kottayam","kolhapur","kollam","kota","kozhikode","kurnool","lucknow","ludhiana","madurai",
        "malappuram","mathura","goa","mangalore","meerut","moradabad","mysore","nagpur","nanded","nashik","nellore",
        "noida","palakkad","patna","pondicherry","raipur","rajkot","rajahmundry","ranchi","rourkela","salem","sangli",
        "siliguri","solapur","srinagar","sultanpur","surat","thiruvananthapuram","thrissur","tiruchirappalli","guwahati",
        "tirunelveli","tiruppur","ujjain","vijayapura","vadodara","varanasi","vasai-virar City","vijayawada","visakhapatnam","warangal"]

    

    def __init__(self):
        self.all_cities = []
        f = open('all_cities.txt')
        for word in f.read().split():
            self.all_cities.append(word)
        

    
    
    def name(self):
        return 'action_location'
        
    def run(self, dispatcher, tracker, domain):

        loc = tracker.get_slot('location')
        if loc.lower() in self.tier1_tier2:
            return [SlotSet('location_match','one')]
        elif loc.lower() in self.all_cities:
            return [SlotSet('location_match','out')]

        #for city in self.tier1_tier2:
        #   if (loc.lower() == city):
        #       return [SlotSet('location_match','one')]
        
        return [SlotSet('location_match','zero')]

class ActionSendMail(Action):
    def name(self):
        return 'action_sendmail'
    def run(self, dispatcher, tracker, domain):
        email = tracker.get_slot('emailid')
        gmail_user = 'restchatbot007@gmail.com'
        gmail_password = 'Chat@P@ssw0rd1'
        sent_from = gmail_user
        to = [email]
        SUBJECT = "Top 10 restaurant list"
        message = "Test"
        TEXT = tracker.get_slot("mail_details")
        #print(TEXT)
        #print(email)
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to,message)
            server.close()
            print('Please check your mailbox!')
        except:
            print('Something went wrong...')
            
            
class ActionRestarted(Action):  
    def name(self):         
        return 'action_restarted'   
    def run(self, dispatcher, tracker, domain): 
        return[Restarted()] 
class ActionSlotReset(Action):  
    def name(self):         
        return 'action_slot_reset'  
    def run(self, dispatcher, tracker, domain):         
        return[AllSlotsReset()]
