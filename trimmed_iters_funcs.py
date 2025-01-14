import networkx as nx
import numpy as np


from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network, shortest_augmenting_path

real_topo_users = {0: (4, 22, 25, 41), 1: (1, 3, 5, 6), 2: (1, 7, 15, 17), 3: (3, 7, 9, 11),  4: (11, 13, 17, 18), 5: (1, 7, 9, 11), 6: (2, 3, 10, 11), 7: (2, 16, 17, 19), 8: (1, 2, 11, 12), 10: (2, 8, 15, 16), 11: (5, 116, 133, 138), 12: (5, 13, 15, 17), 13: (5, 13, 15, 23), 14: (5, 13, 18, 19), 16: (1, 6, 8, 12), 17: (18, 21, 37, 41), 19: (1, 2, 3, 6), 21: (1, 13, 14, 30), 22: (1, 7, 12, 25), 26: (16, 17, 19, 23), 27: (8, 28, 40, 49), 28: (14, 15, 16, 21), 29: (11, 35, 61, 63), 30: (1, 9, 69, 95), 33: (1, 7, 13, 15), 34: (1, 2, 47, 48), 35: (1, 2, 3, 26), 36: (10, 21, 24, 29), 37: (5, 6, 15, 21), 38: (1, 2, 8, 9), 39: (1, 4, 13, 14), 40: (1, 5, 11, 17), 41: (16, 17, 19, 23), 42: (5, 11, 14, 15), 43: (18, 24, 28, 29), 45: (8, 10, 16, 19), 47: (2, 11, 16, 30), 48: (9, 10, 11, 13), 49: (8, 35, 96, 97), 50: (13, 23, 27, 31), 51: (3, 4, 14, 18), 52: (26, 27, 46, 52), 54: (4, 5, 17, 25), 55: (24, 29, 30, 45), 57: (4, 11, 13, 35), 58: (11, 18, 20, 28), 61: (1, 2, 23, 25), 62: (1, 3, 10, 14), 63: (9, 22, 42, 43), 64: (1, 5, 17, 18), 65: (1, 4, 10, 13), 67: (12, 16, 18, 19), 68: (1, 7, 13, 19), 70: (9, 12, 22, 34), 71: (9, 22, 31, 51), 72: (9, 13, 17, 20), 76: (8, 9, 16, 18), 77: (1, 13, 15, 32), 79: (1, 2, 24, 25), 80: (1, 11, 12, 18), 81: (3, 13, 15, 27), 82: (4, 6, 7, 8), 83: (4, 5, 9, 12), 84: (1, 4, 5, 14), 86: (2, 5, 8, 10), 88: (15, 19, 25, 30), 89: (1, 11, 14, 17), 90: (4, 6, 10, 16), 92: (1, 8, 15, 19), 93: (8, 28, 40, 49), 94: (1, 2, 8, 27), 95: (2, 3, 11, 21), 96: (8, 12, 16, 18), 97: (6, 11, 13, 20), 98: (5, 8, 12, 19), 100: (3, 6, 9, 10), 101: (2, 12, 16, 23), 102: (1, 4, 6, 7), 104: (7, 20, 22, 24)}
presave_centers = {0: 35, 1: 2, 2: 26, 3: 12, 4: 8, 5: 1, 6: 9, 7: 12, 8: 7, 10: 11, 11: 81, 12: 12, 13: 12, 14: 18, 16: 3, 17: 32, 19: 7, 21: 12, 22: 9, 26: 14, 27: 24, 28: 1, 29: 22, 30: 31, 33: 12, 34: 28, 35: 11, 36: 26, 37: 13, 38: 7, 39: 8, 40: 2, 41: 14, 42: 17, 43: 20, 45: 4, 47: 1, 48: 12, 49: 32, 50: 33, 51: 14, 54: 21, 55: 14, 57: 31, 58: 23, 61: 7, 62: 4, 63: 30, 64: 4, 65: 7, 68: 9, 70: 26, 71: 30, 72: 18, 76: 1, 77: 12, 79: 17, 81: 10, 82: 9, 83: 6, 84: 11, 86: 6, 88: 18, 89: 18, 92: 15, 93: 24, 94: 15, 95: 13, 96: 22, 97: 10, 98: 16, 100: 3, 101: 11, 102: 2, 104: 1}

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

