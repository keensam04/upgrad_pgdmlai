from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.form_policy import FormPolicy
from rasa_core.policies.memoization import MemoizationPolicy


if __name__ == '__main__':
	logging.basicConfig(level='INFO')
	
	training_data_file = './data/stories.md'
	model_path = './models/dialogue'
	
	memoization_policy = MemoizationPolicy(max_history=4)
	keras_policy = KerasPolicy(max_history=5, epochs=500)

	agent = Agent('restaurant_domain.yml', policies=[memoization_policy, keras_policy, FormPolicy()])
	training_data = agent.load_data(training_data_file, augmentation_factor = 50)
	agent.train(training_data)
	agent.persist(model_path)
