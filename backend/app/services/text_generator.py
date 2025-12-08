from typing import Sequence, TypedDict, Annotated, Optional
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

# import os
import time
import json

import asyncio
from app.services.platforms.combined_service import post
from app.scraper import search, search_and_scrape
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse
from app.logger import setup_logger

logger = setup_logger(__name__)

# from dotenv import load_dotenv
# load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    tweet: Annotated[str, "≤15 words, must include hashtags, mentions, emojis"]
    blog_post: Annotated[str, "≥250 words, detailed and informative"]
    reddit_post: Annotated[str, "JSON string with 'title' and 'body'; 'body' supports Markdown"]
    input_index: int
       
def run_document_agent(current_user: UserResponse, db: AsyncSession, inputs=None, auto=False, categories=None):  
    
    # time.sleep(2)   #   Pause at start 
    
    @tool 
    def update(tweet: str, blog_post: str, reddit_post: str) -> dict:
        """Updates the document with tweet, blog_post and reddit_post"""

        time.sleep(1)
        
        return {
            "tweet": tweet,
            "blog_post": blog_post,
            "reddit_post": reddit_post
        }

        
    @tool
    def save(filename: str, tweet: str, blog_post: str, reddit_post: str) -> str:
        """Save the Document in a text file and finish the process.

        Args:
            filename (str): Name of the text file.
            tweet (str): A short message (max 15 words) including hashtags (#), mentions (@), w
                        and emojis 😃🔥✨ when relevant.
                        
            blog_post (str): A detailed and informative blog_post of atleast 250 words, expanding on the tweets theme.
            reddit_post (str): JSON string with 'title' and 'body'; 'body' supports Markdown
        """
        
        time.sleep(1)
        
        if not filename.endswith(".txt"):
            filename = f"{filename}.txt"
            
        #post code --> write later (check the returns)
        # try:
        #     postTweet(tweet)
        #     logger.info("Tweet posted successfully!")
        # except Exception as e:
        #     logger.info(f"Tweet posting failed: {str(e)}")
            
        # try:
        #     postBlog(blog_post)
        #     logger.info("Blog posted successfully!")
        # except Exception as e:
        #     logger.info(f"Blog posting failed: {str(e)}")
            
        # try:
        #     reddit_post_dict = json.loads(reddit_post)
        #     title = reddit_post_dict['title']
        #     body = reddit_post_dict['body']
  
        #     postReddit(title=title, text=body)
        #     logger.info("Reddit posted Successfully!")
                
        # except Exception as e:
        #     logger.info(f"Reddit posting failed: {str(e)}")
        
        
        # post(current_user, db)
            
        return f"Document has been saved successfully to {filename}"
    
        #   Save file code
        # DATA_PATH = r"C:\Users\rvisw\OneDrive\Desktop\shashank_Project\content_creation_agent\data\final_ouput"
        # FILE_PATH = os.path.join(DATA_PATH, filename)
        
        
        # try: 
        #     document_content = f"Tweet: \n{tweet}\nBlog Post: \n{blog_post}\n Reddit Post: \n{reddit_post}\n"
        #     with open(FILE_PATH, "w", encoding="utf-8") as file:
        #         file.write(document_content)
        #     logger.info(f"\n Document saved to {filename}")
        #     return f"Document has been saved successfully to {filename}"
        # except Exception as e:
        #     return f"File not saved due to error: {str(e)}"
        
              
    @tool    
    def search_tool(query: str) -> str:
        """
        This tool searches and returns information from the web using search api and scraping.
        """
        
        time.sleep(1)
        
        data = asyncio.run(search(query, categories=categories))
        scraped_data = asyncio.run(search_and_scrape(query, categories=categories, data=data, maxURL=5))
        
        # data["results"] -> format
        # "url": "https://finance.yahoo.com/news/buy-cryptocurrency-xrp-while-under-091500196.html?fr=sycsrp_catchall",
        # "title": "Should You Buy Cryptocurrency XRP While It's Under $3?",
        # "content": "This has always been the core of XRP's investing thesis: As more banks adopt the technology, it will..."
        
        #   If you want to mention source: output = f"Sources: {},\ncontent:{content}" return this.
        
        results = []
        results.append("Search Results: \n")
        for result in data["results"]:
            if result.get("title").strip() and result.get("content").strip():
                results.append(f'title: {result["title"]}\ncontent: {result["content"]}\n')
        
        results.append("Scraped Results: \n")
        for result in scraped_data:         #   If you want first search to be latest (last in content) use "reversed(scraped_data)"
            if result.get('text'):
                results.append(f'title: {result["title"]}\ncontent: {result["text"]}\n')
        
        content = "\n\n".join(results)
        
        if not content:
            return f"Information not found in the retrieved content."
        
        return content
        
        
    tools = [search_tool, update, save]
    llm = init_chat_model('gemini-2.5-flash', model_provider="google_genai").bind_tools(tools)

    #   Function to automate user input
    def get_User_or_Auto_input(state: AgentState, config=None) -> HumanMessage :
        
        cfg = config.get("configurable", {}) if config else {}
        
        if cfg.get("auto_mode"):
            inputs = cfg.get("inputs")
            current_idx = state.get("input_index", 0)
            user_message = HumanMessage(content="Save it")  # Default (if not saved by previous command)
            
            if current_idx < len(inputs):
                user_input = inputs[current_idx]
                user_message = HumanMessage(content=user_input)
        
        # if AUTO_MODE:
        #     user_input = f"Save it."
        #     user_message = HumanMessage(content=user_input)
        
        elif not state["messages"]:
            user_input = "I'm ready to help you update the document. What would you like to create?"
            user_message = HumanMessage(content=user_input)
            
        else:
            user_input = input("\n How would you like to update the document?")
            logger.info(f"\n USER: {user_input}")
            user_message = HumanMessage(content=user_input)
            
        return user_message


    def our_agent(state: AgentState, config=None) -> AgentState:
        
        system_prompt = SystemMessage(content=f"""
            You are an Intelligent AI Assistant. Your role is to retrieve information using `search_tool`, 
            then generate, update, or save content in strict compliance with the JSON schema below:

            {{
                "tweet": [
                    "Must include hashtags (#), mentions (@), and emojis 😃🔥✨ when relevant",
                    "Maximum of 15 words",
                    "Concise, catchy, and engaging"
                ],
                "blog_post": [
                    "At most 1000 words",
                    "Detailed, informative, and engaging", 
                    "Should expand on the Tweet's theme with depth and clarity",
                    "Blog post must be written as a raw HTML fragment (no <!doctype>, <html>, <head>, or <body> tags). Use valid HTML elements like <h1>, <p>, <ul>, etc."
                ],
                "reddit_post": [
                    "JSON string with keys 'title' and 'body'",
                    "'title': short and catchy (≤300 characters)",
                    "'body': detailed text with Reddit Markdown (not HTML)",
                    "This should only contain 'title' and 'body'.Do not include extra fields ",
                    "Body may include bullet points, lists, and formatting relevant to discussion",
                    "can be empty if not applicable"
                    "Add relevant subreddit flair if appropriate(optional)",
                    "End with a question or call to discussion to encourage comments(optional)"
                ]
            }}

            ### Rules:
            - Always call `search_tool` first to gather context, unless the answer is already fully in the current document.
            - The query sent to search_tool must be a concise, summarized version of the user input, formatted as a search-friendly string or set of keywords, suitable for search engines like Google, Bing, or Qwant.
            - **After retrieving documents**, always generate both `tweet`, `blog_post` and `reddit_post` and call the `update` tool with the full updated content
            - Always use **tools** (`update`, `save`) for any JSON output. Do NOT directly print JSON in your final reply.
            - `update` must include both the full updated "tweet", "blog_post" and "reddit_post".
            - `save` saves both tweet and blog post content together.
            - **IMPORTANT**: After calling `save`, wait for the tool result. If you see "Document has been saved successfully", the process is complete.
            - Always generate a descriptive filename ending with `.txt` (e.g., `"tweet_marketing.txt"`, `"blog_ai_trends.txt"`).
            - Filenames must reflect the document content meaningfully.
            - Cite specific parts of retrieved information in the blog post.
            - After `update` or `save`, always pass the **entire current state** of the document as tool arguments.
            - If API posting fails but file is saved, consider it a success.

            ### Current Document:
            {{
                "tweet": "{state.get('tweet', '')}",
                "blog_post": "{state.get('blog_post', '')}",
                "reddit_post": "{state.get('reddit_post', '')}"
            }}
        """)
        
        
        user_message = get_User_or_Auto_input(state, config)

        prompt = [system_prompt] + list(state["messages"]) + [user_message]
        
        response = llm.invoke(prompt)
        
        logger.info(f"\nCurrent tweet: {state['tweet']}")
        logger.info(f"\nCurrent blog_post: {state['blog_post']}")
        logger.info("\nCurrent reddit_post: {state['reddit_post']}")
        
        logger.info(f"\n AI: {response.content}")
        if hasattr(response, "tool_calls") and response.tool_calls:
            logger.info(f"\n Using TOOLS: {[tc for tc in response.tool_calls]}")

        return {
            "messages": list(state['messages']) + [user_message, response], 
            "input_index": state["input_index"]+1, 
        }

    def should_continue(state: AgentState):
        """Decides whether we continue or end the conversation"""
        messages = state['messages']
        
        if not messages: 
            return "continue"
        #   End if Saved
        for message in reversed(messages):
            if(isinstance(message, ToolMessage)):
            
                if ("saved successfully" in message.content.lower() or ("document has been saved" in message.content.lower())):
                    logger.info("Found save confirmation - Ending...")  
                    return "end"
            
                if ("File not saved" in message.content.lower()):
                    logger.error("Save Error - Ending....")
                    return "end"
                #   End if no retrieved data
            
                if ("information not found" in message.content.lower() and "retrieved content" in message.content.lower()):
                    logger.error("No data found - Ending.....")  
                    return "end"
        
        return "continue"

    def log_messages(messages):
        """Funtion I made to log messages in a readable format"""
        if not messages: 
            return
        
        for message in messages[-3:]:
            if isinstance(message, ToolMessage):
                logger.info(f"\n TOOL RESULT: {message.content}")

    def create_stateful_tool_node(tools):
        
        def stateful_tool_node(state: AgentState):
            tool_node = ToolNode(tools)
            result = tool_node.invoke(state)
            
            updated_tweet = ""
            updated_blog_post = ""
            updated_reddit_post = ""
        
            if state["messages"]:
                last_ai_message = state["messages"][-1]
                if hasattr(last_ai_message, "tool_calls"):
                    for tool_call in last_ai_message.tool_calls:
                        if tool_call["name"] in ["update", "save"]:
                            tool_args = tool_call["args"]
                            updated_tweet = tool_args["tweet"]
                            updated_blog_post = tool_args["blog_post"]
                            updated_reddit_post = tool_args["reddit_post"]
                            
            return {
                "messages": result["messages"],
                "tweet": updated_tweet,
                "blog_post": updated_blog_post,
                "reddit_post": updated_reddit_post
            }            
            
        return stateful_tool_node
                
    graph = StateGraph(AgentState)

    graph.add_node("tools", create_stateful_tool_node(tools))
    graph.add_node("agent", our_agent)

    graph.add_edge(START, "agent")
    graph.add_edge("agent", "tools")

    graph.add_conditional_edges(
        "tools",
        should_continue,
        {
            "continue": "agent",
            "end": END
        }
    )

    app = graph.compile()


    logger.info("\n *****DRAFTER*****")
    
    # Toggle Automatic
    
    config = None
    
    if inputs and auto:
        config = {
            "configurable": {
                "inputs": inputs,
                "auto_mode": auto
            }
        }
        
    state = {"messages": [], 'tweet':"", 'blog_post':"", 'reddit_post':"", "input_index":0}

    final_state = None
    
    for step in app.stream(state, config=config, stream_mode="values"):
        if "messages" in step:
            log_messages(step["messages"])
        final_state = step
        
    logger.info("\n***FINISHED DRAFTER***")
    return final_state

if __name__ == "__main__":
    run_document_agent()
            


