import streamlit as st
from llama_questions import generate_questions
from llama_qna import extract_questions, generate_distractors_for_multiple_answers
from llama_answers import generate_response
from finb import generate_fill_in_the_blanks
from dist_mmr import get_ranked_distractors_mmr
from llama_sa import generate_sa_questions, generate_sa_response
from sense2vec import Sense2Vec
import random

s2v = Sense2Vec().from_disk('s2v_old')

# Sample contexts
SAMPLE_CONTEXTS = {
    "NASA": """Looking beyond the manned lunar landings, NASA investigated several post-lunar applications for Apollo hardware. The Apollo Extension Series (Apollo X,) proposed up to 30 flights to Earth orbit, using the space in the Spacecraft Lunar Module Adapter (SLA) to house a small orbital laboratory (workshop). Astronauts would continue to use the CSM as a ferry to the station. This study was followed by design of a larger orbital workshop to be built in orbit from an empty S-IVB Saturn upper stage, and grew into the Apollo Applications Program (AAP). The workshop was to be supplemented by Apollo Telescope Missions, which would replace the LM's descent stage equipment and engine with a solar telescope observatory. The most ambitious plan called for using an empty S-IVB as an interplanetary spacecraft for a Venus fly-by mission.""",
    
    "Public Schools": """In the United States, each state determines the requirements for getting a license to teach in public schools. Teaching certification generally lasts three years, but teachers can receive certificates that last as long as ten years. Public school teachers are required to have a bachelor's degree and the majority must be certified by the state in which they teach. Many charter schools do not require that their teachers be certified, provided they meet the standards to be highly qualified as set by No Child Left Behind. Additionally, the requirements for substitute/temporary teachers are generally not as rigorous as those for full-time professionals. The Bureau of Labor Statistics estimates that there are 1.4 million elementary school teachers, 674,000 middle school teachers, and 1 million secondary school teachers employed in the U.S.""",
    "World War": """World War II began in 1939 when Nazi Germany invaded Poland. The war in Europe was led by Adolf Hitler, who had established a powerful dictatorship in Germany. Japan joined the conflict by attacking Pearl Harbor in Hawaii on December 7, 1941, which prompted the United States to enter the war. The major Allied Powers included Great Britain, the United States, and the Soviet Union, who fought against the Axis Powers of Germany, Italy, and Japan. The war came to an end in 1945, following the surrender of Germany in May and Japan in August. The Japanese surrender came shortly after the United States dropped atomic bombs on two Japanese cities, Hiroshima and Nagasaki. The war resulted in significant changes to the global political landscape and led to the creation of the United Nations.""",
    # "Sparrow": """A sparrow is a small bird which is found throughout the world. There are many different species of sparrows. Sparrows are only about four to six inches in length. Many people appreciate their beautiful song. Sparrows prefer to build their nests in low places-usually on the ground, clumps of grass, low trees and low bushes. In cities they build their nests in building nooks or holes. They rarely build their nests in high places. They build their nests out of twigs, grasses and plant fibres. Their nests are usually small and well-built structures.Female sparrows lay four to six eggs at a time. The eggs are white with reddish brown spots. They hatch between eleven to fourteen days. Both the male and female parents care for the young. Insects are fed to the young after hatching. The large feet of the sparrows are used for scratching seeds. Adult sparrows mainly eat seeds. Sparrows can be found almost everywhere, where there are humans. Many people throughout the world enjoy these delightful birds. The sparrows are some of the few birds that engage in dust bathing. Sparrows first scratch a hole in the ground with their feet, then lie in it and fling dirt or sand over their bodies with flicks of their winds. They also bathe in water, or in dry or melting snow. Water bathing is similar to dust bathing, with the sparrow standing in shallow water and flicking water over its back with its wings, also ducking its head under the water. Both activities are social, with up to a hundred birds participating at once, and is followed by preening and sometimes group singing."""
}

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'input'
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'selected_types' not in st.session_state:
        st.session_state.selected_types = []
    if 'generated_questions' not in st.session_state:
        st.session_state.generated_questions = None
    if 'show_answers' not in st.session_state:
        st.session_state.show_answers = {}
    if 'mcq_options' not in st.session_state:
        st.session_state.mcq_options = {}
    if 'context_source' not in st.session_state:
        st.session_state.context_source = 'custom'

    # Clear answer states when generating new questions
    if st.session_state.page == 'input':
        for key in list(st.session_state.keys()):
            if key.startswith(('fib_answer_', 'sa_answer_')):
                del st.session_state[key]

