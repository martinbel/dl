## Tensorflow Object Detection API environment set-up

### Create a new conda environment

`conda create -n tfobj
conda activate tfobj
conda install -c anaconda tensorflow-gpu
conda install -c anaconda cython contextlib2 jupyter pillow lxml matplotlib
conda install -c conda-forge pycocotools
`
#### Git clone tensorflow models folder.
`cd /mnt
git clone https://github.com/tensorflow/models
cd /mnt/models/research/
protoc object_detection/protos/*.proto --python_out=.`

#### Add this at the end of ~/.bashrc
`export PYTHONPATH=$PYTHONPATH:/mnt/models/research/
export PYTHONPATH=$PYTHONPATH:/mnt/models/research/slim/
python object_detection/builders/model_builder_test.py
`

#### Create a gun detector
`python split_guns_dataset.py`

#### Create csv with annotations
`python xml_to_csv.py`

#### Create TFRecords
`python generate_tfrecord.py --csv_input=/mnt/dl/data/guns/train_labels.csv  --output_path=/mnt/dl/data/guns/train.record --image-dir /mnt/dl/data/guns/train/`
`python generate_tfrecord.py --csv_input=/mnt/dl/data/guns/test_labels.csv  --output_path=/mnt/dl/data/guns/test.record --image-dir /mnt/dl/data/guns/test`

#### Copy and rename the training script to train_obj.py
`cp /mnt/models/research/object_detection/main_train.py .`

#### Run the folowing before training
`export PYTHONPATH="${PYTHONPATH}:/mnt/models/"
export PYTHONPATH="${PYTHONPATH}:/mnt/models/research/"
export PYTHONPATH="${PYTHONPATH}:/mnt/models/research/slim/"
`

#### Training
`cd g_detector
PIPELINE_CONFIG_PATH=models/ssd_mobilenet_v1_coco/pipeline.config
MODEL_DIR=models/ssd_mobilenet_v1_g
NUM_TRAIN_STEPS=50000
SAMPLE_1_OF_N_EVAL_EXAMPLES=1
python train_objtf.py \
    --label_map_path=/mnt/dl/data/guns/label_map.pbtxt \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
    --alsologtostderr
`

#### Freeze model
`python /mnt/models/research/object_detection/export_inference_graph.py \
  --input_type_tensor \
  --pipeline_config_path=models/ssd_mobilenet_v1_coco/pipeline.config \
  --trained_checkpoint_prefix=models/ssd_mobilenet_v1_g/model.ckpt-20904 \
  --output_directory=models/ssd_mobilenet_v1_g/
`

#### Test the model predictions with a video
`python video_inference.py`
