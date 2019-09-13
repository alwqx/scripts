# 常用Linux脚本汇总
![](https://raw.githubusercontent.com/adolphlwq/osshub/master/oss/banner/cradle.jpg)

## cimage
图片批量压缩，参考[Linux使用imagemagick的convert命令压缩图片，节省服务器空间](https://blog.csdn.net/songwenbinasdf/article/details/51205480)：
```shell
#! /bin/bash
find ./ -regex '.*\(jpg\|JPG\|png\|jpeg\)' -size +500k -exec convert -resize 1024x1024 {} {} \;
```