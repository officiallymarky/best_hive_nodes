import requests
from tenacity import retry, stop_after_attempt, wait_exponential

BECON_URL = 'https://beacon.peakd.com/api/best'
DEFAULT_NODES = ['https://api.hive.blog', 'https://api.openhive.network', 'https://anyx.io']


def return_default_nodes(message):
	print(message)
	return DEFAULT_NODES

@retry(stop=stop_after_attempt(5),
	   wait=wait_exponential(multiplier=1, min=0.5, max=5),
	   retry_error_callback=return_default_nodes)
def get_best_hive_nodes(score=90):
	node_list = requests.get(BECON_URL)
	return find_best_nodes(node_list.json(), score)

def find_best_nodes(node_list, score):
	nodes = []

	for node in node_list:
		if node['score'] > score:
			nodes.append(node['endpoint'])
	return nodes
