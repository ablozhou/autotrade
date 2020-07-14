# autotrade 环境准备
采用 conda 建立虚拟环境autotrade
conda create -n autotrade

如果虚拟环境存在,则激活
conda activate autotrade
或
source activate autotrade

取消虚拟环境
$ conda deactivate

## 安装依赖项
$ conda list -e > requirements.txt
$ conda clean -i # 如果出现keyerror提示需要执行
$ conda install --yes --file requirements.txt

或者
$ pip freeze > requirements.txt
environment location: /Users/zhh/anaconda3/envs/autotrade
$ pip install -r requirements.txt
