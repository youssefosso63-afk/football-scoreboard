from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import Team, Score, Match

def index(request):
    scores = Score.objects.all().order_by('-pts')
    return render(request, 'vb/scoreboard.html', {'scores': scores})

def match_setup(request):
    teams = Team.objects.all()
    return render(request, 'vb/match_setup.html', {'teams': teams})

def live_redirect(request):
    team1_id = request.GET.get('team1')
    team2_id = request.GET.get('team2')
    return redirect('live_match', team1_id=team1_id, team2_id=team2_id)

def live_match(request, team1_id, team2_id):
    team1 = Team.objects.get(id=team1_id)
    team2 = Team.objects.get(id=team2_id)
    return render(request, 'vb/scoring_system.html', {'team1': team1, 'team2': team2})

@csrf_exempt
def submit_score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        team1 = Team.objects.get(id=data['team1_id'])
        team2 = Team.objects.get(id=data['team2_id'])

        Match.objects.create(
            team1=team1, team2=team2,
            scheduled_date=timezone.now(),
            team1_sets=data['sets1'], team2_sets=data['sets2'],
            mvp_name=data['mvp'],
            is_played=True,
            played_at=timezone.now()
        )

        for team, sets_for, sets_against in [(team1, data['sets1'], data['sets2']),
                                              (team2, data['sets2'], data['sets1'])]:
            score, _ = Score.objects.get_or_create(team=team)
            score.matches += 1
            if sets_for > sets_against:
                score.W += 1
                score.pts += 3
            else:
                score.L += 1
            score.save()

        return JsonResponse({'status': 'ok'})

def mvp_list(request):
    matches = Match.objects.filter(is_played=True).order_by('-played_at')
    return render(request, 'vb/mvp.html', {'matches': matches})

def schedule_match(request):
    if request.method == 'POST':
        team1 = Team.objects.get(id=request.POST['team1'])
        team2 = Team.objects.get(id=request.POST['team2'])
        Match.objects.create(
            team1=team1, team2=team2,
            scheduled_date=request.POST['scheduled_date'],
            is_played=False
        )
        return redirect('upcoming_matches')
    teams = Team.objects.all()
    return render(request, 'vb/schedule_match.html', {'teams': teams})

def upcoming_matches(request):
    matches = Match.objects.filter(is_played=False).order_by('scheduled_date')
    return render(request, 'vb/matches.html', {'matches': matches})

def played_matches(request):
    matches = Match.objects.filter(is_played=True).order_by('-played_at')
    return render(request, 'vb/old.html', {'matches': matches})