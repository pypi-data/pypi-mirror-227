import argparse
import subprocess as subp
from nd_kafka.base import BaseNDKafka


class Topic(BaseNDKafka):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.replication_factor = kwargs.get('replication_factor', '2')    #Setting Defult --replication-factor 2
        self.partitions = kwargs.get('partitions', '1')                    #Setting Defult --partitions 1
        new_required_items = ['replication_factor', 'partitions']
        self.required_items.extend(new_required_items)


    def create_topic(self):
        error_list = []

        # Check if all required items have values
        for item in self.required_items:
            if getattr(self, item) is None:
                error_list.append(f"Error: {item} is missing!")
        
        if error_list:
            return False, error_list

        # Create a dictionary of arguments
        arguments = {
            "kafka_servers": {
                "option_strings": ["--kafka-servers"],
                "dest": "kafka_servers",
                "type": str,
                "default": self.kafka_server,
                "help": "kafka servers (comma separated)",
            },
            "topic": {
                "option_strings": ["--topic"],
                "dest": "topic",
                "type": str,
                "default": self.topic,
                "help": "topic where to publish data to",
            },
            "partitions": {
                "option_strings": ["--partitions"],
                "dest": "partitions",
                "type": str,
                "default": self.partitions,
                "help": "define no. of partions in a topic.",
            },
            "replication_factor": {
                "option_strings": ["--replication-factor"],
                "dest": "replication_factor",
                "type": str,
                "default": self.replication_factor,
                "help": "define replication fator for partions in a topic.",
            },
            "configs": {
                "option_strings": ["--configs"],
                "dest": "configs",
                "type": str,
                "default": self.configs,
                "help": "custom client properties to enable IAM auth enabled kafka cluster.",
            },
            "kafka_path": {
                "option_strings": ["--kafka-path"],
                "dest": "kafka_path",
                "type": str,
                "default": self.kafka_path,
                "help": "ocation where kafka is installed",
            },
        }


        parser = argparse.ArgumentParser()
        # Add the arguments from the dictionary to the parser
        for key, value in arguments.items():
            parser.add_argument(*value["option_strings"], **value)

        # Parse the arguments
        args = parser.parse_args()

        # Create the topic process in a separate thread
        return self.__create_cli_for_topic_creation(args)


    def __create_cli_for_topic_creation(self, arguments):
        print(f"Initializing kafka new topic for servers: {arguments.kafka_servers}")
        print(f"topic: {arguments.topic}")

        kafka_topic_init_cmd = [
            f"{arguments.kafka_path}/bin/kafka-topics.sh",
            "--bootstrap-server", arguments.kafka_servers,
            "--create",
            "--topic", arguments.topic,
            # "--partitions", arguments.partitions,
            # "--replication-factor", arguments.replication_factor,
        ]

        # If seprate config is defined (E.g for AWS IAM Auth. refer-> https://github.com/aws/aws-msk-iam-auth)
        if arguments.configs:
            kafka_topic_init_cmd = kafka_topic_init_cmd + ["--command-config", arguments.configs]

        try:
            # Execute the Kafka topic creation command
            process = subp.Popen(kafka_topic_init_cmd, stdout=subp.PIPE, stderr=subp.PIPE)

            # Capture the output and error messages
            stdout, stderr = process.communicate()

            # Print the output and error messages if they exist
            # if stdout is not None:
            #     print("Command output:")
            #     print(stdout.decode("utf-8"))

            # if stderr is not None:
            #     print("Command errors:")
            #     print(stderr.decode("utf-8"))

            # Check the return code
            if process.returncode == 0:
                return (True, stdout.decode("utf-8"))
            else:
                return (False, stdout.decode("utf-8"))
        except Exception as e:
            print(f"Error in creating topic: {e}")
            return (False, str(e))