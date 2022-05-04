


# --- GENERAL ---


# loading graph

def read_json_file(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


# define plotting function
def PlotSemiLogPlot(data, xlabel='', title='', figsize=((8,3)), dpi=200, path=None):
    min_val, max_val = (min(data), max(data))
    
    # compute bins
    log_bins = np.logspace(min_val if min_val == 0 else np.log10(min_val), np.log10(max_val), 101)
    lin_bins = np.linspace(min_val, max_val, 101)

    # create histogram values
    hist_log, edges_log = np.histogram(data.values, log_bins, density=True)
    hist_lin, edges_lin = np.histogram(data.values, lin_bins)

    # determine x-values
    log_x = (edges_log[1:] + edges_log[:-1]) / 2.
    lin_x = (edges_lin[1:] + edges_lin[:-1]) / 2.

    xx, yy = zip(*[(i,j) for (i,j) in zip(log_x, hist_log) if j > 0])
    
    # plot figure
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=figsize, dpi=dpi)

    # linear scale plot
    ax[0].plot(lin_x, hist_lin, marker='.', alpha=0.5)
    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel('count of communities')
    ax[0].set_title('linear scale')
    #ax[0].legend()

    # log-log scale plot
    ax[1].plot(xx, yy, marker='.', alpha=0.5)
    ax[1].set_yscale('log')
    #ax[1].set_xscale('log')
    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel('probability density')
    ax[1].set_title('semi-log scale')
    #ax[1].legend()
    fig.suptitle(title, fontsize=12)
    plt.savefig(path)


    # show figure
    plt.tight_layout()
    
    plt.show()
    return
    
### ---RQ1---



### ---RQ2---


def visualize_graph(name, graph, coloring_attribute = None, num_samples = None, config = None, print_config = True):
    graph_copy = graph.copy()
    
    if num_samples is not None:
        graph_copy = graph_copy.subgraph(random.sample(graph_copy.nodes, num_samples))
        
    keep = ['group', 'weights', 'size']
    
    # calculating here since value might change if graph is a subgraph
    sorted_degrees = sorted(graph_copy.degree(weight='weight'), key=lambda x: x[1], reverse=True)
    degrees = dict(sorted_degrees)
    if coloring_attribute is not None:
        for k, v in graph_copy.nodes(data=True):
                        
            v['group'] = v[coloring_attribute]
            v['weights'] = 1
            v['size'] = degrees[k]
            
            #np.nansum([v['num_comments'], v['num_submissions']])
            for attr in list(v.keys()):
                if attr not in keep:
                #if coloring_attribute != attr:
                    del v[attr]
    #new_graph_copy = nw.get_filtered_network(graph_copy, node_group_key='group')
    
    network, config = nw.visualize(graph_copy, plot_in_cell_below=False, config = config)
    
    # print config if not defined
    if print_config:
        print('config file: \n')
        print(config)

    fig, ax = nw.draw_netwulf(network)
    N = 5 # top k
    top_nodes = list(list(zip(*sorted_degrees[:N]))[0])
    
    for node_id in top_nodes:
        nw.add_node_label(ax, network, node_id)
    
    fig.set_size_inches(18.5, 10.5)
    # save figure
    plt.savefig(f'{DATA_DIR / name}.jpg')
    return
    
    
def generateWordCloud(freqs, color_func, save):
    # dictionary of {word: tfidf-score}
    #freqs = TFIDF[label]

    # Create and generate a word cloud image:
    
    wordcloud = WordCloud(width=700, height=300, max_font_size=50, max_words=100, background_color="white")
    wordcloud = wordcloud.generate_from_frequencies(freqs)

    # Display the generated image:
    #default_colors = wordcloud.to_array()
    fig = plt.figure(figsize=(20,10), dpi = 400)
    plt.imshow(wordcloud.recolor(color_func=color_func, random_state=3), interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    
    # save image
    name = 'data/figs/rq2/wc_com_' + save + '.png'
    wordcloud.to_file(name)
    return
    
    
    
    
    
### ---RQ3---










