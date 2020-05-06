# https://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration
# The machinery in charge of routing messages.
broker_url = 'pyamqp://guest:guest@192.168.56.102:5672//'

# Also use Redis to store results.
# result_backend = 'redis://'

# Expire task results after 5 minutes.
# result_expires = 5 * 60
task_serializer = 'json'
accept_content = ['json']

imports = (
    'task.worker',
)
listener_list = [{'host': '192.168.56.102', 'port': 5672, filter: ''}]