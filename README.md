2017年的时候用OpenMVG+OpenMVS串了一个三维建模流程。

建模的命令是python xxxx_pipeline.py input_dir output_dir
[1] python openMVG_openMVS_Pipeline_tradition.py data1\src data1\out1
[2] python openMVG_openMVS_Pipeline_backup.py data1\src data1\out2
[3] python openMVG_openMVS_Pipeline_nobackup.py data1\src data1\out3
[4] python visualsfm_openmvs_Pipeline.py data1\src data1\out4
[5] python pipeline_for_VSExMotion.py data1\src data1\vse

命令[5]除了生成模型外还生成了一个info.txt，可以用程序ShowMVSResult.bat来观看，注意data\vse\show_config.txt是要手工写的，
如果render_to_image 后面填1， 可以渲染到图片里， 保存到参数grab_dir后面的文件夹里。
Make_Video_from_fold.bat可以把文件夹里的图片合成视频，请用文本方式打开了更改路径。

OpenMVS生成的是.ply模型，我调用MeshLab生成.obj模型。
MeshLab可以从这下载，采用默认路径安装。

链接：https://pan.baidu.com/s/1Zk7xWsdzInSY7tQ3pqDndQ 密码：1szw

python用2不用3。Anaconda2也行。

visualsfm_OpenMVS_pipeline.py 需要CUDA才能运行。