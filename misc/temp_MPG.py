# Dijkstra
def disjoint_path_priority(G,users,c,index):
        G_trimmed = G.copy()
        users_TBD = list(users)
        shortest_paths_disj = []
        shortest_paths_disj_edges = []
        while len(users_TBD) > 0:
            shortest_paths = {}
            shortest_paths_cost = {}
            for u in users_TBD:
                G_no_u = G_trimmed.copy()
                try:
                    G_no_u.remove_nodes_from([v for v in list(users) if v!=u])
                    G_no_u.add_node(u)
                    shortest_path = nx.shortest_path(G_no_u,source=c,target=u, weight='weight')
                    shortest_paths[u] = shortest_path
                    shortest_paths_cost[u] = nx.path_weight(G_no_u, shortest_paths[u], weight="weight")
                except nx.NetworkXNoPath as e:
                    return []
            sorted_paths = sorted(shortest_paths, key=shortest_paths.get, reverse=True)
            try:
                chosen_shortest_path_user = sorted_paths[index]
            except IndexError:
                    chosen_shortest_path_user = sorted_paths[-1]
            chosen_shortest_path = shortest_paths[chosen_shortest_path_user]
            shortest_paths_disj.append(chosen_shortest_path)
            users_TBD.remove(chosen_shortest_path_user)
            for i in range(len(chosen_shortest_path)-1):
                G_trimmed.remove_edge(chosen_shortest_path[i],chosen_shortest_path[i+1])

        for path in shortest_paths_disj:
            for i in range(len(path)-1):
                shortest_paths_disj_edges.append((path[i],path[i+1]))
        return shortest_paths_disj_edges


def find_disjoint_path_edges(G,users,c,check_connected=False):
        for j in [0,-1]+list(range(1,len(users)-1)): # first longest, then shortest, ...
             disj_paths_edges = disjoint_path_priority(G,users,c,j)
             if disj_paths_edges != []:
                  return disj_paths_edges
        return []            

def users_connected_center_disj(G,users,c):
    shortest_disj = find_disjoint_path_edges(G,users,c,check_connected=True)
    if len(shortest_disj) == 0:
        return [False,None]
    else:
        return [True,shortest_disj]



def protocol(algo,G,users):            
    # initialise G'
    G_prime = nx.Graph()
    G_prime.add_nodes_from(G.nodes())

    # central node used in SP and MPG
    if algo in {'SP','MPG'}:
        central = find_center_node(G,users)[0]

    # SP: entanglement over shortest path edges
    # MPG,MPC: entangement over all edges
    if algo == 'SP':
        entangle_edges = find_disjoint_path_edges(G,users,central)
    elif algo in {'MPG','MPC'}:
        entangle_edges = G.edges(data=True)
    
    edge_memory = {}
    hasGHZ = False 
    iter = 0

    while not hasGHZ:
        
        iter += 1
        new_edges = []
        
        for e in entangle_edges:
            e_tuple = (e[0],e[1])
            if e in G_prime.edges():
                e_mem = edge_memory[e_tuple]
                if e_mem == 0:
                    G_prime.remove_edge(*e)
                elif e_mem > 0:
                    edge_memory[e_tuple] -= 1

            elif e not in G_prime.edges():
                edge_memory[e_tuple] = 0
                
                e_prob = G.get_edge_data(*e_tuple).get('p', 1.0)
                rng = np.random.random()
                if rng < e_prob:
                    if algo == 'SP':
                        G_prime.add_edge(*e_tuple)
                    elif algo in {'MPG','MPC'}:
                        G_prime.add_edge(*e_tuple,weight=e[2]['weight'])
                    edge_memory[e_tuple] = T_c

                    new_edges.append(e)
        

        # Plot each time a new edge is found
        plot_new_e = False
        if plot_new_e and len(new_edges)>0:
            nx.draw(G_prime, with_labels=True, edgecolors='black', font_size=5, node_size=70, pos=pos[i],node_color=real_topo_colors[i])
            plt.title(algo + ': iteration ' + str(iter))
            plt.show()
        
        # SP,MPG: checks if each user node connects to central node
        # MPC: checks if all user nodes are connected
        if algo == 'SP':
            hasGHZ = all([e in G_prime.edges() for e in entangle_edges])

        elif algo == 'MPG':
            UCCD = users_connected_center_disj(G_prime,users,central)
            hasGHZ = UCCD[0]
            valid_edges = UCCD[1]

        elif algo == 'MPC':
            users_path_exist = []
            for nodes in combinations(users, 2):
                G_prime_no_u = G_prime.copy()
                for u in [u_ for u_ in users if u_ not in nodes]:
                    G_prime_no_u.remove_node(u)
                users_path_bool = nx.has_path(G_prime_no_u, *nodes)
                users_path_exist.append(users_path_bool)
            if all(users_path_exist):
                hasGHZ = True

            #steiner = nx.algorithms.approximation.steinertree.steiner_tree(G_prime,users,weight='weight')


        if hasGHZ:
            if algo == 'SP':
                return (G_prime,iter,entangle_edges)

            elif algo == 'MPG':
                return (G_prime,iter,valid_edges)

            elif algo == 'MPC':
                return (G_prime,iter)#,steiner.edges())