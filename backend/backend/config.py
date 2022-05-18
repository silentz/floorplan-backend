import jsonargparse


parser = jsonargparse.ArgumentParser(description='Floorplan recognition service')
parser.add_argument('--config', action=jsonargparse.ActionConfigFile)

parser.add_argument('--app.host',    type=str, required=True, help='Server host')
parser.add_argument('--app.port',    type=int, required=True, help='Server port')
parser.add_argument('--app.workers', type=int, required=True, help='Number of workers')

parser.add_argument('--input.min_image_width',  type=int, required=True, help='Minimum input image width')
parser.add_argument('--input.min_image_height', type=int, required=True, help='Minimum input image height')

parser.add_argument('--triton.host',       type=str, required=True, help='Triton inference server host')
parser.add_argument('--triton.port',       type=int, required=True, help='Triton inference server port')
parser.add_argument('--triton.model_name', type=str, required=True, help='Triton inference server model name')
parser.add_argument('--triton.image_size', type=int, required=True, help='Triton inference server model image size')
parser.add_argument('--triton.n_classes',  type=int, required=True, help='Triton inference server model pad value')
parser.add_argument('--triton.pad_value',  type=tuple, required=True, help='Triton inference server model pad value')

parser.add_argument('--render.wall_class',  type=int, required=True, help='Wall class for 3d renderer')
parser.add_argument('--render.wall_height', type=int, required=True, help='Wall height for 3d renderer')
parser.add_argument('--render.colorize',    type=int, required=True, help='Colorize model or not')

parser.add_argument('--postprocess.wall_class', type=int, required=True, help='Postprocess wall class')
parser.add_argument('--postprocess.door_class', type=int, required=True, help='Postprocess door class')
parser.add_argument('--postprocess.back_class', type=int, required=True, help='Postprocess background class')

args = parser.parse_args()
