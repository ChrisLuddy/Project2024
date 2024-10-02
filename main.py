from AI_Crew import AI_Crew


if __name__ == "__main__":
    # Define the model configuration for each agent (Placeholder models for local and API testing. Successful on personal keys / local machine)
    models_config = {
        "Researcher": {"model": "ollama/mistral-nemo:12b", "base_url": "http://localhost:11434"},
        "Accountant": {"model": "gpt-4o-mini", "base_url": "https://api.openai.com/v1"},
        "Recommender": {"model": "groq/llama3-8b-8192", "base_url": "https://api.groq.com/openai/v1"},
        "Blogger": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"}
    }

    # Initialize the AI_Crew with an API key and the model configuration
    ai_crew = AI_Crew(api_key=" ", models_config=models_config)

    # Define tasks for each agent
    tasks = [


        ai_crew.create_task(
            agent=ai_crew.agents[0],
            description="Research the stock performance and recent news of Tesla (TSLA). ",
            expected_output="Provide a summary of Tesla's recent stock performance, financials, and any news articles."
        ),

        ai_crew.create_task(
            agent=ai_crew.agents[1],
            description="Calculate key accounting ratios for Tesla (e.g., P/E ratio, Debt-to-Equity, and Return on Equity).",
            expected_output="Provide calculations and interpretations for P/E, Debt-to-Equity, and ROE ratios."
        ),
        ai_crew.create_task(
            agent=ai_crew.agents[2],
            description="Based on Tesla's stock and financial data, make a buy, sell, or hold recommendation.",
            expected_output="Provide a recommendation with supporting reasons: buy, sell, or hold."
        ),
        ai_crew.create_task(
            agent=ai_crew.agents[3],
            description="Format the research, accounting data, and recommendation into a blog post.",
            expected_output="A well-formatted blog post combining research, financial ratios, and a final recommendation."
        )
    ]
    # Execute the tasks and print the results
    result = ai_crew.kickoff(tasks)

    print("############")
    print(result)
