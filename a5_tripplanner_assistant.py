#########################################################################
#
#     Trip Planner Assistant (as part of Assignment #5)
#      by RK on 20th June 2025
#
#        The implemented code got it reviewed by chatGPT & Gemini
#########################################################################

#########################################################################
#
#     imports in the order
#       (python generic, specific, langchain, langgraph and others)
#########################################################################
import os
import re
import operator
import requests
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, Sequence, List, Optional

from IPython.display import Image, display
from dotenv import load_dotenv

from langchain.tools import tool
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.runnables import RunnableLambda

from langgraph.graph import StateGraph, START, MessagesState, END
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
#########################################################################


#########################################################################
#                   Utility functions - START
#########################################################################

#########################################################################
# Utility: to perform websearch using duckduckgo search
def tp_utility_websearch_ddg(in_query:str, max_results:int = 5)->str:
    from langchain_community.tools import DuckDuckGoSearchRun

    try:
        search = DuckDuckGoSearchRun(max_results=max_results)
        raw_ddg_results = search.invoke(in_query) # This returns a raw string or list of dicts depending on DDG tool config
        # DuckDuckGoSearchRun.invoke usually returns a string summary, but if not, format it similarly to Tavily
        # For simplicity, assuming it returns a string suitable for direct use
        search_input_for_llm = raw_ddg_results
        
    except Exception as e:
        print(" tp_utility_websearch_ddg exception is: ", e)
        search_input_for_llm = "No search results found for the query." # Ensure it returns a string even on error
    else:
        print(" DDG Search OK ")

    finally:
        return search_input_for_llm # Ensure a string is returned


#########################################################################
# Utility: to perform websearch using tavily search
def tp_utility_websearch_tavily(in_query: str, max_results: int = 5) -> str:
    from langchain_community.tools import TavilySearchResults

    try:
        search = TavilySearchResults(k=max_results)
        raw_tavily_results = search.invoke({"query": in_query})
        # Format the search results into a single string for the LLM ---
        formatted_search_results = []
        if raw_tavily_results:
            for i, res_dict in enumerate(raw_tavily_results):
                # Each res_dict should have a 'content' key, which is the snippet
                content = res_dict.get('content', 'No content available.')
                url = res_dict.get('url', '#')
                title = res_dict.get('title', 'No Title')
                formatted_search_results.append(
                    f"--- Search Result {i+1} ---\n"
                    f"Title: {title}\n"
                    f"URL: {url}\n"
                    f"Snippet:\n{content}"
                )
            # Join all individual formatted results with a separator
            search_input_for_llm = "\n\n".join(formatted_search_results)
        else:
            search_input_for_llm = "No search results found for the query."

    except Exception as e:
        print(" tp_utility_websearch_tavily exception is: ", e)
        search_input_for_llm = "No search results found for the query." # Ensure it returns a string
    else:
        print(" Tavily search OK ")

    finally:
        return search_input_for_llm

#########################################################################
# Utility: to get to remove LLM thinkin tags from the final output
import re
from langchain_core.messages import BaseMessage # IMPORTANT: Import BaseMessage

def tp_utility_remove_llmthought_tags(data: str | BaseMessage) -> str:
    """
    Removes content, including the tags, for <think> and </think>.
    This function is designed to handle input that might be a raw string OR a LangChain BaseMessage (like AIMessage).
    """
    text_to_process = ""
    if isinstance(data, BaseMessage):
        text_to_process = data.content
    elif isinstance(data, str):
        text_to_process = data
    else:
        print(f"Warning: tp_utility_remove_llmthought_tags received unexpected type: {type(data)}. Attempting to stringify.")
        text_to_process = str(data)

    pattern = r"<think>.*?</think>"
    cleaned_text = re.sub(pattern, "", text_to_process, flags=re.DOTALL)
    return cleaned_text.strip()

