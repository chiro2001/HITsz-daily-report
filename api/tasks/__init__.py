import importlib
from reporter.utils import logger

task_names = [
    'epidemic'
]
task_modules = {
    'epidemic': 'app_epidemic_report'
}


def get_tasks() -> list:
    tasks = []
    for name in task_names:
        try:
            module_name = task_modules[name]
        except KeyError:
            logger.error(f'Config task error for module name {name}')
            continue
        try:
            a = importlib.import_module(f'tasks.{module_name}')
            tasks.append(a)
        except ImportError as e:
            logger.error(f'Cannot import module tasks.{module_name}! {e}')
            continue
    return tasks


def get_apps() -> list:
    apps = []
    for a in get_tasks():
        try:
            apps.append(a.app)
        except AttributeError:
            logger.error(f'Module {a.name} do not has app')

    return apps
