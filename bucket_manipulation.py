# coding: utf-8
# Copyright (c) 2016, 2022, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# Uploads all files from a local directory to an object storage bucket
# using multiple processes so that the uploads are done in parallel.
#
# Assumptions: Object storage bucket already exists. See object_crud.py for
#                an example of creating a bucket.
#              Loads configuration from default profile in the default config
#                file

import oci
import os
import argparse
from multiprocessing import Process
from glob import glob

def download_from_object_storage(config, namespace, bucket, file_name):
    """
    download_from_object_storage will download a file from an object storage bucket.
    This function is intended to be run as a separate process.  The client is
    created with each invocation so that the separate processes do
    not have a reference to the same client.

    :param config: a configuration dictionary used to create ObjectStorageClient
    :param namespace: Namespace where the bucket resides
    :param bucket: Name of the bucket in which the object will be stored
    :param file_name: The name of the file to download from object storage
    :rtype: None
    """    
    ostorage = oci.object_storage.ObjectStorageClient(config)
    get_object_response = ostorage.get_object(namespace,
                        bucket,
                        file_name)   
    print("Finished downloading {}".format(file_name))


def upload_to_object_storage(config, namespace, bucket, file_name):
    """
    upload_to_object_storage will upload a file to an object storage bucket.
    This function is intended to be run as a separate process.  The client is
    created with each invocation so that the separate processes do
    not have a reference to the same client.

    :param config: a configuration dictionary used to create ObjectStorageClient
    :param namespace: Namespace where the bucket resides
    :param bucket: Name of the bucket in which the object will be stored
    :param file: The name of the file to upload to object storage
    :rtype: None
    """
       
    ostorage = oci.object_storage.ObjectStorageClient(config)
    ostorage.put_object(namespace,
                        bucket,
                        file_name,
                        file_name)
    print("Finished uploading {}".format(file_name))


if __name__ == "__main__":    
    config = oci.config.from_file("~/.oci/config")
    object_storage = oci.object_storage.ObjectStorageClient(config)
    namespace = object_storage.get_namespace().data

    description = "\n".join(["This is an example to show how multiple files can be uploaded to in",
                             "parallel. The example uses multiple processes.",
                             "",
                             "All the files in 'directory' will be uploaded to the object storage bucket",
                             "specified by 'bucket_name'  The default profile is used.",
                             "",
                             "The bucket must already exist. See object_crud.py for a bucket creation",
                             "example."])
    
    

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    
    parser.add_argument(dest='bucket_name',
                        help="Name of object storage bucket")
    parser.add_argument(dest='file',
                        help='This parameter designates the file name. Not required if this is an upload task')
    parser.add_argument(dest='action',
                        help='Designates the action to execute. Available options are "upload" and "download"')
    args = parser.parse_args()

    action = args.action
    bucket_name = args.bucket_name
    
    if action == 'upload':      
        proc_list = []
        p = Process(target=upload_to_object_storage, args=(config,
                                                        namespace,
                                                        args.bucket_name,
                                                        args.file))
        p.start()
        proc_list.append(p)

        for job in proc_list:
            job.join()
    elif action == 'download':
        print("Starting download for {}".format(bucket_name))
        p = Process(target=download_from_object_storage, args=(config,
                                                            namespace,
                                                            args.bucket_name,
                                                            args.file))
        p.start()
        p.join()
    else:
        parser.usage()
        exit(1)