import functools
from langchain_openai import ChatOpenAI
from AutoYT_SYSTEM_PROMPTS import(
VIDEO_MAKER_SYSTEM_PROMPT,
VIDEO_UPLOADER_SYSTEM_PROMPT
)
from typing import Annotated, Sequence, TypedDict
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, StateGraph
from tools import make_video, upload
from define_vars import set_environment_variables
import operator

set_environment_variables("AutoYT")

#Specify what OpenAI LLM we want to use
LLM = ChatOpenAI(model="gpt-3.5-turbo-0125")

#Assign names to our agents
VIDEO_MAKER_AGENT_NAME = "video_maker"
VIDEO_UPLOADER_AGENT_NAME = "video_uploader"


#create an agent template
def create_agent(llm: BaseChatModel, system_prompt: str, tools: list):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    return agent_executor
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def agent_node(state: AgentState, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}

#Create our video maker agent
video_maker_agent = create_agent(llm=LLM, system_prompt=VIDEO_MAKER_SYSTEM_PROMPT, tools=[make_video])

#Create our video uploader agent
video_uploader_agent = create_agent(llm=LLM, system_prompt=VIDEO_UPLOADER_SYSTEM_PROMPT, tools=[upload])


#Corresponding nodes
video_maker_agent_node = functools.partial(
    agent_node, agent=video_maker_agent, name=VIDEO_MAKER_AGENT_NAME
)

video_uploader_agent_node = functools.partial(
    agent_node, agent=video_uploader_agent, name=VIDEO_UPLOADER_AGENT_NAME
)

#Make a new workflow
workflow = StateGraph(AgentState)

#Add our agents to the workflow
workflow.add_node(VIDEO_MAKER_AGENT_NAME, video_maker_agent_node)
workflow.add_node(VIDEO_UPLOADER_AGENT_NAME, video_uploader_agent_node)

#Video maker agent sends its outputs to video uploader agent
workflow.add_edge(VIDEO_MAKER_AGENT_NAME, VIDEO_UPLOADER_AGENT_NAME)

#Once video uploader agent is done with it's task, end the script
workflow.add_edge(VIDEO_UPLOADER_AGENT_NAME, END)

#Make it so the workflow starts with the video maker agent
workflow.set_entry_point(VIDEO_MAKER_AGENT_NAME)

video_maker_graph = workflow.compile()

test_input = {"messages": [HumanMessage(content="MAKE THE VIDEO")]}

video_maker_graph.invoke(test_input)