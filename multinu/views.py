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
    context = {
        'form_values': DEFAULT_FORM_VALUES,
        'graph_path': DEFAULT_GRAPH_PATH
    }

    return render(request, 'multinu/index.html', context=context)


def simulate(request):
    call = subprocess.run(
        [
            'julia',
            'multinu/simulate.jl',
            request.POST.get('tf'),
            request.POST.get('dt'),
            request.POST.get('prob'),
            request.POST.get('N_A'),
            request.POST.get('N_B'),
            request.POST.get('P_A01'),
            request.POST.get('P_A02'),
            request.POST.get('P_A03'),
            request.POST.get('P_B01'),
            request.POST.get('P_B02'),
            request.POST.get('P_B03'),
            request.POST.get('omega_A'),
            request.POST.get('omega_B')
        ],
        capture_output=True,
        text=True
    )

    if call.stderr:
        raise RuntimeError(call.stderr)

    graph_path = call.stdout

    context = {
        'form_values': request.POST,
        'graph_path': graph_path
    }

    return render(request, 'multinu/index.html', context=context)
