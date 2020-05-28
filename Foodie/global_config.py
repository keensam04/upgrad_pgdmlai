import yaml

# create a file in the same location as this script named email.yml with below content
# gmail:
#    username: YOUR EMAIL
#    password: YOUR PASSWORD
with open("config_app.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

def get_config(section, key):
	return cfg[section][key]
