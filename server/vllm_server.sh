model_path=$1
vllm serve ${model_path} \
--dtype auto \
--trust-remote-code \
--gpu-memory-utilization 0.5 \
--tensor-parallel-size 8