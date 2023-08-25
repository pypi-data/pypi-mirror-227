# Visualization manager class that handles the visualization of the data with the following methods

# summarize data given a df
# generate goals given a summary
# generate generate visualization specifications given a summary and a goal
# execute the specification given some data

import os
from typing import List, Union
import logging

import pandas as pd
from llmx_zk import llm, TextGenerator
from lida.datamodel import Goal, Summary, TextGenerationConfig
from lida.utils import read_dataframe
from ..components.summarizer import Summarizer
from ..components.goal import GoalExplorer
from ..components.executor import ChartExecutor
from ..components.viz import VizGenerator, VizEditor, VizExplainer, VizEvaluator, VizRepairer, VizRecommender

import lida.web as lida


logger = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, text_gen: TextGenerator = None, llm_model: str = "openai", **kwargs) -> None:
        self.text_gen = text_gen or llm(llm_model, **kwargs)
        self.summarizer = Summarizer()
        self.goal = GoalExplorer()
        self.vizgen = VizGenerator()
        self.vizeditor = VizEditor()
        self.executor = ChartExecutor()
        self.explainer = VizExplainer()
        self.evaluator = VizEvaluator()
        self.repairer = VizRepairer()
        self.recommender = VizRecommender()
        self.data = None
        self.infographer = None

    def check_textgen(self, config: TextGenerationConfig):
        """Check if self.text_gen is the same as the config passed in. If not, update self.text_gen 更新model.generate()的参数"""

        if config.provider is None:
            config.provider = self.text_gen.provider
            return

        if self.text_gen.provider != config.provider:
            print(
                f"Switchging Text Generator Provider from {self.text_gen.provider} to {config.provider}")
            logger.info(
                f"Switchging Text Generator Provider from {self.text_gen.provider} to {config.provider}")
            self.text_gen = llm(provider=config.provider)

    # data summarize
    def summarize(
        self,
        data: Union[pd.DataFrame, str],
        file_name="",
        n_samples: int = 3,
        summary_method: str = "default",
        textgen_config: TextGenerationConfig = TextGenerationConfig(n=1, temperature=0),
    ):

        self.check_textgen(config=textgen_config)

        if isinstance(data, str):
            file_name = data.split("/")[-1]
            data = read_dataframe(data)

        self.data = data
        # self.data = data
        return self.summarizer.summarize(
            data=self.data, text_gen=self.text_gen, file_name=file_name, n_samples=n_samples,
            summary_method=summary_method, textgen_config=textgen_config)

    def goals(
            self, summary, textgen_config: TextGenerationConfig = TextGenerationConfig(),
            n=5):
        self.check_textgen(config=textgen_config)

        return self.goal.generate(summary=summary, text_gen=self.text_gen,
                                  textgen_config=textgen_config, n=n)

    def visualize(
        self,
        summary,
        goal,
        textgen_config: TextGenerationConfig = TextGenerationConfig(),
        library="seaborn",
        return_error: bool = False,
    ):

        self.check_textgen(config=textgen_config)   # 查看配置文件是否需要更新
        # 根据预设的模板和使用的library来得到代码，type:list(str)
        code_specs = self.vizgen.generate(
            summary=summary, goal=goal, textgen_config=textgen_config, text_gen=self.text_gen,
            library=library)

        # print("The response of llm on visualize: \n", code_specs)
        # code_specs = ["import matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\n# plan -\ndef plot(data: pd.DataFrame):\n    data['periodBeginValue'] = pd.to_datetime(data['periodBeginValue'], errors='coerce')\n    data = data[pd.notna(data['periodBeginValue'])]\n    data['periodBeginValue'] = data['periodBeginValue'].dt.strftime('%Y-%m-%d')\n    data = data[data['question'] == '2022年3月，在线上市场，单门冰箱零售量，规模环比增速最快的五个机型分别是哪些？']\n    data = data.sort_values(by='attValue', ascending=False).head(5)\n    fig, ax = plt.subplots(figsize=(8, 6))\n    ax.bar(data['attValue'], data['api_name'], color=np.random.rand(5,3))\n    ax.set_xlabel('Sales')\n    ax.set_ylabel('Brand')\n    ax.set_title('What are the top 5 brands with the highest online retail sales for single-door refrigerators in March 2022?', wrap=True)\n    return plt;\n\nchart = plot(data) # data already contains the data to be plotted. Always include this line. No additional code beyond this line."]

        charts = self.execute(
            code_specs=code_specs,
            data=self.data,
            summary=summary,
            library=library,
            return_error=return_error,
        )
        # print(type(charts))             # list(ChartExecutorResponse->object)
        return charts

    def execute(
        self,
        code_specs,
        data,
        summary: Summary,
        library: str = "seaborn",
        return_error: bool = False,
    ):
        if data is None:
            root_file_path = os.path.dirname(os.path.abspath(lida.__file__))
            data = read_dataframe(
                os.path.join(root_file_path, "files/data", summary.file_name)
            )

        # col_properties = summary.properties
        return self.executor.execute(
            code_specs=code_specs,
            data=data,
            summary=summary,
            library=library,
            return_error=return_error,
        )

    def edit(
        self,
        code,
        summary: Summary,
        instructions: List[str],
        textgen_config: TextGenerationConfig = TextGenerationConfig(n=1, temperature=0),
        library: str = "seaborn",
        return_error: bool = False,
    ):
        """Edit a visualization code given a set of instructions

        Args:
            code (_type_): _description_
            instructions (List[Dict]): A list of instructions

        Returns:
            _type_: _description_
        """

        self.check_textgen(config=textgen_config)

        if isinstance(instructions, str):
            instructions = [instructions]

        code_specs = self.vizeditor.generate(
            code=code,
            summary=summary,
            instructions=instructions,
            textgen_config=textgen_config,
            text_gen=self.text_gen,
            library=library,
        )

        charts = self.execute(
            code_specs=code_specs,
            data=self.data,
            summary=summary,
            library=library,
            return_error=return_error,
        )
        return charts

    def repair(
        self,
        code,
        goal: Goal,
        summary: Summary,
        feedback,
        textgen_config: TextGenerationConfig = TextGenerationConfig(),
        library: str = "seaborn",
        return_error: bool = False,
    ):
        """ Repair a visulization given some feedback"""
        self.check_textgen(config=textgen_config)
        code_specs = self.repairer.generate(
            code=code,
            feedback=feedback,
            goal=goal,
            summary=summary,
            textgen_config=textgen_config,
            text_gen=self.text_gen,
            library=library,
        )
        charts = self.execute(
            code_specs=code_specs,
            data=self.data,
            summary=summary,
            library=library,
            return_error=return_error,
        )
        return charts

    def explain(
        self,
        code,
        textgen_config: TextGenerationConfig = TextGenerationConfig(),
        library: str = "seaborn",
    ):
        """Explain a visualization code given a set of instructions

        Args:
            code (_type_): _description_
            instructions (List[Dict]): A list of instructions

        Returns:
            _type_: _description_
        """
        self.check_textgen(config=textgen_config)
        # print("textgen_config:", textgen_config)
        return self.explainer.generate(
            code=code,
            textgen_config=textgen_config,
            text_gen=self.text_gen,
            library=library,
        )

    def evaluate(
        self,
        code,
        goal: Goal,
        textgen_config: TextGenerationConfig = TextGenerationConfig(),
        library: str = "seaborn",
    ):
        """Evaluate a visualization code given a goal

        Args:
            code (_type_): _description_
            goal (Goal): A visualization goal

        Returns:
            _type_: _description_
        """

        self.check_textgen(config=textgen_config)

        return self.evaluator.generate(
            code=code,
            goal=goal,
            textgen_config=textgen_config,
            text_gen=self.text_gen,
            library=library,
        )

    def recommend(
        self,
        code,
        summary: Summary,
        n=4,
        textgen_config: TextGenerationConfig = TextGenerationConfig(),
        library: str = "seaborn",
        return_error: bool = False,
    ):
        """Edit a visualization code given a set of instructions

        Args:
            code (_type_): _description_
            instructions (List[Dict]): A list of instructions

        Returns:
            _type_: _description_
        """

        self.check_textgen(config=textgen_config)

        code_specs = self.recommender.generate(
            code=code,
            summary=summary,
            n=n,
            textgen_config=textgen_config,
            text_gen=self.text_gen,
            library=library,
        )
        # print("code_specs:\n", code_specs)
        charts = self.execute(
            code_specs=code_specs,
            data=self.data,
            summary=summary,
            library=library,
            return_error=return_error,
        )
        return charts

    def infographics(self, visualization: str, n: int = 1,
                     style_prompt: Union[str, List[str]] = "",
                     return_pil: bool = False
                     ):
        """
        Generate infographics using the peacasso package.

        Args:
            visualization (str): A visualization code
            n (int, optional): The number of infographics to generate. Defaults to 1.
            style_prompt (Union[str, List[str]], optional): A style prompt or list of style prompts. Defaults to "".

        Raises:
            ImportError: If the peacasso package is not installed.
        """

        try:
            import peacasso

        except ImportError as exc:
            raise ImportError(
                'Please install lida with infographics support. pip install lida[infographics]. You will also need a GPU runtime.'
            ) from exc

        from ..components.infographer import Infographer

        if self.infographer is None:
            logger.info("Initializing Infographer")
            self.infographer = Infographer()
        return self.infographer.generate(
            visualization=visualization, n=n, style_prompt=style_prompt, return_pil=return_pil)