#########################################################################
# Utility: to get response from a specific LLM using input query, prompt
def tp_utility_llm(input_query:str, in_prompt:ChatPromptTemplate, llm_type:str) -> str:
    # Set up LLM to get response for different input queries and prompts.
    if llm_type == "ChatAnthropic":
        # use 'ChatAnthropic' only if mentioned explictly
        model='claude-3-5-sonnet-20241022'
        llm=ChatAnthropic(model=model)
    else:
        #default llm model to be used is 'ChatGroq'
        model="deepseek-r1-distill-llama-70b"
        llm=ChatGroq(model_name=model)

    chain = in_prompt | llm | RunnableLambda(tp_utility_remove_llmthought_tags)
    llm_output= chain.invoke({"input_text": input_query})
    return llm_output # This is already a string due to RunnableLambda

#########################################################################
# Utility: to get weather forecast for a given city
def tp_utility_weather_forecast(city: str) -> str:
    """Get the 15-day weather forecast for a given city."""
    api_key=os.getenv("VISUALCROSSING_WEATHER_API_KEY")
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={api_key}&include=days&elements=datetime,tempmax,tempmin,description"

    response = requests.get(url)
    if response.status_code != 200:
        return f"Error getting forecast: {response.text}"

    data = response.json()
    forecast = data.get("days", [])[:15]  # Limit to 15 days

    result = f"15-Day Weather Forecast for {city.title()}:\n"
    for day in forecast:
        result += f"{day['datetime']}: {day['description']}, High: {day['tempmax']}°C, Low: {day['tempmin']}°C\n"
    return result


#########################################################################
#                   Utility functions - END
#########################################################################

#########################################################################
class Tquery(BaseModel):
    origin_city:str
    origin_country:str
    overseas:bool
    destination_city:str
    destination_country:str
    dates_range:str
    ndays:int
    currency:str

# Define a custom reducer function to merge dictionaries
def merge_dicts(current_dict: Optional[dict], new_dict: dict) -> dict:
    """Merges a new dictionary into the current dictionary.
    New values for existing keys will overwrite old values."""
    if current_dict is None:
        return new_dict # If trip_data is initially empty, just set it to the new_dict
    current_dict.update(new_dict) # Update the existing dictionary with values from the new_dict
    return current_dict

class MessagesState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    steps_completed: Annotated[List[str], operator.add]
    trip_data: Annotated[Optional[dict], merge_dicts]
    summary_data: Annotated[Optional[dict], merge_dicts]

#########################################################################
# tool: to get the exchange rate
#@tool
def tp_utility_tool_get_exchange_rate(from_currency: str, to_currency: str = "INR") -> float:
    """
    Get the real-time exchange rate between two currencies.
    """
    import requests
    try:
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}"
        response = requests.get(url)
        data = response.json()
        rate = data["info"]["rate"]
        print(f"1 {from_currency} = {rate:.2f} {to_currency}")
        return rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return 0.0

#########################################################################
#  Parse user input and extract trip request info.
#########################################################################
def tp_user_requirement(state: MessagesState) -> MessagesState:
    from pydantic import BaseModel
    from langchain.output_parsers import PydanticOutputParser
    from langchain_core.output_parsers import JsonOutputParser
    from langchain.prompts import PromptTemplate

    print(f">>> Inside tp_user_requirement >>> ")
    # Fix: Get the content of the latest (Human) message
    input_query_content = state['messages'][-1].content
    print("Input Query Content: ", input_query_content)

    parser = PydanticOutputParser(pydantic_object=Tquery)

    prompt = PromptTemplate(
        template="Extract person information.\n{format_instructions}\nInput: {input_text}",
        input_variables=["input_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    model="deepseek-r1-distill-llama-70b"
    llm=ChatGroq(model_name=model)
    # Fix: Pass the string content to the prompt
    formatted_prompt = prompt.format_prompt(input_text=input_query_content)

    output = llm.invoke(formatted_prompt.to_messages())
    structured = parser.parse(output.content)

    dict_output = str(dict(structured))
    return {
        "messages": state["messages"] + [AIMessage(content=dict_output)], # Use state["messages"] for concatenation
        "trip_data": dict(structured)
    }
#########################################################################

#########################################################################
#  To get the followeing details of the selected city, country
#      attractions, resturants, activities, transportation, events
#########################################################################
def tp_local_attractions(state: MessagesState) -> MessagesState:
    print(" <<< in side tp_local_attractions >>")


    input_query = f"I am from {state["trip_data"]["origin_city"]}, {state["trip_data"]["origin_country"]} Please suggest a trip for the specified details"
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"You are a helpful assistant for a {state["trip_data"]["ndays"]} days trip planner to get the attractions, activities, famous festivals, resturants, events during the {state["trip_data"]["dates_range"]} period for the given {state["trip_data"]["destination_city"]}, {state["trip_data"]["destination_country"]} and nearby places including local transportation. Also list in the priority order along trip planner like day1, day2 etc. with approximate cost",
        ),
        ("human", "{input_text}"),
    ])

    llm_output=tp_utility_llm(input_query, prompt, "ChatGroq")

    return {
        "messages": state["messages"] + [AIMessage(content=str(llm_output))],
        "summary_data": {"attractions": llm_output},
        "steps_completed": ["tp_local_attractions"] # Mark this step as completed
    }

