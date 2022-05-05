import jsonargparse


parser = jsonargparse.ArgumentParser(description='Floorplan recognition service')

parser.add_argument('--app.host',    type=str, required=True, help='Server host')
parser.add_argument('--app.port',    type=int, required=True, help='Server port')
parser.add_argument('--app.workers', type=int, required=True, help='Number of workers')
parser.add_argument('--config', action=jsonargparse.ActionConfigFile)

args = parser.parse_args()
