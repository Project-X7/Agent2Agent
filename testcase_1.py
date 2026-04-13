from policy_agent import PolicyAgent
from helpers import print_llm_response
from helpers import format_llm_response

print("Running Health Insurance Policy Agent")
agent = PolicyAgent()
prompt = "what is the out of pocket limit for my policy? and explain rules around it if any?"

response = format_llm_response(agent.answer_query(prompt))
print_llm_response(response, title="Policy Agent Response")