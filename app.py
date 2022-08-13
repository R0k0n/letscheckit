from traceback import print_tb
from flask import Flask , request
from flask import render_template
import requests

app = Flask(__name__)

def fetch(handle):
    r = requests.get('https://codeforces.com/api/user.status?handle='  + handle + '&from=1&count=1000000')
    r = r.json()
    r = r['result']
    names = []
    tags = {'var' : 'ok'}
    rat = {'var' : 'ok'}
    vis = {'var' : 1}
    st = {}
    for attribute in r:
        name = attribute['problem']['name']
        name = str(attribute['problem'].get('contestId')) + str(attribute['problem']['index'])
        if 'rating' in attribute['problem']:
            difficulty = attribute['problem']['rating']
        if 'tags' in attribute['problem']:
            tag = attribute['problem']['tags']
        solve = attribute['verdict']
        if solve == 'OK':
            if name in vis:
                continue
            vis[name] = 1
            rat[name] = difficulty
            tags[name] = tag
            names.append(name)
        else:
            st[solve] = 1
            
    abc = 800
    solve_by_ratting = {800 : 0}
    while abc < 3500:
        abc += 100
        solve_by_ratting[abc] = 0
            
    for abc in rat.keys():
        if abc == 'var':
            continue
        #print(abc)
        solve_by_ratting[rat[abc]] += 1
        
    print(solve_by_ratting)
        
    
    print(st.keys())
        
    tag_solve_count = {'greedy' : 0}
    
    for abc in rat.keys():
        if abc == 'var':
            continue
        for value in tags[abc]:
            if value in tag_solve_count:
                tag_solve_count[value] += 1
            else:
                tag_solve_count[value] = 1
                
    
    print(tag_solve_count)
            
    return {"solved_by_tag": tag_solve_count, "solved_by_rating": solve_by_ratting }

@app.route("/")
def hello_world():
    args = request.args
    handle = args.get('handle')
    if not handle:
        handle ='_shadow'
    data = fetch(handle)
    return render_template('home.html' , handle = handle , solved_by_tag = data['solved_by_tag'], solved_by_rating = data['solved_by_rating'])

