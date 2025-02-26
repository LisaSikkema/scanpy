from pathlib import Path

from matplotlib.testing import setup
setup()

import scanpy as sc

HERE: Path = Path(__file__).parent
ROOT = HERE / '_images'
FIGS = HERE / 'figures'

sc.pl.set_rcParams_defaults()
sc.set_figure_params(dpi=40, color_map='viridis')

#####
# Test images are saved under the folder ./figures
# if test images need to be updated, simply copy them from
# the ./figures folder to ./_images/


def test_heatmap(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=15)

    adata = sc.datasets.krumsiek11()
    sc.pl.heatmap(adata, adata.var_names, 'cell_type', use_raw=False, show=False, dendrogram=True)
    save_and_compare_images('master_heatmap')

    # test swap axes
    sc.pl.heatmap(adata, adata.var_names, 'cell_type', use_raw=False, show=False, dendrogram=True,
                  swap_axes=True, figsize=(10, 3), cmap='YlGnBu')
    save_and_compare_images('master_heatmap_swap_axes')

    # test heatmap numeric column():

    # set as numeric column the vales for the first gene on the matrix
    adata.obs['Gata2'] = adata.X[:, 0]
    sc.pl.heatmap(adata, adata.var_names, 'Gata2', use_raw=False,
                  num_categories=4, figsize=(4.5, 5), show=False)
    save_and_compare_images('master_heatmap2')

    # test var/obs standardization and layer
    adata.layers['test'] = -1 * adata.X.copy()
    sc.pl.heatmap(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True, show=False,
                  standard_scale='var', layer='test')
    save_and_compare_images('master_heatmap_std_scale_var')

    sc.pl.heatmap(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True, show=False,
                  standard_scale='obs')
    save_and_compare_images('master_heatmap_std_scale_obs')


def test_dotplot(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=15)

    adata = sc.datasets.krumsiek11()
    sc.pl.dotplot(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True, show=False)
    save_and_compare_images('master_dotplot')

    # test dotplot numeric column():
    adata.obs['Gata2'] = adata.X[:, 0]
    sc.pl.dotplot(adata, adata.var_names, 'Gata2', use_raw=False,
                  num_categories=7, figsize=(7, 2.5), show=False)
    save_and_compare_images('master_dotplot2')

    # test dotplot dot_min, dot_max, color_map, and var_groups
    pbmc = sc.datasets.pbmc68k_reduced()
    marker_genes = ['CD79A', 'MS4A1', 'CD8A', 'CD8B', 'LYZ', 'LGALS3', 'S100A8', 'GNLY', 'NKG7', 'KLRB1',
                    'FCGR3A', 'FCER1A', 'CST3']
    sc.pl.dotplot(pbmc, marker_genes, groupby='louvain',
                  dot_max=0.7, dot_min=0.1, color_map='hot_r',
                  var_group_positions=[(0, 1), (11, 12)],
                  var_group_labels=['B cells', 'dendritic'],
                  figsize=(7, 2.5), dendrogram=True, show=False)
    save_and_compare_images('master_dotplot3')

    # test dict as markers input
    markers_dict = {'T-cell': 'CD3D', 'B-cell': 'CD79A', 'myeloid': 'CST3'}
    sc.pl.dotplot(pbmc, markers_dict, groupby='bulk_labels',
                  dot_max=0.7, dot_min=0.1, color_map='winter',
                  figsize=(7, 2.5), dendrogram=True, show=False)
    save_and_compare_images('master_dotplot_dict')

    # test var/group standardization smallest_dot
    sc.pl.dotplot(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True, show=False,
                  standard_scale='var', smallest_dot=40)
    save_and_compare_images('master_dotplot_std_scale_var')

    sc.pl.dotplot(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True, show=False,
                  standard_scale='group', smallest_dot=10)
    save_and_compare_images('master_dotplot_std_scale_group')


def test_matrixplot(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=15)

    adata = sc.datasets.krumsiek11()
    sc.pl.matrixplot(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True, show=False)
    save_and_compare_images('master_matrixplot')

    # test swap_axes
    sc.pl.matrixplot(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True, show=False, swap_axes=True)
    save_and_compare_images('master_matrixplot_swap_axes')

    # test var/group standardization and layer
    adata.layers['test'] = -1 * adata.X.copy()
    sc.pl.matrixplot(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True,
                     show=False, standard_scale='var', layer='test', cmap='Blues_r')
    save_and_compare_images('master_matrixplot_std_scale_var')

    sc.pl.matrixplot(adata, adata.var_names, 'cell_type', use_raw=False, dendrogram=True,
                     show=False, standard_scale='group', swap_axes=True)
    save_and_compare_images('master_matrixplot_std_scale_group')

    # test matrixplot numeric column and alternative cmap
    adata.obs['Gata2'] = adata.X[:, 0]
    sc.pl.matrixplot(adata, adata.var_names, 'Gata2', use_raw=False,
                     num_categories=4, figsize=(8, 2.5), cmap='viridis', show=False)
    save_and_compare_images('master_matrixplot2')


