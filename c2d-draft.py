from urllib.parse import quote_plus
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import requests
import json
import os
from IPython.display import Markdown, display
from toolbox_langchain import ToolboxClient
from langgraph.prebuilt import create_react_agent
import nest_asyncio
import asyncio
import gradio as gr
import time

# --- Configuration ---
MODEL = "gemini-2.5-flash"
driver = "ODBC Driver 17 for SQL Server"
username = "H@rd@_IND"
password = "H@rD@DmY"
server = "eeeit.work"
database = "HardaIndoreERPDummy"

params = quote_plus(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")
connection_uri = f"mssql+pyodbc:///?odbc_connect={params}"

os.environ["GOOGLE_API_KEY"] = "Your API key"
llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash")



def generic_month_year_tool(input_text: str, tool_endpoint: str) -> str:
    """
    Generic handler for month/year tools.
    tool_endpoint: e.g. 'count-by-month', 'sum-biltiesWeight-by-month', etc.
    """
    url = f"http://localhost:5000/api/tool/{tool_endpoint}/invoke"
    headers = {"Content-Type": "application/json"}
    try:
        month = 0
        year = 0
        try:
            parsed = json.loads(input_text)
            month = int(parsed.get("month", 0))
            year = int(parsed.get("year", 0))
        except:
            if "," in input_text:
                parts = [x.strip() for x in input_text.split(",")]
                month = int(parts[0]) if len(parts) > 0 else 0
                year = int(parts[1]) if len(parts) > 1 else 0
            elif "July" in input_text or "july" in input_text:
                month = 7
                year = int("".join(filter(str.isdigit, input_text))) or 2025
            else:
                month = 0
                year = 0
        payload = {"params": [{"month": month}, {"year": year}]}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Unexpected error: {e}"




#start of tools

count_bilties_by_month = Tool(
    name="count_bilties_by_month",
    func=generic_month_year_tool,
    description="Counts BiltyMaster entries by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically."
)

total_unpaid_bilties_by_month = Tool(
    name="total_unpaid_bilties_by_month",
    func=generic_month_year_tool,
    description="Counts total unpaid bilties by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

daily_breakdown_bilty_by_month = Tool(
    name="daily_breakdown_bilty_by_month",
    func=generic_month_year_tool,
    description="Daily breakdown of bilties by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

average_bilty_value_by_month = Tool(
    name="average_bilty_value_by_month",
    func=generic_month_year_tool,
    description="Calculates average bilty value by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

total_paid_bilties_by_month = Tool(
    name="total_paid_bilties_by_month",
    func=generic_month_year_tool,
    description="Counts total paid bilties by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

percentage_of_paid_unpaid_bilties_by_month = Tool(
    name="percentage_of_paid_unpaid_bilties_by_month",
    func=generic_month_year_tool,
    description="Calculates the percentage of paid to unpaid bilties by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

top_5_branches_paid_bilties_by_month = Tool(
    name="top_5_branches_paid_bilties_by_month",
    func=generic_month_year_tool,
    description="Retrieves the top 5 branches by paid bilties for a specific month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

sum_crossing_Recd_Weight_by_month = Tool(
    name="Sum_crossing_Recd_Weight_by_month",
    func=generic_month_year_tool,
    description="Sum of crossing Recd weight by month",
)

average_crossing_recd_weight_per_challan_by_month = Tool(
    name="average_crossing_recd_weight_per_challan_by_month",
    func=generic_month_year_tool,
    description="Calculates the average crossing Recd weight per challan by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

maximum_crossing_recd_weight_in_a_single_challan_by_month = Tool(
    name="maximum_crossing_recd_weight_in_a_single_challan_by_month",
    func=generic_month_year_tool,
    description="Calculates the maximum crossing Recd weight in a single challan by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

branch_wise_crossing_recd_weight_by_month = Tool(
    name="branch_wise_crossing_recd_weight_by_month",
    func=generic_month_year_tool,
    description="Retrieves the branch-wise crossing received weight by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

total_paid_cartage_by_month = Tool(
    name="total_paid_cartage_by_month",
    func=generic_month_year_tool,
    description="Counts total paid cartage by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

total_unpaid_cartage_by_month = Tool(
    name="total_unpaid_cartage_by_month",
    func=generic_month_year_tool,
    description="Counts total unpaid cartage by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

percentage_of_paid_unpaid_cartage_by_month = Tool(
    name="percentage_of_paid_unpaid_cartage_by_month",
    func=generic_month_year_tool,
    description="Calculates the percentage of paid to unpaid cartage by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

branch_wise_paid_cartage_by_month = Tool(
    name="branch_wise_paid_cartage_by_month",
    func=generic_month_year_tool,
    description="Counts branch-wise paid cartage by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

average_cartage_per_bilty_by_month = Tool(
    name="average_cartage_per_bilty_by_month",
    func=generic_month_year_tool,
    description="Calculates average cartage per bilty by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

sum_biltiesWeight_by_month = Tool(
    name="Sum_biltiesWeight_by_month",
    func=generic_month_year_tool,
    description="Sum of Bilties Weight from BiltyMaster entries by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically."
)

average_bilty_weight_by_month = Tool(
    name="average_bilty_weight_by_month",
    func=generic_month_year_tool,
    description="Calculates average bilty weight by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

maximum_bilty_weight_by_month = Tool(
    name="maximum_bilty_weight_by_month",
    func=generic_month_year_tool,
    description="Retrieves the maximum bilty weight by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

branch_wise_sum_bilties_weight_by_month = Tool(
    name="branch_wise_sum_bilties_weight_by_month",
    func=generic_month_year_tool,
    description="Counts branch-wise sum of bilties weight by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

total_crossing_challan_by_month = Tool(
    name="total_crossing_challan_by_month",
    func=generic_month_year_tool,
    description="Counts total crossing challans by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically."
)

paid_crossing_challans_by_month = Tool(
    name="paid_crossing_challans_by_month",
    func=generic_month_year_tool,
    description="Counts paid crossing challans by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

unpaid_crossing_challans_by_month = Tool(
    name="unpaid_crossing_challans_by_month",
    func=generic_month_year_tool,
    description="Counts unpaid crossing challans by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

vehicle_wise_crossing_challan_summary_by_month = Tool(
    name="vehicle_wise_crossing_challan_summary_by_month",
    func=generic_month_year_tool,
    description="Retrieves vehicle-wise crossing challan summary by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

sum_paid_amount_by_month = Tool(
    name="sum_paid_amount_by_month",
    func=generic_month_year_tool,
    description="sum of paid amount by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

total_unpaid_amount_by_month = Tool(
    name="total_unpaid_amount_by_month",
    func=generic_month_year_tool,
    description="Calculates the total unpaid amount by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

daily_paid_amount_trend_by_month = Tool(
    name="daily_paid_amount_trend_by_month",
    func=generic_month_year_tool,
    description="Retrieves the daily paid amount trend by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

branch_wise_paid_amount_by_month = Tool(
    name="branch_wise_paid_amount_by_month",
    func=generic_month_year_tool,
    description="Retrieves branch-wise paid amount by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

paid_amount_due_by_month = Tool(
    name="paid_amount_due_by_month",
    func=generic_month_year_tool,
    description="Sum of paid amount due by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

total_overdue_amount_by_month = Tool(
    name="total_overdue_amount_by_month",
    func=generic_month_year_tool,
    description="Calculates the total overdue amount by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

top_10_customers_with_highest_due_amount = Tool(
    name="top_10_customers_with_highest_due_amount",
    func=generic_month_year_tool,
    description="Retrieves the top 10 customers with the highest due amount by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

payment_recovery_rate_by_month = Tool(
    name="payment_recovery_rate_by_month",
    func=generic_month_year_tool,
    description="Calculates the payment recovery rate by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

total_Vehicle_Load_by_month = Tool(
    name="total_Vehicle_Load_by_month",
    func=generic_month_year_tool,
    description="Total Vehicle Load by Month",
)

average_vehicle_load_by_month = Tool(
    name="average_vehicle_load_by_month",
    func=generic_month_year_tool,
    description="Calculates the average vehicle load by month and year.",
)

maximum_vehicle_load_by_month = Tool(
    name="maximum_vehicle_load_by_month",
    func=generic_month_year_tool,
    description="Calculates the maximum vehicle load by month and year.",
)

route_wise_vehicle_load_summary_by_month = Tool(
    name="route_wise_vehicle_load_summary_by_month",
    func=generic_month_year_tool,
    description="Retrieves the route-wise vehicle load summary by month and year.",
)

branch_godown_wise_total_cartage = Tool(
    name="branch_godown_wise_total_cartage",
    func=generic_month_year_tool,
    description="Total Cartage by Branch and Godown. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

branch_wise_paid_vs_unpaid_cartage = Tool(
    name="branch_wise_paid_vs_unpaid_cartage",
    func=generic_month_year_tool,
    description="Compares paid vs unpaid cartage by branch for a specific month and year.",
)

godown_wise_cartage_share = Tool(
    name="godown_wise_cartage_share",
    func=generic_month_year_tool,
    description="Calculates the cartage share by godown for a specific month and year.",
)

monthly_cartage_comparison_by_month = Tool(
    name="monthly_cartage_comparison_by_month",
    func=generic_month_year_tool,
    description="Compares monthly cartage by month and year.",
)

branch_godown_wise_total_paid_bilty = Tool(
    name="branch_godown_wise_total_paid_bilty",
    func=generic_month_year_tool,
    description="Total Paid Bilties by Branch and Godown. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

branch_wise_unpaid_bilties = Tool(
    name="branch_wise_unpaid_bilties",
    func=generic_month_year_tool,
    description="Retrieves unpaid bilties by branch for a specific month and year.",
)

godown_wise_paid_bilty_share = Tool(
    name="godown_wise_paid_bilty_share",
    func=generic_month_year_tool,
    description="Calculates the paid bilty share by godown for a specific month and year.",
)

monthly_paid_bilty_comparison_by_month = Tool(
    name="monthly_paid_bilty_comparison_by_month",
    func=generic_month_year_tool,
    description="Compares monthly paid bilties by month and year.",
)

booking_bilty_by_month_summary = Tool(
    name="booking_bilty_by_month_summary",
    func=generic_month_year_tool,
    description="Counts booking bilties by month and year. Input should be a month (1-12) and year (YYYY). If input is 'July 2025', it will parse the month and year automatically.",
)

booking_bilty_count_per_day = Tool(
    name="booking_bilty_count_per_day",
    func=generic_month_year_tool,
    description="Retrieves the booking bilty count per day for a specific month and year.",
)

booking_bilty_weight_summary = Tool(
    name="booking_bilty_weight_summary",
    func=generic_month_year_tool,
    description="Retrieves the booking bilty weight summary for a specific month and year.",
)

branch_wise_booking_bilty_breakdown = Tool(
    name="branch_wise_booking_bilty_breakdown",
    func=generic_month_year_tool,
    description="Retrieves the branch-wise booking bilty breakdown for a specific month and year.",
)



import io
import sys

async def run_agent_capture_output(query):
    buffer = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer  # Redirect stdout to buffer

    try:
        async with ToolboxClient("http://localhost:5000") as toolbox:
            tools = toolbox.load_toolset("basic")
            # all_tools = tools + [sql_tool]
            all_tools = tools
            agent = create_react_agent(llm, all_tools, verbose=True, handle_parsing_errors=True)
            question = query
            async for step in agent.astream({"messages": [("user", question)]}, stream_mode="values"):
                message = step["messages"][-1]
                if isinstance(message, tuple):
                    print(message)
                else:
                    message.pretty_print()
    finally:
        sys.stdout = sys_stdout  # Restore stdout

    return buffer.getvalue()


system_message = SystemMessage(
    content="""You are a result formatting assistant designed to take raw outputs retrieved from SQL query executions and transform them into well-structured, user-friendly responses.

Your job is to:

Analyze the incoming data from the SQL output (assume it is either tabular or textual).

If the data is tabular (i.e., multiple rows and columns or a result set from a SELECT query), convert it into a markdown-formatted table.

If the data is a single value or a one-liner, output only a concise, markdown-formatted one-liner response.

Keep the response clean, easy to read, and free of unnecessary technical formatting or verbose SQL-related phrasing.

Also it is mandatory to give insights derived from the data in 3 - 4 bullet points highlighting major insights in **bold**.

Output must be strictly in Markdown format only.
Do not include explanations or system-related messages.
Focus only on the final answer that the user would find helpful.

You are not allowed to modify or interpret the meaning of the data — only format and refine its presentation."""
)

def user_prompt(text):
    user_message = HumanMessage(
        content=f"""
                Format the following SQL query output into a clean and user-friendly response using Markdown:

                If the data is tabular (multiple rows or key-value records), present it as a markdown table.

                If it is a single value or a short message, format it as a concise one-liner in markdown.

                Do not add any explanations or extra text.

                Here is the raw output:
                {text}
        """
    )
    return user_message

async def final_output(query):
    output = await run_agent_capture_output(query)

    response = llm.invoke([
        system_message,
        user_prompt(output)
    ])

    return response.content

related_queries = {
    "Count of Bilties in July Month 2025": [
        "Total Unpaid Bilties in July Month 2025",
        "Daily Breakdown of Bilties in July Month 2025",
        "Average Bilty Value in July Month 2025"
    ],
    "Total Paid Bilties in July Month 2025": [
        "Total Unpaid Bilties in July Month 2025",
        "Percentage of Paid vs Unpaid Bilties in July Month 2025",
        "Top 5 Branches by Paid Bilties in July Month 2025"
    ],
    "Total Crossing Recd Weight in July Month 2025": [
        "Average Crossing Recd Weight per Challan in July Month 2025",
        "Maximum Crossing Recd Weight in a Single Challan in July Month 2025",
        "Branch-wise Crossing Recd Weight in July Month 2025"
    ],
    "Total Paid Cartage in July Month 2025": [
        "Total Unpaid Cartage in July Month 2025",
        "Percentage of Paid vs Unpaid Cartage in July Month 2025",
        "Branch-wise Paid Cartage in July Month 2025",
        "Average Cartage per Bilty in July Month 2025"
    ],
    "Sum of Bilties Weight in July Month 2025": [
        "Average Bilty Weight in July Month 2025",
        "Maximum Bilty Weight in July Month 2025",
        "Branch-wise Sum of Bilties Weight in July Month 2025"
    ],
    "Total Crossing Challan in July Month 2025": [
        "Paid Crossing Challans in July Month 2025",
        "Unpaid Crossing Challans in July Month 2025",
        "Vehicle-wise Crossing Challan Summary in July Month 2025"
    ],
    "Total Paid Amount in July Month 2025": [
        "Total Unpaid Amount in July Month 2025",
        "Daily Paid Amount Trend in July Month 2025",
        "Branch-wise Paid Amount in July Month 2025"
    ],
    "Paid Amount Due in July Month 2025": [
        "Total Overdue Amount in July Month 2025",
        "Top 10 Customers with Highest Due Amount",
        "Payment Recovery Rate in July Month 2025"
    ],
    "Total Vehicle Load in July Month 2025": [
        "Average Vehicle Load in July Month 2025",
        "Maximum Vehicle Load in July Month 2025",
        "Route-wise Vehicle Load Summary in July Month 2025"
    ],
    "Branch plus Godown Wise Total Cartage in July Month 2025": [
        "Branch-wise Paid vs Unpaid Cartage",
        "Godown-wise Cartage Share",
        "Monthly Cartage Comparison with June 2025"
    ],
    "Branch plus Godown Wise Total Paid Biltys in July Month 2025": [
        "Branch-wise Unpaid Bilties",
        "Godown-wise Paid Bilty Share",
        "Monthly Paid Bilty Comparison with June 2025"
    ],
    "Booking Bilty Summary July Month 2025": [
        "Booking Bilty Count per Day in July Month 2025",
        "Booking Bilty Weight Summary in July Month 2025",
        "Branch-wise Booking Bilty Breakdown"
    ]
}


final_system_message = SystemMessage(
    content="""You are a logistics data insights assistant.
                You will be given:
                - The main query name and its raw output.
                - Three related sub-queries and their raw outputs.

                Your task:
                1. **Main Query Output:**
                - Display the main query name and output exactly as given, in a markdown table or block for readability.
                - Do not analyze this; keep it as raw reference data.

                2. **Sub-query Analysis:**
                - For each of the three sub-queries:
                    - Interpret the output in the context of the main query.
                    - Extract **meaningful insights**.
                    - Highlight key metrics, anomalies, or trends using **bold text**.
                    - Keep insights **clear, concise, and actionable**.
                    - Avoid repeating raw data unless it supports your insight.

                3. **Overall Insights:**
                - Summarize the key takeaways from all sub-queries combined.
                - Relate these insights directly to the **main query** to give a complete business perspective.
                - Present in **bullet points**.

                4. **Formatting Rules:**
                - Use markdown headings:
                    - `## Main Query Result`
                    - `## Related Query Insights` (with sub-headings per sub-query)
                    - `## Overall Summary`
                - Highlight important values with **bold**.
                - Use bullet points for clarity.

                **Example Input:**
                Main Query: Total Bilties in July Month 2025 → 800
                Sub-query 1: Total Unpaid Bilties in July Month 2025 → 120
                Sub-query 2: Daily Breakdown of Bilties in July Month 2025 → {day-wise numbers}
                Sub-query 3: Average Bilty Value in July Month 2025 → ₹4,200

                **Example Output:**
                ## Main Query Result
                **Total Bilties in July Month 2025:** 800

                ## Related Query Insights
                ### Total Unpaid Bilties in July Month 2025
                - **120 unpaid bilties** represent **15%** of total bilties — a notable gap in revenue collection.
                - This indicates a need for improved payment follow-up processes.

                ### Daily Breakdown of Bilties in July Month 2025
                - Peak activity occurred on **July 12** and **July 25**, suggesting **periodic demand spikes**.
                - Low activity days align with weekends, indicating potential downtime in operations.

                ### Average Bilty Value in July Month 2025
                - The **average bilty value** is ₹4,200, which is consistent with historical pricing.
                - Stable pricing suggests no recent market shocks or unusual rate changes.

                ## Overall Summary
                - July saw **800 bilties**, with a **15% unpaid rate**, affecting cash flow.
                - Demand spiked mid and late month, which can be leveraged for targeted operations.
                - Pricing remains stable, indicating steady market conditions.
                - **Recommendation:** Focus on unpaid bilty recovery and capitalize on peak demand periods.
            """
)

def final_user_prompt(text):
    user_message = HumanMessage(
        content=f"""

                This is the final output of the main query and sub-query analysis:
                {text}


                Instructions:
                - Keep the Main Query result exactly as provided.
                - For each Related Query result, provide analysis and insights in the context of the Main Query.
                - Highlight important numbers and trends in **bold**.
                - End with an "Overall Summary" combining all insights.
                - Output in Markdown format.
            """
    )
    return user_message


async def additional_output(query):
    output = f"main_query: {query} /n output: "
    output += await final_output(query)
    output += "sub_queries:"

    for i in related_queries.get(query, []):
        output += f" {i}  /n output: "
        output += "\n\n" + await final_output(i)
        time.sleep(10)

    response = llm.invoke([
        final_system_message,
        final_user_prompt(output)
    ])

    return response.content


extra_system_message = SystemMessage(
    content="""
                You are an insights summarization and rewriting assistant for a logistics analytics system.

                You will receive a detailed markdown report that includes:
                - The main query result (raw)
                - Additional related insights from other data sources

                Your task:
                1. Keep the **main query result** exactly as provided.
                2. Integrate the insights from related data into a short, focused narrative — do not mention that they came from “sub-queries” or secondary data.
                3. Ensure the rewritten output feels like a **direct, enriched answer** to the user's main question.
                4. Highlight unusual findings, anomalies, or important metrics using **bold text** so they stand out.
                5. Keep the tone **professional, concise, and business-focused**.
                6. Output must be in **Markdown format**:
                - Start with the main query result clearly stated.
                - Follow with a 2–3 bullet points summary that blends key insights naturally.
                - Avoid listing data sources or sub-query names.
                - write any major areas of concern or opportunity identified in the analysis separately.

                Goal:
                Make the user feel like they asked for one thing but you’re giving them more valuable context, without revealing the behind-the-scenes data structure.

            """
)

def extra_user_prompt(text):
    user_message = HumanMessage(
        content=f"""

                This is the raw output of the main query and sub-query analysis:
                {text}
            """
    )
    return user_message

async def presenter(query):
    output = await additional_output(query)
    time.sleep(10)
    response = llm.invoke([
        extra_system_message,
        extra_user_prompt(output)
    ])

    return response.content


import gradio as gr
import asyncio
import os
import time
import tempfile
from typing import Optional

list_of_queries = [
    "Count of Bilties in July Month 2025",
    "Total Paid Bilties in July Month 2025",
    "Total Paid Cartage in July Month 2025",
    "Total Crossing Recd Weight in July Month 2025",
    "Sum of Bilties Weight in July Month 2025",
    "Total Crossing Challan in July Month 2025",
    "Total Paid Amount in July Month 2025",
    "Paid Amount Due in July Month 2025",
    "Total Vehicle Load in July Month 2025",
    "Branch plus Godown Wise Total Cartage in July Month 2025",
    "Branch plus Godown Wise Total Paid Biltys in July Month 2025",
    "Booking Bilty Summary July Month 2025"
]



async def process_query(query):
    """
    Enhanced query processor with better user feedback and error handling.
    Preserves your existing business logic while adding UX improvements.
    """
    if not query or not query.strip():
        return """
        <div class="status-message info">
            <div class="status-icon">🚀</div>
            <div class="status-content">
                <h3>Ready to Analyze</h3>
                <p>Please select a query from the dropdown to get started with AI-powered logistics analysis.</p>
            </div>
        </div>
        """

    try:
        # Simulate processing time for demo (replace with your actual presenter() call)
        await asyncio.sleep(1)

        # Your existing process_query logic here - UNCHANGED
        return await presenter(query)

        # # Demo response (remove this and uncomment above line)
        # return f"""
        # <div class="status-message success">
        #     <div class="status-icon">✅</div>
        #     <div class="status-content">
        #         <h3>Analysis Complete</h3>
        #         <p><strong>Query:</strong> {query}</p>
        #         <div class="result-summary">
        #             <h4>Sample Results:</h4>
        #             <ul>
        #                 <li>Total Records Processed: 1,247</li>
        #                 <li>Analysis Duration: 0.8 seconds</li>
        #                 <li>Data Quality Score: 98.5%</li>
        #             </ul>
        #         </div>
        #     </div>
        # </div>
        # """

    except Exception as e:
        return f"""
        <div class="status-message error">
            <div class="status-icon">❌</div>
            <div class="status-content">
                <h3>Error Processing Query</h3>
                <p>We encountered an issue while processing your request. Please try again or contact support.</p>
                <details class="error-details">
                    <summary>Technical Details</summary>
                    <code>{str(e)}</code>
                </details>
            </div>
        </div>
        """

def show_loading():
    """Display loading state during query processing"""
    return """
    <div class="status-message loading">
        <div class="loading-spinner"></div>
        <div class="status-content">
            <h3>Processing Your Query</h3>
            <p>Analyzing transportation data... This may take a few moments.</p>
        </div>
    </div>
    """

def clear_interface():
    """Reset interface to initial state"""
    return (
        None,  # Clear dropdown selection
        """
        <div class="status-message info">
            <div class="status-icon">🔄</div>
            <div class="status-content">
                <h3>Interface Reset</h3>
                <p>Ready for your next query analysis.</p>
            </div>
        </div>
        """
    )

# =============================================================================
# MODERN CSS STYLING - Transportation & Logistics Theme
# =============================================================================

enhanced_css = """
/* =================================================================
   MODERN TRANSPORTATION LOGISTICS THEME
   Professional blue/orange palette with smooth interactions
   ================================================================= */

/* Import Google Fonts for professional typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* =================================================================
   ROOT VARIABLES & GLOBAL STYLES
   ================================================================= */

:root {
    /* Primary Transportation Theme Colors */
    --primary-blue: #1e3a8a;
    --primary-blue-light: #3b82f6;
    --primary-blue-dark: #1e40af;

    /* Accent Colors */
    --accent-orange: #f97316;
    --accent-orange-light: #fb923c;
    --accent-green: #10b981;
    --accent-red: #ef4444;

    /* Neutral Palette */
    --neutral-50: #f8fafc;
    --neutral-100: #f1f5f9;
    --neutral-200: #e2e8f0;
    --neutral-300: #cbd5e1;
    --neutral-400: #94a3b8;
    --neutral-500: #64748b;
    --neutral-600: #475569;
    --neutral-700: #334155;
    --neutral-800: #1e293b;
    --neutral-900: #0f172a;

    /* Spacing & Sizing */
    --spacing-xs: 0.5rem;
    --spacing-sm: 0.75rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;

    /* Border Radius */
    --radius-sm: 0.5rem;
    --radius-md: 0.75rem;
    --radius-lg: 1rem;
    --radius-xl: 1.5rem;

    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);

    /* Transitions */
    --transition-fast: 0.15s ease-in-out;
    --transition-normal: 0.3s ease-in-out;
    --transition-slow: 0.5s ease-in-out;
}

/* =================================================================
   BASE STYLES & LAYOUT
   ================================================================= */

body, html, .gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: linear-gradient(135deg, var(--neutral-50) 0%, var(--neutral-100) 100%) !important;
    color: var(--neutral-800) !important;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: var(--spacing-lg) !important;
}

/* =================================================================
   HERO SECTION
   ================================================================= */

.hero-section {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    padding: var(--spacing-xl) var(--spacing-lg);
}

.hero-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-orange) 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: var(--spacing-md);
    line-height: 1.1;
}

.hero-subtitle {
    font-size: clamp(1.1rem, 2.5vw, 1.3rem);
    color: var(--neutral-600);
    max-width: 600px;
    margin: 0 auto var(--spacing-xl) auto;
    font-weight: 500;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: var(--spacing-xl);
    flex-wrap: wrap;
    margin-top: var(--spacing-xl);
}

.stat-item {
    text-align: center;
    padding: var(--spacing-md);
    background: white;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    min-width: 120px;
    transition: transform var(--transition-normal);
}

.stat-item:hover {
    transform: translateY(-2px);
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary-blue);
    display: block;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--neutral-500);
    font-weight: 500;
}

/* =================================================================
   FEATURE CARDS
   ================================================================= */

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--spacing-lg);
    margin: var(--spacing-2xl) 0;
}

.feature-card {
    background: white;
    border-radius: var(--radius-xl);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--neutral-200);
    transition: all var(--transition-normal);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-blue), var(--accent-orange));
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-xl);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: var(--spacing-md);
    display: block;
}

.feature-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--neutral-800);
    margin-bottom: var(--spacing-sm);
}

.feature-description {
    color: var(--neutral-600);
    line-height: 1.6;
}

/* =================================================================
   FORM COMPONENTS
   ================================================================= */

.query-section {
    background: white;
    border-radius: var(--radius-xl);
    padding: var(--spacing-2xl);
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--neutral-200);
    margin: var(--spacing-xl) 0;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--neutral-800);
    margin-bottom: var(--spacing-md);
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.section-subtitle {
    color: var(--neutral-600);
    margin-bottom: var(--spacing-xl);
    font-size: 1rem;
}

/* Dropdown Styling */
.dropdown-container {
    margin-bottom: var(--spacing-xl);
}

.dropdown-container label {
    font-weight: 600 !important;
    color: var(--neutral-700) !important;
    font-size: 1rem !important;
    margin-bottom: var(--spacing-sm) !important;
    display: block !important;
}

.gr-dropdown {
    margin-bottom: var(--spacing-lg) !important;
}

.gr-dropdown select {
    border-radius: var(--radius-md) !important;
    border: 2px solid var(--neutral-200) !important;
    padding: var(--spacing-md) var(--spacing-lg) !important;
    font-size: 1rem !important;
    background: white !important;
    color: var(--neutral-700) !important;
    transition: all var(--transition-normal) !important;
    box-shadow: var(--shadow-sm) !important;
}

.gr-dropdown select:focus {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1) !important;
    outline: none !important;
}

.gr-dropdown select:hover {
    border-color: var(--neutral-300) !important;
}

/* Button Styling */
.button-group {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
    margin: var(--spacing-xl) 0;
}

.gr-button {
    border-radius: var(--radius-lg) !important;
    padding: var(--spacing-md) var(--spacing-xl) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: all var(--transition-normal) !important;
    border: none !important;
    cursor: pointer !important;
    min-width: 140px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: var(--spacing-sm) !important;
}

.gr-button.primary {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-light) 100%) !important;
    color: white !important;
    box-shadow: var(--shadow-md) !important;
}

.gr-button.primary:hover {
    background: linear-gradient(135deg, var(--primary-blue-dark) 0%, var(--primary-blue) 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-lg) !important;
}

.gr-button.secondary {
    background: white !important;
    color: var(--neutral-700) !important;
    border: 2px solid var(--neutral-200) !important;
    box-shadow: var(--shadow-sm) !important;
}

.gr-button.secondary:hover {
    background: var(--neutral-50) !important;
    border-color: var(--neutral-300) !important;
    transform: translateY(-1px) !important;
}

.gr-button:active {
    transform: translateY(0) !important;
}

/* =================================================================
   OUTPUT & STATUS MESSAGES
   ================================================================= */

.output-section {
    background: white;
    border-radius: var(--radius-xl);
    padding: var(--spacing-2xl);
    margin: var(--spacing-xl) 0;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--neutral-200);
    min-height: 400px;
}

/* Force markdown content to be visible with dark text */
.results-container,
.results-container * {
    color: var(--neutral-800) !important;
}

.results-container h1,
.results-container h2,
.results-container h3,
.results-container h4,
.results-container h5,
.results-container h6 {
    color: var(--neutral-900) !important;
    font-weight: 700 !important;
}

.results-container p,
.results-container li,
.results-container td,
.results-container th {
    color: var(--neutral-700) !important;
}

.results-container table {
    border-collapse: collapse !important;
    width: 100% !important;
    margin: var(--spacing-md) 0 !important;
}

.results-container th,
.results-container td {
    border: 1px solid var(--neutral-300) !important;
    padding: var(--spacing-sm) var(--spacing-md) !important;
    text-align: left !important;
}

.results-container th {
    background-color: var(--neutral-100) !important;
    font-weight: 600 !important;
    color: var(--neutral-800) !important;
}

.results-container code {
    background-color: var(--neutral-100) !important;
    color: var(--neutral-800) !important;
    padding: 0.2em 0.4em !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.results-container pre {
    background-color: var(--neutral-100) !important;
    color: var(--neutral-800) !important;
    padding: var(--spacing-md) !important;
    border-radius: var(--radius-md) !important;
    overflow-x: auto !important;
}

.results-container blockquote {
    border-left: 4px solid var(--primary-blue) !important;
    margin: var(--spacing-md) 0 !important;
    padding: var(--spacing-md) !important;
    background-color: var(--neutral-50) !important;
    color: var(--neutral-700) !important;
}

.status-message {
    display: flex;
    align-items: flex-start;
    gap: var(--spacing-md);
    padding: var(--spacing-xl);
    border-radius: var(--radius-lg);
    margin: var(--spacing-md) 0;
    animation: fadeIn 0.5s ease-in-out;
}

.status-message.info {
    background: linear-gradient(135deg, #dbeafe 0%, #f0f9ff 100%);
    border-left: 4px solid var(--primary-blue);
}

.status-message.success {
    background: linear-gradient(135deg, #d1fae5 0%, #ecfdf5 100%);
    border-left: 4px solid var(--accent-green);
}

.status-message.error {
    background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
    border-left: 4px solid var(--accent-red);
}

.status-message.loading {
    background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%);
    border-left: 4px solid var(--accent-orange);
}

.status-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
    margin-top: 0.1rem;
}

.status-content h3 {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--neutral-800);
    margin: 0 0 var(--spacing-sm) 0;
}

.status-content p {
    color: var(--neutral-600);
    margin: 0 0 var(--spacing-md) 0;
    line-height: 1.6;
}

.result-summary {
    background: rgba(255, 255, 255, 0.7);
    border-radius: var(--radius-md);
    padding: var(--spacing-lg);
    margin-top: var(--spacing-md);
}

.result-summary h4 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--neutral-800);
    margin: 0 0 var(--spacing-sm) 0;
}

.result-summary ul {
    margin: 0;
    padding-left: var(--spacing-lg);
}

.result-summary li {
    color: var(--neutral-700);
    margin-bottom: var(--spacing-xs);
}

.error-details {
    margin-top: var(--spacing-md);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.5);
    border-radius: var(--radius-sm);
}

.error-details summary {
    cursor: pointer;
    font-weight: 600;
    color: var(--neutral-700);
}

.error-details code {
    display: block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    color: var(--accent-red);
    margin-top: var(--spacing-sm);
    padding: var(--spacing-sm);
    background: rgba(239, 68, 68, 0.1);
    border-radius: var(--radius-sm);
}

/* =================================================================
   LOADING ANIMATION
   ================================================================= */

.loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--neutral-200);
    border-top: 3px solid var(--accent-orange);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    flex-shrink: 0;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* =================================================================
   MOBILE RESPONSIVENESS
   ================================================================= */

@media (max-width: 768px) {
    .gradio-container {
        padding: var(--spacing-md) !important;
    }

    .hero-section {
        padding: var(--spacing-md);
    }

    .hero-stats {
        gap: var(--spacing-md);
    }

    .stat-item {
        min-width: 100px;
        padding: var(--spacing-sm);
    }

    .features-grid {
        grid-template-columns: 1fr;
        gap: var(--spacing-md);
    }

    .feature-card, .query-section, .output-section {
        padding: var(--spacing-lg);
    }

    .button-group {
        flex-direction: column;
        align-items: stretch;
    }

    .gr-button {
        min-width: auto !important;
    }

    .status-message {
        flex-direction: column;
        text-align: center;
    }
}

@media (max-width: 480px) {
    .hero-title {
        font-size: 2.2rem;
    }

    .hero-subtitle {
        font-size: 1rem;
    }

    .feature-card, .query-section, .output-section {
        padding: var(--spacing-md);
    }

    .status-message {
        padding: var(--spacing-md);
    }
}

/* =================================================================
   ACCESSIBILITY IMPROVEMENTS
   ================================================================= */

.gr-button:focus-visible {
    outline: 3px solid var(--primary-blue) !important;
    outline-offset: 2px !important;
}

.gr-dropdown select:focus-visible {
    outline: 3px solid var(--primary-blue) !important;
    outline-offset: 2px !important;
}

/* Reduced motion for accessibility */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }

    .loading-spinner {
        animation: none;
    }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    :root {
        --neutral-200: #000000;
        --neutral-600: #ffffff;
        --primary-blue: #0000ff;
        --accent-orange: #ff6600;
    }
}
"""

# =============================================================================
# GRADIO INTERFACE DEFINITION
# =============================================================================

def create_interface():
    """Create the enhanced Gradio interface with modern styling and UX"""

    with gr.Blocks(
        css=enhanced_css,
        title="Transbiz AI - Transportation Logistics Dashboard",
        theme=gr.themes.Soft()
    ) as demo:

        # =================================================================
        # MAIN HEADING
        # =================================================================

        with gr.Row():
            gr.HTML("""
                <div style="text-align: center; margin: 2rem 0 1rem 0;">
                    <h1 style="
                        font-size: clamp(2.5rem, 6vw, 4.5rem);
                        font-weight: 900;
                        background: linear-gradient(135deg, #1e3a8a 0%, #f97316 100%);
                        background-clip: text;
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        margin: 0;
                        letter-spacing: -0.02em;
                        line-height: 1.1;
                    ">TransBizAI</h1>
                </div>
            """)

        # =================================================================
        # HERO SECTION
        # =================================================================

        with gr.Row(elem_classes="hero-section"):
            gr.HTML("""
                <div class="hero-title">🚛 Transbiz AI</div>
                <div class="hero-subtitle">
                    Advanced AI-powered insights for transportation and logistics operations.
                    Track bilties, manage cartage, monitor payments, and optimize your fleet in real-time.
                </div>
                <div class="hero-stats">
                    <div class="stat-item">
                        <span class="stat-number">1.2K+</span>
                        <span class="stat-label">Queries Processed</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">98.5%</span>
                        <span class="stat-label">Accuracy Rate</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">24/7</span>
                        <span class="stat-label">Real-time Monitoring</span>
                    </div>
                </div>
            """)

        # =================================================================
        # FEATURES OVERVIEW
        # =================================================================

        with gr.Row():
            gr.HTML("""
                <div class="features-grid">
                    <div class="feature-card">
                        <span class="feature-icon">📊</span>
                        <h3 class="feature-title">Real-time Analytics</h3>
                        <p class="feature-description">
                            Generate instant reports on bilties, cartage, and payment status with AI-powered insights.
                        </p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon">📈</span>
                        <h3 class="feature-title">Performance Monitoring</h3>
                        <p class="feature-description">
                            Visualize and track logistics performance metrics over time to identify trends.
                        </p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon">⚡</span>
                        <h3 class="feature-title">Smart Optimization</h3>
                        <p class="feature-description">
                            Make data-driven operational decisions with intelligent recommendations and forecasts.
                        </p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon">🔄</span>
                        <h3 class="feature-title">Automated Workflows</h3>
                        <p class="feature-description">
                            Reduce manual work with one-click intelligent queries and automated data processing.
                        </p>
                    </div>
                </div>
            """)

        # =================================================================
        # QUERY INTERFACE
        # =================================================================

        with gr.Row(elem_classes="query-section"):
            with gr.Column():
                gr.HTML("""
                    <h2 class="section-title">

                        Select Your Analysis Query
                    </h2>
                    <p class="section-subtitle">
                        Choose from our comprehensive set of logistics analytics queries to get instant insights
                        into your transportation operations.
                    </p>
                """)

                # Query Selection Dropdown
                with gr.Row(elem_classes="dropdown-container"):
                    query_input = gr.Dropdown(
                        choices=["Select a query to analyze your logistics data..."] + list_of_queries,
                        label="Available Analytics Queries",
                        elem_classes="query-dropdown",
                        interactive=True,
                        value="Select a query to analyze your logistics data..."
                    )

                # Action Buttons
                with gr.Row(elem_classes="button-group"):
                    submit_btn = gr.Button(
                        "Run Analysis",
                        elem_classes="primary",
                        variant="primary"
                    )
                    clear_btn = gr.Button(
                        "Reset",
                        elem_classes="secondary",
                        variant="secondary"
                    )

        # =================================================================
        # RESULTS SECTION
        # =================================================================

        with gr.Row(elem_classes="output-section"):
            with gr.Column():
                gr.HTML("""
                    <h2 class="section-title">

                        Analysis Results
                    </h2>
                """)

                output_display = gr.Markdown(
                    """
                    ## Ready to Analyze

                    Select a query above and click "Run Analysis" to get started with AI-powered logistics insights.
                                        """,
                    elem_classes="results-container"
                )

        # =================================================================
        # EVENT HANDLERS
        # =================================================================

        # Submit button with loading state
        submit_btn.click(
            fn=show_loading,
            outputs=output_display
        ).then(
            fn=process_query,
            inputs=query_input,
            outputs=output_display
        )

        # Clear button functionality
        clear_btn.click(
            fn=clear_interface,
            outputs=[query_input, output_display]
        )

        # Auto-submit on dropdown selection (optional UX enhancement)
        # Uncomment the line below if you want queries to run automatically on selection
        # query_input.change(fn=process_query, inputs=query_input, outputs=output_display)

    return demo

# =============================================================================
# APPLICATION LAUNCHER
# =============================================================================

if __name__ == "__main__":
    # Create and launch the enhanced interface
    demo = create_interface()

    # Launch with optimized settings for production
    demo.launch(
        inbrowser=True,
        share=False,  # Set to True if you want a public link
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,  # Default Gradio port
        show_error=True,  # Show detailed errors in development
        favicon_path=None,  # Add your favicon path here if available
        max_threads=10  # Optimize for concurrent users
    )