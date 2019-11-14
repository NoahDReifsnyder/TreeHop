import random
import matplotlib
import matplotlib.pyplot as plt
expectation_types = ['Immediate', 'Informed', 'Regression', 'G-Regression']

n = 10
loop = .08
fall = .02
success = 1 - loop - fall

series_sum = .08/.92

one_node = series_sum * fall + fall

a_s = one_node
for t in range(n-2):
    a_s = a_s * success
    a_s += one_node
print(a_s)



Informed = {"name": "Informed", "cost": 20-(10*a_s), "failure": a_s, "score": 0}
Regression = {"name": "Regression", "cost": 10, "failure": 88, "score": 0}
Gregression = {"name": "G-Regression", "cost": 15-(10*a_s), "failure": a_s, "score": 0}
Immediate = {"name": "Immediate", "cost": 10, "failure": 92, "score": 0}
Exp = [Informed, Regression, Gregression, Immediate]
error = .1
scores = {}
for i in range(100):
    for x in Exp:
        if x['name'] not in scores:
            scores[x['name']] = {}
        diff = x['cost'] * error
        new = random.random() * diff + x['cost'] - diff
        print(new, x['cost'])
        if i > 0:
            scores[x['name']][i] = scores[x['name']][i-1] + new
        else:
            scores[x['name']][i] = new
print(scores)
types = ['-.', 'x', 'o', '-']
for key in scores:
    plt.plot(scores[key].keys(), scores[key].values(), types.pop(), label=key)
plt.legend(loc='upper left')
plt.show()
