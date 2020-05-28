from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
from rasa_nlu import config
from rasa_nlu.components import ComponentBuilder
import load_lookuppy
import rasa_nlu

filename = './data/locationlist.txt'
load_lookuppy.cities_func(filename)
filename = './data/cuisinelist.txt'
load_lookuppy.cuisines_func(filename)
 
builder = ComponentBuilder(use_cache=True)

def train_nlu(data, config_file, model_dir):
	print('******* Rasa NLU Version - ',rasa_nlu.__version__,' *******')
	training_data = load_data(data)
	trainer = Trainer(config.load(config_file), builder)
	trainer.train(training_data)
	model_directory = trainer.persist(model_dir, fixed_model_name = 'restaurantnlu')
	
def run_nlu():
	interpreter = Interpreter.load('./models/nlu/default/restaurantnlu', builder)
	print(interpreter.parse("south indian restaurants in agra costs less than 500"))

if __name__ == '__main__':
	train_nlu('./data/data.json', 'config_spacy.json', './models/nlu')
#	run_nlu()