#########################################################################
#  To get the weather details for the trip
#########################################################################
def tp_local_weather(state: MessagesState) -> MessagesState:
    print(" <<< in side tp_local_weather >>>")

    #first get 15 days forecast
    forecast1 = tp_utility_weather_forecast(state["trip_data"]["destination_city"])

    #get the average weather of the city during the planned dates
    input_query = f"Get the summary on weather situation for an outdoor trip for the given input. Please suggest a trip advise based on weather for the specified details"
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"You are a helpful assistant to get the weather situation of {state["trip_data"]["destination_city"]}, {state["trip_data"]["destination_country"]} in the period {state["trip_data"]["dates_range"]} for outdoor trip. You may also use last 5 years history data of the place for better suggestion on weather. Also suggest required precautions based on the weather and output should include advise on outdoor trip, precautions, minimum/maximum/average temperature, weather conditions for the trip period.",
        ),
        ("human", "{input_text}"),
    ])

    historic_weather_data=tp_utility_llm(input_query, prompt, "ChatGroq")
    weather_details = forecast1 + historic_weather_data

    return {
        "messages": state["messages"] + [AIMessage(content=weather_details)], # FIX: Correctly concatenate lists
        "summary_data": {"weather": weather_details},
        "steps_completed": ["tp_local_weather"] # Mark this step as completed
    }


