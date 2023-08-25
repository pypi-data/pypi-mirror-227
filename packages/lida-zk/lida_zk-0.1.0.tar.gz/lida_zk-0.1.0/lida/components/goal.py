import json
import logging
from lida.utils import clean_code_snippet
from llmx_zk import TextGenerator
from lida.datamodel import Goal, TextGenerationConfig


system_prompt_chinese = """你是一位经验丰富的数据分析师和可视化专家，当给出数据摘要时，他可以生成给定数量的关于数据的有洞察力的目标。你建议的可视化必须遵循可视化最佳实践（例如，必须使用条形图而不是饼图来比较数量），并且要有意义（例如，在适当的情况下在地图上绘制经度和纬度）。

您建议的目标必须提到上面数据集摘要中的确切字段. ##您的输出必须仅为JSON列表格式的代码段,且必须也只能包含"index","question","visualization"和"rationale"四个字段.
字段表示含义如下：
"index" : 索引,从0开始
"question" : 根据给定的数据集生成的有意义的问题
"visualization" : 根据数据集和"question"生成的可视化目标
"rationale" : 该可视化目标的意义,即为什么选择这样的可视化目标

举例如下:
[{ "index": 0,  "question": "What is the distribution of X", "visualization": "histogram of X", "rationale": "This tells about "}, .. ]
"""

system_prompt_mine = """You are a an experienced data analyst as well as visualization specialist who can generate a given number of insightful GOALS about data, when given a summary of the data. The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities) AND BE MEANINGFUL (e.g., plot longitude and latitude on maps where appropriate).

The GOALS that you recommend must mention the exact fields from the dataset summary above. Your OUTPUT MUST BE ONLY A CODE SNIPPET of a JSON LIST in the format, and it must only contain four fields: "index", "question", "visualization", and "rational":
The meaning of the field representation is as follows:
'index': Index, starting from 0
'question': A meaningful question generated based on a given dataset
'visualization': Visualization targets generated based on datasets and questions
'rational': The meaning of the visualization goal, which is why such a visualization goal was chosen

For example:
[{ "index": 0,  "question": "What is the distribution of X", "visualization": "histogram of X", "rationale": "This tells about "}, .. ]

"""

# 原始 prompt
system_prompt = """You are a an experienced data analyst as well as visualization specialist who can generate a given number of insightful GOALS about data, when given a summary of the data. The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities) AND BE MEANINGFUL (e.g., plot longitude and latitude on maps where appropriate).

The GOALS that you recommend must mention the exact fields from the dataset summary above. Your OUTPUT MUST BE ONLY A CODE SNIPPET of a JSON LIST in the format:
```[{ "index": 0,  "question": "What is the distribution of X", "visualization": "histogram of X", "rationale": "This tells about "}, .. ]
```
"""

logger = logging.getLogger(__name__)


class GoalExplorer():
    """Generat goals given a summary of data"""

    def __init__(self) -> None:
        pass

    def generate(self, summary: dict, textgen_config: TextGenerationConfig,
                 text_gen: TextGenerator, n=5) -> list[Goal]:
        """Generate goals given a summary of data"""

        user_prompt = f"""The number of GOALS to generate is {n}. Generate {n} GOALS in the right format given the data summary below,\n .
        {summary} \n""" + """

        .
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": user_prompt},
        ]

        result: list[Goal] = text_gen.generate(messages=messages, config=textgen_config)

        try:
            json_string = clean_code_snippet(result.text[0]["content"])
            result = json.loads(json_string)
            # cast each item in the list to a Goal object
            if isinstance(result, dict):
                result = [result]
            result = [Goal(**x) for x in result]
        except json.decoder.JSONDecodeError:
            logger.info(f"Error decoding JSON: {result.text[0]['content']}")
            print(f"Error decoding JSON: {result.text[0]['content']}")
            raise ValueError(
                "The model did not return a valid JSON object while attempting generate goals. Please try again.")
        return result