def test_stacked_violin(image_comparer, plt):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=26)

    adata = sc.datasets.krumsiek11()
    sc.pl.stacked_violin(adata, adata.var_names, 'cell_type', use_raw=False, color='blue', show=False)

    plt.title("image may have cut labels.\nThis is ok for test")
    save_and_compare_images('master_stacked_violin')

    # test swapped axes
    sc.pl.stacked_violin(adata, adata.var_names, 'cell_type', use_raw=False,
                         swap_axes=True, figsize=(3, 5), show=False)
    save_and_compare_images('master_stacked_violin_swapped_axes')


def test_tracksplot(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=15)

    adata = sc.datasets.krumsiek11()
    sc.pl.tracksplot(adata, adata.var_names, 'cell_type', dendrogram=True, use_raw=False)
    save_and_compare_images('master_tracksplot')


def test_violin(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=40)

    sc.pl.set_rcParams_defaults()
    sc.set_figure_params(dpi=50, color_map='viridis')

    pbmc = sc.datasets.pbmc68k_reduced()
    sc.pl.violin(pbmc, ['n_genes', 'percent_mito', 'n_counts'],
                 stripplot=True, multi_panel=True, jitter=True, show=False)
    save_and_compare_images('master_violin_multi_panel')


def test_dendrogram(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=10)

    pbmc = sc.datasets.pbmc68k_reduced()
    sc.pl.dendrogram(pbmc, 'bulk_labels')
    save_and_compare_images('dendrogram')


def test_correlation(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=15)

    pbmc = sc.datasets.pbmc68k_reduced()
    sc.pl.correlation_matrix(pbmc, 'bulk_labels')
    save_and_compare_images('correlation')


def test_rank_genes_groups(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=15)

    pbmc = sc.datasets.pbmc68k_reduced()

    from matplotlib import rcParams
    rcParams['axes.grid'] = True
    rcParams['figure.figsize'] = 4, 4

    sc.pl.rank_genes_groups(pbmc, n_genes=12, n_panels_per_row=3, show=False)
    save_and_compare_images('master_ranked_genes_sharey')

    # test ranked genes panels sharey = False
    sc.pl.rank_genes_groups(pbmc, n_genes=12, n_panels_per_row=3, sharey=False, show=False)
    save_and_compare_images('master_ranked_genes')

    # test ranked genes using heatmap
    sc.pl.rank_genes_groups_heatmap(pbmc, n_genes=5, cmap='YlGnBu', show=False)
    save_and_compare_images('master_ranked_genes_heatmap')

    # test ranked genes using heatmap (swap_axes=True show_gene_labels=False)
    sc.pl.rank_genes_groups_heatmap(pbmc, n_genes=20, swap_axes=True, use_raw=False,
                                    show_gene_labels=False, show=False, vmin=-3, vmax=3, cmap='bwr')
    save_and_compare_images('master_ranked_genes_heatmap_swap_axes')

    # test ranked genes using stacked violin plots
    sc.pl.rank_genes_groups_stacked_violin(pbmc, n_genes=3, show=False)
    save_and_compare_images('master_ranked_genes_stacked_violin', tolerance=20)

    # test ranked genes using dotplot
    sc.pl.rank_genes_groups_dotplot(pbmc, n_genes=4, show=False)
    save_and_compare_images('master_ranked_genes_dotplot')

    # test ranked genes using matrixplot
    sc.pl.rank_genes_groups_matrixplot(pbmc, n_genes=5, show=False)
    save_and_compare_images('master_ranked_genes_matrixplot')

    # test ranked genes using matrixplot
    sc.pl.rank_genes_groups_matrixplot(pbmc, n_genes=5, show=False)
    save_and_compare_images('master_ranked_genes_matrixplot')

    # test ranked genes using matrixplot (swap_axes=True)
    sc.pl.rank_genes_groups_matrixplot(pbmc, n_genes=5, swap_axes=True, show=False)
    save_and_compare_images('master_ranked_genes_matrixplot_swap_axes')

    # test ranked genes using tracks_plot
    sc.pl.rank_genes_groups_tracksplot(pbmc, n_genes=5, show=False)
    save_and_compare_images('master_ranked_genes_tracksplot')

    # # test ranked genes using violin plots
    # sc.pl.rank_genes_groups_violin(pbmc, groups=pbmc.obs.bulk_labels.cat.categories[0], n_genes=5,
    #                                jitter=False, strip=False, show=False)
    # save_and_compare_images('master_ranked_genes_stacked_violin', tolerance=tolerance)


