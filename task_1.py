import os
import re
import argparse


def parse_gitignore(gitignore_path):
    exact_rules = []
    glob_rules = []
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        for line in f:
            rule = line.strip()
            if not rule or rule.startswith('#'):
                continue
            elif rule.startswith('*'):
                suffix = re.escape(rule[1:])
                pattern = re.compile(f'.*{suffix}$')
                glob_rules.append((rule, pattern))
            else:
                exact_rules.append(rule.replace("\\", "/"))
    return exact_rules, glob_rules


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_dir', required=True)
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    gitignore_path = os.path.join(project_dir, '.gitignore')

    if os.path.isfile(gitignore_path):
        exact_rules, glob_rules = parse_gitignore(gitignore_path)
        proj_name = os.path.basename(project_dir)
        ignored_files = []
        for root, _, files in os.walk(project_dir):
            for filename in files:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, project_dir).replace('\\', '/')
                if rel_path == '.gitignore':
                    continue
                matched_rule = None

                for rule in exact_rules:
                    if rel_path == rule:
                        matched_rule = rule
                        break

                if not matched_rule:
                    for rule, pattern in glob_rules:
                        if re.match(pattern, rel_path):
                            matched_rule = rule
                            break

                if matched_rule:
                    output_path = os.path.join(proj_name, rel_path)
                    ignored_files.append((output_path, matched_rule))

        ignored_files.sort(key=lambda x: x[0])
        print("Ignored files:")
        for path, rule in ignored_files:
            print(f"{path} ignored by expression {rule}")
