import os
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure the API
genai.configure(api_key=os.environ["API_KEY"])

# Define safety settings to block none
safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def get_response(user_prompt, conversation_history, *simulation_parameters):
    # System instruction with simulation parameters
    system_instruction = f'''You have the opportunity to apply your skills in collective neutrino oscillations to help a user by speaking to them and/or setting parameters in a simulation of a neutrino gas! Your job is to reply in chat and provide numerical values for the parameters (whether or not you change them), all in JSON format.

Technical information:
The simulation models a gas of two groups of neutrinos (A and B) which undergo vacuum oscillations and interact with each other. Each neutrino in the gas is represented by a 2-level (2-flavor) quantum state characterized by its Bloch vector, AKA polarization. Polarizations are in the mass basis so that vacuum oscillations cause them to rotate about the z (3) axis. Meanwhile, neutrino-neutrino interactions cause their polarizations to rotate about each other.
The simulation follows the "once-in-a-lifetime encounter" approach. In this approach, in each time step, a neutrino has a certain probability of interacting with one other random neutrino (homogeneous gas). When two neutrinos interact, they become entangled, and after each interaction, their individual polarizations are re-obtained via partial traces of density matrices; their entanglement correlations are traced out. Each neutrino also undergoes vacuum oscillations individually. The limit of infinitely weak interactions at infinitesimally small time steps is the mean-field approach (quantum kinetics without collisions).

Current simulation parameters (and parameter descriptions):
Simulation time: {simulation_parameters[0]} (Duration of the whole simulation.)
Time step: {simulation_parameters[1]} (Time per simulation step.)
Probability of interaction per neutrino per step: {simulation_parameters[2]} (Note that the strength of each interaction is set to be equal to the time step divided by the probability (proportional to the time step, inversely proportional to probability).)
Number of neutrinos in group A: {simulation_parameters[3]}
Number of neutrinos in group B: {simulation_parameters[4]}
Initial 1 (x) polarization component of all group A neutrinos: {simulation_parameters[5]}
Initial 2 (y) polarization component of all group A neutrinos: {simulation_parameters[6]}
Initial 3 (z) polarization component of all group A neutrinos: {simulation_parameters[7]}
Initial 1 (x) polarization component of all group B neutrinos: {simulation_parameters[8]}
Initial 2 (y) polarization component of all group B neutrinos: {simulation_parameters[9]}
Initial 3 (z) polarization component of all group B neutrinos: {simulation_parameters[10]}
Oscillation frequency of all group A neutrinos: {simulation_parameters[11]}
Oscillation frequency of all group B neutrinos: {simulation_parameters[12]}

Your reply format:
Respond with a strictly formatted JSON key. The first field of the JSON key, "Chat reply", should be a friendly and informative reply to the user directly, which should contain a well-thought explanation of the simulation parameter changes (if any). The tone of your "Chat reply" should be the same as the way I've been talking to you now! The following JSON fields should be exactly as in the simulation parameters above. Repeat the current simulation parameter if that parameter does not need to be changed.'''

    # Initialize the model with the system instruction
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-exp-0827",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    # Format the conversation history correctly
    formatted_conversation_history = [
        {"role": entry["role"], "parts": entry["parts"]} for entry in conversation_history
    ]

    # Start the chat session with the formatted history
    chat_session = model.start_chat(
        history=formatted_conversation_history
    )

    # Send the user prompt and get the response
    response = chat_session.send_message(
        user_prompt,
        safety_settings=safety_settings
    )

    # Extract the response content correctly using dot notation
    response_text = response.candidates[0].content.parts[0].text

    # Extract and process the JSON response
    try:
        json_start_index = response_text.index('```json') + len('```json')
        json_end_index = response_text.index('```', json_start_index)
        json_str = response_text[json_start_index:json_end_index].strip()
        response_data = json.loads(json_str)
    except (ValueError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to parse JSON from model response: {e}")

    # Extract simulation parameters from response
    simulation_parameters = [
        response_data.get("Simulation time"),
        response_data.get("Time step"),
        response_data.get("Probability of interaction per neutrino per step"),
        response_data.get("Number of neutrinos in group A"),
        response_data.get("Number of neutrinos in group B"),
        response_data.get("Initial 1 (x) polarization component of all group A neutrinos"),
        response_data.get("Initial 2 (y) polarization component of all group A neutrinos"),
        response_data.get("Initial 3 (z) polarization component of all group A neutrinos"),
        response_data.get("Initial 1 (x) polarization component of all group B neutrinos"),
        response_data.get("Initial 2 (y) polarization component of all group B neutrinos"),
        response_data.get("Initial 3 (z) polarization component of all group B neutrinos"),
        response_data.get("Oscillation frequency of all group A neutrinos"),
        response_data.get("Oscillation frequency of all group B neutrinos")
    ]

    # Ensure all parameters are converted to strings (to prevent 'None' errors)
    simulation_parameters = [str(param) if param is not None else "0" for param in simulation_parameters]

    # Update the conversation history correctly
    conversation_history.append({"role": "user", "parts": [user_prompt]})
    conversation_history.append({"role": "model", "parts": [response_text]})

    ai_reply = response_data.get("Chat reply")

    return simulation_parameters, ai_reply, conversation_history
