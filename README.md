# docker-image-layer-explorer
CLI tool to view and extract content of docker image layer

# Requirements

- python >= v3.6
- docker

# Installation

Run following command to download docker-image-layer-explorer v0.1.0
```sh
sudo wget https://github.com/Kartik1397/docker-image-layer-explorer/releases/download/v0.1.0/docker-image-layer-explorer -O /usr/local/bin/docker-image-layer-explorer && sudo chmod a+x /usr/local/bin/docker-image-layer-explorer
```

# Usage

```
usage: docker-image-explorer [-h] [--layer LAYER] [--extract EXTRACT] image_id
```

# Examples

List layers
```
$ docker-image-layer-explorer 85f93f2efdc5
Fetching image...
Extracting image...
Indexing layers...
aa5968d388b8652cd305e0e037751228967839d83d0cafbde5debf0b092e7c42 /bin/sh -c #(nop) ADD file:ac5fb7eb0d68040d948989f...
ef306f82e70bd4ca1850bd125a272afc3ac0c29e3fcea0d3aed35428da354e73 /bin/sh -c #(nop) WORKDIR /data
0ba82feddb65d36f34126908ae47f836db4ca57610c4c5a25c50036abe8feb03 /bin/sh -c #(nop) COPY file:7f3c4f20ece18d5f3ae769...
74003a41c47e423cf1b01d92fcc3090b175389b0b6d9a49cfb181540afaf0354 |2 lua_version=5.4 pandoc_version=3.1.1 /bin/sh -c...
cbf67576ef5078a32599df9e4ed27665891727aa42c26438c7b8895a462e60f3 /bin/sh -c #(nop) COPY file:5ca8cd1c206ec9e63e04f7...
3b2a149d9c8b763821d8c97c08f85ea75ca631f163432f75d964bd95a8bbc936 /bin/sh -c apk --no-cache add         librsvg
```

Check content of layer
```
$ docker-image-layer-explorer 85f93f2efdc5 --layer cbf67576ef5078a32599df9e4ed27665891727aa42c26438c7b8895a462e60f3
Indexing layers...
drwxr-xr-x  0 0      0           0 Feb 10 22:16 usr/
drwxr-xr-x  0 0      0           0 Feb 10 22:16 usr/local/
drwxr-xr-x  0 0      0           0 Mar  6 17:58 usr/local/bin/
-rwxr-xr-x  0 0      0    61612368 Mar  6 17:58 usr/local/bin/pandoc-crossref
```

Extract/Download layer using --extract argument
```
$ docker-image-layer-explorer 85f93f2efdc5 --layer cbf67576ef5078a32599df9e4ed27665891727aa42c26438c7b8895a462e60f3 --extract ./
Indexing layers...
Extracting layer...
$ tree cbf67576ef5078a32599df9e4ed27665891727aa42c26438c7b8895a462e60f3
cbf67576ef5078a32599df9e4ed27665891727aa42c26438c7b8895a462e60f3
└── usr
    └── local
        └── bin
            └── pandoc-crossref

4 directories, 1 file
```
