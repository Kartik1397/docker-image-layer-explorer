import argparse
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser(
            prog='docker-image-explorer',
            description='List view view content of docker image layers')

parser.add_argument('image_id')
parser.add_argument('--layer', nargs=1, required=False)
parser.add_argument('--extract', nargs=1, required=False)

args = parser.parse_args()

image_id = args.image_id
layers = args.layer
extract_to = args.extract
image_path = f'/tmp/{image_id}.tar'
image_dir = f'/tmp/{image_id}'

if not Path(image_path).exists():
    print('Fetching image...')
    os.system(f'docker save {image_id} > {image_path}')

if not Path(image_dir).exists():
    print(f'Extracting image...')
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    os.system(f'tar -xf {image_path} --directory {image_dir}')

def run_command(command):
    return os.popen(command).read()

with open(f'{image_dir}/{image_id}.json') as image_json_file:
    image_json = json.loads(image_json_file.read())
    history = filter(lambda x: not x.get('empty_layer'), image_json['history'])
    diff_ids = image_json['rootfs']['diff_ids']

    print('Indexing layers...')
    output = run_command(f"ls {image_dir}/*/*.tar | xargs sha256sum")
    lines = output.split('\n')
    
    layer_id_by_diff_id = {}

    for diff_id, path in [tuple(line.split('  ')) for line in lines if line]:
        layer_id = path.split('/')[3]
        layer_id_by_diff_id[diff_id] = layer_id

    for history_item, diff_id in zip(history, diff_ids):
        command = history_item.get('created_by')
        ellipsis = '...' if len(command) > 50 else ''
        if not layers:
            print(diff_id.split(':')[1], f'{command[:50]}{ellipsis}')

    if layers and extract_to:
        print('Extracting layer...')
        layer_id = layer_id_by_diff_id[layers[0]]
        dest = f'{extract_to[0]}/{layers[0]}'
        os.system(f"mkdir -p {dest}")
        os.system(f"tar -xf {image_dir}/{layer_id}/layer.tar --directory {dest}")
    elif layers:
        layer_id = layer_id_by_diff_id[layers[0]]
        output = run_command(f"tar -tvf {image_dir}/{layer_id}/layer.tar")
        print(output)

