import os
import re
import yaml
import warnings
from jinja2 import Template


class Chatterfile:
    def __init__(self, path='Chatterfile'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(script_dir, path)
        self._configs = {}
        self._prompts = {}
        self._read_chatterfile()

    def _read_chatterfile(self):
        with open(self._path, 'r') as f:
            chatterfile_content = f.read()

        # Split by '@' and ignore the first empty chunk
        chunks = chatterfile_content.split('@')[1:]

        for chunk in chunks:
            # Split each chunk into the first line and the rest
            first_line, yaml_str = chunk.split('\n', 1)

            # Remove ':' and extra spaces
            key = first_line.split(':', 1)[1].strip()

            # Parse the YAML content
            parsed_yaml = yaml.safe_load(yaml_str.replace('\t', '    '))

            # Classify based on first key-value
            if first_line.startswith('config'):
                self._configs[key] = parsed_yaml
            elif first_line.startswith('prompt_id'):
                prompt = parsed_yaml.get('prompt')

                # convert formatted string to jinja2 template
                if prompt and "{" in prompt and "}" in prompt:
                    if not "{{" in prompt and not "}}" in prompt:
                        updated_prompt = re.sub(r"{([^{}]+)}", r"{{\1}}", prompt)
                        parsed_yaml['prompt'] = updated_prompt
                self._prompts[key] = parsed_yaml

    def get_config(self, key):
        return self._configs.get(key)

    def get_prompt(self, key):
        return self._prompts.get(key)

    def get_prompts(self):
        return self._prompts

    def render_prompt(self, key, variables):
        prompt = self.get_prompt(key)['prompt']
        template = Template(prompt)
        return template.render(variables)

# chatterfile = Chatterfile(path='Chatterfile-local')
# print(chatterfile.get_config('cf1'))
# print(chatterfile.get_prompt('president'))
# print(chatterfile.render_prompt(key='president', variables={"jinja2": "usa"}))
