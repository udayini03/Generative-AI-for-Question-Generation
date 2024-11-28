from langchain_ollama import OllamaLLM
ollama = OllamaLLM(
      base_url='http://localhost:11434',
      model="llama3.1"
   )

def generate_sa_questions(text, n):
   prompt = f"""
Given is the below text:
\n\n
{text}
\n\n
and the number 
\n\n
{n}

Consider the text as the context and generate exactly {n} short answer questions based on this context.
The questions should cover important meanings of the text and be clear with proper sentence formation.
Please ensure you generate only {n} unique questions without repetition.
Output only the questions in the form of "Question: "
"""

   output = ollama.invoke(prompt)
   return output

# text = """Thirteen thousand species of plants have been identified in the Alpine regions. Alpine plants are grouped by habitat and soil type which can be limestone or non-calcerous. The habitats range from meadows, bogs, woodland (deciduous and coniferous) areas to soilless scree and moraines, and rock faces and ridges. A natural vegetation limit with altitude is given by the presence of the chief deciduous treesâ€”oak, beech, ash and sycamore maple. These do not reach exactly to the same elevation, nor are they often found growing together; but their upper limit corresponds accurately enough to the change from a temperate to a colder climate that is further proved by a change in the presence of wild herbaceous vegetation. This limit usually lies about 1,200 m (3,940 ft) above the sea on the north side of the Alps, but on the southern slopes it often rises to 1,500 m (4,920 ft), sometimes even to 1,700 m (5,580 ft)."""
# n = 5
# print(generate_questions(text, n))

def generate_sa_response(ques, text):
   prompt = f"""
Given is the below text:
\n\n
{text}
\n\n
and a question
{ques}

Using only the information from the context, provide a clear answer to the short answer question.
Include only essential details for a complete response.
Answer should only be in the form of "Answer: "
"""

   output = ollama.invoke(prompt)
   return output