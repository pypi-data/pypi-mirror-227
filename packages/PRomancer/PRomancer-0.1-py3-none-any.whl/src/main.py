import argparse

from template_handler import TemplateHandler
from git_handler import GitHandler
from pr_handler import PrHandler


def main():
    parser = argparse.ArgumentParser(description="Automate your PR creation")

    parser.add_argument('-t', '--template', type=str, help='Template name', default='default.md')
    parser.add_argument('--title', type=str, help='PR title')
    parser.add_argument('--jira-ticket', type=str, help='Jira ticket')
    parser.add_argument('-desc', '--description', type=str, help='PR description')
    parser.add_argument('--additional_notes', type=str, help='Additional notes')
    parser.add_argument('-b1', '--branch1', type=str, help='First branch for diff')
    parser.add_argument('-b2', '--branch2', type=str, help='Second branch for diff')

    args = parser.parse_args()

    template = TemplateHandler.load_template(args.template)

    git_handler = GitHandler()
    diff = git_handler.get_git_diff(args.branch1, args.branch2)
    modified_files = git_handler.parse_git_diff(diff)

    pr_text = template.format(
        title=args.title,
        jira_ticket=args.jira_ticket,
        description=args.description,
        organization='myorg',
        purpose='Purpose',
        approach='Approach',
        testing='Testing',
        screenshots='Screenshots',
        files_changed='\n'.join(modified_files),
        additional_notes=args.additional_notes
    )

    pr_text = PrHandler.create_pr(pr_text)
    print(pr_text)


if __name__ == "__main__":
    main()