def test_rank_genes_symbols(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=15)

    adata = sc.datasets.krumsiek11()

    # add a 'symbols' column
    adata.var['symbols'] = adata.var.index.map(lambda x: "symbol_{}".format(x))
    symbols = ["symbol_{}".format(x) for x in adata.var_names]
    sc.pl.heatmap(adata, symbols, 'cell_type', use_raw=False, show=False, dendrogram=True,
                  gene_symbols='symbols')
    save_and_compare_images('master_heatmap_gene_symbols')

    sc.pl.dotplot(adata, symbols, 'cell_type', use_raw=False, dendrogram=True, show=False,
                  gene_symbols='symbols')

    save_and_compare_images('master_dotplot_gene_symbols')

    sc.pl.matrixplot(adata, symbols, 'cell_type', use_raw=False, dendrogram=True, show=False,
                     gene_symbols='symbols')

    save_and_compare_images('master_matrixplot_gene_symbols')

    sc.pl.stacked_violin(adata, symbols, 'cell_type', use_raw=False, color='blue', show=False,
                         gene_symbols='symbols')
    save_and_compare_images('master_stacked_violin_gene_symbols', tolerance=21)

    sc.pl.tracksplot(adata, symbols, 'cell_type', dendrogram=True, use_raw=False,
                     gene_symbols='symbols')
    save_and_compare_images('master_tracksplot_gene_symbols')


def test_scatterplots(image_comparer):
    save_and_compare_images = image_comparer(ROOT, FIGS, tol=15)

    pbmc = sc.datasets.pbmc68k_reduced()

    # test pca
    sc.pl.pca(pbmc, color='bulk_labels', show=False)
    save_and_compare_images('master_pca')

    # test projection='3d'
    sc.pl.pca(pbmc, color='bulk_labels', projection='3d', show=False)
    save_and_compare_images('master_3dprojection')

    sc.pl.pca(pbmc, color=['CD3D', 'CD79A'], components=['1,2', '1,3'],
              vmax=5, use_raw=False, vmin=-5, cmap='seismic', show=False)
    save_and_compare_images('master_multipanel')

    # test tsne
    # I am removing this test because  slight differences are present even
    # after setting a random_state.
    # sc.tl.tsne(pbmc, random_state=0, n_pcs=30)
    # sc.pl.tsne(pbmc, color=['CD3D', 'louvain'], show=False)
    # save_and_compare_images('master_tsne', tolerance=tolerance)

    # test umap with louvain clusters and palette with custom colors
    sc.pl.umap(pbmc, color=['louvain'],
               palette=['b', 'grey80', 'r', 'yellow', 'black', 'gray', 'lightblue'],
               frameon=False, show=False)
    save_and_compare_images('master_umap')

    # test umap with gene expression
    import numpy as np
    sc.pl.umap(pbmc, color=np.array(['LYZ', 'CD79A']), s=20, alpha=0.5, frameon=False,
               title=['gene1', 'gene2'], show=False)
    save_and_compare_images('master_umap_gene_expr')

    # test umap using layer
    pbmc.layers['test'] = pbmc.X.copy() + 100
    sc.pl.umap(pbmc, color=np.array(['LYZ', 'CD79A']), s=20, alpha=0.5, frameon=False,
               title=['gene1', 'gene2'], layer='test', show=False, vmin=100)
    save_and_compare_images('master_umap_layer')

    # test edges = True
    sc.pp.neighbors(pbmc)
    sc.pl.umap(pbmc, color='louvain', edges=True, edges_width=0.1, s=50, show=False)
    save_and_compare_images('master_umap_with_edges', tolerance=35)

    # test diffmap
    # sc.tl.diffmap(pbmc)
    # sc.pl.diffmap(pbmc, components='all', color=['CD3D'], show=False)
    # save_and_compare_images('master_diffmap', tolerance=tolerance)

    # test gene_symbols
    pbmc.var["numbers"] = [str(x) for x in range(pbmc.shape[1])]
    sc.pl.umap(pbmc, color=['1', '2', '3'], gene_symbols="numbers", show=False)
    save_and_compare_images('master_umap_symbols')
