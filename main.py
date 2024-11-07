import chainlit as cl
from openai import AsyncOpenAI
import asyncio
import random
from config.starters import starters

# Initialize the OpenAI client
client = AsyncOpenAI()

@cl.set_starters
async def set_starters():
    # Select two random starters from the list
    random_starters = random.sample(list(starters), 4)
    return random_starters

@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant who writes recipes in the style of food bloggers. Do not engage in any conversations outside of this topic."}],
    )

# Asynchronous function to interact with OpenAI's API and stream responses
async def oai_message(prompt):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": prompt})

    # Create a Chainlit message object for streaming
    msg = cl.Message(content="")

    # Send the initial message to the user interface
    await msg.send()

    # Stream the response from OpenAI
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_history,
        stream=True
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    # Update the message history with the assistant's response
    message_history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("message_history", message_history)

    return msg.content

# Define the first processing step
@cl.step(name="Character Padding", type="tool")
async def step_one(input_text):
    await cl.Message(content="Step 1: Building a backstory...").send()
    prompt = f"Your role is to create recipes with extremely long-winded preambles about the user's personal history. The preamble will be of little relevance to the recipe barring some tenuous cultural connection. The recipe requested is: {input_text}. Please come up with a character and context for the preamble. Explain their tenuous connection to the recipe, their name, their background and what they're going to bang on about. Don't write the preamble just yet, just summarise the character in a number of bullet points. Do not make obvious racial connections between the cuisine and the character's name. The name can also be a pen name, like the brand of the food blog. The 'character' will be a food blogger, but you can also describe the person they will use to contextualise the recipe (eg a historical character, a family member, etc. Keep it short and concise; this is just an outline."
    summary = await oai_message(prompt)
    return summary

# Define the second processing step
@cl.step(name= "Backstory Creation", type="tool")
async def step_two(input_text, recipe_name):
    await cl.Message(content="Step 2: Connecting the backstory to the recipe in some way...").send()
    prompt = f"You've come up with the following character and context for your long-winded backstory: {input_text}. Now, outline how you'll craft the the preamble for the recipe '{recipe_name}' that connects the backstory to the recipe in some way. Explain how their personal history is relevant to the recipe – this can be outlandish, and should parody the clichéd nature of these recipe preambles on websites, blogs, etc. Again, be super-concise, as this is just the outline; keep it to a short paragraph and a few summarising bullet points. Use line breaks to keep the pars extremely short."
    translation = await oai_message(prompt)
    return translation

# Define the third processing step
@cl.step(name= "Recipe Cramming", type="tool")
async def step_three(input_text, character, recipe_name):
    await cl.Message(content="Step 3: Shoehorning in the actual recipe...").send()
    await asyncio.sleep(1)  # Simulate processing time
    prompt = f"Here's your character: {character} and here's your preamble basis: {input_text} that connects the backstory to the recipe. Now, write the actual preamble and recipe for '{recipe_name}'. Be rambly in the preamble, using short paragraphs and a folksy style; but avoid addressing the reader directly or introducing yourself (as this would be unsuual on your own blog). The recipe section should be and rushed and overly brief for the recipe itself. Explain that you're tired after writing that long backstory, so you're not going to spend much time on this, and offer unhelpful advice like 'have fun!'. Be extremely vague about details, and be overly folksy where actual detail would help. Make sure to include the ingredients and a very brief, rushed method that leaves out key steps. The recipe should be a parody of the kind of content you're satirizing. Don't refer to the rushed nature of the recipe, but write it as if it were fully genuine. Keep paragraphs short – insert par breaks every sentence or two – to make it seem really like a folksy blog post. Format the recipe using bullets and step numbers. Insert a line break after every sentence or two sentences at absolute most. Don't write in an overly verbose style, or a faux-poetic style, just make it rambly – more like a wannabe Carrie Bradshaw or Niall Harbison than a romantic poet. Formatting: Break up the long pre-amble using headers. There should be between eight and 10 such sections. Put all ingredients in bold during the text and the method; put all quantities in bold during the ingredients list."
    sentiment_analysis = await oai_message(prompt)
    return sentiment_analysis

# Handle incoming messages
@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content

    # Pass the user's input through the defined steps sequentially
    character = await step_one(user_input)
    backstory = await step_two(character, recipe_name=user_input)
    final_output = await step_three(backstory, character, recipe_name=user_input)