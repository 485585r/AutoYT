import os
from decouple import config
from datetime import date

def set_environment_variables(project_name: str = "") -> None:
    if not project_name:
        project_name = f"Test_{date.today()}"





    os.environ["OPENAI_API_KEY"] = str(config("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",
                                              default="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"))
    os.environ["LANGCHAIN_API_KEY"] = str(config("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",
                                                 default="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"))
    os.environ["LANGCHAIN_PROJECT"] = project_name
    os.environ['TAVILY_API_KEY'] = str(
        config("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", default="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"))

    print("API KEYS LOAED AND TRACING SET WITH PROJECT NAME", project_name)