#########################################################################
#  To get the hotel details for the trip
#########################################################################
def tp_local_hotels(state: MessagesState)-> MessagesState:
    print(" <<< in side tp_local_hotels >>")
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a helpful assistant that converts travel-related unstructured text into a structured CSV table.
            Output should not contain any additional details like thinking etc from model.
            Output should be strictly in structured CSV format with the following columns and currency should be in INR only.
            HotelName, Description, Estimated Cost per night, currency code
            """
        ),
        (
            "human",
            "Text: {input_text}\n\n"
            "Extract hotel details as output in the specified CSV format."
        )
    ])


    query_budget=f'find budget hotels, Youth hostels, OYO at {state["trip_data"]["destination_city"]}, {state["trip_data"]["destination_country"]} for {state["trip_data"]["ndays"]} days dates from {state["trip_data"]["dates_range"]}'
    # tp_utility_websearch_ddg and tp_utility_websearch_tavily now return formatted strings
    search_result1_1 = tp_utility_websearch_ddg(query_budget, 10)
    search_result1_2 = tp_utility_websearch_tavily(query_budget, 10)
    # Concatenate the strings directly, not list representations
    search_result1 = search_result1_1 + "\n\n" + search_result1_2


    query_luxury=f'find luxury hotels at {state["trip_data"]["destination_city"]}, {state["trip_data"]["destination_country"]} for {state["trip_data"]["ndays"]} days dates from {state["trip_data"]["dates_range"]}'
    search_result2_1 = tp_utility_websearch_ddg(query_luxury, 5)
    search_result2_2 = tp_utility_websearch_tavily(query_luxury, 5)
    search_result2 = search_result2_1 + "\n\n" + search_result2_2
    search_result = search_result1 + "\n\n" + search_result2

    ##LLM to summarize budget and luxury hotel details in CSV format
    csv_output = tp_utility_llm(search_result, prompt, "ChatGroq")

    return {
        "messages": state["messages"] + [AIMessage(content=str(csv_output))], # FIX: Correctly concatenate lists
        "summary_data": {"hotels": csv_output},
        "steps_completed": ["tp_local_hotels"] # Mark this step as completed
    }



#########################################################################
#  To get the visa processing details for the trip (if applicable)
#########################################################################
def tp_visa(state: MessagesState) -> MessagesState:
    print(" <<< in side tp_visa >>")
    query = (
        f'find the tourist visa fee, 3rd party handling cost in INR and travel insurance cost in INR for one person '
        f'to travel from {state["trip_data"]["origin_city"]}, {state["trip_data"]["origin_country"]} '
        f'to {state["trip_data"]["destination_city"]}, {state["trip_data"]["destination_country"]} and come back'
    )

    # tp_utility_websearch_tavily now returns a formatted string directly
    search_input_for_llm_string = tp_utility_websearch_tavily(query, 3)

    # This commented block is no longer needed since formatting is done in tp_utility_websearch_tavily
    """
    # Step 2: Format the search results into a single string for the LLM
    formatted_search_results_list = []
    if raw_tavily_results:
        for i, res_dict in enumerate(raw_tavily_results):
            content = res_dict.get('content', 'No content available.')
            url = res_dict.get('url', '#')
            title = res_dict.get('title', 'No Title')
            formatted_search_results_list.append(
                f"--- Search Result {i+1} ---\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Snippet:\n{content}"
            )
        # This is the string that will be passed as input_query to tp_utility_llm
        search_input_for_llm_string = "\n\n".join(formatted_search_results_list)
    else:
        search_input_for_llm_string = "No search results found for the query."
    """

    print(f"--- Formatted Search Results for LLM: ---\n{search_input_for_llm_string}")

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a helpful assistant that converts tourist visa related unstructured text into a structured CSV table.
            Output should not contain any additional details like thinking etc from model. Also, no need of work, business visa details.
            Output should be strictly in structured CSV format with the following columns for the tourist visa and cost should be in INR.
            Consultant/company name, Details, number of working days for processing, Purpose, Estimated Cost, currency code.
            The Purpose can be strictly contains only in the 4 categories. The categories are  visa fee, 3rd party handling cost, travel insurance, other costs.
            All the places cost should be in INR only.
            """
        ),
        (
            "human",
            "Text: {input_text}\n\n" # This is where the formatted string will go
            "Extract tourist visa fee and processing cost in INR and output in the specified CSV format."
        )
    ])

    # Pass the correctly formatted STRING to your LLM utility
    csv_output = tp_utility_llm(search_input_for_llm_string, prompt, "ChatAnthropic")
    print("LLM converted CSV output:", csv_output)

    # This part is already correct
    new_messages = state["messages"] + [AIMessage(content=csv_output)]

    return {
        "messages": new_messages,
        "summary_data": {"visa": csv_output},
        "steps_completed": ["tp_visa"] # Mark this step as completed
    }


#########################################################################
#  To prepare the itinerary for the trip
#########################################################################
def tp_itinerary(state: MessagesState)-> MessagesState:
    print(" <<< in side tp_itinerary >>")
    # Return new state with updated messages
    return {
        "messages": state["messages"] + [AIMessage(content="itinerary details added.")],
        "steps_completed": ["tp_itinerary"] # Mark this step as completed
    }

#########################################################################
#  To get the consolidation on the trip plan
#########################################################################
def tp_consolidated_plan(state: MessagesState)-> MessagesState:
    print(" <<< in side tp_consolidated_plan >>")
    return {
        "messages": state["messages"] + [AIMessage(content="consolidated plan added")],
        "steps_completed": ["tp_consolidated_plan"] # Mark this step as completed
    }

