from django.shortcuts import render

import subprocess

DEFAULT_FORM_VALUES = {
    'tf': 500,
    'dt': 0.001,
    'prob': 0.1,
    'N_A': 60,
    'N_B': 40,
    'P_A01': 0.001,
    'P_A02': 0,
    'P_A03': 0.9999995,
    'P_B01': -0.001,
    'P_B02': 0,
    'P_B03': -0.9999995,
    'omega_A': 0.1,
    'omega_B': 0.2
}
DEFAULT_GRAPH_PATH = 'multinu/default_graph.png'


def index(request):
    if request.method == 'GET':
        form_values = DEFAULT_FORM_VALUES
        graph_path = DEFAULT_GRAPH_PATH
    
    elif request.method == 'POST':
        form_values = request.POST.dict()

        if form_values.get('prompt'):
            # AI logic here.
            pass

        graph_path = _run_simulation(
            form_values.get('tf'),
            form_values.get('dt'),
            form_values.get('prob'),
            form_values.get('N_A'),
            form_values.get('N_B'),
            form_values.get('P_A01'),
            form_values.get('P_A02'),
            form_values.get('P_A03'),
            form_values.get('P_B01'),
            form_values.get('P_B02'),
            form_values.get('P_B03'),
            form_values.get('omega_A'),
            form_values.get('omega_B')
        )

    context = {
        'form_values': form_values,
        'graph_path': graph_path
    }

    return render(request, 'multinu/index.html', context=context)


def _run_simulation(*args):
    call = subprocess.run(['julia', 'multinu/simulate.jl', *args], capture_output=True, text=True)

    if call.stderr:
        raise RuntimeError(call.stderr)

    graph_path = call.stdout

    return graph_path
