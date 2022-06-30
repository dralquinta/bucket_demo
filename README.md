# bucket_demo
The following repo shows a demo of how to upload and download bulk files into a bucket at OCI

## Expected results: 

Consider the following structure for the demo: 

```shell
$ tree -L 2
.
├── bucket_manipulation.py
├── demobucket
├── dummydir
│   └── dummyfilewithcontent.out
└── README.md
```


### Upload

```shell
$ python3 bucket_manipulation.py demobucket dummydir n/a upload
Starting upload for dummydir/dummyfilewithcontent.out
Finished uploading dummyfilewithcontent.out
```

### Download

```shell
python3 bucket_manipulation.py demobucket dummyfile download
Starting download for demobucket
Finished downloading dummyfile
```
