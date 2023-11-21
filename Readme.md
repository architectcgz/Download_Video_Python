blob 格式的视频 
在javascript中可以使用blob 类来创建类似文件的objects类型  来存储任意raw data
不需要将自己的数据保存为特定的文件形式
传递数据时是以二进制数据从server传递到浏览器
![Alt text](image-1.png)

客户端观看视频时，首先获得了m3u8文件
![Alt text](image-1.png)
![Alt text](image-2.png)
m3u8文件中包含了不同质量视频的解决方法的连接
如图中的low_index- 低质量  mid_index 
![Alt text](image-3.png)