#########################################################################
#  To calculate the overall cost
#########################################################################
def tp_cost_estimation(state: MessagesState)-> MessagesState:
    print(" <<< in side tp_cost_estimation >>")
    return {
        "messages": state["messages"] + [AIMessage(content="cost estimation details added.")],
        "steps_completed": ["tp_cost_estimation"] # Mark this step as completed
    }

#########################################################################
#  To conver various currencies into required currency
#########################################################################
def tp_currency_conversion(state: MessagesState) -> MessagesState:
    print(" <<< in side tp_currency_conversion >>")
    from_currency = "IDR" #state["trip_data"]["currency"] # Assuming currency is correctly extracted earlier
    to_currency = "INR"

    rate = tp_utility_tool_get_exchange_rate(from_currency, to_currency)
    print(f"Exchange rate: {rate}")

    return {
        "messages": state["messages"] + [AIMessage(content=f"Currency conversion done. 1 {from_currency} = {rate:.2f} {to_currency}")],
        "trip_data": {"exchange_rate": rate}, # Store rate if needed
        "steps_completed": ["tp_currency_conversion"] # Mark this step as completed
    }


#########################################################################
#  Router function for to decide need visa for the trip
#########################################################################
def router_function_tp_visa(state: MessagesState) -> str:
    print(" <<< in side router_function_tp_visa >>> ")
    if state["trip_data"]["overseas"] == True:
        print(f" Overeseas Trip from {state["trip_data"]["origin_city"]} --> {state["trip_data"]["destination_city"]} ")
        return "tp_visa"
    else:
        print(f" Domestic Trip from {state["trip_data"]["origin_city"]} --> {state["trip_data"]["destination_city"]} ")
        # FIX: Correctly update summary_data using merge_dicts
        # Directly return a state update for summary_data, as a router shouldn't modify state directly
        # However, if this is a "node" in a StateGraph, it can return a state dict.
        # If it's a router (conditional edge), it should only return the next node name.
        # Let's assume it's a router in a conditional edge, so we'll handle summary_data elsewhere if needed.
        # For now, it only returns the next node name.
        return "tp_itinerary"

#########################################################################
#  Purpose: To wait for the completion of all parallel nodes
#########################################################################
def merge_wait_for_parallel_nodes(state: MessagesState) -> MessagesState:
    # No longer add "some_task_name" here. Upstream nodes are responsible for updating steps_completed.
    print(" <<< in side merge_wait_for_parallel_nodes >>")

    # The order of checks might matter depending on which node finishes first.
    # Ensure all required tasks are in the steps_completed list.
    required_tasks = ["tp_local_attractions", "tp_local_weather", "tp_local_hotels"]
    
    # Conditionally add tp_visa if it was an overseas trip
    if state["trip_data"].get("overseas") == True:
        required_tasks.append("tp_visa")
    else:
        # If domestic, ensure 'visa' is set to 'NA' in summary_data for completeness
        # This update should technically be handled by the router or an explicit node for domestic path
        # For simplicity now, if not overseas, we assume visa is not relevant or set to NA by the router's path.
        pass

    all_tasks_done = all(task in state.get("steps_completed", []) for task in required_tasks)

    if all_tasks_done:
        print("All parallel tasks done. Proceeding.")
        return {"messages": state["messages"] + [AIMessage(content="All parallel data collection tasks completed.")]}
    else:
        print("Still waiting for parallel tasks to finish.")
        # Return None or an empty dict so LangGraph waits for more updates
        return {} # Returning empty dict will make LangGraph wait if no output channel changes.


