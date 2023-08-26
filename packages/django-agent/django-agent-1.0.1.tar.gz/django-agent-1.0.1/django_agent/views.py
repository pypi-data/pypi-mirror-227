import json
import shlex
import subprocess
import traceback
from typing import Any

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods

from django_agent.decorators import agent_token_required
from django_agent import __version__


def exception(e: Exception) -> JsonResponse:
    return JsonResponse({
        'error': True,
        'exception': type(e).__name__,
        'traceback': traceback.format_exc()
    })


def shell_output(cp: subprocess.CompletedProcess) -> JsonResponse:
    return JsonResponse({
        'error': False,
        'returncode': cp.returncode,
        'stdout': cp.stdout.decode('utf-8'),
        'stderr': cp.stderr.decode('utf-8')
    })


def python_output(o: Any) -> JsonResponse:
    return JsonResponse({
        'error': False,
        'output': o
    })


def error(message: str) -> JsonResponse:
    return JsonResponse({
        'error': True,
        'message': message
    })


@agent_token_required
@csrf_exempt
@require_http_methods(['GET', 'POST'])
def shell(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                command = data.get('command', '')
            except json.JSONDecodeError:
                command = None
        else:
            command = request.POST.get('command')
    else:
        command = request.GET.get('command')

    if not command:
        return error('Command is empty')

    if not isinstance(command, str):
        return error('Command must be string')

    try:
        cp = subprocess.run(shlex.split(command), capture_output=True)
        return shell_output(cp)

    except Exception as e:
        return exception(e)


@agent_token_required
@require_GET
def info(request):
    return JsonResponse({
        'version': __version__
    })
