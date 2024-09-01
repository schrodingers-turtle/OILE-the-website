import os
import google.generativeai as genai
import json

# Configure API
genai.configure(api_key=os.environ["API_KEY"])

# Create the model configuration
generation_config = genai.GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-pro-exp-0827")


def edit_params(prompt, *simulation_parameters):# Construct the full prompt with system instructions and user input
    full_prompt = f"""
You have the opportunity to apply your skills in collective neutrino oscillations to help a user by speaking to them and/or setting parameters in a simulation of a neutrino gas! Your job is to reply in chat and provide numerical values for the parameters (whether or not you change them), all in JSON format.

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
Respond with a strictly formatted JSON key. The first field of the JSON key, "Chat reply", should a friendly and informative reply to the user directly, which should containing a well-thought explanation of the simulation parameter changes (if any). The tone of your "Chat reply" should be the same as the way I've been talking to you now! The following JSON fields should exactly as in the simulation parameters above. Repeat the current simulation parameter if that parameter does not need to be changed.

The user has the following single message for you:
{prompt}
"""[1:-1]

    # Generate the model's response
    response = model.generate_content(
        full_prompt,
        generation_config=generation_config
    )

    # Extract the model's response text
    model_response = response.text

    # Remove code block markers if present
    json_str = model_response.replace("```json\n", "").replace("\n```", "")

    # Parse JSON
    response_data = json.loads(json_str)

    # Split JSON into different variables
    ai_reply = response_data.get("Chat reply")
    simulation_time = response_data.get("Simulation time")
    time_step = response_data.get("Time step")
    probability_of_interaction = response_data.get("Probability of interaction per neutrino per step")
    num_neutrinos_group1 = response_data.get("Number of neutrinos in group A")
    num_neutrinos_group2 = response_data.get("Number of neutrinos in group B")
    initial_polarization_group1_x = response_data.get("Initial 1 (x) polarization component of all group A neutrinos")
    initial_polarization_group1_y = response_data.get("Initial 2 (y) polarization component of all group A neutrinos")
    initial_polarization_group1_z = response_data.get("Initial 3 (z) polarization component of all group A neutrinos")
    initial_polarization_group2_x = response_data.get("Initial 1 (x) polarization component of all group B neutrinos")
    initial_polarization_group2_y = response_data.get("Initial 2 (y) polarization component of all group B neutrinos")
    initial_polarization_group2_z = response_data.get("Initial 3 (z) polarization component of all group B neutrinos")
    oscillation_frequencies_group1 = response_data.get("Oscillation frequency of all group A neutrinos")
    oscillation_frequencies_group2 = response_data.get("Oscillation frequency of all group B neutrinos")

    simulation_parameters = [
        simulation_time,
        time_step,
        probability_of_interaction,
        num_neutrinos_group1,
        num_neutrinos_group2,
        initial_polarization_group1_x,
        initial_polarization_group1_y,
        initial_polarization_group1_z,
        initial_polarization_group2_x,
        initial_polarization_group2_y,
        initial_polarization_group2_z,
        oscillation_frequencies_group1,
        oscillation_frequencies_group2
    ]

    simulation_parameters = [str(param) for param in simulation_parameters]

    return simulation_parameters, ai_reply
