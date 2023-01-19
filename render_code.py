from jinja2 import Environment, FileSystemLoader
import yaml

secrets_file = 'secrets.yml'
with open(secrets_file, 'r') as f:
    secrets = yaml.safe_load(f)

wifi = secrets['wifi']
home_assistant = secrets['home_assistant']

environment = Environment(loader=FileSystemLoader("src/"))

def do_work(file, params) -> None:
    template = environment.get_template(file)
    rendered_script = template.render(params)
    with open(f'output/{file}', 'w') as file:
        file.write(rendered_script)

do_work("boot.py", wifi)
do_work("main.py", home_assistant)
