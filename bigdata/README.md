# Setup bigdata env for Nanjing
## HDFS
The dockerfile is https://github.com/dockerq/docker-hdfs.Run script `setup-hdfs.sh`:
```
path/to/setup-hdfs.sh /tmp/hdfs
```

run `put-files-to-hdfs.sh` to put sample data to hdfs
```
put-files-to-hdfs.sh
```

## Cassandra
version is `2.2.5`
volume of host is `/home/linker/cassandra-runtime`

```
./setup-cassandra.sh
```
