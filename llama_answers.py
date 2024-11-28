from langchain_ollama import OllamaLLM

def generate_response(ques, text):
   ollama = OllamaLLM(
      base_url='http://localhost:11434',
      model="llama3.1"
   )
   # Construct the prompt based on user input
  
   prompt = f"""
Given is the below text:
\n\n
{text}
\n\n
and a question
{ques}

Using only the information from the context, provide a clear, concise answer in a few words to the question.
Avoid repeating any part of the question in the answer, and include only essential details for a complete response.
Answer in the form of "Answer: "
"""

   output = ollama.invoke(prompt)
   return output

# ques = "How many hymns did Luther write for the first choral hymnal?"
# para = """Luther's hymns were included in early Lutheran hymnals and spread the ideas of the Reformation. He supplied four of eight songs of the First Lutheran hymnal Achtliederbuch, 18 of 26 songs of the Erfurt Enchiridion, and 24 of the 32 songs in the first choral hymnal with settings by Johann Walter, Eyn geystlich Gesangk Buchleyn, all published in 1524."""
# para = """While most chloroplasts originate from that first set of endosymbiotic events, Paulinella chromatophora is an exception that acquired a photosynthetic cyanobacterial endosymbiont more recently. It is not clear whether that symbiont is closely related to the ancestral chloroplast of other eukaryotes. Being in the early stages of endosymbiosis, Paulinella chromatophora can offer some insights into how chloroplasts evolved. Paulinella cells contain one or two sausage shaped blue-green photosynthesizing structures called chromatophores, descended from the cyanobacterium Synechococcus. Chromatophores cannot survive outside their host. Chromatophore DNA is about a million base pairs long, containing around 850 protein encoding genesâ€”far less than the three million base pair Synechococcus genome, but much larger than the approximately 150,000 base pair genome of the more assimilated chloroplast. Chromatophores have transferred much less of their DNA to the nucleus of their host. About 0.3â€“0.8% of the nuclear DNA in Paulinella is from the chromatophore, compared with 11â€“14% from the chloroplast in plants."""
# ques = "Where did most chloroplasts come from?"
# para = """It is an important source of renewable energy and its technologies are broadly characterized as either passive solar or active solar depending on the way they capture and distribute solar energy or convert it into solar power. Active solar techniques include the use of photovoltaic systems, concentrated solar power and solar water heating to harness the energy. Passive solar techniques include orienting a building to the Sun, selecting materials with favorable thermal mass or light dispersing properties, and designing spaces that naturally circulate air."""
# ques = "What is an example of a passive solar technique?"
# para = """Tehran is the country's capital and largest city, as well as its leading cultural and economic center. Iran is a major regional and middle power, exerting considerable influence in international energy security and the world economy through its large reserves of fossil fuels, which include the largest natural gas supply in the world and the fourth-largest proven oil reserves. Iran's rich cultural legacy is reflected in part by its 19 UNESCO World Heritage Sites, the fourth-largest number in Asia and 12th-largest in the world."""
# ques = "What resource does Iran have the fourth largest supply of in the world?"
# para = """Laptops have become an essential tool in modern society, providing the flexibility to work from anywhere. They combine the power of a desktop computer with the portability of a mobile device. Modern laptops are equipped with advanced processors, high-resolution displays, and extensive connectivity options. They are used in various fields, including education, business, and entertainment. With the advent of new technologies, laptops have seen significant improvements in battery life, performance, and design. The availability of lightweight models with long battery life makes them ideal for students and professionals on the go."""
# ques = "What is one of the main advantages of laptops compared to desktop computers?"
# print(generate_response(ques, para))