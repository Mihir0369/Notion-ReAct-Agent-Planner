from agent.bot import make_agent
from dotenv import load_dotenv

def main():
    load_dotenv()
    agent = make_agent()
    query = "Tell me the weather in Toronto"

    response = agent.invoke({"messages": [("user", query)]})
    print(response['messages'][-1].content)

if __name__ == "__main__":
    main()
