import requests
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Replace "your_api_key_here" with your actual OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_key"

llm = ChatOpenAI()

class SkiVacationApp:
    def make_recommendations(self):
        # Get user input
        skiing_ability = input("Rate your skiing abilities Using this scale: Beginner, Intermediate, Advanced, Expert: ")
        num_guests = int(input("Enter the number of guests: "))
        skiing_preferences = input("Enter Ski Preferences (Moguls, Trees, or Groomers): ")
        town_importance = input("Rate the importance of the ski town from: Not Important, Somewhat Important, Very Important, Most Important: ")
        vacationLength = input("How Long will your vacation be?")
        budget = int(input("input the maximum amount willing to spend on entire vacation: "))
        #NEED WORK:  RELATE BUDGET TO RESORT INTO TIERS FOR LODGING, FOOD, ETC.        
        
        # rank Resorts based on input
        ranked_resort = self.rank_resorts(skiing_ability, budget, num_guests, skiing_preferences, town_importance)
        print(ranked_resort)
        location = input("Please select your resort from the list of rankings for more recommendations: ")

        resortDF = pd.read_csv ('skiResortData.csv')
        resortDF['resort_name'] = resortDF['resort_name'].str.split(',').str[0]
        # isValidResort = location in [resortDF['resort_name']]
        #FIX TO CHECK IF RESORT SELECTED IS REAL
        
        #Make Recs
        print("\nRecommendations:")
        print(f"- Food:", self.food_recommendations(location,budget,num_guests))
        print(f"- Lodging:", self.lodging_recommendations(location,budget,num_guests))
        print(f"- Equipment Rentals:", self.equipment_recommendations(location,budget,num_guests,skiing_ability))
        print(f"- Nearby Amenities:", self.ammenities_recommendations(location, budget, num_guests))
        print(f"Predicted Lift Queue Time:", self.predict_lift_queue(location,skiing_ability,num_guests,skiing_preferences))

    
    def rank_resorts(self, skiing_ability, budget, num_guests, ski_preferences, town_importance):
        prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """
         You recommend ski resorts based on skiing_ability, budget, number of guests, ski preferences, town Importance, and average snowfall. 
         The user will provide this info as a list, in this structure: [skiing_ability, budget, number of guests, ski preferences, town Importance].
         You can only select from resorts in the United States, and the resort must exist.
        Output the result as a ranking from 1 to 5.
         """),
         ("user", "{input}")
        ])
        #Create Output Parser
        output_parser = StrOutputParser()
        #Create Chain
        chain = prompt | llm | output_parser
        #Combine Inputs
        fullInput = [skiing_ability,budget, num_guests, ski_preferences, town_importance]
        
        #Invoke chain to get resort rankings
        resortsRanked = chain.invoke({"input": fullInput})

        return resortsRanked
    
    def predict_lift_queue(self, location, skiing_ability, num_guests, ski_preferences):
        # Divide Resort Dataframe into tiers
        # Higher tier (more popular) should reflect higher wait times, especially for beginner/intermediate terrain
        #Return lift queue based on location tier, num guests, and ski ability/preferences
        return "Short"
    
    def food_recommendations(self,location,budget,num_guests):
        prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """
            You recommend resturants and food spots in ski towns for a given location.
            The user will provie a location, budget, and number of guests as a list in this format: [location,budget, num_guests].
            You will return a list of the best potential resturants in the area, taking into consideration the budget and the review for the resturaunt.
            Every resturant you recommend must exist, and be near the location provided.
         """),
         ("user", "{input}")
        ])
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        fullInput = [location,budget, num_guests]
        
        foodRecs = chain.invoke({"input": fullInput})
        return foodRecs
    
    def lodging_recommendations(self,location,budget,num_guests):
        prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """
            You recommend lodging and hotels in ski towns for a given location.
            The user will provie a location, budget, and number of guests as a list in this format: [location,budget, num_guests].
            You will return a list of potential lodging and hotels in the area, taking into consideration the budget.
            Every resturant you recommend must exist, and be near the location provided.
         """),
         ("user", "{input}")
        ])
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        fullInput = [location,budget, num_guests]
        
        lodgingRecs = chain.invoke({"input": fullInput})
        return lodgingRecs
    
    def equipment_recommendations(self,location,budget,num_guests,start_date,end_date,skiing_ability):
        #LLM call to recommend equipment rentals
        return 0
    
    def ammenities_recommendations(self,location,budget,num_guests,start_date,end_date):
        #LLM call to recommend ammenities
        return 0

if __name__ == "__main__":
    app = SkiVacationApp()
    app.make_recommendations()