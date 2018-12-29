from github import Github
import github
import os
import datetime
import json
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

#g = Github()
# g = Github(os.environ["user"], os.environ["password"])

# user = g.get_user()

yearStart = datetime.datetime(2018, 1, 1, 0, 0, 0, 0)


@app.route("/", methods=['GET'])
def hello():
    return "hi"

# @app.route("/authenticate", methods=['GET', 'POST'])
# def authenticate():
#     global g
#     token = request.form['token']
#     g = Github(token)
#     return "success"


@app.route("/get_highest_starred_repo_created/<token>", methods=['GET'])
def get_highest_starred_repo_created(token):
    g = Github(token)
    user = g.get_user()
    highestStars = -1
    highestRepo = ""
    for repo in user.get_repos():
        if repo.stargazers_count > highestStars:
            highestStars = repo.stargazers_count
            highestRepo = repo.name
    return str([highestStars, highestRepo])



@app.route("/get_first_repo_created/<token>", methods=['GET'])
def get_first_repo_created(token):
    g = Github(token)
    user = g.get_user()
    earliestRepo = github.Repository.Repository
    earliestTime = datetime.datetime(2900, 12, 30)
    for repo in user.get_repos():
        if repo.created_at > yearStart:
            if repo.created_at < earliestTime:
                earliestRepo = repo
                earliestTime = repo.created_at
    return earliestRepo.name

@app.route("/get_num_repos_created/<token>", methods=['GET'])
def get_num_repos_created(token):
    g = Github(token)
    user = g.get_user()
    num_repos = 0
    for repo in user.get_repos():
        if repo.created_at > yearStart:
            num_repos += 1
    return str(num_repos)

@app.route("/get_favorite_languages/<token>", methods=['GET'])
def get_favorite_languages(token):
    g = Github(token)
    user = g.get_user()
    languages = []
    num_occurences = []
    for repo in user.get_repos():
        if repo.language not in languages:
            languages.append(repo.language)
            num_occurences.append(1)
        else:
            idx = languages.index(repo.language)
            num_occurences[idx] += 1
    languages_with_occurences = sorted(zip(languages, num_occurences), key=lambda x: x[1], reverse=True)

    return str([i[0] for i in languages_with_occurences])

@app.route("/get_recommended_repos/<token>", methods=['GET'])
def get_recommended_repos(token):
    g = Github(token)
    user = g.get_user()
    repositories = g.search_repositories(query='language:' + get_favorite_languages(token).split(",")[0][3:-1], sort="stars", order="desc")
    recommended_repos = {}
    for repo in  repositories[:10]:
        recommended_repos.update({repo.name : repo.html_url})
    return json.dumps(recommended_repos)

@app.route("/get_tastebreaker_repos/<token>", methods=['GET'])
def get_tastebreaker_repos(token):
    g = Github(token)
    user = g.get_user()
    tastebreaker_repos = {}
    repositories_a = g.search_repositories(query='good-first-issues:>3 language:' + get_favorite_languages(token).split(",")[1][3:-1])

    for repo in repositories_a[:5]:
        tastebreaker_repos.update({repo.name : repo.html_url})

    if len(get_favorite_languages(token).split(","))>2:
        repositories_b = g.search_repositories(query='good-first-issues:>3 language:' + get_favorite_languages(token).split(",")[2][3:-1])
        for repo in repositories_b[:5]:
            tastebreaker_repos.update({repo.name : repo.html_url})

    return json.dumps(tastebreaker_repos)



@app.route("/get_recommended_contribution_repos/<token>", methods=['GET'])
def get_recommended_contribution_repos(token):
    g = Github(token)
    user = g.get_user()
    recommended_contribution_repos = {}
    repositories = g.search_repositories(query='good-first-issues:>3 language:' + get_favorite_languages(token).split(",")[0][3:-1])
    for repo in repositories[:10]:
        recommended_contribution_repos.update({repo.name : repo.html_url})
    return json.dumps(recommended_contribution_repos)


@app.route("/get_best_starred_repos/<token>", methods=['GET'])
def get_best_starred_repos(token):
    g = Github(token)
    user = g.get_user()
    starred_list = []
    starred_repos = user.get_starred()
    for repo in starred_repos:
        starred_list.append((repo, repo.stargazers_count))
    starred_list = sorted(starred_list, key=lambda x: x[1], reverse=True)
    sorted_list = [i[0] for i in starred_list[:10]]
    starred_dict = {}
    for repo in sorted_list:
        starred_dict.update({repo.name : repo.html_url})
    return json.dumps(starred_dict)

if __name__ == "__main__":
    app.run()