def reset_app():
    st.session_state.page = 'input'
    st.session_state.step = 1
    st.session_state.selected_types = []
    st.session_state.generated_questions = None
    st.session_state.mcq_options = {}
    st.session_state.context_source = 'custom'
    st.rerun()

def input_page():
    st.title("PrashnaForger")
    
    # context = st.text_area("Enter any context or passage and we will provide you with best possible questions", height=200)
    # num_mcq = st.number_input("Number of Multiple Choice Questions", min_value=0, step=1)
    # num_fill_in_blank = st.number_input("Number of Fill in the Blank Questions", min_value=0, step=1)
    # num_short_answer = st.number_input("Number of Short Answer Questions", min_value=0, step=1)
    # if st.button("Generate Questions"):
    #     with st.spinner("Generating questions..."):
    #         # Generate all types of questions
    #         mcq_data = generate_mcq_questions(context, num_mcq)
    #         fib_data = generate_fill_in_blank_questions(context, num_fill_in_blank)
    #         sa_data = generate_short_answer_questions(context, num_short_answer)
            
    #         # Store in session state
    #         st.session_state.generated_questions = {
    #             'mcq': mcq_data,
    #             'fib': fib_data,
    #             'sa': sa_data
    #         }
    #         st.session_state.page = 'questions'
    #         st.rerun()

    # Add the introductory content
    st.markdown("""
    **"Forging Questions, Unveiling Insights"**

    Welcome to **PrashnaForge** – your intelligent assistant for generating thoughtful questions from reading passages! Powered by cutting-edge generative AI, PrashnaForge transforms text into a variety of engaging question types to enhance learning and comprehension.

    🔍 **How it Works:**
    - Enter or select a passage to begin.
    - Choose the types of questions you'd like to generate: Multiple Choice, Fill in the Blanks, or Short Answer.
    - Specify the number of questions for each type.

    **Call to Action:**  
    Start forging questions and elevate your comprehension journey!
    """)

    # Step 1: Select question types
    if st.session_state.step == 1:
        st.subheader("Step 1: Select Question Types")
        
        # Create columns for better layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            mcq_selected = st.checkbox("Multiple Choice Questions", 
                                     value="mcq" in st.session_state.selected_types)
        with col2:
            fib_selected = st.checkbox("Fill in the Blank Questions", 
                                     value="fib" in st.session_state.selected_types)
        with col3:
            sa_selected = st.checkbox("Short Answer Questions", 
                                    value="sa" in st.session_state.selected_types)
        
        # Store selected types
        st.session_state.selected_types = []
        if mcq_selected:
            st.session_state.selected_types.append("mcq")
        if fib_selected:
            st.session_state.selected_types.append("fib")
        if sa_selected:
            st.session_state.selected_types.append("sa")
        
        # Continue button
        if st.session_state.selected_types:
            if st.button("Continue"):
                st.session_state.step = 2
                st.rerun()
        else:
            st.warning("Please select at least one question type to continue.")
    
    # Step 2: Enter context and number of questions
    elif st.session_state.step == 2:
        st.subheader("Step 2: Enter Context and Number of Questions")
        
        # Back button
        if st.button("← Back to Question Type Selection"):
            st.session_state.step = 1
            st.rerun()
        
        # context = st.text_area("Enter the context or passage", height=200)
        # Context source selection
        st.radio(
            "Choose context source:",
            options=["Sample Context", "Custom Context"],
            key="context_source",
            horizontal=True
        )

        context = ""
        if st.session_state.context_source == "Sample Context":
            selected_sample = st.selectbox(
                "Select a sample context:",
                options=list(SAMPLE_CONTEXTS.keys())
            )
            context = SAMPLE_CONTEXTS[selected_sample]
            st.markdown("**Selected Context:**")
            st.markdown(f"*{context}*")
        else:
            context = st.text_area("Enter your own context or passage:", height=200)
        # Only show number inputs for selected question types
        num_questions = {}
        
        if "mcq" in st.session_state.selected_types:
            num_questions['mcq'] = st.number_input(
                "Number of Multiple Choice Questions", 
                min_value=1, 
                value=1,
                step=1
            )
            
        if "fib" in st.session_state.selected_types:
            num_questions['fib'] = st.number_input(
                "Number of Fill in the Blank Questions", 
                min_value=1, 
                value=1,
                step=1
            )
            
        if "sa" in st.session_state.selected_types:
            num_questions['sa'] = st.number_input(
                "Number of Short Answer Questions", 
                min_value=1, 
                value=1,
                step=1
            )

        if st.button("Generate Questions"):
            if not context:
                st.warning("Please enter some context before generating questions.")
                return

            with st.spinner("Generating questions..."):
                # Generate questions based on selected types
                mcq_data = generate_mcq_questions(context, num_questions.get('mcq', 0)) if 'mcq' in st.session_state.selected_types else ([], [], [])
                fib_data = generate_fill_in_blank_questions(context, num_questions.get('fib', 0)) if 'fib' in st.session_state.selected_types else ([], [])
                sa_data = generate_short_answer_questions(context, num_questions.get('sa', 0)) if 'sa' in st.session_state.selected_types else ([], [])
                
                # Store in session state
                st.session_state.generated_questions = {
                    'mcq': mcq_data,
                    'fib': fib_data,
                    'sa': sa_data
                }
                st.session_state.page = 'questions'
                st.rerun()

