"""n = int(input())
msters = list(map(int, input().split()))
msters.sort()
cnt = 0
ans = 0
while msters and msters[-1] >= 2*n:        #先处理血量大于2*n的怪物
    ans += msters.pop() - n            #实际攻击时将接受剩余aoe的血量预留下来，实际攻击次数就相当于接受完n次aoe后的血量
    cnt += 1                    #记录已经触发的aoe次数
for msterhp in msters:        #再依次从小到大取数
    nowhp = msterhp - cnt            #当前怪物接受完之前的aoe后的剩余血量
    if nowhp > msterhp // 2:        #如果当前敌人没有触发aoe，就攻击他直到触发他的aoe
        ans += nowhp - msterhp//2
        nowhp = msterhp//2
    if nowhp - (n-cnt) > 0:    #再计算当前敌人需要的攻击次数
        ans += nowhp - (n-cnt)
    cnt += 1        #记录的aoe次数+1
print(ans)

from collections import defaultdict

N = 200010
mod = int(1e9) + 7
n = 0
f = [0] * N
w = [0] * N
d = [0] * N
sum = [0] * N
g = defaultdict(list)

def dfs(u, fa, depth):
    d[u] = depth
    sum[u] = w[u]
    f[u] += 1 * w[u] * d[u]
    for x in g[u]:
        if x == fa:
            continue
        t = dfs(x, u, depth + 1)
        f[u] += t[0]
        sum[u] += t[1]
    return f[u], sum[u]

n = int(input())
w=[0]+list(map(int,input().split()))
for i in range(1, n):
    a, b = map(int, input().split())
    g[a].append(b)
    g[b].append(a)
dfs(1, 0, 1)
res = f[1]
for i in range(2, n + 1):
    if d[i] <= 2:
        continue
    down = 1 * (d[i] - 2) * sum[i]
    res = min(res, f[1] - down)
print(res)
"""


def dfs(u, fa):
    global ans
    # 如果1号点到u+1点的距离 <= k，则答案加1
    if dist[u] <= k:
        ans += 1
    # 如果1号点到叶子的距离 < k，则还可以再这个叶子下加 k - dist[u] 个
    if u != 0 and len(g[u]) == 1 and dist[u] < k:
        ans += k - dist[u]
    # 继续遍历子树 v
    for v in g[u]:
        if v == fa:
            continue
        dist[v] = dist[u] + 1
        dfs(v, u)


n, k = map(int, input().split())

# 建图
g = [[] for _ in range(n)]
for _ in range(1, n):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    g[v].append(u)
INF = int(1e9)

ans = 0
dist = [INF] * n
# 计算1号点到每个点的距离，1号点到自己的距离为 0
dist[0] = 0

dfs(0, -1)
print(dist)
print(ans)