def make_star_from_paths(G, best_paths):
    J = G.__class__()
    J.add_nodes_from(
        G.nodes(data=True)
    )  # Graph J with nodes from G and no edges (yet!)
    for path in best_paths:
        for u, v in zip(path, path[1:]):
            J.add_edge(u, v)  # add edge to new graph J
            J.edges[u, v].update(G.get_edge_data(u, v))
    return J

def is_valid_star(disjoint_paths, users):
    users_valid = {u: False for u in users}
    for path in disjoint_paths:
        if path[0] in users:
            users_valid[path[0]] = True
        if path[-2] in users: # -1 as exclude super-sink
            users_valid[path[-2]] = True
    return all([is_valid for is_valid in users_valid.values()])

def get_source_and_star(G_base, users, w, first_guess=None):

    
    #     """
    #     improved version of get_source and get_star ... use this instead of get source OR get star!
    #     https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.disjoint_paths.edge_disjoint_paths.html

    #     Input Pararmeters:
    #     G      - Networkx graph G(V,E) which defines the topology of the network. see graphs.py for more details
    #     users  - List of nodes in G which between which a GHZ should be shared. users[0] is the centre of the star which should be calculated before sending to SP_protocol
    #     Outputs:
    #     best_source - the best source node in graph for SP (and maybe but not confirmed MPG)
    #     best_paths  - the list of paths from source - destinations
    #     J      - Networkx graph J(V,E') with edges of the star-path connecting each destination user with the source node
    #
    # Note shortest path currently min-hop distance
    G = G_base.copy()
    candidate_nodes = [
        node for node in G.nodes if G.degree(node) >= len(users)
    ]  # any node with degree >= number of user
    candidate_nodes += [
         node for node in users if G.degree(node) == len(users) - 1
    ]  # + also users with degree >= num users - 1 (excluding ones already added)
    super_destination = ("x", "x")
    [
        G.add_edge(node, super_destination, weight=0, p=1) for node in users
    ]  # any p > than that of network?
    if first_guess is not None:
        candidate_nodes = [first_guess] + candidate_nodes

    H = build_auxiliary_edge_connectivity(G)
    # Note that the auxiliary digraph has an edge attribute named capacity
    R = build_residual_network(H, "capacity")

    best_source = None
    best_paths = []  # default empty?
    min_length = np.inf
    for node in candidate_nodes:
        disjoint_paths = list(
            nx.edge_disjoint_paths(
                G,
                node,
                super_destination,
                auxiliary=H,
                residual=R,
                flow_func=shortest_augmenting_path,
            )
        )
        success = is_valid_star(disjoint_paths, users)

        if w == 'hops':
            tot_length = sum( [len(path) - 1 for path in disjoint_paths] )
        elif w == 'weight':
            tot_length = sum( [nx.path_weight(G, path, 'weight') for path in disjoint_paths] )
        elif w == 'p':
            tot_length = sum( [nx.path_weight(G, path, 'p') for path in disjoint_paths] )


        if (tot_length < min_length) and success:
            min_length = tot_length
            best_source = node
            best_paths = disjoint_paths
            # print(x)
    G.remove_edges_from(list(G.edges(super_destination)))
    G.remove_node(super_destination)

    if best_source is None:
        #return None, [], None
        raise ValueError(f"valid source for users {users} not found. Perhaps there were no valid candidate nodes? {candidate_nodes}")

    best_paths_remove_super_sink = [path[:-1] for path in best_paths]
    best_paths_edges = [list(zip(path, path[1:])) for path in best_paths_remove_super_sink]
    best_paths_edges = [edge for edges in best_paths_edges for edge in edges]

    J = make_star_from_paths(G, best_paths_remove_super_sink)
    return best_source, best_paths_edges, J

def users_connected_center_disj(G,users,c):
    shortest_disj = find_disjoint_path_edges(G,users,c,check_connected=True)
    if len(shortest_disj) == 0:
        return [False,None]
    else:
        return [True,shortest_disj]
    
