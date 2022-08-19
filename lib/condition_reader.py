import yaml

with open('../SampleCase/condition.yaml', 'r') as f:
    data = yaml.safe_load(f)
    print(data)

