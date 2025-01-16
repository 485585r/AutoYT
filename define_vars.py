import os
#from decouple import config
from datetime import date

def set_environment_variables(project_name: str = "") -> None:
    if not project_name:
        project_name = f"Test_{date.today()}"





    os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
    os.environ["LANGCHAIN_API_KEY"] = "YOUR_API_KEY"
    os.environ["LANGCHAIN_PROJECT"] = project_name
    os.environ['TAVILY_API_KEY'] = "YOUR_API_KEY"

    print("API KEYS LOADED AND TRACING SET WITH PROJECT NAME", project_name)