def generate_mcq_questions(context, num_mcq):
    generated_questions_text = generate_questions(context, num_mcq)
    questions = extract_questions(generated_questions_text)

    if len(questions) > num_mcq:
        questions = questions[:num_mcq]

    mcq_questions, mcq_answers, mcq_distractors = [], [], []

    # Clear previous MCQ options
    st.session_state.mcq_options = {}
    
    for i, question in enumerate(questions):
        answer_text = generate_response(question, context)
        answer = answer_text.split(": ")[1]
        if answer.endswith('.'):
            answer = answer[:-1]

        mcq_questions.append(question)
        mcq_answers.append(answer)
        if ',' in answer:
            ranked_distractors = generate_distractors_for_multiple_answers(answer, context)
            mcq_distractors.append(ranked_distractors)
        else:
            ranked_distractors = get_ranked_distractors_mmr(answer, context, s2v, top_n=5, diversity=0.8)
            mcq_distractors.append(ranked_distractors)
        
        # Store shuffled options in session state
        options = ranked_distractors
        random.shuffle(options)
        options = options[:3]
        options = options + [answer]
        st.session_state.mcq_options[i] = options

    return mcq_questions, mcq_answers, mcq_distractors

def generate_fill_in_blank_questions(context, num_fill_in_blank):
    fill_in_the_blanks = generate_fill_in_the_blanks(context)
    fill_in_blank_questions = fill_in_the_blanks['sentences'][:num_fill_in_blank]
    fill_in_blank_answers = fill_in_the_blanks['keys'][:num_fill_in_blank]
    return fill_in_blank_questions, fill_in_blank_answers

def generate_short_answer_questions(context, num_short_answer):
    generated_questions_text = generate_sa_questions(context, num_short_answer)
    questions = extract_questions(generated_questions_text)

    if len(questions) > num_short_answer:
        questions = questions[:num_short_answer]

    short_answer_questions, short_answer_answers = [], []
    for question in questions:
        answer_text = generate_sa_response(question, context)
        answer = answer_text.split(": ")[1]
        if answer.endswith('.'):
            answer = answer[:-1]
        short_answer_questions.append(question)
        short_answer_answers.append(answer_text)

    return short_answer_questions, short_answer_answers

