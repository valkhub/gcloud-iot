import argparse
from google.cloud import pubsub

# Grant access to the Cloud IoT Core service account on a given PubSub topic
def set_topic_policy(topic_name):
    """Sets the IAM policy for a topic for Cloud IoT Core."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    policy = topic.get_iam_policy()

    # Add a group as publishers.
    publishers = policy.get('roles/pubsub.publisher', [])
    publishers.append(policy.service_account(
            'cloud-iot@system.gserviceaccount.com'))
    policy['roles/pubsub.publisher'] = publishers

    # Set the policy
    topic.set_iam_policy(policy)

    print('IAM policy for topic {} set.'.format(topic.name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_argument(
            dest='topic_name',
            help='The PubSub topic to grant Cloud IoT Core access to')

    args = parser.parse_args()

    set_topic_policy(args.topic_name)
