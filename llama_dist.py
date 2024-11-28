from langchain_ollama import OllamaLLM

def generate_dist(answer, context):
   ollama = OllamaLLM(
      base_url='http://localhost:11434',
      model="llama3.1"
   )
   # Construct the prompt based on user input
  
   prompt = f"""
Given is the below text:
\n\n
{context}
\n\n
and an answer
{answer}

Given the following context and answer, generate three distractor answers. 
The distractors should be similar in tone, structure, and relevance to the answer but should differ in key aspects to subtly mislead a reader without directly copying the answer. 
The distractors should be in similar length to the answer and no more than it. Additional information about the answer should not ever be displayed
Avoid using the main keywords found in the answer. Ensure each distractor is distinct and plausible based on the context provided.
Give distractors in the format below
"Distractors: 
1.
2.
3."
"""

   output = ollama.invoke(prompt)
   return output

# answer = "Publishing"
# text = """Elon Musk is a highly influential entrepreneur and engineer known for pioneering ventures that have transformed multiple industries. Born in Pretoria, South Africa, in 1971, Musk developed an early interest in technology and innovation. He moved to the United States to attend the University of Pennsylvania, where he studied economics and physics before embarking on a journey that would see him become one of the world’s most recognizable tech visionaries. Musk's career took off in the 1990s with Zip2, a software company he co-founded that provided business directories and maps for newspapers, which was eventually sold to Compaq for nearly $300 million. Musk then co-founded X.com, an online payment company that later became PayPal, now one of the world’s largest payment platforms, which was acquired by eBay in 2002. In the early 2000s, Musk launched SpaceX, aiming to reduce space transportation costs and make space travel more accessible. Under Musk’s leadership, SpaceX has achieved remarkable milestones, including the development of the Falcon and Starship rockets and successful missions with NASA. Musk also became CEO of Tesla, an electric vehicle company revolutionizing the automotive industry. Tesla's advancements in battery technology and autonomous driving have made it a leader in sustainable transportation."""
# print(generate_response(answer, text))