#########################################################################
#  To generate the final report on Trip planner
#########################################################################
def tp_final_report(state: MessagesState)-> MessagesState:
    print(" <<< in side tp_final_report >>")
    #Let's get each stage details
    summary = state.get("summary_data", {})
    attraction_details = summary.get("attractions", "No attraction details found.")
    hotel_details = summary.get("hotels", "No hotel details found.")
    weather_details = summary.get("weather", "No weather details found.")
    visa_details = summary.get("visa", "Not applicable or no visa details found.") # Default for domestic trips

    tp_final_summary = f"""### Final Report on Trip Plan ###

    **Attractions & Itinerary:**
    {attraction_details}

    **Hotels:**
    {hotel_details}

    **Weather:**
    {weather_details}

    **Visa Info:**
    {visa_details}
    """

    # Return new state with updated messages
    return {
        "messages": state["messages"] + [AIMessage(content=tp_final_summary)],
        "steps_completed": ["tp_final_report"] # Mark this step as completed
    }

#########################################################################
# Trip Planner Main
#########################################################################
def tp_main():
    graph = StateGraph(MessagesState)
    graph.add_node("tp_user_requirement",    tp_user_requirement)
    graph.add_node("tp_local_attractions",   tp_local_attractions)
    graph.add_node("tp_local_weather",       tp_local_weather)
    graph.add_node("tp_local_hotels",        tp_local_hotels)
    graph.add_node("tp_itinerary",           tp_itinerary)
    graph.add_node("tp_visa",                tp_visa)
    graph.add_node("tp_consolidated_plan",   tp_consolidated_plan)
    graph.add_node("tp_cost_estimation",     tp_cost_estimation)
    graph.add_node("tp_currency_conversion", tp_currency_conversion)
    graph.add_node("tp_final_report",        tp_final_report)

    graph.set_entry_point("tp_user_requirement")

    # parallel execution
    graph.add_edge("tp_user_requirement", "tp_local_attractions")
    graph.add_edge("tp_user_requirement", "tp_local_weather")
    graph.add_edge("tp_user_requirement", "tp_local_hotels")

    # Use a conditional edge to decide on tp_visa based on 'overseas' flag
    graph.add_conditional_edges(
        "tp_user_requirement", # Source node for the condition
        router_function_tp_visa, # Router function
        {
            "tp_visa":      "tp_visa", # If router returns "tp_visa", go to tp_visa
            "tp_itinerary": "tp_itinerary" # If router returns "tp_itinerary" (domestic case), skip tp_visa
        }
    )

    # merge point (post parallel execution) - All parallel paths now go to `merge_wait_task`
    graph.add_node("merge_wait_task",      merge_wait_for_parallel_nodes)
    graph.add_edge("tp_local_attractions", "merge_wait_task")
    graph.add_edge("tp_local_weather",     "merge_wait_task")
    graph.add_edge("tp_local_hotels",      "merge_wait_task")
    graph.add_edge("tp_visa",              "merge_wait_task")  

    # After merge, proceed sequentially
    graph.add_edge("merge_wait_task",       "tp_consolidated_plan")
    graph.add_edge("tp_consolidated_plan",  "tp_itinerary")


    # Current simple flow for currency conversion
    graph.add_edge("tp_itinerary", "tp_currency_conversion")

    #Final wrapup
    graph.add_edge("tp_currency_conversion", "tp_cost_estimation")
    graph.add_edge("tp_cost_estimation", "tp_final_report")
    graph.add_edge("tp_final_report", END)


    app = graph.compile()
    display(Image(app.get_graph().draw_mermaid_png()))

    query="I am from Bengaluru, India. I would like to go for a trip to Bali, Indonesia from 25th June to 30th June. Give me trip planner along with cost in INR."
    response = app.invoke({"messages": [HumanMessage(content=query)]})
    print(" << in tp_init response print>>>")
    #print("1. Input Query", response["messages"][0]) # This will be the initial HumanMessage
    #print("2. Parsed details", response["messages"][1]) # This will be the AIMessage with structured data
    #print("3. Final Response:\n", response["messages"][-1].content) # Print the content of the last message (final report)
    #print("4. Parsed Dict Object", response["trip_data"])
    #print("5. Summary Data", response["summary_data"])


#########################################################################
#  START of program
#########################################################################
if __name__ == "__main__":
    load_dotenv()

    print("AI Trip Planner Assistant Start...")
    tp_main()
    print("AI Trip Planner Assistant End...")
