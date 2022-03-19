import boto3
import argparse
import re


def get_parser():
    description = 'List AWS s3 buckets'
    example_use_text = '''Example of use:
    python ls3.py
    python ls3.py prod
    python ls3.py ^prod.*
    python ls3.py bucket-name-1 bucket-name-2 bucket-name-3'''

    parser = argparse.ArgumentParser(description=description, epilog=example_use_text, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('names',  nargs='*', help='A name (or list of names) of AWS S3 buckets, it can be regex pattern. Without this parameter it shows all buckets')

    return parser


def list_s3(s3, names=None):
    response = s3.list_buckets()
    all_buckets = [bucket["Name"] for bucket in response['Buckets']]
    
    if names:
        buckets = []
        for name in names:
            buckets.extend(list(filter(re.compile(name).match, all_buckets)))
        return set(buckets)
    else:
        return all_buckets


def main():
    parser = get_parser()
    args = parser.parse_args()
    args_bucket_names = args.names

    s3 = boto3.client('s3')
    buckets = list_s3(s3, args_bucket_names)

    
    if buckets:
        print("List of buckets:")
        for bucket in buckets:
            print(f'    {bucket}')
    else:
        print("No suck buckets")


if __name__ == '__main__':
    main()