def users_connected(G,users):
    for u in users:
        for v in users:
            if v!= u:
                if not nx.has_path(G,u,v):
                    return False
    return True

def check_disjoint_flow(G_base,users,c,w):
    G = G_base.copy()
    
    super_destination = ("x", "x")
    [
        G.add_edge(node, super_destination, weight=0, p=1) for node in users
    ]  # any p > than that of network?
    
    H = build_auxiliary_edge_connectivity(G)
    # Note that the auxiliary digraph has an edge attribute named capacity
    R = build_residual_network(H, "capacity")
    
    try:
        disjoint_paths = list(
            nx.edge_disjoint_paths(
                G,
                c,
                super_destination,
                auxiliary=H,
                residual=R,
                flow_func=shortest_augmenting_path,
            )
        )
    except nx.NetworkXNoPath:
        return [False, None]
    
    success = is_valid_star(disjoint_paths, users)

    if success:
        paths_remove_super_sink = [path[:-1] for path in disjoint_paths]
        paths_edges = [list(zip(path, path[1:])) for path in paths_remove_super_sink]
        paths_edges = [edge for edges in paths_edges for edge in edges]
        return [True, paths_edges]
    elif not success:
        return [False, None]

    # to end
    return
    if w == 'hops':
        tot_length = sum( [len(path) - 1 for path in disjoint_paths] )
    elif w == 'weight':
        tot_length = sum( [nx.path_weight(G, path, 'weight') for path in disjoint_paths] )
    elif w == 'p':
        tot_length = sum( [nx.path_weight(G, path, 'p') for path in disjoint_paths] )

    
def protocol_presave(prtcl,G,users,i):
    
    T_c = np.inf
    
    if prtcl not in {'SP','MPG','MPC'}:# presave paths, center... etc  
        raise ValueError("algorithm must be SP, MPG or MPC.")
    
    if not isinstance(G, nx.Graph):
        raise TypeError("G must be a NetworkX graph.")
    
    if not isinstance(users, (list, set, tuple)):
        raise TypeError("users must be a list or set of nodes.")
    
    # initialise G'
    G_prime = nx.Graph()
    G_prime.add_nodes_from(G.nodes())

    # evan output
    if prtcl == 'MPG':
        evan_output = get_source_and_star(G,users,'weight')
   
    # central node used in SP and MPG
    center = presave_centers[i]

    # SP: entanglement over shortest path edges
    # MPG,MPC: entangement over all edges
    if prtcl == 'SP':
            entangle_edges = evan_output[1]
            
    elif prtcl in {'MPG','MPC'}:
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
                    if prtcl == 'SP':
                        G_prime.add_edge(*e_tuple)
                    elif prtcl in {'MPG','MPC'}:
                        G_prime.add_edge(*e_tuple,weight=e[2]['weight'])
                    edge_memory[e_tuple] = T_c

                    new_edges.append(e)
        
        
        # SP,MPG: checks if each user node connects to central node
        # MPC: checks if all user nodes are connected
        if prtcl == 'SP':
            hasGHZ = all([e in G_prime.edges() for e in entangle_edges])

        elif prtcl == 'MPG':
            if users_connected(G_prime,users):
                UCCD = check_disjoint_flow(G_prime,users,evan_output[0],'weight')
                hasGHZ = UCCD[0]
                valid_edges = UCCD[1]
        

        elif prtcl == 'MPC':
            hasGHZ = users_connected(G_prime,users)

    if hasGHZ:
        if prtcl == 'SP':
            return (G_prime,iter,entangle_edges)

        elif prtcl == 'MPG':
            return (G_prime,iter,valid_edges)

        elif prtcl == 'MPC':

            G_prime_connected = G_prime.copy()
            for node in G_prime.nodes():
                if not nx.has_path(G_prime,users[0],node): # connected to 1 user means connected to all users
                    G_prime_connected.remove_node(node)
            steiner = nx.algorithms.approximation.steinertree.steiner_tree(G_prime_connected, users, weight='weight',method='mehlhorn')
            
            return (G_prime,iter,steiner)