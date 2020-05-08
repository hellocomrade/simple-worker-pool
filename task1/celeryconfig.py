# https://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration
# The machinery in charge of routing messages.
broker_url = 'pyamqp://guest:guest@192.168.56.102:5672/'
message_queue_host = '192.168.56.102'
message_queue_exchange = 'waveform-exchange'
message_queue_routing_key = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']
# Also use Redis to store results.
# result_backend = 'redis://'

# Expire task results after 5 minutes.
# result_expires = 5 * 60
task_serializer = 'json'
accept_content = ['json']

imports = (
    'task1.worker',
)
