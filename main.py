import argparse
import tensorflow as tf
import os
from model import cyclegan
from ops import *

parser = argparse.ArgumentParser(description="")
parser.add_argument(
    "--dataset_dir", dest="dataset_dir", default="alderley", help="path of the dataset"
)
parser.add_argument("--epoch", dest="epoch", type=int, default=20, help="# of epoch")
parser.add_argument(
    "--epoch_step",
    dest="epoch_step",
    type=int,
    default=10,
    help="# of epoch to decay lr",
)
parser.add_argument(
    "--batch_size", dest="batch_size", type=int, default=1, help="# images in batch"
)
parser.add_argument(
    "--train_size",
    dest="train_size",
    type=int,
    default=1e5,
    help="# images used to train",
)
parser.add_argument(
    "--load_size",
    dest="load_size",
    type=int,
    default=286,
    help="scale images to this size",
)
parser.add_argument(
    "--fine_size",
    dest="fine_size",
    type=int,
    default=256,
    help="then crop to this size",
)
parser.add_argument(
    "--ngf",
    dest="ngf",
    type=int,
    default=32,
    help="# of gen filters in first conv layer",
)
parser.add_argument(
    "--ndf",
    dest="ndf",
    type=int,
    default=32,
    help="# of discri filters in first conv layer",
)
parser.add_argument(
    "--n_d", dest="n_d", type=int, default=2, help="# of discriminators"
)
parser.add_argument(
    "--n_scale", dest="n_scale", type=int, default=2, help="# of scales"
)
parser.add_argument(
    "--gpu", dest="gpu", type=int, default=0, help="# index of gpu device"
)
parser.add_argument(
    "--input_nc", dest="input_nc", type=int, default=3, help="# of input image channels"
)
parser.add_argument(
    "--output_nc",
    dest="output_nc",
    type=int,
    default=3,
    help="# of output image channels",
)
parser.add_argument(
    "--lr", dest="lr", type=float, default=0.0002, help="initial learning rate for adam"
)
parser.add_argument(
    "--beta1", dest="beta1", type=float, default=0.5, help="momentum term of adam"
)
parser.add_argument(
    "--which_direction", dest="which_direction", default="AtoB", help="AtoB or BtoA"
)
parser.add_argument("--phase", dest="phase", default="train", help="train, test")
parser.add_argument(
    "--save_freq",
    dest="save_freq",
    type=int,
    default=1000,
    help="save a model every save_freq iterations",
)
parser.add_argument(
    "--print_freq",
    dest="print_freq",
    type=int,
    default=5,
    help="print the debug information every print_freq iterations",
)
parser.add_argument(
    "--continue_train",
    dest="continue_train",
    type=bool,
    default=False,
    help="if continue training, load the latest model: 1: true, 0: false",
)
parser.add_argument(
    "--checkpoint_dir",
    dest="checkpoint_dir",
    default="./checkpoint",
    help="models are saved here",
)
parser.add_argument(
    "--sample_dir",
    dest="sample_dir",
    default="./check/alderley/sample",
    help="sample are saved here",
)
parser.add_argument(
    "--test_dir",
    dest="test_dir",
    default="./check/alderley/testa2b",
    help="test sample are saved here",
)
parser.add_argument(
    "--L1_lambda",
    dest="L1_lambda",
    type=float,
    default=10.0,
    help="weight on L1 term in objective",
)
parser.add_argument(
    "--use_resnet",
    dest="use_resnet",
    type=bool,
    default=True,
    help="generation network using reidule block",
)
parser.add_argument(
    "--use_lsgan",
    dest="use_lsgan",
    type=bool,
    default=True,
    help="gan loss defined in lsgan",
)
parser.add_argument(
    "--max_size",
    dest="max_size",
    type=int,
    default=50,
    help="max size of image pool, 0 means do not use image pool",
)
args = parser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu)


def main(_):
    if not os.path.exists(args.checkpoint_dir):
        os.makedirs(args.checkpoint_dir)
    if not os.path.exists(args.sample_dir):
        os.makedirs(args.sample_dir)
    if not os.path.exists(args.test_dir):
        os.makedirs(args.test_dir)
    tfconfig = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    tfconfig.gpu_options.allow_growth = True
    with tf.compat.v1.Session(config=tfconfig) as sess:
        model = cyclegan(sess, args)
        print("Model initialized")
        show_all_variables()
        model.train(args) if args.phase == "train" else model.test(args)


if __name__ == "__main__":
    tf.compat.v1.app.run()
