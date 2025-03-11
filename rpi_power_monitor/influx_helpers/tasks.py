from string import Template
import os

from influxdb_client.domain import Task




def _add_task(task_api, task_name, template_name, bucket_name, org_name, org_id, Org) -> bool:
    '''Constructs an Influx v2 `Task` class instance'''
    
    # Templates require the following variables:
    # BUCKET_NAME
    
    template_dir = os.path.join(os.path.dirname(__file__), f'flux_templates') 
    
    try:
        with open(os.path.join(template_dir, f'{template_name}.txt'), 'r') as f:
            template_contents = f.read()
    except Exception as e:
        return False
    
    T = Template(template_contents)
    flux = T.substitute(BUCKET_NAME=bucket_name, TASK_NAME=task_name)
    
    task = Task(
        id='dummy-text', # This isn't actually set when creating the task
        org_id=org_id,
        name=task_name,
        flux=flux
    )
    
    try:
        task_api.create_task_every(task_name, flux, '5m', Org)
        return True
    except Exception as e:
        return False
