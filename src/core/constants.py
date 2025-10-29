"""Constants configuration module"""
import yaml
import os
from pathlib import Path

# Get project root directory
ROOT_DIR = Path(__file__).parent.parent.parent

# Load configuration file
CONFIG_PATH = ROOT_DIR / "config.yaml"

def load_config():
    """Load configuration from config file"""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_PATH}\n"
            f"Please create config.yaml file and configure the relevant parameters"
        )
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config

# Load configuration
_config = load_config()

# Region configuration
def _get_region_tuple(region_config):
    """Convert region in configuration to tuple format"""
    return (
        region_config['x'],
        region_config['y'],
        region_config['width'],
        region_config['height']
    )

TIMESTAMP_REGION = _get_region_tuple(_config['timestamp_region'])
TERMINAL_REGION = _get_region_tuple(_config['terminal_region'])
CURSOR_REGION = _get_region_tuple(_config['cursor_region'])

# Prompt templates
class Prompts:
    """Prompt templates"""
    
    # System prompt
    SYSTEM_PROMPT = (
        "Here are several rules you must follow: "
        "1.Do not interact with humans while performing your task. "
        "2.After each round of task completion, summarize your progress in a paragraph. "
        "Note: Do not create a new file, just place this summary in the dialog box. "
        "3.After each round of task completion, provide a test script (usually by running a file: python file_path). "
        "Only display the script, do not engage in human-computer interaction. "
        "4.The test result must only be in the form of printed output to the console."
    )
    
    # Extract timestamp text
    EXTRACT_TIMESTAMP = (
        "Extract the text in this image."
        "Return only the text, and do not include any other information."
    )
    
    # Extract unit test script
    EXTRACT_UNIT_TEST = (
        "Extract the unit test script from the screenshot. "
        "Common unit test scripts are usually by running a file like this: python file_path.py. "
        "Return only the script without quotation marks."
    )
    
    # Extract Cursor output
    EXTRACT_CURSOR_OUTPUT = (
        "Extract the cursor summary information from the screenshot. "
        "Return only the summary information, and do not include any other information."
    )
    
    # Extract terminal information
    EXTRACT_TERMINAL_INFO = (
        "Extract the terminal information from the screenshot. "
        "Return only the terminal information, and do not include any other information."
    )
    
    # Refine advice
    @staticmethod
    def refine_prompt_template(user_input: str, refine_advice: str) -> str:
        """Generate refined prompt"""
        return (
            f"Refine the user input based on the refine advice. "
            f"User input at the start of this round: {user_input} "
            f"Refine advice in this round: {refine_advice}"
            f"Return only the refined user input, and do not include any other information."
        )
    
    # Generate refine advice
    @staticmethod
    def generate_refine_advice_template(user_input: str, cursor_output: str, terminal_info: str) -> str:
        """Generate refine advice prompt"""
        return (
            f"Generate 'continue/stop' and refine advice based on the user input, "
            f"cursor main output, and terminal information. "
            f"User input: {user_input} "
            f"Cursor main output in this round: {cursor_output} "
            f"Terminal information in this round: {terminal_info} "
            f"Refine advice focuses on : what else I can do to make the project better. "
            f"It should be a paragraph. "
            f"Return your response in the following JSON format: "
            f"{{ 'action': 'continue' or 'stop', 'advice': 'your detailed refine advice here' }}"
        )
    
    # API configuration prompt
    @staticmethod
    def api_config_template() -> str:
        """Generate API configuration prompt"""
        return (
            f"Here are the API configuration information you need to follow WHEN YOU NEED THEM. "
            f"OpenAI API key: {os.getenv('ALTERNATIVE_OPENAI_API_KEY')} ,"
            f"OpenAI API base: {os.getenv('ALTERNATIVE_OPENAI_API_BASE')},"
            f"ALTERNATIVE_WECHAT_APP_ID: {os.getenv('ALTERNATIVE_WECHAT_APP_ID')} ,"
            f"ALTERNATIVE_WECHAT_APP_SECRET: {os.getenv('ALTERNATIVE_WECHAT_APP_SECRET')}"
        )
    
    # Test result prefix
    TEST_RESULT_PREFIX = "This is part result of the test scripts in the terminal: "