def questions_page():
    st.title("PrashnaForger")
    st.subheader("Generated Questions")
    
    # # Add a button to go back to input
    # if st.button("← Back to Input"):
    #     st.session_state.page = 'input'
    #     st.rerun()
    
    # # Create tabs for different question types
    # tab1, tab2, tab3 = st.tabs(["Multiple Choice", "Fill in the Blank", "Short Answer"])
    
    # with tab1:
    #     display_mcq_questions(*st.session_state.generated_questions['mcq'])
    
    # with tab2:
    #     display_fill_in_blank_questions(*st.session_state.generated_questions['fib'])
    
    # with tab3:
    #     display_short_answer_questions(*st.session_state.generated_questions['sa'])
    # Add buttons for navigation
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Start Over"):
            reset_app()
    
    # Create tabs only for selected question types
    tabs = []
    tab_names = []
    
    if "mcq" in st.session_state.selected_types:
        tab_names.append("Multiple Choice")
    if "fib" in st.session_state.selected_types:
        tab_names.append("Fill in the Blank")
    if "sa" in st.session_state.selected_types:
        tab_names.append("Short Answer")
    
    tabs = st.tabs(tab_names)
    
    # Display questions in respective tabs
    tab_index = 0
    
    if "mcq" in st.session_state.selected_types:
        with tabs[tab_index]:
            display_mcq_questions(*st.session_state.generated_questions['mcq'])
        tab_index += 1
    
    if "fib" in st.session_state.selected_types:
        with tabs[tab_index]:
            display_fill_in_blank_questions(*st.session_state.generated_questions['fib'])
        tab_index += 1
    
    if "sa" in st.session_state.selected_types:
        with tabs[tab_index]:
            display_short_answer_questions(*st.session_state.generated_questions['sa'])

def display_mcq_questions(mcq_questions, mcq_answers, mcq_distractors):
    st.subheader("Multiple Choice Questions")
    for i, (question, answer) in enumerate(zip(mcq_questions, mcq_answers)):
        st.write(f"{i+1}. {question}")
        
        # Use stored options from session state
        options = st.session_state.mcq_options.get(i, [])
        display_options = ["Select an answer"] + options
        # Use a unique key for each question's answer state
        answer_key = f"mcq_answer_{i}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = None
        
        # Only display radio buttons if options are available
        if options:
            selected_option = st.radio(
                f"Select your answer for question {i+1}",
                options=display_options,
                key=f"mcq_question_{i}"
            )
            
            # Only process the answer if a real option is selected
            if selected_option != "Select an answer":
                # Store the selection without reloading
                st.session_state[answer_key] = selected_option
                
                # Show result based on stored selection
                if st.session_state[answer_key] == answer:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong!")
        
        st.divider()

def display_fill_in_blank_questions(fill_in_blank_questions, fill_in_blank_answers):
    st.subheader("Fill in the Blank")
    for i, (question, answer) in enumerate(zip(fill_in_blank_questions, fill_in_blank_answers)):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{i+1}. {question}")
        
        # Use session state to maintain answer visibility
        answer_key = f"fib_answer_{i}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = False
            
        with col2:
            button_label = "Hide Answer" if st.session_state[answer_key] else "Show Answer"
            if st.button(button_label, key=f"fib_button_{i}"):
                st.session_state[answer_key] = not st.session_state[answer_key]
        
        if st.session_state[answer_key]:
            st.info(f"Answer: {answer}")
        
        st.divider()

def display_short_answer_questions(short_answer_questions, short_answer_answers):
    st.subheader("Short Answer Questions")
    for i, (question, answer) in enumerate(zip(short_answer_questions, short_answer_answers)):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{i+1}. {question}")
        
        # Use session state to maintain answer visibility
        answer_key = f"sa_answer_{i}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = False
            
        with col2:
            button_label = "Hide Answer" if st.session_state[answer_key] else "Show Answer"
            if st.button(button_label, key=f"sa_button_{i}"):
                st.session_state[answer_key] = not st.session_state[answer_key]
        
        if st.session_state[answer_key]:
            st.info(f"Answer: {answer}")
        
        st.divider()

def main():
    st.set_page_config(page_title="Question Generation App", layout="wide")
    initialize_session_state()
    
    if st.session_state.page == 'input':
        input_page()
    else:
        questions_page()

if __name__ == "__main__":
    main()