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
        lower_budget = int(input("input the minimum amount willing to spend on entire vacation: "))
        higher_budget = int(input("input the maximum amount willing to spend on entire vacation: "))
        budget = (lower_budget,higher_budget)
        
        

        # Extract relevant information
        ranked_resort = self.rank_resorts(skiing_ability, budget, num_guests, skiing_preferences, town_importance)
        print(ranked_resort)
        location = input("Please select your resort from the list of rankings for more recommendations: ")
        # resortDF = pd.read_csv ('skiResortData.csv')
        # resortDF['resort_name'] = resortDF['resort_name'].str.split(',').str[0]
        # isValidResort = location in [resortDF['resort_name']]
        #FIX TO CHECK IF RESORT SELECTED IS REAL
        
        print("\nRecommendations:")
        print(f"- Food:", self.food_recommendations(location,budget))
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
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        fullInput = [skiing_ability,budget, num_guests, ski_preferences, town_importance]
        
        resortsRanked = chain.invoke({"input": fullInput})

        return resortsRanked
    
    def predict_lift_queue(self, location, skiing_ability, num_guests, ski_preferences):
        # Add logic to predict lift queue time based on skiing ability, resort popularity, etc.
        # For simplicity, this example returns a static value.
        # Return values for each of the most common lifts
        return "Short"
    
    def food_recommendations(self,location,budget,start_date,end_date):
        #LLM call to recommend food in the area for a given price point
        return 0
    
    def lodging_recommendations(self,location,budget,num_guests,start_date,end_date, town_importance):
        #LLM call to recommend lodging in the area for a given price point
        return 0
    
    def equipment_recommendations(self,location,budget,num_guests,start_date,end_date,skiing_ability):
        #LLM call to recommend equipment rentals
        return 0
    
    def ammenities_recommendations(self,location,budget,num_guests,start_date,end_date):
        #LLM call to recommend ammenities
        return 0

if __name__ == "__main__":
    app = SkiVacationApp()
    app.make_recommendations()