class BaseNDKafka:

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.kafka_server = kwargs.get('kafka_server')
        self.topic = kwargs.get('topic')
        self.configs = kwargs.get('configs')
        self.kafka_path = kwargs.get('kafka_path')
        self.required_items = ['kafka_server', 'topic', 'configs', 'kafka_path']