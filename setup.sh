conda create -n vc python=3.9
conda activate vc
# conda config
conda config --set ssl_verify true 
conda config --set proxy_servers.http http://127.0.0.1:7890
conda config --set show_channel_urls yes
conda config --add channels conda-forge
# install dependencies
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
pip install -r requirements.txt