import os


class TemplateHandler:

    @staticmethod
    def load_template(template_name):
        template_path = os.path.join('~/.promancer/templates', template_name)

        try:
            with open(template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            with open(os.path.join(os.path.dirname(__file__), f'../templates/{template_name}'), 'r') as f:
                return f.read()
