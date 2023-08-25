from dataclasses import asdict
from typing import Dict
from llmx_zk import TextGenerator, TextGenerationConfig, TextGenerationResponse

from ..scaffold import ChartScaffold

# 你是一个乐于助人的助手，擅长为可视化编写完美的代码。给定一些代码模板，在给定数据集和所描述的目标的情况下，完成模板以生成可视化。您编写的代码必须遵循可视化最佳实践，即满足指定目标，应用正确的转换，使用正确的可视化类型，使用正确数据编码，并使用正确的美学（例如，确保轴清晰可见）。应用的转换必须正确，使用的字段必须正确。可视化代码必须正确，并且不得包含任何语法或逻辑错误。你必须首先为你将如何解决任务生成一个简短的计划，例如你将应用什么转换，例如如果你需要构建一个新的列，你将使用什么字段，你将采用什么可视化类型，你将运用什么美学，等等。

# 您必须始终使用提供的代码模板返回代码。不要添加注释或解释。
system_prompt = """
You are a helpful assistant highly skilled in writing PERFECT code for visualizations. Given some code template, you complete the template to generate a visualization given the dataset and the goal described. The code you write MUST FOLLOW VISUALIZATION BEST PRACTICES ie. meet the specified goal, apply the right transformation, use the right visualization type, use the right data encoding, and use the right aesthetics (e.g., ensure axis are legible). The transformations you apply MUST be correct and the fields you use MUST be correct. The visualization CODE MUST BE CORRECT and MUST NOT CONTAIN ANY SYNTAX OR LOGIC ERRORS. You MUST first generate a brief plan for how you would solve the task e.g. what transformations you would apply e.g. if you need to construct a new column, what fields you would use, what visualization type you would use, what aesthetics you would use, etc.
YOU MUST ALWAYS return code using the provided code template. DO NOT add notes or explanations.
"""


class VizGenerator(object):
    """Generate visualizations from prompt"""

    def __init__(
        self
    ) -> None:

        self.scaffold = ChartScaffold()

    def generate(self, summary: Dict, goal: Dict,
                 textgen_config: TextGenerationConfig, text_gen: TextGenerator, library='altair'):
        """Generate visualization code given a summary and a goal"""

        library_template, library_instructions = self.scaffold.get_template(goal, library)
        # print(f"The template on {library}: \n{library_template}")
        print(f"The instruction on LLM: \n{library_instructions}")
        # role: 标识信息的发送者角色
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"The dataset summary is : {summary}"},
            library_instructions,
            {"role": "system", "content": f"Use the code template below \n {library_template}. DO NOT modify the rest of the code template."},
            {"role": "user",
             "content":
             "Always add a legend with various colors where appropriate. The visualization code MUST only use data fields that exist in the dataset (field_names) or fields that are transformations based on existing field_names). Only use variables that have been defined in the code or are in the dataset summary. You MUST return a full python code program that starts with an import statement. DO NOT add any explanation"}]

        # print(textgen_config.messages)
        completions: TextGenerationResponse = text_gen.generate(
            messages=messages, config=textgen_config)
        return [x['content'] for x in completions.text]
