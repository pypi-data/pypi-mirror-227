from argparse import Namespace
import ast
import configparser
import copy
from dask import array as da
import gc
import gdown
import glob
from imageio.v2 import imread
import io
from magicgui import magicgui
import matplotlib
from matplotlib import patches, pyplot as plt
from matplotlib.path import Path

matplotlib.use("Agg")
import napari
from napari_bioformats import napari_get_reader
from napari.layers import Image
from napari.utils.progress import progress
import networkx as nx
import numpy as np
from numpy import math, unicode
import os
import pandas as pd
from pandas import DataFrame
from PIL import Image
import phenograph
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import RAPID.GUI.config as cfg
import RAPID.GUI.GUIUtils as utils
from RAPID.Impressionist import runRAPIDzarr
from RAPID.network import objectmodels, IID_loss
from RAPID.network.model import load_checkpoint, weight_init, RAPIDMixNet
from RAPID.spatialanalysis import KNN
from RAPID.util.utils import generate_colormap, denoise_img, preprocess, save_preprocess, run_pca
from RAPID.util.mst import prep_for_mst, generate_mst
import re
from scipy import ndimage
from scipy.spatial import distance
import seaborn as sns
import shutil
from shutil import copyfile
from skimage import img_as_ubyte, measure, morphology
from skimage.color import label2rgb
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import stat
import tifffile
import torch
from torch import optim
import torch.nn as nn
import umap
import vaex
import vaex.ml
from vispy.color import ColorArray, Colormap
import webbrowser
import zarr

path = os.path.dirname(os.path.abspath(__file__)) + "/../models/ModelDenoise_UnetPlus40.pt"
if not os.path.exists(path):
    gdown.download("https://drive.google.com/uc?id=1aYBi0oKbJq-bjYBPc6DxhRl8cjMU8O4d", path, verify=False)
gc.enable()


### TODO: Add to documentation.
### TODO: Add error messages on Jupyter.
### TODO: Fix colors in the table for different analyses.

### TODO: Subclustering and/or merging, numerator and denominator of table are different
### TODO: Biaxial color according to cell marker flip axis?
### TODO: Loading pixel clustering, selecting images to load is not scrollable.

class RAPIDGUI():
    """
    Class containing all functions available in the RAPID GUI, as well as core functions/attributes.
    """

    def apply_clusters_defined_patches(self,
                                       patchesstart,
                                       isloadingmodel,
                                       results_folder,
                                       modelparams,
                                       markerindices,
                                       markernames,
                                       modelpath,
                                       add_grey_img,
                                       add_color_img,
                                       ):
        """
        Perform pixel-based clustering on user-defined patches.

        Args:
            patchesstart (list): List of vertices defining top-left corner for each 64x64 patch, for each image.
            isloadingmodel (bool): If True, load pre-trained model weights. Otherwise, use random weight initialization.
            results_folder (str): Path to the folder where results will be saved.
            modelparams (iterable): List of parameters for the desired clustering algorithm.
            markerindices (list): List of indices of cell markers to be considered for clustering.
            markernames (list): List of names of cell markers to be considered for clustering.
            modelpath (str): Path to pretrained model, if loading a model.
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """

        # Prompt user to define parameters.
        args = runRAPIDzarr.get_parameters()

        # Find the number of patches across all the images.
        args.npatches = 0
        for img in patchesstart:
            args.npatches += len(img)

        if isloadingmodel:
            params = utils.RAPIDTrainLoadedParams(args, israndompatches=False)
            args.rfold = "/".join(modelpath[:-1])
            copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(results_folder, "checkpoint.pth"))
            args.loadmodel = True
        else:
            maximgshape = np.insert(cfg.max_img_shape, 0, cfg.num_markers)
            params = utils.RAPIDPixelParameters(len(markerindices), maximgshape, israndompatches=False)
            args.rfold = cfg.output_folder
            args.loadmodel = False

        if modelparams == []:
            params.exec()
            if not params.OK:
                return
            args.ncluster = int(params.nc)
            args.nit = int(params.nit)
            args.bs = int(params.bs)
            args.mse = params.mse == "True"
            args.rescalefactor = float(params.RCN)
            args.lr = float(params.lr)
            args.SCANloss = params.SCAN
            args.rescale = params.RC == "True"
            denoise = params.denoise
            normalize = params.normalize
            modelparams = [args.ncluster, args.nit, args.bs, args.mse, args.rescalefactor, args.lr, args.SCANloss,
                           args.rescale, denoise, normalize]
        else:
            args.ncluster, args.nit, args.bs, args.mse, args.rescalefactor, \
            args.lr, args.SCANloss, args.rescale, denoise, normalize = modelparams
        args.normalize, args.normalizeall, args.normtype, args.pca = utils.pixel_normtype(normalize)

        # Normalize data for RAPID input.
        cfg.viewer.status = "Generating RAPID data..."
        self.generate_RAPID_data(markerindices,
                                 markernames,
                                 os.path.join(results_folder, "RAPID_Data"),
                                 denoise,
                                 args.normalize,
                                 args.normalizeall,
                                 args.normtype,
                                 args.pca,
                                 )

        # Update parameters and save them to the output folder.
        hf = zarr.open(os.path.join(results_folder, "RAPID_Data"), mode='r+')
        args.nchannels = hf["data"].shape[1]
        args.distance = True
        args.predict = False
        args.patchsize = 64
        args.epoch = 1
        args.GUI = True
        args.testbs = 20000
        if not cfg.has_added_table:
            cfg.analysis_mode = "Pixel"
        if not os.path.exists(args.rfold):
            os.mkdir(args.rfold)
            args.rfold = args.rfold + "/"
        else:
            args.rfold = args.rfold + "/"
        hf.attrs['arg'] = vars(args)

        # Train RAPID algorithm.
        cfg.viewer.status = "Training RAPID..."
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        cfg.viewer.window._status_bar._toggle_activity_dock(True)
        grey, prob, tab, colors, _ = runRAPIDzarr.train_rapid(args,
                                                              device,
                                                              os.path.join(results_folder, "RAPID_Data"),
                                                              results_folder,
                                                              patchesstart,
                                                              )
        grey += 1
        cfg.viewer.window._status_bar._toggle_activity_dock(False)

        # Reshape results into multi-channel image array.
        count = 0
        for i in range(cfg.num_imgs):
            vdim = cfg.img_shape_list[i][0]
            hdim = cfg.img_shape_list[i][1]
            cfg.labeled_imgs.append(utils.convert_dtype(grey[count: count + vdim * hdim].reshape(vdim, hdim)))
            count += vdim * hdim

        # Save colors to the output folder.
        if isloadingmodel:
            colors = np.load("/".join(modelpath[:-1]) + "/color.npy")
        np.save(os.path.join(results_folder, "color.npy"), colors)

        # Update any relevant variables and close the window.
        self.apply_pixel_clustering(tab.values,
                                    args,
                                    colors,
                                    add_grey_img,
                                    add_color_img,
                                    results_folder,
                                    )
        cfg.pixel_cluster_count += 1
        cfg.analysis_log.append("Pixel")
        return modelparams

    def apply_contrast_limits(self,
                              img,
                              contrast_limits,
                              ):
        """
        Apply both lower- and upper-bound thresholds to an image array.

        Args:
            img (numpy.ndarray): Array for image data having contrast limits applied to it.
            contrast_limits (iterable): List containing the lower and upper bound values for the contrast limits being applied.
        """
        lower = contrast_limits[0]
        upper = contrast_limits[1]
        img[img < lower] = lower
        img[img > upper] = upper
        img = (img - lower) / (upper - lower) * 255
        img[img < 0] = 0
        img[img > 255] = 255
        return img.astype(np.uint8)

    def apply_edits(self,
                    editactions,
                    imgindex=-1,
                    ):
        """
        Apply any changes made in the Edit Image popup window.

        Args:
            editactions (list): Sequence of edits to be made for each image.
            imgindex (int, optional): Index of image to apply edits to. If -1, apply across all images (Default: -1).
        """
        imgnums = [i for i in range(cfg.num_imgs) if not i == imgindex]
        for i in range(cfg.num_markers):
            for edits in editactions:
                for j in imgnums:
                    if edits[j][i] == "Gaussian":
                        cfg.viewer.layers[i].data[j, :, :] = ndimage.gaussian_filter(
                            cfg.viewer.layers[i].data[j, :, :], [1, 1])
                    elif edits[j][i] == "Median":
                        cfg.viewer.layers[i].data[j, :, :] = ndimage.median_filter(cfg.viewer.layers[i].data[j, :, :],
                                                                                   [1, 1])
                    elif len(edits[j][i]) == 2:
                        cfg.viewer.layers[i].data[j, :, :] = self.apply_contrast_limits(
                            cfg.viewer.layers[i].data[j, :, :],
                            edits[j][i],
                        )
                if any([edits[j][i] == "Denoise" or edits[j][i] == "Binarize" for j in imgnums]):
                    denoiseimgnums = [j for j in imgnums if edits[j][i] == "Denoise" or edits[j][i] == "Binarize"]
                    cfg.viewer.layers[i].data[denoiseimgnums, :, :] = np.moveaxis(
                        denoise_img(np.moveaxis(cfg.viewer.layers[i].data[denoiseimgnums, :, :], 0, -1).astype(float)),
                        -1, 0)
                if any([edits[j][i] == "Binarize" for j in imgnums]):
                    binarizeimgnums = [j for j in imgnums if edits[j][i] == "Binarize"]
                    cfg.viewer.layers[i].data[binarizeimgnums, :, :][
                        cfg.viewer.layers[i].data[binarizeimgnums, :, :] > 0] = 255
            if not imgindex == -1:
                cfg.viewer.layers[i].data[imgindex, :, :] = cfg.edit_viewer.layers[i].data

    def apply_object_clustering(self,
                                clusterids,
                                tabindex,
                                segmentedtab,
                                results_folder,
                                add_grey_img,
                                add_color_img,
                                labelnames,
                                ):
        """
        Apply object cluster labels to segmented images, add relabeled images to the viewer, and save relabeled images
        and data tables to output folder.

        Args:
            clusterids (numpy.ndarray): Array of cluster IDs for each cell across all images.
            tabindex (int): Index of first table for the selected round of segmentation being used for clustering.
            segmentedtab (numpy.ndarray): Array of average expression values for each cell across all images.
            results_folder (str): Path to folder where results will be saved.
            add_grey_img (bool): True if adding greyscale labeled images to the viewer, otherwise False.
            add_color_img (bool): True if adding RGB-color images to the viewer, otherwise False.
            labelnames (list): List of names for each of the clusters if applicable.
        """

        paramslist = cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        numclusters = len(np.unique(clusterids))

        vals = list(np.unique(clusterids))
        for i in range(len(clusterids)):
            clusterids[i] = vals.index(clusterids[i]) + 1

        # Save data table for segmented results with cluster assignments as well as image ID and (x,y)-coordinates.
        cord = np.vstack(cfg.cell_coordinates[int(tabindex / cfg.num_imgs)])
        imgid = []
        for i in range(cfg.num_imgs):
            imgid.append(np.repeat(i + 1, len(cfg.data_list[cfg.segmentation_indices[i + tabindex]])))
        segmentedtab_DF = pd.DataFrame(segmentedtab)
        segmentedtab_DF.columns = np.array(paramslist)
        segmentedtab_DF.insert(0, "Cluster", [str(val) for val in clusterids])
        segmentedtab_DF.insert(0, "ImgID", np.hstack(imgid))
        segmentedtab_DF.insert(0, "Y", cord[:, 1])
        segmentedtab_DF.insert(0, "X", cord[:, 0])
        segmentedtab_DF.to_csv(os.path.join(results_folder, "SegmentationClusterIDs.csv"))
        cfg.object_cluster_dfs.append(segmentedtab_DF)

        # Insert cluster IDs to segmentation data table
        segmentedtab = np.insert(segmentedtab, 0, clusterids, axis=1)

        # Initialize image array to store cluster IDs for each pixel
        labelimg = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]), dtype=np.uint8)

        # Initialize list of arrays containing mean cluster expression levels, sample and cluster IDs, and cell counts.
        data = []

        # Generate colors to map to each cluster ID
        color = generate_colormap(numclusters + 1)[:-1, :]
        cfg.object_cluster_colors.append(color)
        np.save(os.path.join(results_folder, "color.npy"), color)

        # Retrieve segmentation results being used for clustering.
        analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Segmentation"][
                          tabindex // cfg.num_imgs] * cfg.num_imgs
        for i in range(cfg.num_imgs):
            # Get name of current image
            imgname = os.path.splitext(os.path.split(cfg.file_names[i])[-1])[0]

            # Number of cells in the current image.
            numcells = len(cfg.data_list[cfg.segmentation_indices[i + tabindex]])

            # Cluster IDs for each of the cells in the current image.
            to_values = clusterids[:numcells]
            cfg.cell_cluster_vals.append(to_values)

            # Save image with labeled cluster IDs.
            imgshape = (cfg.img_shape_list[i][0], cfg.img_shape_list[i][1])
            relabeled = self.method_searchsort(np.arange(1, 1 + numcells),
                                               to_values,
                                               cfg.labeled_imgs[i + analysisnum].flatten().astype(int),
                                               )
            labelimg[i, :imgshape[0], :imgshape[1]] = relabeled.reshape((imgshape[0], imgshape[1])).astype(np.uint8)
            labelimg[i, :imgshape[0], :imgshape[1]][cfg.labeled_imgs[i + analysisnum] == 0] = 0
            utils.save_img(os.path.join(results_folder,
                                        f"ObjectClusterLabels_{imgname}.tif",
                                        ),
                           labelimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] + 1,
                           cfg.img_is_flipped[i],
                           )

            # Save colored clustered image.
            rgbimg = np.zeros((cfg.max_img_shape[0], cfg.max_img_shape[1], 3),
                              dtype=np.uint8,
                              )
            for j in range(len(vals)):
                rgbimg[:, :, 0][labelimg[i, :, :] == j + 1] = color[j][0]
                rgbimg[:, :, 1][labelimg[i, :, :] == j + 1] = color[j][1]
                rgbimg[:, :, 2][labelimg[i, :, :] == j + 1] = color[j][2]
            utils.save_img(os.path.join(results_folder,
                                        f"ObjectClusters_{imgname}.tif",
                                        ),
                           rgbimg[:cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1], :],
                           cfg.img_is_flipped[i],
                           )

            # Add images to the viewer.
            if add_grey_img:
                paddedrgbimg = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1], 3), dtype=np.uint8)
                paddedrgbimg[0, :cfg.max_img_shape[0], :cfg.max_img_shape[1], :] = rgbimg

            if i == 0:
                if add_grey_img:
                    cfg.viewer.add_image(labelimg[[i], :, :],
                                         name=f"Object Cluster IDs {cfg.object_cluster_count + 1}", blending="additive",
                                         contrast_limits=(0, np.max(labelimg)))
                if add_color_img:
                    cfg.viewer.add_image(paddedrgbimg, name=f"Object Clusters {cfg.object_cluster_count + 1}",
                                         blending="additive")
            else:
                if add_grey_img and add_color_img:
                    cfg.viewer.layers[-2].data = np.vstack((cfg.viewer.layers[-2].data, labelimg[[i], :, :]))
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, paddedrgbimg))
                elif add_grey_img:
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, labelimg[[i], :, :]))
                elif add_color_img:
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, paddedrgbimg))

            # Group cells with the same cluster ID and find mean expression values for each cluster.
            tabres = pd.DataFrame(segmentedtab[:numcells])
            tabres = tabres.groupby(0)
            tabres = tabres.apply(np.mean)
            tabres.insert(0, "Sample", i + 1)
            _, counts = np.unique(to_values, return_counts=True)
            tabres.insert(2, "Cells", counts)
            datatab = np.zeros((numclusters, tabres.values.shape[1]))
            datatab[np.unique(to_values.astype(np.uint8) - 1), :] = tabres.values
            datatab[:, 0] = np.repeat(i + 1, numclusters)
            datatab[:, 1] = np.arange(numclusters) + 1
            data.append(datatab)
            datatab = datatab[:, 2:]
            cfg.data_list.append(datatab)

            # Update variables.
            cfg.current_table_orders_filtered.append(list(range(len(np.unique(to_values)))))
            minvals = []
            maxvals = []
            uniqueclusters = np.unique(to_values.astype(np.uint8) - 1)
            for j in range(1, datatab.shape[1]):
                minvals.append(np.min(datatab[uniqueclusters, j]))
                maxvals.append(np.max(datatab[uniqueclusters, j]))
            cfg.min_vals.append(copy.deepcopy(minvals))
            cfg.max_vals.append(copy.deepcopy(maxvals))
            cfg.lower_bounds_list.append(copy.deepcopy(minvals))
            cfg.upper_bounds_list.append(copy.deepcopy(maxvals))
            clusterids = clusterids[numcells:]
            segmentedtab = segmentedtab[numcells:]
        data = np.nan_to_num((np.vstack(data)))
        cfg.labeled_imgs += [utils.convert_dtype(labelimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]])
                             for i in range(len(labelimg))]

        # Find weighted average data across all images and store min and max expression averages for each parameter.
        if cfg.num_imgs > 1:
            weighted_average = np.zeros((numclusters, data.shape[1] - 2))
            for i in range(numclusters):
                clusterids = [i + j * numclusters for j in range(int(len(data) / numclusters))]
                weighted_average[i, 0] = np.sum(data[clusterids, 2])
                weighted_average[i, 1:] = np.average(data[clusterids, 3:], axis=0, weights=data[clusterids, 2])
            cfg.data_list.append(weighted_average)
            cfg.current_table_orders_filtered.append(list(range(len(weighted_average))))
            minvals = []
            maxvals = []
            for i in range(weighted_average.shape[1] - 1):
                minvals.append(np.min(weighted_average[:, i + 1]))
                maxvals.append(np.max(weighted_average[:, i + 1]))
            cfg.min_vals.append(copy.deepcopy(minvals))
            cfg.max_vals.append(copy.deepcopy(maxvals))
            cfg.lower_bounds_list.append(copy.deepcopy(minvals))
            cfg.upper_bounds_list.append(copy.deepcopy(maxvals))

        # Save full clustered data table.
        data = pd.DataFrame(data)
        data.columns = np.hstack([["Sample", "Cluster", "# Cells"], paramslist])
        data.to_csv(os.path.join(results_folder, "ObjectClusterAvgExpressionVals.csv"))
        tabledata, my_data_scaled, distmatrix, uniqueclusters = prep_for_mst(clustertable=data,
                                                                             minclustersize=1,
                                                                             clustersizes=data["# Cells"],
                                                                             includedmarkers=paramslist,
                                                                             )
        generate_mst(distancematrix=distmatrix,
                     normalizeddf=my_data_scaled,
                     colors=color,
                     randomseed=0,
                     clusterheatmap=True,
                     outfolder=results_folder,
                     displaymarkers=paramslist,
                     uniqueclusters=uniqueclusters,
                     samplenames=list(np.unique(data['Sample'])),
                     displaysingle=False,
                     values="# Cells",
                     )

        cfg.viewer.add_image(imread(os.path.join(results_folder, "MeanExpressionHeatmap.png")),
                             name=f"Object Clusters {cfg.object_cluster_count + 1} Heatmap",
                             blending="additive",
                             visible=False,
                             )

        # Update table sort module and other necessary variables.
        for i in range(cfg.num_imgs):
            cfg.table_img_names.append(
                f"Object Cluster {cfg.object_cluster_count + 1} - {cfg.file_names[i].split('/')[-1]}")
            cfg.object_cluster_indices.append(cfg.table_count)
            cfg.table_count += 1
            cfg.currently_selected.append([])
        if cfg.num_imgs > 1:
            cfg.table_img_names.append(f"Object Cluster {cfg.object_cluster_count + 1} - Combined Average")
            cfg.object_cluster_indices.append(cfg.table_count)
            cfg.table_count += 1
            cfg.currently_selected.append([])
        cfg.segmentation_clustering_rounds[int(tabindex / cfg.num_imgs)].append(cfg.object_cluster_count)
        cfg.object_cluster_count += 1
        cfg.analysis_log.append("Object")
        cfg.clusters_are_pixel_based.append(False)
        cfg.cluster_names.append(labelnames)
        cfg.update_log_file = False
        cfg.sort_table_widget.data.choices = tuple(cfg.table_img_names)
        cfg.sort_table_widget.data.value = f"Object Cluster {cfg.object_cluster_count} - {cfg.file_names[0].split('/')[-1]}"
        cfg.sort_table_widget.reset_choices()
        cfg.update_log_file = True

    def apply_pixel_clustering(self,
                               tab,
                               args,
                               colors,
                               add_grey_img,
                               add_color_img,
                               results_folder,
                               ):
        """
        Populate the viewer and the table with results from RAPID-P clustering.

        Args:
            tab (numpy.ndarray): Data being used to populate the table.
            args (Namespace): Additional user-defined parameters used for training.
            colors (numpy.ndarray): Array (#clusters x 3) of RGB values for each cluster.
            add_grey_img (bool): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't.
            add_color_img (bool): If True, add RGB-colored segmented image to the viewer. Otherwise, don't.
            results_folder (str): Path to the folder where results will be saved.
        """
        if cfg.num_imgs > 1:
            data = np.zeros((cfg.num_imgs + 1, args.ncluster, tab.shape[1] - 2))
        else:
            data = np.zeros((cfg.num_imgs, args.ncluster, tab.shape[1] - 2))
        for i in range(cfg.num_imgs):
            data[i, :, :] = tab[args.ncluster * i:args.ncluster * (i + 1), 2:]
            cfg.table_img_names.append(
                f"Pixel Cluster {cfg.pixel_cluster_count + 1} - {cfg.file_names[i].split('/')[-1]}")
            cfg.pixel_cluster_indices.append(cfg.table_count)
            cfg.table_count += 1
        if 'None' in cfg.table_img_names:
            cfg.table_img_names.remove('None')
        if cfg.num_imgs > 1:
            cfg.table_img_names.append(f"Pixel Cluster {cfg.pixel_cluster_count + 1} - Combined Average")
            cfg.pixel_cluster_indices.append(cfg.table_count)
            cfg.table_count += 1
            table = np.zeros((args.ncluster, tab.shape[1]))
            for i in range(args.ncluster):
                npixels = 0
                for j in range(cfg.num_imgs):
                    npixels += tab[args.ncluster * j + i, 2]
                for j in range(cfg.num_imgs):
                    table[i, 3:] += tab[args.ncluster * j + i, 3:] * float(tab[args.ncluster * j + i, 2] / npixels)
                table[i, 2] = npixels
            data[-1, :, :] = table[:, 2:]
            for i in range(cfg.num_imgs + 1):
                minvals = []
                maxvals = []
                for j in range(data.shape[2] - 1):
                    minvals.append(np.min(data[i, :, j + 1]))
                    maxvals.append(np.max(data[i, :, j + 1]))
                cfg.min_vals.append(copy.deepcopy(minvals))
                cfg.max_vals.append(copy.deepcopy(maxvals))
                cfg.lower_bounds_list.append(copy.deepcopy(minvals))
                cfg.upper_bounds_list.append(copy.deepcopy(maxvals))
                cfg.currently_selected.append([])
        elif cfg.num_imgs == 1:
            minvals = []
            maxvals = []
            for j in range(data.shape[2] - 1):
                minvals.append(np.min(data[0, :, j + 1]))
                maxvals.append(np.max(data[0, :, j + 1]))
            cfg.min_vals.append(copy.deepcopy(minvals))
            cfg.max_vals.append(copy.deepcopy(maxvals))
            cfg.lower_bounds_list.append(copy.deepcopy(minvals))
            cfg.upper_bounds_list.append(copy.deepcopy(maxvals))
            cfg.currently_selected.append([])

        if not cfg.has_added_table:
            self.update_table(data[0, :, :],
                              cfg.lower_bounds_list[cfg.table_index],
                              cfg.upper_bounds_list[cfg.table_index],
                              data.shape[1],
                              )

        cfg.current_table_order_full = []
        for i in range(data.shape[1]):
            cfg.current_table_order_full.append(i)
        for i in range(len(data)):
            cfg.data_list.append(data[i, :, :])
            cfg.current_table_orders_filtered.append(list(range(data.shape[1])))

        # Add the clustered image(s) to the main GUI viewer window.
        for i in range(cfg.num_imgs):
            labelimg = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1]),
                                dtype=cfg.labeled_imgs[i - cfg.num_imgs].dtype)
            colorimg = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1], 3), dtype=np.uint8)
            labelimg[0, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = cfg.labeled_imgs[i - cfg.num_imgs]
            for j in range(args.ncluster):
                colorimg[labelimg == j + 1] = colors[j, :]

            if i == 0:
                if add_grey_img:
                    cfg.viewer.add_image(labelimg,
                                         name=f"Pixel Cluster IDs {cfg.pixel_cluster_count + 1}",
                                         blending="additive",
                                         contrast_limits=(0, args.ncluster))
                if add_color_img:
                    cfg.viewer.add_image(colorimg,
                                         name=f"Pixel Clusters {cfg.pixel_cluster_count + 1}",
                                         blending="additive")
            else:
                if add_grey_img and add_color_img:
                    cfg.viewer.layers[-2].data = np.vstack((cfg.viewer.layers[-2].data, labelimg))
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, colorimg))
                elif add_grey_img:
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, labelimg))
                elif add_color_img:
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, colorimg))
        self.set_invisible(cfg.viewer)
        cfg.viewer.layers[-1].visible = True

        cfg.viewer.add_image(imread(os.path.join(results_folder, "MeanExpressionHeatmap.png")),
                             name=f"Pixel Clusters {cfg.pixel_cluster_count + 1} Heatmap",
                             blending="additive",
                             visible=False,
                             )

        # Update any necessary variables.
        cfg.viewer.status = "RAPID clustering done"
        cfg.clusters_are_pixel_based.append(True)
        cfg.pixel_cluster_colors.append(colors)
        cfg.cluster_names.append([])
        cfg.update_log_file = False
        cfg.sort_table_widget.data.choices = tuple(cfg.table_img_names)
        cfg.sort_table_widget.data.value = f"Pixel Cluster {cfg.pixel_cluster_count + 1} - {cfg.file_names[0].split('/')[-1]}"
        cfg.sort_table_widget.reset_choices()
        cfg.update_log_file = True

    def apply_segmentation(self,
                           add_grey_img,
                           add_color_img,
                           quant_avg,
                           outfolder,
                           zarrpath="",
                           probthreshold=None,
                           minsize=None,
                           maxsize=None,
                           loadedresultspaths=[],
                           ):
        """
        Convert outputs from segmentation algorithm to an image with labeled cells, and quantify average marker
        expression and morphological information.

        Args:
            add_grey_img (bool): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't.
            add_color_img (bool): If True, add RGB-colored segmented image to the viewer. Otherwise, don't.
            quant_avg (bool): If True, use mean expression values for quantification. Otherwise, calculate root-mean-square values.
            outfolder (str): Path to the folder where results will be saved.
            zarrpath (str, optional): Path to zarr file where results and image properties will be stored (Default: "").
            probthreshold (float, optional): Value in the range [0,1] defining model prediction probability threshold for cells to include (Default: None).
            minsize (int, optional): Minimum pixel area of cells to include in segmentation (Default: None).
            maxsize (int, optional): Maximum pixel area of cells to include in segmentation (Default: None).
            loadedresultspaths (list, optional): List of paths for the segmented images being loaded (Default: []).
        """

        cfg.viewer.status = "Calculating cell phenotypes"
        cortabs = []
        numcells = 0
        for img_index, path in enumerate(cfg.file_names):
            # Get name of current image
            imgname = os.path.splitext(os.path.split(path)[-1])[0]

            if loadedresultspaths == []:
                # Find cells within threshold values set by the user.
                xcrop = cfg.max_img_shape[0]
                ycrop = cfg.max_img_shape[1]
                fh = zarr.open(zarrpath,
                               mode='r',
                               )
                blobs = np.array(fh[f"Features{img_index}"]) >= probthreshold
                blobs = measure.label(blobs[:xcrop, :ycrop],
                                      connectivity=1,
                                      )
                blobs = morphology.remove_small_objects(blobs,
                                                        min_size=int(minsize),
                                                        )
                blobs = utils.remove_large_objects(blobs,
                                                   maxsize=int(maxsize),
                                                   )
                label_image = objectmodels.expand_objects(objectimg=blobs,
                                                          numiterations=round(0.284 / cfg.resolution),
                                                          )
                label_image = morphology.remove_small_objects(label_image.astype(bool),
                                                              min_size=int(minsize),
                                                              in_place=True,
                                                              )

                # Label the segmented images and save to output folder.
                label_image, _ = measure.label(label_image,
                                               connectivity=1,
                                               return_num=True,
                                               )
                label_image = label_image[:cfg.img_shape_list[img_index][0], :cfg.img_shape_list[img_index][1]]
                label_image = label_image.astype(np.uint32)
            else:
                # Store labeled segmented image files.
                filename = os.path.join(os.path.abspath(loadedresultspaths[img_index]))
                label_image, flipimg = self.parse_img(filename,
                                                      True,
                                                      )
                cfg.img_is_flipped.append(flipimg)

            object_count = len(np.unique(label_image)) - 1
            utils.save_img(os.path.join(outfolder, f"SegmentedLabels_{imgname}.tif"),
                           label_image,
                           cfg.img_is_flipped[img_index],
                           )
            cfg.labeled_imgs.append(utils.convert_dtype(label_image))

            quant_tab = utils.quantify_segmented_img(object_count,
                                                     cfg.num_markers,
                                                     quant_avg,
                                                     label_image,
                                                     img_index,
                                                     )

            # Create RGB-colored image for segmentation and save it to the output folder.
            rgb_image = (label2rgb(label_image,
                                   image=None,
                                   colors=None,
                                   alpha=0.3,
                                   bg_label=0,
                                   bg_color=(0, 0, 0),
                                   image_alpha=1,
                                   kind='overlay',
                                   ) * 255).astype(np.uint8)

            # Save RGB-colored segmented image to the output folder
            utils.save_img(os.path.join(outfolder, f"Segmented_{imgname}.tif"),
                           rgb_image[:cfg.img_shape_list[img_index][0], :cfg.img_shape_list[img_index][1], :],
                           cfg.img_is_flipped[img_index],
                           )

            # Add the segmented image(s) to the main GUI viewer window.
            utils.add_results_to_viewer(img_index,
                                        cfg.max_img_shape,
                                        add_grey_img,
                                        add_color_img,
                                        rgb_image,
                                        label_image,
                                        cfg.viewer,
                                        [0, 1],
                                        f"Labels {cfg.segment_count + 1}",
                                        f"Segment {cfg.segment_count + 1}",
                                        )

            # Store centroid coordinates and cell labels, and store full quantified tables in memory.
            cortabs.append([prop.centroid for prop in measure.regionprops(label_image)])
            cfg.data_list.append(quant_tab)
            cfg.currently_selected.append([])
            cfg.current_table_orders_filtered.append(list(range(len(quant_tab))))
            numcells += len(quant_tab)

            # Store min and max values for each of the cell markers and morphological parameters.
            minvals = []
            maxvals = []
            for j in range(quant_tab.shape[1]):
                minvals.append(np.min(quant_tab[:, j]))
                maxvals.append(np.max(quant_tab[:, j]))
            cfg.segmentation_indices.append(len(cfg.lower_bounds_list))
            cfg.lower_bounds_list.append(copy.deepcopy(minvals))
            cfg.upper_bounds_list.append(copy.deepcopy(maxvals))
            cfg.min_vals.append(copy.deepcopy(minvals))
            cfg.max_vals.append(copy.deepcopy(maxvals))

            # Update dropdown menu for table widget.
            cfg.table_img_names.append(f"(Segment [{cfg.segment_count}]) - {path.split('/')[-1]}")
            cfg.table_count += 1

        cfg.total_num_cells.append(numcells)

        # Set only the most recently-added image to visible.
        self.set_invisible(cfg.viewer)
        cfg.viewer.layers[-1].visible = True

        # Store cell coordinates.
        cfg.cell_coordinates.append(cortabs)
        if 'None' in cfg.table_img_names:
            cfg.table_img_names.remove('None')

        # Save table to the output folder as a csv file, and keep track of the current order of cell IDs in the table.
        startindex = len(cfg.data_list) - cfg.num_imgs
        cfg.current_table_order_full = list(range(len(cfg.data_list[startindex])))
        for i in range(cfg.num_imgs):
            imgname = os.path.splitext(os.path.split(cfg.file_names[i])[-1])[0]
            segmentedtable = pd.DataFrame(np.hstack([np.vstack(cfg.data_list[i + startindex]), cortabs[i]]))
            segmentedtable.columns = np.hstack(
                [cfg.markers, "Area", "Eccentricity", "Perimeter", "Major Axis", "y", "x"])
            segmentedtable.to_csv(os.path.join(outfolder, f"Segmentation_Table_{imgname}.csv"))
            cfg.current_table_orders_filtered.append(list(range(len(cfg.data_list[i + startindex]))))

        # Update any pertinent variables.
        cfg.segmentation_clustering_rounds.append([])
        cfg.update_log_file = False
        cfg.sort_table_widget.data.choices = tuple(cfg.table_img_names)
        cfg.sort_table_widget.data.value = f"(Segment [{cfg.segment_count}]) - {cfg.file_names[0].split('/')[-1]}"
        cfg.sort_table_widget.reset_choices()
        cfg.update_log_file = True
        cfg.segment_count += 1
        cfg.analysis_log.append("Segmentation")
        cfg.object_img_names.append(f"Segment {cfg.segment_count}")
        cfg.analysis_mode = "Segmentation"

        # If this is the first table being generated, set upper and lower bounds consistent with first segmented image.
        if not cfg.has_added_table:
            cfg.lower_bounds_list[cfg.table_index] = copy.deepcopy(cfg.min_vals[0])
            cfg.upper_bounds_list[cfg.table_index] = copy.deepcopy(cfg.max_vals[0])
            self.update_table(cfg.data_list[startindex],
                              cfg.lower_bounds_list[cfg.table_index],
                              cfg.upper_bounds_list[cfg.table_index],
                              len(cfg.data_list[startindex]),
                              list(range(1, 1 + len(cfg.data_list[startindex]))),
                              )

        cfg.viewer.status = "Segmentation complete"

    def biaxial_gate(self,
                     segindex=None,
                     chan1="",
                     chan2="",
                     colorparam="",
                     norm="",
                     colorbygroups=[],
                     colorbyindivclusters=None,
                     colorbycombclusters=None,
                     clusteringindex=None,
                     ):
        """
        Generate a biaxial plot according to cell markers and normalization algorithm defined by the user.

        Args:
            segindex (int, optional): Index of segmentation round to be used for biaxial gating (Default: None).
            chan1 (str, optional): Name of parameter to define the horizontal axis (Default: "").
            chan2 (str, optional): Name of parameter to define the vertical axis (Default: "").
            colorparam (str, optional): Name of parameter to define the color gradient (Default: "").
            norm (str, optional): Normalization algorithm to be used for data preprocessing (Default: "").
            colorbygroups (list, optional): List of group assignment indices to use for coloring biaxial plot(s) (Default: []).
            colorbyindivclusters (bool, optional): If True, generate a plots for each cluster, with vertex colors representing membership of the respective cluster. Otherwise, do nothing (Default: None).
            colorbycombclusters (bool, optional): If True, generate a plot with vertices colored according to cluster assignment. Otherwise, do nothing (Default: None).
            clusteringindex (int, optional): Index of the round of clustering to be used for color assignment, if applicable (Default: None).
        """
        params = cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        # User must first run object-based segmentation in order to generate a Biaxial Plot.
        if cfg.segment_count == 0:
            utils.display_error_message("You must segment before running biaxial gating",
                                        "Biaxial gating cannot be done until the image has been segmented")
            return

        # Prompt user to select which cell markers to use as parameters for the plot and vertex coloring.
        if any(param is None for param in (segindex, colorbyindivclusters, colorbycombclusters)) or any(
                param == "" for param in (norm, chan1, chan2, colorparam)):
            biaxial = utils.BiaxialGate()
            biaxial.exec()
            if not biaxial.OK:
                return
            segindex = biaxial.segmentationindex
            chan1 = biaxial.chan1
            chan2 = biaxial.chan2
            colorparam = biaxial.color
            norm = biaxial.norm
            colorbygroups = biaxial.colorbygroups
            if len(cfg.segmentation_clustering_rounds[segindex]) > 0:
                colorbyindivclusters = biaxial.colorbyindivclusters
                colorbycombclusters = biaxial.colorbycombclusters

        cfg.plot_segmentation_indices.append(segindex * cfg.num_imgs)

        # Compile quantified cells from each individual image into one combined data array.
        numcells = 0
        for i in range(cfg.num_imgs):
            numcells += len(cfg.data_list[cfg.segmentation_indices[segindex * cfg.num_imgs + i]])
        fullquantified = np.zeros((numcells, cfg.data_list[cfg.segmentation_indices[segindex * cfg.num_imgs]].shape[1]))
        count = 0
        cellsperimage = []
        for i in range(cfg.num_imgs):
            cellsincurrimg = []
            index1 = params.index(chan1) + 1
            index2 = params.index(chan2) + 1
            currentimage = cfg.data_list[cfg.segmentation_indices[segindex * cfg.num_imgs + i]]
            for j in range(count, count + len(currentimage)):
                cellsincurrimg.append(j)
            fullquantified[count:count + len(currentimage), :] = currentimage
            count += len(currentimage)
            cellsperimage.append(cellsincurrimg)

        # Remove rows with NaN values from the data array
        removerows = np.unique(np.argwhere(np.isnan(fullquantified[:, [index2, index1]]))[:, 0])
        fullquantified = np.delete(fullquantified, removerows, axis=0)
        for i in range(cfg.num_imgs):
            for cellnum in removerows:
                if cellnum in cellsperimage[i]:
                    cellsperimage[i].remove(cellnum)

        # Color data points on a red-blue gradient according to expression of a defined cell marker, if applicable.
        name = ""
        cols = np.zeros((len(fullquantified), 3)).astype(np.float)
        if colorparam != '---(Optional)---':
            colorindex = params.index(colorparam) + 1
            max = np.percentile(fullquantified[:, colorindex], 97)
            min = np.min(fullquantified[:, colorindex])
            for i in range(len(fullquantified)):
                cols[i, 0] = (fullquantified[i, colorindex] - min) / (max - min)
                cols[i, 2] = 1.0 - (fullquantified[i, colorindex] - min) / (max - min)
            cols[cols > 1.0] = 1.0
            cols[cols < 0.0] = 0.0
            name = f" ({colorparam})"
        cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)

        # Perform any necessary normalization and define vertices that will be plotted on the biaxial scatterplot
        x = fullquantified[:, index1]
        y = fullquantified[:, index2]
        if norm == "Log10":
            x = np.log10(x * 9.0 + 1.0)
            y = np.log10(y * 9.0 + 1.0)
        elif norm == "Log2":
            x = np.log2(x + 1.0)
            y = np.log2(y + 1.0)
        x = np.append(x, [-0.05 * np.max(x), 1.05 * np.max(x)])
        y = np.append(y, [-0.05 * np.max(y), 1.05 * np.max(y)])

        # Use resulting points to generate a scatterplot and add it to the viewer.
        plt.figure(figsize=(10, 10))
        plt.scatter(x, y, s=1, c=cols)
        plt.show(block=False)
        plt.title(f"Biaxial Gate{name}")
        plt.xlabel(str(chan1))
        plt.ylabel(str(chan2))
        outfolder = utils.create_new_folder("Biaxial_",
                                            cfg.output_folder,
                                            )
        plt.savefig(os.path.join(outfolder, "Biaxial.png"), format="PNG", dpi=300)
        im = imread(os.path.join(outfolder, "Biaxial.png"))
        im = np.asarray(im)
        im[:, :, [0, 2]] = im[:, :, [2, 0]]
        locs = np.where((im[:, :, 0] == 242) & (im[:, :, 1] == 255) & (im[:, :, 2] == 242))
        cfg.plot_x_mins.append(np.min(locs[0]))
        cfg.plot_x_maxs.append(np.max(locs[0]))
        cfg.plot_y_mins.append(np.min(locs[1]))
        cfg.plot_y_maxs.append(np.max(locs[1]))
        self.set_invisible(cfg.viewer)
        cfg.viewer.add_image(im,
                             name=f"Biaxial {cfg.biaxial_count} ({chan1} vs. {chan2})",
                             blending="additive",
                             )

        # If given segmented image iteration has been clustered, check if the user elected to use clustering as
        # a basis for vertex coloring.
        if len(cfg.segmentation_clustering_rounds[segindex]) > 0:
            # If the user is coloring according to cluster assignment, prompt to define which clustering
            # iteration is being used.
            if colorbyindivclusters or colorbycombclusters:
                if len(cfg.segmentation_clustering_rounds[segindex]) > 1:
                    if clusteringindex is None:
                        iteration = utils.ObjectClusterIteration(cfg.segmentation_clustering_rounds[segindex])
                        iteration.exec()
                        if not iteration.OK:
                            return
                        clusteringindex = iteration.iteration

                    startindex = cfg.segmentation_clustering_rounds[segindex][clusteringindex]
                else:
                    startindex = cfg.segmentation_clustering_rounds[segindex][0]
                clusternums = []
                for i in range(cfg.num_imgs):
                    curclusternums = cfg.cell_cluster_vals[startindex * cfg.num_imgs + i]
                    for n in curclusternums:
                        clusternums.append(n - 1)
                analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][startindex] * cfg.num_imgs
                labelimg = self.concat_label_imgs(
                    [cfg.labeled_imgs[ind] for ind in range(analysisnum, analysisnum + cfg.num_imgs)])
                numclusters = len(np.unique(labelimg)) - 1

            # If selected by user, add an additional stack of scatterplots with vertices colored red if
            # corresponding to a cell in the respective cluster, or blue otherwise.
            if colorbyindivclusters:
                self.set_invisible(cfg.viewer)
                pathlist = []
                for i in range(numclusters):
                    plt.figure(figsize=(10, 10))
                    col = np.zeros((len(fullquantified), 3)).astype(np.float)
                    for j in range(len(fullquantified)):
                        if int(clusternums[j]) == i:
                            col[j, 0] = 1.0
                            col[j, 2] = 0.0
                        else:
                            col[j, 0] = 0.0
                            col[j, 2] = 1.0
                    col = np.append(col, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                    plt.scatter(x, y, s=1, c=col, marker='.')
                    ax = plt.gca()
                    plt.title(f"Cluster {i + 1}")
                    plt.xlabel(chan1)
                    plt.ylabel(chan2)
                    plt.savefig(os.path.join(outfolder, f"Biaxial_Cluster{i + 1}.png"), format="PNG", dpi=300)
                    pathlist.append(os.path.join(outfolder, f"Biaxial_Cluster{i + 1}.png"))
                imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
                cfg.viewer.add_image(imx,
                                     name=f"Biaxial {cfg.biaxial_count} ({chan1} vs. {chan2}) (Individual Clusters)",
                                     blending="additive")

            # If selected by user, add an additional scatterplot colored according to cluster assignment.
            if colorbycombclusters:
                self.set_invisible(cfg.viewer)
                col_list = generate_colormap(numclusters + 1)
                cols = np.zeros((len(fullquantified), 3)).astype(np.float)
                for i in range(len(fullquantified)):
                    cols[i, :] = col_list[int(clusternums[i]), :] / np.array([255.0, 255.0, 255.0])
                plt.figure(figsize=(10, 10))
                cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                plt.scatter(x, y, s=1, c=cols, marker='.')
                ax = plt.gca()
                plt.title("Clusters")
                plt.xlabel(chan1)
                plt.ylabel(chan2)
                filename = os.path.join(outfolder, "BiaxialClusters.png")
                plt.savefig(filename, format="PNG", dpi=300)
                cfg.viewer.add_image(imread(filename, pilmode='RGB'),
                                     name=f"Biaxial {cfg.biaxial_count} ({chan1} vs. {chan2}) (Combined Clusters)",
                                     blending="additive")

        # If selected by user, add an additional scatterplot colored according to group assignment.
        if colorbygroups != []:
            for ind in colorbygroups:
                group = cfg.groups_list[ind + 1]
                imggroupnames = list(group.values())
                shufflelist = [list(group.keys()).index(name) for name in
                               [os.path.split(fn)[-1] for fn in cfg.file_names]]
                nameindices = list(set(imggroupnames))
                numgroups = len(nameindices)
                imagegroups = []
                for i in range(cfg.num_imgs):
                    imagegroups.append(nameindices.index(imggroupnames[i]))
                imagegroups = [imagegroups[i] for i in shufflelist]
                self.set_invisible(cfg.viewer)
                col_list = generate_colormap(numgroups + 1)
                cols = np.zeros((len(fullquantified), 3)).astype(np.float)
                count = 0
                for i in range(cfg.num_imgs):
                    for j in range(count, count + len(cellsperimage[i])):
                        cols[j, :] = col_list[imagegroups[i], :] / np.array([255.0, 255.0, 255.0])
                    count += len(cellsperimage[i])
                plt.figure(figsize=(10, 10))
                cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                plt.scatter(x, y, s=1, c=cols, marker='.')
                ax = plt.gca()
                plt.title(f"{chan1} vs. {chan2} ({cfg.groups_names[ind + 1]})")
                plt.xlabel(chan1)
                plt.ylabel(chan2)
                filename = os.path.join(outfolder, f"BiaxialGroups_{cfg.groups_names[ind + 1]}.png")
                plt.savefig(filename, format="PNG", dpi=300)
                cfg.viewer.add_image(imread(filename, pilmode='RGB'),
                                     name=f"Biaxial {cfg.biaxial_count} ({chan1} vs. {chan2}) ({cfg.groups_names[ind + 1]})",
                                     blending="additive")

        # Keep track of coordinates on Biaxial plot, and update variables.
        coordslist = []
        coords = np.hstack((np.expand_dims(x / np.max(x), 1), np.expand_dims(y / np.max(y), 1)))
        count = 0
        for i in range(cfg.num_imgs):
            numcells = len(cfg.data_list[cfg.segmentation_indices[segindex * cfg.num_imgs + i]])
            coordslist.append(coords[count:count + numcells].astype(np.float))
            count += numcells
        cfg.plot_coordinates.append(coordslist)
        cfg.plot_is_umap.append(False)
        cfg.biaxial_count += 1
        utils.log_actions(f"gui.biaxial_gate(segindex={segindex}, chan1=\"{chan1}\", chan2=\"{chan2}\", "
                          f"colorparam=\"{colorparam}\", norm=\"{norm}\", colorbygroups={colorbygroups}, "
                          f"colorbyindivclusters={colorbyindivclusters}, colorbycombclusters={colorbycombclusters}, "
                          f"clusteringindex={clusteringindex})")

    def calculate_table_cell_color(self,
                                   analysismode,
                                   ):
        color = QColor(0, 0, 0)
        if analysismode == "Segment":
            return
        elif analysismode == "Pixel":
            return
        elif analysismode == "Object":
            return
        return color

    def change_folder_gui(self):
        self.change_folder()

    def change_folder(self,
                      output_folder="",
                      ):
        """
        Change the root directory path where results from the GUI will be saved.
        """
        if output_folder == "":
            dialog = QFileDialog()
            output_folder = dialog.getExistingDirectory(None, "Select Output Folder")

        if output_folder != "":
            utils.log_actions(f"gui.change_folder(output_folder=\"{output_folder}\")")
            output_folder = utils.create_new_folder("RAPID_GUI", output_folder)
            os.rename(cfg.output_folder, output_folder)
            cfg.action_logger_path = cfg.action_logger_path.replace(cfg.output_folder, output_folder)
            cfg.edit_img_path = cfg.edit_img_path.replace(cfg.output_folder, output_folder)
            cfg.merge_img_paths = [path.replace(cfg.output_folder, output_folder) for path in
                                   cfg.merge_img_paths]
            cfg.object_cluster_directories = [path.replace(cfg.output_folder, output_folder) for path in
                                              cfg.object_cluster_directories]
            cfg.pixel_cluster_directories = [path.replace(cfg.output_folder, output_folder) for path in
                                             cfg.pixel_cluster_directories]
            cfg.segmentation_zarr_paths = [path.replace(cfg.output_folder, output_folder) for path in
                                           cfg.segmentation_zarr_paths]
            cfg.output_folder = output_folder
        return

    def colormap_group_gui(self):
        self.colormap_group()

    def colormap_group(self,
                       newcolorlist=[],
                       ):
        """
        Load preset colormap options from a csv file to allow the user to assign custom colors to each cluster.

        Args:
            newcolorlist (optional, list): List of colors for each cluster in the current table (Default: []).
        """
        if cfg.analysis_mode == "Segmentation":
            utils.display_error_message("Must be displaying clustered image",
                                        "Please ensure that the currently selected table corresponds to clustering results.")

        ind = cfg.analysis_index
        if cfg.num_imgs > 1:
            ind = int(cfg.analysis_index / (cfg.num_imgs + 1))

        if cfg.analysis_mode == "Pixel":
            analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Pixel"][ind] * cfg.num_imgs
        else:
            analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][ind] * cfg.num_imgs
        labelimg = self.concat_label_imgs(
            [cfg.labeled_imgs[ind] for ind in range(analysisnum, analysisnum + cfg.num_imgs)])
        nc = len(np.unique(labelimg)[np.unique(labelimg) > 0])

        if newcolorlist == []:
            if nc < 57:
                colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color56.csv"
            elif 56 < nc < 142:
                colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color141.csv"
            else:
                colorcsvpath = os.path.dirname(os.path.abspath(__file__)) + "/../util/color282.csv"
            colordf = pd.read_csv(colorcsvpath, 
                                  index_col=0,
                                  )

            cmapwidget = utils.ColorAssign(nc, 
                                           colordf, 
                                           cfg.viewer,
                                           )
            cmapwidget.exec()
            if not cmapwidget.OK:
                return
            newcolorlist = cmapwidget.newcolorlist.tolist()

        if cfg.analysis_mode == "Pixel":
            cfg.pixel_cluster_colors[ind] = np.array(newcolorlist)
            data = cfg.data_list[cfg.table_index]
            index = [f"RP-{i + 1}" for i in range(nc)]
            cols = cfg.full_tab.columns[3:]
        else:
            cfg.object_cluster_colors[ind] = np.array(newcolorlist)
            data = cfg.data_list[cfg.table_index][:, 1:-4]
            index = [f"RO-{i + 1}" for i in range(nc)]
            cols = cfg.full_tab.columns[3:-4]

        scaler = MinMaxScaler()
        scaler.fit(data)
        my_data_scaled = scaler.transform(data).T

        # Cutoff the overflowing values
        my_data_scaled[my_data_scaled > 1] = 1
        my_data_scaled = pd.DataFrame(my_data_scaled)
        my_data_scaled.columns = index

        # Get the selected markers
        my_data_scaled.index = cols.values
        minhight = 4
        minwidth = 6
        ClusterDend = sns.clustermap(my_data_scaled + 0.001, col_cluster=True, linewidth=1, metric='cosine',
                                     cmap="vlag",
                                     row_cluster=True, yticklabels=True, xticklabels=True, vmin=0, vmax=1, cbar=False,
                                     figsize=(int(max(minhight, my_data_scaled.shape[1] * 0.8)),
                                              int(max(minwidth, len(my_data_scaled) * 0.4))),
                                     linecolor='#799579')
        ClusterDend.ax_row_dendrogram.set_visible(False)
        ClusterDend.ax_col_dendrogram.set_visible(False)
        ClusterDend.cax.set_visible(False)
        for tick_label in ClusterDend.ax_heatmap.axes.get_xticklabels():
            if cfg.analysis_mode == "Pixel":
                tick_text = tick_label.get_text().replace(r"RP-", "")
                tick_label.set_color(cfg.pixel_cluster_colors[ind][int(tick_text) - 1, :] / 255)
                if cfg.pixel_cluster_colors[ind][int(tick_text) - 1, 0] == 255 and cfg.pixel_cluster_colors[ind][
                    int(tick_text) - 1, 1] == 255 and cfg.pixel_cluster_colors[ind][int(tick_text) - 1, 2] == 255:
                    tick_label.set_color("black")
            else:
                tick_text = tick_label.get_text().replace(r"RO-", "")
                tick_label.set_color(cfg.object_cluster_colors[ind][int(tick_text) - 1, :] / 255)
                if cfg.object_cluster_colors[ind][int(tick_text) - 1, 0] == 255 and cfg.object_cluster_colors[ind][
                    int(tick_text) - 1, 1] == 255 and cfg.object_cluster_colors[ind][int(tick_text) - 1, 2] == 255:
                    tick_label.set_color("black")

        if cfg.analysis_mode == "Pixel":
            plt.savefig(os.path.join(cfg.pixel_cluster_directories[ind], "ClusterHeatmap.png"), dpi=300)
            np.save(os.path.join(cfg.pixel_cluster_directories[ind], "COLOR.npy"), cfg.pixel_cluster_colors[ind])
        else:
            plt.savefig(os.path.join(cfg.object_cluster_directories[ind], "ClusterHeatmap.png"), dpi=300)
            np.save(os.path.join(cfg.object_cluster_directories[ind], "COLOR.npy"), cfg.object_cluster_colors[ind])

        utils.log_actions(f"gui.colormap_group(newcolorlist={newcolorlist})")

    def concat_label_imgs(self,
                          imgs,
                          ):
        """
        Combine several image arrays with appropriate padding and/or data type expansion when necessary.

        Args:
            imgs (list): List containing each of the image arrays to be concatenated.

        :return: concatimg *(numpy.ndarray)*: \n
            Image array containing all input image arrays concatenated.
        """
        dtype = np.uint32
        while True:
            for img in imgs:
                if img.dtype == dtype:
                    break
            dtype = np.uint16
            for img in imgs:
                if img.dtype == dtype:
                    break
            dtype = np.uint8
            break
        concatimg = np.zeros((len(imgs), cfg.max_img_shape[0], cfg.max_img_shape[1]), dtype=dtype)
        for i, img in enumerate(imgs):
            concatimg[i, :img.shape[0], :img.shape[1]] = img
        return concatimg

    def count_visible_layers(self):
        """
        Count the number of layers in the main viewer window.

        :return: numvisible *(int)*: \n
            Number of layers in the main viewer window that are currently visible.
        """
        numvisible = 0
        for le in range(len(cfg.viewer.layers)):
            if cfg.viewer.layers[le].visible:
                numvisible += 1
        return numvisible

    def create_shape_path(self,
                          verts,
                          shapetype,
                          ):
        """
        Connect a series of vertices into a shape.

        Args:
            verts (iterable): Coordinates for vertices being connected to form the shape.
            shapetype (str): Shape for the connected series of vertices.

        :return: path *(matplotlib.path.Path)*: \n
            The connected path of the vertices.
        """
        if shapetype != 'ellipse':
            path = Path(verts)
        else:
            centerx = (verts[0][0] + verts[2][0]) / 2
            centery = (verts[0][1] + verts[2][1]) / 2
            height = abs(verts[0][1] - verts[2][1])
            width = abs(verts[0][0] - verts[2][0])
            path = matplotlib.patches.Ellipse((centerx, centery), width, height)
        return path

    def create_table(self,
                     data,
                     ):
        """
        Add the contents of a data table in the table widget within teh RAPID GUI.

        Args:
            data (pandas.DataFrame): Dataset being displayed in the table.
        """
        headerList = []
        for n, key in enumerate(data.keys()):
            headerList.append(key)
        cfg.table_widget = QTableWidget()
        numcols = len(data.keys())
        numrows = len(data[headerList[0]])
        cfg.table_widget.setRowCount(numrows)
        cfg.table_widget.setColumnCount(numcols)
        print(data.keys())
        for j, key in enumerate(data.keys()):
            for i, item in enumerate(data[key]):
                if data[headerList[j]][i] is not None and j == 1 and i >= 3 and not cfg.analysis_mode == "Segmentation":
                    val = int(data[headerList[j]][i])
                elif data[headerList[j]][i] is not None:
                    val = round(data[headerList[j]][i], 3)
                else:
                    val = data[headerList[j]][i]
                if math.isnan(val):
                    val = ""
                newitem = QTableWidgetItem(str(val))
                if i == 0:
                    if j == 0:
                        newitem = QTableWidgetItem("≥")
                elif i == 1:
                    if j == 0:
                        newitem = QTableWidgetItem("≤")
                elif j == 0 and i == 2:
                    newitem = QTableWidgetItem("")
                elif i == 2 and j == 1 and not (cfg.analysis_mode == "Segmentation"):
                    newitem = QTableWidgetItem("")
                    newitem.setBackground(QColor(0, 0, 0))
                elif i == 2 or j == 0:
                    newitem = QTableWidgetItem("")
                    if key not in ["Area", "Eccentricity", "Perimeter", "Major Axis"]:
                        newitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        newitem.setCheckState(QtCore.Qt.Unchecked)
                elif j == 1 and not (cfg.analysis_mode == "Segmentation"):
                    newitem.setBackground(QColor(0, 0, 0))
                else:
                    if cfg.analysis_mode == "Object" and numrows > 4:
                        minv = cfg.min_vals[cfg.table_index][j - 2]
                        maxv = cfg.max_vals[cfg.table_index][j - 2]
                        clusterindex, numtabs = utils.find_analysis_round()
                        tabnum = cfg.analysis_index % numtabs
                        for k in range(len(cfg.segmentation_clustering_rounds)):
                            l = cfg.segmentation_clustering_rounds[k]
                            if clusterindex in l:
                                segmentindex = k * cfg.num_imgs
                        if tabnum == cfg.num_imgs:
                            maxsegment = []
                            for k in range(cfg.num_imgs):
                                maxsegment.append(np.array(cfg.max_vals[cfg.segmentation_indices[segmentindex + k]]))
                            maxsegment = np.vstack(maxsegment)
                            maxsegment = list(np.amax(maxsegment, axis=0))
                        else:
                            maxsegment = cfg.max_vals[cfg.segmentation_indices[segmentindex + tabnum]]
                        adj = (data[key][i] - minv) / (maxv - minv) * maxsegment[j - 2] / np.max(
                            np.asarray(maxsegment[:-4]))
                    elif cfg.analysis_mode == "Segmentation" and numrows > 4:
                        minv = cfg.min_vals[cfg.table_index][j - 1]
                        maxv = cfg.max_vals[cfg.table_index][j - 1]
                        adj = (data[key][i] - minv) / (maxv - minv)
                    elif cfg.analysis_mode == "Pixel":
                        minv = cfg.min_vals[cfg.table_index][j - 2]
                        maxv = cfg.max_vals[cfg.table_index][j - 2]
                        clusterindex, _ = utils.find_analysis_round()
                        adj = ((data[key][i] - minv) / (maxv - minv) * cfg.max_pixel_clustervals[clusterindex][
                            j - 2]) / 255
                    else:
                        adj = 0.5
                    if math.isnan(adj):
                        adj = 0.5
                    if adj > 1.0:
                        adj = 1.0
                    if adj < 0.0:
                        adj = 0.0
                    newitem.setBackground(QColor(int(adj * 255), 0, int(255 - adj * 255)))
                if i < 3 or j == 0:
                    newitem.setBackground(QColor(0, 0, 0))
                newitem.setTextAlignment(Qt.AlignHCenter)
                font = QFont("Helvetica", pointSize=12, weight=QFont.Bold)
                newitem.setFont(font)
                newitem.setTextAlignment(Qt.AlignCenter)
                cfg.table_widget.setItem(i, j, newitem)
        cfg.table_widget.cellChanged.connect(self.toggle_checkbox)
        cfg.table_widget.setHorizontalHeaderLabels(headerList)
        cfg.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        cfg.table_widget.resizeColumnsToContents()
        cfg.table_widget.resizeRowsToContents()
        style = "::section {""background-color: black; background-position: bottom center; }"
        cfg.table_widget.horizontalHeader().setStyleSheet(style)
        cfg.table_widget.verticalHeader().setStyleSheet(style)
        cfg.table_widget.setMaximumHeight(cfg.table_widget.rowHeight(3) * 14)

    def display_selected_cells(self,
                               plotindex=None,
                               shapetypes=[],
                               vertslist=[],
                               ):
        """
        Mask the image according to the cells within user-defined shapes overlaid on a Biaxial or UMAP plot.

        Args:
            plotindex (int, optional): Index of the plot of vertices being selected from (Default: None).
            shapetypes (list, optional): List of geometries for each shape drawn by the user (Default: []).
            vertslist (list, optional): List of vertices for each shape drawn by the user (Default: []).
        """
        # https://stackoverflow.com/questions/21339448/how-to-get-list-of-points-inside-a-polygon-in-python
        # Can only use display selected for UMAP or Biaxial gating.
        if cfg.biaxial_count == 1 and cfg.umap_count == 1:
            utils.display_error_message("No UMAP or biaxial gate output detected",
                                        "You must first generate a UMAP or biaxial-gate plot in order to select cells to be displayed")
            return

        # Select which plot is being used.
        if plotindex is None:
            plotindex = 0
            if len(cfg.plot_is_umap) > 1:
                selectplot = utils.BiaxialUMAPIterations(cfg.plot_is_umap)
                selectplot.exec()
                if not selectplot.OK:
                    return
                plotindex = selectplot.iteration
        numcells = cfg.total_num_cells[int(cfg.plot_segmentation_indices[plotindex] / cfg.num_imgs)]
        cfg.viewer.status = "Displaying selected cells"

        if shapetypes == [] or vertslist == []:
            # Find the most recent shapes layer to define which vertices to use to define the shapes.
            ind = -1
            for i in reversed(range(len(cfg.viewer.layers))):
                if isinstance(cfg.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and cfg.viewer.layers[
                    i].visible:
                    ind = i
                    break
            # If no shapes have been drawn, prompt user to first draw a shape.
            if ind == -1:
                utils.display_error_message("Please draw a shape in the viewer first",
                                            "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
                return

            shapetypes = [cfg.viewer.layers[ind].shape_type[i] for i in range(len(cfg.viewer.layers[ind].data))]
            vertslist = [cfg.viewer.layers[ind].data[i] for i in range(len(cfg.viewer.layers[ind].data))]
            cfg.viewer.layers.pop(ind)
        else:
            vertslist = [np.array(verts) for verts in vertslist]

        # Define the colors of each of the shapes, which will be coordinated with the selected cells.
        if len(shapetypes) == 1:
            cols = [np.array([1, 0, 0])]
        elif len(shapetypes) == 2:
            cols = [np.array([1, 0, 0]), np.array([0, 1, 1])]
        elif len(shapetypes) == 3:
            cols = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
        else:
            cols = generate_colormap(len(shapetypes) + 1) / 255.0
            cols = [cols[i] for i in range(len(cols) - 1)]

        # Update the shapes layer with shapes colored consistently with the displayed images.
        cfg.viewer.add_shapes(vertslist, shape_type=shapetypes, edge_width=0, edge_color=cols, face_color=cols,
                              name="Selected Regions")
        self.set_invisible(cfg.viewer)

        shapeverts = []
        for verts in vertslist:
            # Find the vertices of the shapes relative to the scale of the plot, and the vertices within each shape.
            verts = copy.deepcopy(verts[:, -2:])
            verts[:, 0] = ((cfg.plot_x_maxs[plotindex] - verts[:, 0]) / (
                    cfg.plot_x_maxs[plotindex] - cfg.plot_x_mins[plotindex])) * 1.1 - 0.05
            verts[:, 1] = ((verts[:, 1] - cfg.plot_y_mins[plotindex]) / (
                    cfg.plot_y_maxs[plotindex] - cfg.plot_y_mins[plotindex])) * 1.1 - 0.05
            verts[:, [0, 1]] = verts[:, [1, 0]]
            shapeverts.append([tuple(x) for x in verts.tolist()])

        # Keep track of masked images and percentages of cells that are selected in each shape.
        masklist = []
        percents = []
        segindex = cfg.plot_segmentation_indices[plotindex]
        analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Segmentation"][segindex // cfg.num_imgs]
        for shape in range(len(shapeverts)):
            p = self.create_shape_path(shapeverts[shape],
                                       shapetypes[shape],
                                       )

            # Keep track of quantified cell marker expression for each selected cell.
            inclrows = []

            # Mask each image to filter out cells that aren't selected.
            masks = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]))

            # Keep track of the total number of cells and number of selected cells to calculate percentages.
            selectedcells = 0
            for i in range(cfg.num_imgs):
                # Add the number of total and selected cells in the image.
                rows = list(p.contains_points(cfg.plot_coordinates[plotindex][i]))
                rows = [j for j, b in enumerate(rows) if b]
                inclrows.append(rows)
                selectedcells += len(rows)

                # Mask the image for the selected cells.
                labelimg = copy.deepcopy(cfg.labeled_imgs[analysisnum * cfg.num_imgs + i])
                labelimg[np.isin(labelimg, [r + 1 for r in rows], invert=True)] = 0
                labelimg = self.method_searchsort(np.unique(labelimg),
                                                  np.array([j for j in range(len(np.unique(labelimg)))]),
                                                  labelimg,
                                                  )
                cfg.labeled_imgs.append(utils.convert_dtype(labelimg))
                masks[i, :len(labelimg), :labelimg.shape[1]][labelimg > 0] = 1

            # Make sure there is at least one cell selected.
            if selectedcells == 0:
                utils.display_error_message("No cells selected",
                                            "Make sure there is at lease one cell within the bounds of your shape")
                return

            else:
                # Keep track of the masked image to add to the viewer later.
                masklist.append(masks)

                # Keep track of min/max vals for each marker for the table for each image, as well as the
                # coordinates for each selected cell.
                mins = []
                maxs = []
                cortabs = []
                cfg.current_table_order_full = inclrows[0]
                for i in range(cfg.num_imgs):
                    # Re-index the selected cells and create a new table entry.
                    newentry = cfg.data_list[cfg.segmentation_indices[segindex + i]][inclrows[i], :]
                    cfg.data_list.append(newentry)
                    cfg.current_table_orders_filtered.append(list(range(len(newentry))))

                    # Find the coordinates of only the selected cells.
                    cortabs.append([cfg.cell_coordinates[int(segindex / cfg.num_imgs)][i][j] for j in inclrows[i]])

                    # Find the min/max vals for each marker for the table for the current image.
                    minvals = []
                    maxvals = []
                    for j in range(cfg.data_list[cfg.segmentation_indices[segindex + i]].shape[1]):
                        try:
                            minvals.append(
                                np.min(cfg.data_list[cfg.segmentation_indices[segindex + i]][inclrows[i], j]))
                            maxvals.append(
                                np.max(cfg.data_list[cfg.segmentation_indices[segindex + i]][inclrows[i], j]))
                        except:
                            minvals.append(0)
                            maxvals.append(0)
                    mins.append(copy.deepcopy(minvals))
                    maxs.append(copy.deepcopy(maxvals))

                    # Keep track of the orders of the cells and default to no cells being selected in the table.
                    cfg.currently_selected.append([])

                # Keep track of the coordinates for each selected cell and the min/max values for each marker
                # for each cell in each image.
                cfg.cell_coordinates.append(cortabs)
                minvals = []
                maxvals = []
                for i in range(len(mins[0])):
                    minvals.append(min([l[i] for l in mins]))
                    maxvals.append(max([l[i] for l in maxs]))
                for i in range(cfg.num_imgs):
                    cfg.min_vals.append(copy.deepcopy(minvals))
                    cfg.max_vals.append(copy.deepcopy(maxvals))
                    cfg.lower_bounds_list.append(copy.deepcopy(minvals))
                    cfg.upper_bounds_list.append(copy.deepcopy(maxvals))

                # Keep track of the percentages of cells selected for each image.
                percent = round(float(selectedcells * 100 / numcells), 2)
                percents.append(copy.deepcopy(percent))

                # Update the dropdown options for the sort table widget.
                for i in range(len(inclrows)):
                    imgname = f"Selected{cfg.display_selected_count}-{i + 1} ({percent}%)"
                    cfg.table_img_names.append(f"{imgname} - {cfg.table_img_names[cfg.segmentation_indices[i]]}")
                    cfg.segmentation_indices.append(cfg.table_count)
                    cfg.table_count += 1
                cfg.analysis_log.append("Segmentation")
                cfg.total_num_cells.append(numcells)

        # Add the selected cells from each image to the viewer.
        for i in range(len(masklist)):
            cmap = Colormap(ColorArray([(0, 0, 0), cols[i]]))
            imgname = f"Selected{cfg.display_selected_count}-{i + 1} ({percents[i]}%)"
            cfg.viewer.add_image(masklist[i], name=imgname, blending="additive", colormap=cmap)
            cfg.object_img_names.append(imgname)
            cfg.segmentation_clustering_rounds.append([])
        cfg.update_log_file = False
        cfg.sort_table_widget.data.choices = tuple(cfg.table_img_names)
        cfg.sort_table_widget.data.value = f"Selected{cfg.display_selected_count}-1 ({percents[0]}%) - {cfg.table_img_names[cfg.segmentation_indices[0]]}"
        cfg.display_selected_count += 1
        cfg.sort_table_widget.reset_choices()
        cfg.update_log_file = True
        utils.log_actions(f"gui.display_selected_cells(plotindex={plotindex}, shapetypes={shapetypes}, "
                          f"vertslist={[verts.tolist() for verts in vertslist]})")

    def draw_shapes(self,
                    data,
                    shape_type,
                    properties,
                    name,
                    text,
                    face_color,
                    ):
        properties = {'class': np.array(properties), }
        text_properties = {'text': '{class}', 'anchor': 'center', 'size': text[0], 'color': np.array(text[1]), }
        cfg.viewer.add_shapes(data=np.array(data), shape_type=shape_type, edge_width=0, properties=properties,
                              name=name, text=text_properties, face_color=np.array(face_color))

    def edit_image(self,
                   editactions=[],
                   ):
        """
        Open a new popup napari window to allow the user to edit each image and change the raw data.

        Args:
            editactions (list, optional):  (Default: [])
        """
        # Prompt user to decide whether to edit all images, or to apply edits from one image to all others.
        if editactions != []:
            self.apply_edits(editactions)
            cfg.edit_actions += editactions
            utils.log_actions(f"gui.edit_image(editactions={editactions})")
            return

        editoptions = utils.EditOptions()
        editoptions.exec()
        if not editoptions.OK:
            return
        allimgs = editoptions.allimages
        loadedits = editoptions.loadedits

        # Load previous edits if selected by the user
        if loadedits:
            editactions = []
            path = QFileDialog().getOpenFileName(filter="*editlog.txt")[0]
            if path == "":
                return
            with open(path, 'r') as file:
                for line in file:
                    edit = line[:-1]
                    editactions.append(ast.literal_eval(edit))
            if not len(editactions[0]) == cfg.num_imgs:
                if len(editactions[0]) == 1:
                    editactions = [action * cfg.num_imgs for action in editactions]
                else:
                    utils.display_error_message("Incompatible number of images",
                                                "Please ensure you are using the same number of images that you used for the edits being loaded")
                    return
            if not len(editactions[0][0]) == cfg.num_markers:
                utils.display_error_message("Incompatible number of cell markers",
                                            "Please ensure you are using the same number of cell markers that you used for the edits being loaded")
                return
            self.apply_edits(editactions)
            cfg.edit_actions += editactions
            utils.log_actions(f"gui.edit_image(editactions={editactions})")
            return

        # Prompt user to select which image will be used, if only using one.
        if not allimgs:
            selectimg = utils.SelectImgDropdown()
            selectimg.exec()
            if not selectimg.OK:
                return
            imgindex = selectimg.imgindex
        else:
            imgindex = 0

        # Create a new viewer window where images will be added for editing.
        cfg.edit_viewer = napari.Viewer()
        names = []
        for i in range(len(cfg.file_names)):
            names.append(cfg.file_names[i].split("/")[-1])
        cfg.edit_viewer_img_id = 0
        editdata = np.zeros((len(cfg.markers), cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]))

        # Keep track of contrast limits for each image and every action taken.
        contrastlimits = []
        editactions = []
        cl = []
        for i in range(len(cfg.markers)):
            cl.append([0, 255])
        for i in range(len(cfg.file_names)):
            contrastlimits.append(copy.deepcopy(cl))

        @magicgui(call_button="Apply Changes")
        def apply_changes_editgui() -> Image:
            # Apply all changes, including any adjusted contrast limits, to the raw images in the main viewer.
            for i in range(len(cfg.markers)):
                editdata[i, cfg.edit_viewer_img_id, :, :] = copy.deepcopy(cfg.edit_viewer.layers[i].data)
                contrastlimits[cfg.edit_viewer_img_id][i] = [cfg.edit_viewer.layers[i].contrast_limits[0],
                                                             cfg.edit_viewer.layers[i].contrast_limits[1]]
                for j in range(cfg.num_imgs):
                    if contrastlimits[j][i] != [0, 255]:
                        editdata[i, j, :, :] = self.apply_contrast_limits(editdata[i, j, :, :],
                                                                          contrastlimits[j][i],
                                                                          )
                cfg.viewer.layers[i].data = editdata[i, :, :, :]
            cfg.edit_actions += editactions
            cfg.edit_actions.append(contrastlimits)

            if not cfg.has_edited_image:
                cfg.edit_img_path = utils.create_new_folder("ImageEdits", cfg.output_folder)
            with open(os.path.join(cfg.edit_img_path, "editlog.txt"), 'w') as file:
                for item in cfg.edit_actions:
                    file.write("%s\n" % item)
            utils.log_actions(f"gui.edit_image(editactions={editactions})")
            cfg.edit_viewer.window.qt_viewer.close()
            cfg.edit_viewer.window._qt_window.close()

        @magicgui(call_button="Apply Changes")
        def apply_changes_one_editgui() -> Image:
            self.apply_edits(editactions,
                             imgindex,
                             )

            # Apply all changes, including any adjusted contrast limits, to the raw images in the main viewer.
            contrastlimits = []
            for i in range(len(cfg.markers)):
                editdata[i, cfg.edit_viewer_img_id, :, :] = copy.deepcopy(cfg.edit_viewer.layers[i].data)
                contrastlimits.append(
                    [cfg.edit_viewer.layers[i].contrast_limits[0], cfg.edit_viewer.layers[i].contrast_limits[1]])
                cfg.viewer.layers[i].data = self.apply_contrast_limits(cfg.viewer.layers[i].data,
                                                                       contrastlimits[i],
                                                                       )
            cfg.edit_actions += editactions
            for i in range(cfg.num_imgs - 1):
                contrastlimits.append(contrastlimits[0])
            cfg.edit_actions.append(contrastlimits)

            if not cfg.has_edited_image:
                cfg.edit_img_path = utils.create_new_folder("ImageEdits", cfg.output_folder)
            with open(os.path.join(cfg.edit_img_path, "editlog.txt"), 'w') as file:
                for item in cfg.edit_actions:
                    file.write("%s\n" % item)

            utils.log_actions(f"gui.edit_image(editactions={editactions})")
            cfg.edit_viewer.window.qt_viewer.close()
            cfg.edit_viewer.window._qt_window.close()

        @magicgui(call_button="Binarize")
        def binarize_image_editgui() -> Image:
            # Apply a denoising algorithm to binarize any or all of the cell markers in the given image.
            markers = utils.ImageEditingMarkers()
            markers.exec()
            if markers.OK:
                for i in markers.markernums:
                    data = denoise_img(cfg.edit_viewer.layers[i].data)
                    data[data > 0] = 255
                    cfg.edit_viewer.layers[i].data = data

            # Keep track of which marker had a Median filter applied to them for the current image.
            binarizelog = []
            for i in range(cfg.num_markers):
                binarizelog.append([])
            fullbinarizelog = []
            if allimgs:
                for i in range(len(cfg.file_names)):
                    fullbinarizelog.append(copy.deepcopy(binarizelog))
                for i in range(cfg.num_markers):
                    if i in markers.markernums:
                        fullbinarizelog[cfg.edit_viewer_img_id][i] = "Binarize"
            else:
                for i in range(cfg.num_markers):
                    if i in markers.markernums:
                        binarizelog[i] = "Binarize"
                for i in range(len(cfg.file_names)):
                    fullbinarizelog.append(copy.deepcopy(binarizelog))
            editactions.append(fullbinarizelog)
            print(editactions)

        @magicgui(auto_call=True, image={"choices": names, "label": ""})
        def change_image_editgui(image: str):
            # Because only one image is shown at once, allow user to switch between images.
            for i in range(len(cfg.edit_viewer.layers)):
                editdata[i, cfg.edit_viewer_img_id, :, :] = copy.deepcopy(cfg.edit_viewer.layers[i].data)
                contrastlimits[cfg.edit_viewer_img_id][i] = cfg.edit_viewer.layers[i].contrast_limits
            cfg.edit_viewer_img_id = names.index(image)
            for i in range(len(cfg.edit_viewer.layers)):
                cfg.edit_viewer.layers[i].contrast_limits = contrastlimits[cfg.edit_viewer_img_id][i]
                cfg.edit_viewer.layers[i].data = editdata[i, cfg.edit_viewer_img_id, :, :]

        @magicgui(call_button="Denoise")
        def denoise_image_editgui() -> Image:
            # Apply a denoising algorithm to any or all of the cell markers in the given image.
            markers = utils.ImageEditingMarkers()
            markers.exec()
            if markers.OK:
                data = np.zeros((len(cfg.edit_viewer.layers[0].data), cfg.edit_viewer.layers[0].data.shape[1],
                                 len(markers.markernums)))
                for i in range(len(markers.markernums)):
                    data[:, :, i] = cfg.edit_viewer.layers[markers.markernums[i]].data
                denoised = denoise_img(data, [j for j in range(len(markers.markernums))])
                for i in range(len(markers.markernums)):
                    cfg.edit_viewer.layers[markers.markernums[i]].data = denoised[:, :, i]

            # Keep track of which marker had a Median filter applied to them for the current image.
            denoiselog = []
            for i in range(cfg.num_markers):
                denoiselog.append([])
            fulldenoiselog = []
            if allimgs:
                for i in range(len(cfg.file_names)):
                    fulldenoiselog.append(copy.deepcopy(denoiselog))
                for i in range(cfg.num_markers):
                    if i in markers.markernums:
                        fulldenoiselog[cfg.edit_viewer_img_id][i] = "Denoise"
            else:
                for i in range(cfg.num_markers):
                    if i in markers.markernums:
                        denoiselog[i] = "Denoise"
                for i in range(len(cfg.file_names)):
                    fulldenoiselog.append(copy.deepcopy(denoiselog))
            editactions.append(fulldenoiselog)
            print(editactions)

        @magicgui(call_button="Gaussian Filter")
        def gaussian_filter_editgui() -> Image:
            # Apply a gaussian filter to any or all of the cell markers in the given image.
            markers = utils.ImageEditingMarkers()
            markers.exec()
            if markers.OK:
                for i in markers.markernums:
                    cfg.edit_viewer.layers[i].data = ndimage.gaussian_filter(cfg.edit_viewer.layers[i].data, [1, 1])

                # Keep track of which marker had a Gaussian filter applied to them for the current image.
                gausslog = []
                for i in range(cfg.num_markers):
                    gausslog.append([])
                fullgausslog = []
                if allimgs:
                    for i in range(len(cfg.file_names)):
                        fullgausslog.append(copy.deepcopy(gausslog))
                    for i in range(cfg.num_markers):
                        if i in markers.markernums:
                            fullgausslog[cfg.edit_viewer_img_id][i] = "Gaussian"
                else:
                    for i in range(cfg.num_markers):
                        if i in markers.markernums:
                            gausslog[i] = "Gaussian"
                    for i in range(len(cfg.file_names)):
                        fullgausslog.append(copy.deepcopy(gausslog))
                editactions.append(fullgausslog)
                print(editactions)

        @magicgui(call_button="Median Filter")
        def median_filter_editgui() -> Image:
            # Apply a median filter to any or all of the cell markers in the given image.
            markers = utils.ImageEditingMarkers()
            markers.exec()
            if markers.OK:
                for i in markers.markernums:
                    cfg.edit_viewer.layers[i].data = ndimage.median_filter(cfg.edit_viewer.layers[i].data, [3, 3])

            # Keep track of which marker had a Median filter applied to them for the current image.
            medlog = []
            for i in range(cfg.num_markers):
                medlog.append([])
            fullmedlog = []
            if allimgs:
                for i in range(len(cfg.file_names)):
                    fullmedlog.append(copy.deepcopy(medlog))
                for i in range(cfg.num_markers):
                    if i in markers.markernums:
                        fullmedlog[cfg.edit_viewer_img_id][i] = "Median"
            else:
                for i in range(cfg.num_markers):
                    if i in markers.markernums:
                        medlog[i] = "Median"
                for i in range(len(cfg.file_names)):
                    fullmedlog.append(copy.deepcopy(medlog))
            editactions.append(fullmedlog)
            print(editactions)

        @magicgui(call_button="Toggle Visibility")
        def toggle_visibility_editgui() -> Image:
            # If any markers are visible, make them invisible. Otherwise, make all markers visible.
            visible = False
            for le in range(len(cfg.edit_viewer.layers)):
                if cfg.edit_viewer.layers[le].visible:
                    visible = True
            if visible:
                for i in range(len(cfg.edit_viewer.layers)):
                    cfg.edit_viewer.layers[i].visible = False
            else:
                for i in range(len(cfg.edit_viewer.layers)):
                    cfg.edit_viewer.layers[i].visible = True

        filterWidget = QWidget()
        filterLayout = QGridLayout()
        filterLayout.setSpacing(0)
        filterLayout.setContentsMargins(0, 0, 0, 0)
        togglevisgui = toggle_visibility_editgui.native
        togglevisgui.setToolTip("Set all layers to visible/invisible")
        filterLayout.addWidget(togglevisgui, 0, 0)
        if cfg.num_imgs > 1 and allimgs:
            changeimagegui = change_image_editgui.native
            changeimagegui.setToolTip("Choose a different image to edit")
            filterLayout.addWidget(changeimagegui, 0, 1)
            reindex = 0
        else:
            reindex = 1
        gaussiangui = gaussian_filter_editgui.native
        gaussiangui.setToolTip("Apply a Gaussian filter to the image")
        filterLayout.addWidget(gaussiangui, 0, 2 - reindex)
        mediangui = median_filter_editgui.native
        mediangui.setToolTip("Apply a Median filter to the image")
        filterLayout.addWidget(mediangui, 0, 3 - reindex)
        denoiseimagegui = denoise_image_editgui.native
        denoiseimagegui.setToolTip("Remove noise from the image")
        filterLayout.addWidget(denoiseimagegui, 0, 4 - reindex)
        binarizeimagegui = binarize_image_editgui.native
        binarizeimagegui.setToolTip("Binarize the image")
        filterLayout.addWidget(binarizeimagegui, 0, 5 - reindex)
        if allimgs:
            applychangesallgui = apply_changes_editgui.native
        else:
            applychangesallgui = apply_changes_one_editgui.native
        applychangesallgui.setToolTip("Apply changes to the raw images")
        filterLayout.addWidget(applychangesallgui, 1, 2 - reindex, 1, 2 + reindex)
        filterWidget.setLayout(filterLayout)
        cfg.edit_viewer.window.add_dock_widget(filterWidget, name="Filter module", area="bottom")

        # Add first image into the viewer at the start.
        for i in range(len(cfg.markers)):
            cfg.edit_viewer.add_image(cfg.viewer.layers[i].data[imgindex, :, :], name=cfg.markers[i],
                                      rgb=False, colormap=cfg.viewer.layers[i].colormap, contrast_limits=[0, 255],
                                      blending="additive")
            editdata[i, :, :, :] = cfg.viewer.layers[i].data

    def filter_table(self,
                     reset=None,
                     bound="",
                     marker="",
                     val=None,
                     ):
        """
        Allow user to set a lower or upper bound for any of the parameters currently displayed in the table. This will
        also be applied to all other images included in the same round of analysis.

        Args:
            reset (bool, optional): If True, reset all filters in the table. Otherwise, set specified filter (Default: None).
            bound (str, optional): "Lower Bound" if defining a lower bound, "Upper Bound" if defining an upper bound (Default: None).
            marker (str, optional): Name of the cell marker being filtered on (Default: None).
            val (float, optional): Value of the bound being set (Default: None).
        """
        # Get all the markers in the currently displayed table, and only use those as options for filtering.
        markers = []
        for i in range(cfg.table_widget.columnCount()):
            if cfg.table_widget.horizontalHeaderItem(i).text() in cfg.markers:
                markers.append(cfg.table_widget.horizontalHeaderItem(i).text())

        # Prompt user to define which markers, whether to set a lower/upper bound, and the value being used.
        if any(param is None for param in (reset, val)) or any(param == "" for param in (bound, marker)):
            tablefilters = utils.TableFilters(markers)
            tablefilters.exec()
            if not tablefilters.OK:
                return
            reset = tablefilters.reset
            bound = tablefilters.bound
            marker = tablefilters.marker
            val = tablefilters.val

        # If resetting the filters, include all the full datasets.
        if reset:
            cfg.current_table_orders_filtered[cfg.table_index] = copy.deepcopy(cfg.current_table_order_full)
            # If the current table corresponds to segmentation.

            if cfg.analysis_mode == "Segmentation":
                # Reset lower/upper bounds and use the full dataset to display in the table.
                cfg.lower_bounds_list[cfg.table_index] = copy.deepcopy(cfg.min_vals[cfg.table_index])
                cfg.upper_bounds_list[cfg.table_index] = copy.deepcopy(cfg.max_vals[cfg.table_index])
                self.update_table(cfg.data_list[cfg.table_index][cfg.current_table_order_full, :],
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(cfg.data_list[cfg.table_index]),
                                  [id + 1 for id in cfg.current_table_orders_filtered[cfg.table_index]],
                                  )

            # If the current table corresponds to object-based clustering.
            elif cfg.analysis_mode == "Object":
                # Reset lower/upper bounds and use the full dataset to display in the table.
                cfg.lower_bounds_list[cfg.table_index] = copy.deepcopy(cfg.min_vals[cfg.table_index])
                cfg.upper_bounds_list[cfg.table_index] = copy.deepcopy(cfg.max_vals[cfg.table_index])
                analysisnum, numtabs = utils.find_analysis_round()
                ind = [i for i, m in enumerate(cfg.clusters_are_pixel_based) if not m][analysisnum]
                self.update_table(cfg.data_list[cfg.table_index][cfg.current_table_order_full, :],
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(cfg.current_table_order_full),
                                  cfg.current_table_order_full,
                                  headernames=cfg.cluster_names[ind],
                                  )

            # If the current table corresponds to pixel-based clustering.
            else:
                # Reset lower/upper bounds and use the full dataset to display in the table.
                cfg.lower_bounds_list[cfg.table_index] = copy.deepcopy(cfg.min_vals[cfg.table_index])
                cfg.upper_bounds_list[cfg.table_index] = copy.deepcopy(cfg.max_vals[cfg.table_index])
                analysisnum, numtabs = utils.find_analysis_round()
                ind = [i for i, m in enumerate(cfg.clusters_are_pixel_based) if m][analysisnum]
                self.update_table(cfg.data_list[cfg.table_index][cfg.current_table_order_full, :],
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(cfg.data_list[cfg.table_index]),
                                  cfg.current_table_order_full,
                                  headernames=cfg.cluster_names[ind],
                                  )

        # If applying a new filter, add to the existing filters and update the table accordingly.
        else:
            # Lower bounds are represented in the first row, while upper bounds are in the second row.
            if bound == "Lower Bound":
                row = 0
            else:
                row = 1

            # Find the column corresponding to the marker being updated.
            for i in range(cfg.table_widget.columnCount()):
                if marker == cfg.table_widget.horizontalHeaderItem(i).text():
                    column = i

            # Change the filter value in the table.
            cfg.table_widget.item(row, column).setText(str(round(val, 3)))

            # Account for the extra column for cell/pixel counts when clustering.
            if cfg.analysis_mode == "Segmentation":
                c = column - 1
            else:
                c = column - 2

            # If user adjusts lower bound, store that for future reference.
            if row == 0 and c >= 0:
                # Lower bound must be smaller than upper bound.
                cfg.lower_bounds_list[cfg.table_index][c] = val
                if cfg.lower_bounds_list[cfg.table_index][c] > cfg.upper_bounds_list[cfg.table_index][c]:
                    cfg.lower_bounds_list[cfg.table_index][c] = cfg.upper_bounds_list[cfg.table_index][c]

            # If user adjusts upper bound, store that for future reference.
            elif row == 1 and c >= 0:
                # Lower bound must be smaller than upper bound.
                cfg.upper_bounds_list[cfg.table_index][c] = val
                if cfg.upper_bounds_list[cfg.table_index][c] < cfg.lower_bounds_list[cfg.table_index][c]:
                    cfg.upper_bounds_list[cfg.table_index][c] = cfg.lower_bounds_list[cfg.table_index][c]

            # If filtering a segmentation table.
            if cfg.analysis_mode == "Segmentation":
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(cfg.lower_bounds_list[cfg.table_index])):
                    if cfg.lower_bounds_list[cfg.table_index][i] > cfg.min_vals[cfg.table_index][i] or \
                            cfg.upper_bounds_list[cfg.table_index][i] < cfg.max_vals[cfg.table_index][i]:
                        filteredmarkers.append(i)

                # Store the segmentation iteration corresponding to the current data table, and the
                # corresponding quantified values.
                currentdata = cfg.data_list[cfg.table_index][cfg.current_table_order_full, :]

                # Store segmentation data table, and append index values at the end to log sort order.
                filtereddata = np.append(cfg.data_list[cfg.table_index][cfg.current_table_order_full, :],
                                         np.expand_dims(np.arange(len(cfg.data_list[cfg.table_index])), 1), 1)

                # Filter cells one marker at a time according to current lower- and upper-bounds.
                for markerid in filteredmarkers:
                    filtermask = (np.round(filtereddata[:, markerid], 3) <= np.round(
                        cfg.upper_bounds_list[cfg.table_index][markerid], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, markerid], 3) >= np.round(
                        cfg.lower_bounds_list[cfg.table_index][markerid], 3))
                    filtereddata = filtereddata[filtermask]

                # Update the list of cell IDs included in the table for each image.
                cfg.current_table_orders_filtered[cfg.table_index] = [cfg.current_table_order_full[j] for j in
                                                                      filtereddata[:, -1].astype(np.int).tolist()]
                currentdata = currentdata[filtereddata[:, -1].astype(np.int).tolist(), :]

                # Update the table with quantified values for the included cells.
                self.update_table(currentdata,
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(cfg.data_list[cfg.table_index]),
                                  [ind + 1 for ind in cfg.current_table_orders_filtered[cfg.table_index]],
                                  )

                # If any cells are included, and at least one cell is filtered out, add an image to the
                # viewer containing the included cells.
                self.set_invisible(cfg.viewer)
                if len(cfg.data_list[cfg.table_index]) > len(currentdata) > 0:
                    for i in range(cfg.num_imgs):
                        if i == cfg.analysis_index % cfg.num_imgs:
                            analysisnum = [j for j, n in enumerate(cfg.analysis_log) if n == "Segmentation"][
                                cfg.analysis_index // cfg.num_imgs]
                            labelimg = cfg.labeled_imgs[analysisnum * cfg.num_imgs + i]
                            filtered = np.in1d(labelimg,
                                               np.asarray(cfg.current_table_orders_filtered[cfg.table_index]) + 1)
                            filtered = filtered.reshape((1, cfg.img_shape_list[i][0], cfg.img_shape_list[i][1]))
                        else:
                            filtered = np.zeros((1, cfg.img_shape_list[cfg.analysis_index % cfg.num_imgs][0],
                                                 cfg.img_shape_list[cfg.analysis_index % cfg.num_imgs][1]),
                                                dtype=np.bool)
                        if i == 0:
                            cfg.viewer.add_image(filtered, name="Filter", blending="additive", visible=True)
                        else:
                            cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, filtered))

                # Un-check cells that are not included in the filter.
                for i in range(len(cfg.data_list[cfg.table_index])):
                    if i in cfg.currently_selected[cfg.table_index] and cfg.current_table_order_full[i] not in \
                            cfg.current_table_orders_filtered[cfg.table_index]:
                        cfg.currently_selected[cfg.analysis_index].remove(i)

            # If filtering an object clustering table.
            elif cfg.analysis_mode == "Object":
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(cfg.lower_bounds_list[cfg.table_index])):
                    if cfg.lower_bounds_list[cfg.table_index][i] > cfg.min_vals[cfg.table_index][i] or \
                            cfg.upper_bounds_list[cfg.table_index][i] < cfg.max_vals[cfg.table_index][i]:
                        filteredmarkers.append(i)

                # Find object clustering data table, and append index values at the end to log sort order.
                cData = np.append(cfg.data_list[cfg.table_index][cfg.current_table_order_full, 1:],
                                  np.expand_dims(np.arange(len(cfg.data_list[cfg.table_index])), 1), 1)

                # Filter the table one marker at a time according to current lower- and upper-bounds.
                for markerid in filteredmarkers:
                    mask = (cData[:, markerid] <= cfg.upper_bounds_list[cfg.table_index][markerid])
                    cData = cData[mask]
                    mask = (cData[:, markerid] >= cfg.lower_bounds_list[cfg.table_index][markerid])
                    cData = cData[mask]

                # Store cluster IDs that will be included in the table, and in the proper order.
                cfg.current_table_orders_filtered[cfg.table_index] = [cfg.current_table_order_full[i] for i in
                                                                      cData[:, -1].astype(np.int).tolist()]

                # Update the table with quantified values for the included clusters.
                currentdata = cfg.data_list[cfg.table_index][cfg.current_table_order_full, :]
                currentdata = currentdata[cData[:, -1].astype(np.int).tolist(), :]
                analysisnum, numtabs = utils.find_analysis_round()
                ind = [i for i, m in enumerate(cfg.clusters_are_pixel_based) if not m][analysisnum]
                self.update_table(currentdata,
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(cfg.data_list[cfg.table_index]),
                                  cfg.current_table_orders_filtered[cfg.table_index],
                                  headernames=cfg.cluster_names[ind],
                                  )

                # If any clusters are included, and at least one cluster is filtered out, add an image to the
                # viewer containing the cells in the included clusters.
                analysisnum, numtabs = utils.find_analysis_round()
                imganalysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][
                    cfg.analysis_index // numtabs]
                if len(cfg.data_list[cfg.table_index]) > len(currentdata) > 0:
                    currentclusters = np.zeros((cfg.num_imgs,
                                                cfg.max_img_shape[0],
                                                cfg.max_img_shape[1],
                                                ),
                                               dtype=np.bool,
                                               )
                    labelimg = self.concat_label_imgs([cfg.labeled_imgs[ind] for ind in
                                                       range(imganalysisnum * cfg.num_imgs,
                                                             imganalysisnum * cfg.num_imgs + cfg.num_imgs)])
                    for index in cfg.current_table_orders_filtered[cfg.table_index]:
                        currentclusters[labelimg == index + 1] = 1
                    cfg.viewer.add_image(currentclusters, name="Filter", blending="additive", visible=True)

                # Un-check clusters that are not included in the filter.
                objectclusterindex = cfg.object_cluster_indices.index(cfg.table_index)
                ind = cfg.table_index - objectclusterindex % numtabs
                for i in range(len(currentdata)):
                    for j in range(ind, ind + numtabs):
                        if cfg.current_table_order_full[i] in cfg.currently_selected[j] and \
                                cfg.current_table_order_full[
                                    i] not in cfg.current_table_orders_filtered[cfg.table_index]:
                            cfg.currently_selected[j].remove(cfg.current_table_order_full[i])

            # If filtering a pixel clustering table.
            else:
                # Only check filtering for markers that have had their filters changed.
                filteredmarkers = []
                for i in range(len(cfg.lower_bounds_list[cfg.table_index])):
                    if cfg.lower_bounds_list[cfg.table_index][i] > cfg.min_vals[cfg.table_index][i] or \
                            cfg.upper_bounds_list[cfg.table_index][i] < cfg.max_vals[cfg.table_index][i]:
                        filteredmarkers.append(i)

                # Find pixel clustering data table, and append index values at the end to log sort order.
                cData = np.append(cfg.data_list[cfg.table_index][cfg.current_table_order_full, 1:],
                                  np.expand_dims(np.arange(len(cfg.data_list[cfg.table_index])), 1), 1)

                # Filter the table one marker at a time according to current lower- and upper-bounds.
                for markerid in filteredmarkers:
                    filtermask = (cData[:, markerid] <= cfg.upper_bounds_list[cfg.table_index][markerid])
                    cData = cData[filtermask]
                    filtermask = (cData[:, markerid] >= cfg.lower_bounds_list[cfg.table_index][markerid])
                    cData = cData[filtermask]

                # Store cluster IDs that will be included in the table, and in the proper order.
                cfg.current_table_orders_filtered[cfg.table_index] = [cfg.current_table_order_full[i] for i in
                                                                      cData[:, -1].astype(np.int).tolist()]

                # Update the table with quantified values for the included clusters.
                currentdata = cfg.data_list[cfg.table_index][cfg.current_table_order_full, :]
                currentdata = currentdata[cData[:, -1].astype(np.int).tolist(), :]
                analysisnum, numtabs = utils.find_analysis_round()
                ind = [i for i, m in enumerate(cfg.clusters_are_pixel_based) if m][analysisnum]
                self.update_table(currentdata,
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(cfg.data_list[cfg.table_index]),
                                  cfg.current_table_orders_filtered[cfg.table_index],
                                  headernames=cfg.cluster_names[ind],
                                  )

                # If any clusters are included, and at least one cluster is filtered out, add an image to the
                # viewer containing the cells in the included clusters.
                imganalysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Pixel"][
                    cfg.analysis_index // numtabs]
                if len(cfg.data_list[cfg.table_index]) > len(currentdata) > 0:
                    currentclusters = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]),
                                               dtype=np.bool)
                    labelimg = self.concat_label_imgs([cfg.labeled_imgs[ind] for ind in
                                                       range(imganalysisnum * cfg.num_imgs,
                                                             imganalysisnum * cfg.num_imgs + cfg.num_imgs)])
                    for index in cfg.current_table_orders_filtered[cfg.table_index]:
                        currentclusters[labelimg == index] = 1
                    cfg.viewer.add_image(currentclusters, name="Filter", blending="additive", visible=True)

                # Un-check clusters that are not included in the filter.
                pixelclusterindex = cfg.pixel_cluster_indices.index(cfg.table_index)
                ind = cfg.table_index - pixelclusterindex % numtabs
                for i in range(len(currentdata)):
                    for j in range(ind, ind + numtabs):
                        if cfg.current_table_order_full[i] in cfg.currently_selected[j] and \
                                cfg.current_table_order_full[
                                    i] not in cfg.current_table_orders_filtered[cfg.table_index]:
                            cfg.currently_selected[j].remove(cfg.current_table_order_full[i])

        utils.log_actions(f"gui.filter_table(reset={reset}, bound=\"{bound}\", marker=\"{marker}\", val={val})")

    def generate_RAPID_data(self,
                            markerindices,
                            markernames,
                            outfolder,
                            denoise,
                            normalizeeach,
                            normalizeall,
                            normtype,
                            pca,
                            ):
        """
        Normalize images before passing them through the RAPID algorithm.

        Args:
            markerindices (list): List of indices of cell markers being used for clustering.
            markernames (list): List of names of cell markers being used for clustering.
            outfolder (str): Path to folder where results will be saved.
            denoise (bool): If True, apply denoising on the image, otherwise do nothing.
            normalizeeach (bool): If True, apply specified normalization algorithm to each image individually. Otherwise, do nothing.
            normalizeall (bool): If True, apply z-scale normalization on all images together. Otherwise, do nothing.
            normtype (str): Normalization algorithm to be used on the image ({"None", "zscore", "log2", "log10", "all"}).
            pca (bool): If True, apply PCA reduction before normalization. Otherwise, do nothing.
        """

        # Open the zarr file to save files and variables to.
        cfg.viewer.status = "Preprocessing..."
        fh = zarr.open(outfolder, mode='a')
        fh.create_dataset('imageshapelist', data=cfg.img_shape_list, dtype='i4')

        # Initialize an array for the unnormalized dataset.
        unnormalized = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1], len(markerindices)),
                                dtype=np.uint8)

        # Store the max values for each image for relative normalization of the heatmap in the table.
        maxpixelclustervals = []
        for i in range(cfg.num_markers):
            maxpixelclustervals.append(np.amax(cfg.viewer.layers[i].data))
        fh.create_dataset('minmax', data=maxpixelclustervals, dtype='f8')
        cfg.max_pixel_clustervals.append(maxpixelclustervals)

        # Copy image data from viewer into one array, and perform denoising/binarizing if necessary.
        for i in range(len(markerindices)):
            tmp = copy.deepcopy(cfg.viewer.layers[markerindices[i]].data)
            if denoise == "Denoise":
                for j in range(len(tmp)):
                    tmp[j, :, :] = denoise_img(tmp[j, :, :])
            elif denoise == "Binarize":
                for j in range(len(tmp)):
                    tmp[j, :, :] = denoise_img(tmp[j, :, :])
                tmp[tmp > 0] = 255
            unnormalized[:, :, :, i] = tmp

        # Store the total number of pixels in the images being used.
        numpixels = 0
        for shape in cfg.img_shape_list:
            numpixels += shape[1] * shape[0]
        fhdr = fh.create_dataset('data', shape=(numpixels, len(markerindices)), dtype='uint8')
        fhdn = fh.create_dataset('data_normalized', shape=(numpixels, len(markerindices)), dtype='f8')
        fh.attrs['selmarkernames'] = markernames
        fh.attrs['totalpixels'] = numpixels * 1.0
        fh.attrs['imageslist'] = cfg.file_names

        # Determine whether to normalize, and initialize hdf5 file to use for normalization.
        if not (normalizeeach or normalizeall):
            normtype = None
        if not os.path.exists(os.path.join(cfg.output_folder, "hdf5_files")):
            os.mkdir(os.path.join(cfg.output_folder, "hdf5_files"))

        # Normalize each individual image according to the normalization type defined by the user.
        pixels = 0
        for i in range(cfg.num_imgs):
            vdim = cfg.img_shape_list[i][0]
            hdim = cfg.img_shape_list[i][1]
            img = unnormalized[i, :vdim, :hdim, :]
            if normalizeeach:
                img = preprocess(outfolder, medianblur=True, gaussianblur=True, gaussianblurstd=1,
                                 img=da.from_array(img, chunks=10000), normtype=normtype).reshape(-1, img.shape[-1])
            img = img.reshape(-1, img.shape[-1])

            vaex.from_pandas(pd.DataFrame(img).astype('float32')).export_hdf5(
                os.path.join(cfg.output_folder, 'hdf5_files', (f'analysis_{i:02}.hdf5')))
            fhdn[pixels:pixels + vdim * hdim, :] = img
            fhdr[pixels:pixels + vdim * hdim, :] = unnormalized[i, :vdim, :hdim, :].reshape((-1, img.shape[-1]))
            pixels += vdim * hdim

        df = vaex.open(os.path.join(cfg.output_folder, "hdf5_files", "analysis_*.hdf5"))
        arr = df.to_arrays(array_type='list')
        percentlist = [np.percentile(a, 99) for a in arr]
        fh.attrs['percentile'] = percentlist

        # If normalizing across all images, apply z-score normalization on the entire image stack.
        if normalizeall:
            # Apply z-scale normalization.
            df = vaex.open(os.path.join(cfg.output_folder, "hdf5_files", "analysis_*.hdf5"))
            scaler = vaex.ml.StandardScaler(features=df.column_names, prefix='scaled_')
            scaler.fit(df)
            normalized = scaler.transform(df)
            scaled_cols = [col for col in normalized.column_names if 'scaled_' in col]
            fhdn[:, :] = np.asarray(normalized[scaled_cols])

            # If specified by user, apply PCA normalization to the z-scale normalized data.
            if pca:
                npc = len(markerindices)
                if npc > 10:
                    pcanorm = vaex.ml.PCAIncremental(features=scaled_cols, n_components=npc, batch_size=10000000)
                else:
                    pcanorm = vaex.ml.PCA(features=scaled_cols, n_components=npc)
                pcanorm.fit(normalized, progress='widget')
                save_preprocess(pcanorm, cfg.output_folder + "/vmodels", zscore=False, pca=True)
                df_trans = pcanorm.transform(normalized)
                PCA_cols = [col for col in df_trans.column_names if 'PCA_' in col]
                for batch in range(0, len(df_trans), 10000000):
                    bs = np.min((len(df_trans) - batch, 10000000))
                    tmpdata = df_trans[PCA_cols][batch:batch + bs, :npc]
                    fhdn[batch:batch + bs, :] = np.asarray(tmpdata)

        try:
            shutil.rmtree(os.path.join(cfg.output_folder, "hdf5_files"))
        except:
            if not os.access(os.path.join(cfg.output_folder, "hdf5_files"), os.W_OK):
                os.chmod(os.path.join(cfg.output_folder, "hdf5_files"), stat.S_IWUSR)
                shutil.rmtree(os.path.join(cfg.output_folder, "hdf5_files"))
            else:
                pass
        cfg.viewer.status = "RAPID data generation complete"

    def load_environment(self,
                         envpath="",
                         ):
        """
        Open a directory for the user to load a previous RAPID GUI session to resume it exactly as they left it.

        envpath (str, optional): Path to the saved environment file being loaded (Default: "").

        :return: envpath *(str)*: \n
            Path to the saved environment file being loaded.
        """
        config = configparser.ConfigParser()

        if envpath == "":
            envpath = QFileDialog().getOpenFileName(filter="*.ini")[0]
            if envpath == "":
                return envpath

        p = "/".join(envpath.split("/")[:-1])
        imgpaths = glob.glob(p + "/*Layer*")
        order = [int(os.path.split(path)[-1].split("_")[-1]) for path in imgpaths]
        sorted = np.argsort(np.array(order))
        imgpaths = [imgpaths[i] for i in sorted]
        config.read(envpath)

        cfg.has_added_table = config.getboolean("Variables", 'hasaddedtable')
        cfg.has_edited_image = config.getboolean("Variables", 'haseditedimage')
        cfg.has_loaded_pixel = config.getboolean("Variables", 'hasloadedpixel')
        cfg.has_loaded_image = config.getboolean("Variables", 'hasloadedimage')

        cfg.action_logger_path = config.get("Variables", 'action_logger_path')
        cfg.analysis_index = config.getint("Variables", 'analysisindex')
        cfg.analysis_mode = config.get("Variables", 'analysismode')
        cfg.biaxial_count = config.getint("Variables", 'biaxialcount')
        cfg.display_selected_count = config.getint("Variables", 'displayselectedcount')
        cfg.edit_img_path = config.get("Variables", 'editimagepath')
        cfg.num_imgs = config.getint("Variables", 'numimgs')
        cfg.num_markers = config.getint("Variables", 'nummarkers')
        cfg.object_cluster_count = config.getint("Variables", 'objectclustercount')
        cfg.output_folder = os.path.abspath(os.path.join(envpath, "../.."))
        cfg.pixel_cluster_count = config.getint("Variables", 'pixelclustercount')
        cfg.resolution = config.getfloat("Variables", 'resolution')
        cfg.segment_count = config.getint("Variables", 'segmentcount')
        cfg.selected_region_count = config.getint("Variables", 'selectedregioncount')
        cfg.table_count = config.getint("Variables", 'tableimgcount')
        cfg.table_index = config.getint("Variables", 'tableindex')
        cfg.umap_count = config.getint("Variables", 'umapcount')

        cfg.analysis_log = ast.literal_eval(config.get("Variables", 'analysislog'))
        cfg.cell_cluster_vals = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'cellclustervals'))]
        cfg.cell_coordinates = ast.literal_eval(config.get("Variables", 'cellcoordinates'))
        cfg.cluster_names = ast.literal_eval(config.get("Variables", 'clusternames'))
        cfg.clusters_are_pixel_based = ast.literal_eval(config.get("Variables", 'clustersarepixelbased'))
        cfg.current_table_orders_filtered = ast.literal_eval(config.get("Variables", 'currenttableordersfiltered'))
        cfg.current_table_order_full = ast.literal_eval(config.get("Variables", 'currenttableorderfull'))
        cfg.currently_selected = ast.literal_eval(config.get("Variables", 'currentlyselected'))
        for i, step in enumerate(ast.literal_eval(config.get("Variables", 'currentstep'))):
            cfg.viewer.dims.set_current_step(i, step)

        cfg.current_vertical_header_labels = np.array(
            ast.literal_eval(config.get("Variables", 'currentverticalheaderlabels')))

        cfg.data_list = ast.literal_eval(config.get("Variables", 'datalist'))
        cfg.edit_actions = ast.literal_eval(config.get("Variables", 'editactions'))
        cfg.file_names = ast.literal_eval(config.get("Variables", 'filenames'))
        cfg.full_tab = ast.literal_eval(config.get("Variables", 'fulltab'))
        cfg.groups_list = ast.literal_eval(config.get("Variables", 'groupslist'))
        cfg.groups_names = ast.literal_eval(config.get("Variables", 'groupsnames'))
        cfg.histogram_counts = ast.literal_eval(config.get("Variables", 'histogramcounts'))
        cfg.img_is_flipped = ast.literal_eval(config.get("Variables", 'imageisflipped'))
        cfg.img_shape_list = ast.literal_eval(config.get("Variables", 'imageshapelist'))
        cfg.labeled_imgs = ast.literal_eval(config.get("Variables", 'labeledimgs'))
        cfg.full_tab = pd.DataFrame(cfg.full_tab)
        cfg.data_list = [np.array(d) for d in cfg.data_list]
        cfg.labeled_imgs = [np.array(l) for l in cfg.labeled_imgs]
        cfg.lower_bounds_list = ast.literal_eval(config.get("Variables", 'lowerboundslist'))
        cfg.markers = ast.literal_eval(config.get("Variables", 'markers'))
        cfg.max_img_shape = [np.array(l) for l in ast.literal_eval(config.get("Variables", 'maximageshape'))]
        cfg.max_pixel_clustervals = ast.literal_eval(config.get("Variables", 'maxpixelclustervals'))
        cfg.max_vals = ast.literal_eval(config.get("Variables", 'maxvals'))
        cfg.merge_img_paths = ast.literal_eval(config.get("Variables", 'mergedimagespaths'))
        cfg.merge_mem_markers = ast.literal_eval(config.get("Variables", 'mergememmarkers'))
        cfg.merge_nuc_markers = ast.literal_eval(config.get("Variables", 'mergenucmarkers'))
        cfg.min_vals = ast.literal_eval(config.get("Variables", 'minvals'))
        cfg.object_cluster_colors = [np.array(l) for l in
                                     ast.literal_eval(config.get("Variables", 'objectclustercolors'))]
        cfg.object_cluster_dfs = [pd.read_json(l) for l in
                                  ast.literal_eval(config.get("Variables", 'objectclusterdfs'))]
        for i in range(len(cfg.object_cluster_dfs)):
            cfg.object_cluster_dfs[i]["Cluster"] = [str(id) for id in cfg.object_cluster_dfs[i]["Cluster"]]
        cfg.object_cluster_directories = ast.literal_eval(config.get("Variables", 'objectclusterdirectories'))
        cfg.object_cluster_indices = ast.literal_eval(config.get("Variables", 'objectclusterindices'))
        cfg.object_img_names = ast.literal_eval(config.get("Variables", 'objectimgnames'))
        cfg.pixel_cluster_colors = [np.array(l) for l in
                                    ast.literal_eval(config.get("Variables", 'pixelclustercolors'))]
        cfg.pixel_cluster_directories = ast.literal_eval(config.get("Variables", 'pixelclusterdirectories'))
        cfg.pixel_cluster_indices = ast.literal_eval(config.get("Variables", 'pixelclusterindices'))
        cfg.pixel_cluster_markers = ast.literal_eval(config.get("Variables", 'pixelclustermarkers'))
        cfg.plot_coordinates = []
        coords = ast.literal_eval(config.get("Variables", 'plotcoordinates'))
        for i in range(len(coords)):
            cfg.plot_coordinates.append([np.array(l) for l in coords[i]])
        cfg.plot_is_umap = ast.literal_eval(config.get("Variables", 'plotisumap'))
        cfg.plot_segmentation_indices = ast.literal_eval(config.get("Variables", 'plotsegmentationindices'))
        cfg.plot_x_mins = ast.literal_eval(config.get("Variables", 'plotxmins'))
        cfg.plot_x_maxs = ast.literal_eval(config.get("Variables", 'plotxmaxs'))
        cfg.plot_y_mins = ast.literal_eval(config.get("Variables", 'plotymins'))
        cfg.plot_y_maxs = ast.literal_eval(config.get("Variables", 'plotymaxs'))
        cfg.segmentation_clustering_rounds = ast.literal_eval(config.get("Variables", 'segmentationclusteringrounds'))
        cfg.segmentation_indices = ast.literal_eval(config.get("Variables", 'segmentationindices'))
        cfg.segmentation_zarr_paths = ast.literal_eval(config.get("Variables", 'segmentationzarrpaths'))
        cfg.segment_counts = ast.literal_eval(config.get("Variables", 'segmentcounts'))
        cfg.table_img_names.remove('None')
        tableimagenames = ast.literal_eval(config.get("Variables", 'tableimagenames'))
        for name in tableimagenames:
            cfg.table_img_names.append(name)
        cfg.total_num_cells = ast.literal_eval(config.get("Variables", 'totalnumcells'))
        cfg.upper_bounds_list = ast.literal_eval(config.get("Variables", 'upperboundslist'))

        for i in range(len(imgpaths)):
            fh = zarr.open("/".join(imgpaths[i].split("/")[:-1]))
            file = imgpaths[i].split("/")[-1]
            if file.startswith("Image"):
                data = np.array(fh[file])
                try:
                    cmap = Colormap(ColorArray([(0, 0, 0), (
                        fh[file].attrs["Colormap0"] / 255., fh[file].attrs["Colormap1"] / 255.,
                        fh[file].attrs["Colormap2"] / 255.)]))
                    cfg.viewer.add_image(data, contrast_limits=fh[file].attrs["CLRange"],
                                         gamma=fh[file].attrs["Gamma"],
                                         opacity=fh[file].attrs["Opacity"], colormap=cmap,
                                         visible=fh[file].attrs["Visible"],
                                         name=fh[file].attrs["Name"], blending="additive")
                    cfg.viewer.layers[fh[file].attrs["Name"]].contrast_limits = fh[file].attrs["CL"]
                except:
                    cfg.viewer.add_image(data, visible=fh[file].attrs["Visible"], name=fh[file].attrs["Name"],
                                         blending="additive")
            else:
                self.draw_shapes(fh[file].attrs["Data"],
                                 fh[file].attrs["ShapeType"],
                                 fh[file].attrs["Properties"],
                                 fh[file].attrs["Name"],
                                 fh[file].attrs["Text"],
                                 fh[file].attrs["FaceColor"],
                                 )

        if cfg.has_added_table:
            cfg.has_added_table = False
            cfg.current_tab_data = np.array(ast.literal_eval(config.get("Variables", 'currenttabdata')))
            cfg.total_num_rows = config.getint("Variables", 'totalnumrows')
            cfg.table_order = ast.literal_eval(config.get("Variables", 'tableorder'))
            header_names = []
            if not cfg.analysis_mode == "Segmentation":
                clusterindex, _ = utils.find_analysis_round()
                if cfg.analysis_mode == "Pixel":
                    annotationindex = [j for j, n in enumerate(cfg.clusters_are_pixel_based) if n][clusterindex]
                else:
                    annotationindex = [j for j, n in enumerate(cfg.clusters_are_pixel_based) if not n][clusterindex]
                header_names = cfg.cluster_names[annotationindex]
            self.update_table(cfg.current_tab_data,
                              cfg.lower_bounds_list[cfg.table_index],
                              cfg.upper_bounds_list[cfg.table_index],
                              cfg.total_num_rows,
                              cfg.table_order,
                              headernames=header_names,
                              )
            cfg.is_loading_env = True
            cfg.table_params += cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            cfg.sort_table_widget.marker.choices = tuple(cfg.table_params)
            cfg.sort_table_widget.data.choices = cfg.table_img_names
            cfg.sort_table_widget.marker.value = config.get("Variables", 'tablecurrentmarker')
            cfg.sort_table_widget.data.value = config.get("Variables", 'tablecurrentdata')
            cfg.sort_table_widget.sort.value = config.get("Variables", 'tablecurrentsort')
            cfg.is_loading_env = False

        utils.log_actions(f"gui.load_environment(envpath=\"{envpath}\")")
        return envpath

    def load_object_clusters(self,
                             csvpath="",
                             segindex=None,
                             add_grey_img=None,
                             add_color_img=None,
                             ):
        """
        Allow user to select a .csv file that they would like to use to load clusters for a given segmented image.

        Args:
            csvpath (str, optional): Path to the csv file containing cluster assignments for each cell (Default: None).
            segindex (int, optional): Index of segmentation round to be used for biaxial gating (Default: None).
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """

        # Define path to csv file with clustering results to be loaded, and read into a dataframe.
        if csvpath == "":
            loadcsv = utils.LoadObjectClusters()
            loadcsv.exec()
            if not loadcsv.OK:
                return
            csvpath = loadcsv.csvpath
        fulltab = pd.read_csv(csvpath)
        fulltab = fulltab.drop(fulltab.columns[0], axis=1)

        # Select segmentation iteration to be used for cluster assignments.
        if segindex is None:
            segindex = 0
            if len(cfg.object_img_names) > 1:
                segmentedimage = utils.SelectSegmentedImage(cfg.object_img_names)
                segmentedimage.exec()
                if not segmentedimage.OK:
                    return
                segindex = segmentedimage.imageindex
        analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Segmentation"][segindex] * cfg.num_imgs

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        # Get the indices of all the columns to use from the segmented table.
        params = cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        markerinds = [params.index(mname) for mname in fulltab.columns[5:]]
        # [markerinds.append(params.index(mname) + 1) for mname in fulltab.columns[6:]]

        # Retrieve quantified expression of each of the included cell markers for each cell.
        complete_tab = []
        startind = segindex * cfg.num_imgs
        for tab_len in range(cfg.num_imgs):
            complete_tab.append(cfg.data_list[cfg.segmentation_indices[tab_len + startind]][:, markerinds])
        complete_tab = np.vstack(complete_tab)

        # Only can load clusters if there are the same number of cells.
        if len(fulltab) != len(complete_tab):
            utils.display_error_message("Incompatible number of cells",
                                        "Please make sure the table you selected corresponds to the segmented image")
            return

        # Store the loaded clustering results and save to the current output folder.
        cfg.object_cluster_dfs.append(fulltab)
        outfolder = utils.create_new_folder('RAPIDObject_', cfg.output_folder)
        fulltab.to_csv(os.path.join(outfolder, "SegmentationClusterIDs.csv"))

        # Update the segmented data table to include the new cluster IDs for each cell.
        to_values = fulltab['Cluster']
        vals = list(copy.deepcopy(np.unique(to_values)))

        unique = np.unique(to_values)
        for i in range(len(unique)):
            to_values[to_values == unique[i]] = i + 1
        fulltab['Cluster'] = to_values

        # Retrieve relevant columns from relabeled table.
        relabeled_table = fulltab.iloc[:, [i for i in range(3, fulltab.shape[1])]]

        # Initialize data array for clustered image, and generate the colormap.
        relabeledgreyimages = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]), dtype=np.uint8)
        color = generate_colormap(len(np.unique(to_values)) + 1)
        cfg.object_cluster_colors.append(color[:-1, :])
        np.save(os.path.join(outfolder, "color.npy"), color)
        fullclusterdata = []
        startindex = 0
        for i in range(cfg.num_imgs):
            # Get name of current image
            imgname = os.path.splitext(os.path.split(cfg.file_names[i])[-1])[0]

            # Relabel the segmented result for the current image and save it to the output folder.
            numcells = len(cfg.data_list[cfg.segmentation_indices[i + startind]])
            from_values = np.arange(1, 1 + numcells)
            tmp_to_values = to_values[startindex:startindex + numcells].values
            cfg.cell_cluster_vals.append(copy.deepcopy(tmp_to_values))
            relabeled = self.method_searchsort(from_values,
                                               tmp_to_values,
                                               cfg.labeled_imgs[analysisnum + i].flatten().astype(int),
                                               )
            relabeledgreyimages[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = relabeled.reshape(
                (cfg.img_shape_list[i][0], cfg.img_shape_list[i][1])).astype(np.uint8)
            relabeledgreyimages[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]][
                cfg.labeled_imgs[analysisnum + i] == 0] = 0
            utils.save_img(os.path.join(outfolder,
                                        f"ObjectClusterLabels_{imgname}.tif"),
                           relabeledgreyimages[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] + 1,
                           cfg.img_is_flipped[i],
                           )

            # Apply the colormap to the relabeled image and save it to the output folder.
            relabeledimages = np.zeros((cfg.max_img_shape[0], cfg.max_img_shape[1], 3), dtype=np.uint8)
            for j in range(len(vals)):
                relabeledimages[:, :, 0][relabeledgreyimages[i, :, :] == j + 1] = color[j][0]
                relabeledimages[:, :, 1][relabeledgreyimages[i, :, :] == j + 1] = color[j][1]
                relabeledimages[:, :, 2][relabeledgreyimages[i, :, :] == j + 1] = color[j][2]

            utils.save_img(os.path.join(outfolder,
                                        f"ObjectClusters_{imgname}.tif"),
                           relabeledimages[:cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1], :],
                           cfg.img_is_flipped[i],
                           )

            # Add the relabeled colored and/or greyscale image(s) to the viewer.
            if i == 0:
                self.set_invisible(cfg.viewer)
                relab = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1], 3), dtype=relabeledimages.dtype)
                relab[0, :len(relabeledimages), :relabeledimages.shape[1], :] = relabeledimages
                if add_grey_img:
                    cfg.viewer.add_image(relabeledgreyimages[[i], :, :],
                                         name=f"Object Cluster IDs {cfg.object_cluster_count + 1}", blending="additive",
                                         contrast_limits=(0, np.max(relabeledgreyimages)))
                if add_color_img:
                    cfg.viewer.add_image(relab, name=f"Object Clusters {cfg.object_cluster_count + 1}",
                                         blending="additive")
            else:
                relab = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1], 3), dtype=relabeledimages.dtype)
                relab[0, :len(relabeledimages), :relabeledimages.shape[1], :] = relabeledimages
                if add_grey_img and add_color_img:
                    cfg.viewer.layers[-2].data = np.vstack(
                        (cfg.viewer.layers[-2].data, relabeledgreyimages[[i], :, :]))
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, relab))
                elif add_grey_img:
                    cfg.viewer.layers[-1].data = np.vstack(
                        (cfg.viewer.layers[-1].data, relabeledgreyimages[[i], :, :]))
                elif add_color_img:
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, relab))

            # Take the quantified values from only the cells in the current image.
            tmp_tab = relabeled_table[startindex:startindex + len(cfg.data_list[cfg.segmentation_indices[i]])].values
            tmp_tab_df = pd.DataFrame(tmp_tab)
            startindex += len(cfg.data_list[cfg.segmentation_indices[i]])

            # Find the average marker expression across each cluster represented in the table.
            grouped = tmp_tab_df.groupby(0)
            tabres = grouped.apply(np.mean)

            # Include the image ID and the total number of cells from each cluster in the table.
            tabres.insert(0, "Sample", i)
            _, counts = np.unique(tmp_tab[:, 0], return_counts=True)
            tabres.insert(2, "Cells", counts)

            # Find the min and max values of each cell marker for the clusters in the current image.
            clusteravgs = np.zeros((len(unique), relabeled_table.shape[1] + 2))
            clusteravgs[np.unique(tmp_to_values.astype(np.uint8) - 1), :] = tabres.values
            fullclusterdata.append(clusteravgs.astype(np.float))

            cfg.data_list.append(clusteravgs[:, 2:].astype(np.float))

            cfg.current_table_orders_filtered.append(list(range(len(clusteravgs))))
            tab = clusteravgs[np.unique(tmp_to_values.astype(np.uint8) - 1), 2:]
            minvals = []
            maxvals = []
            for i in range(tab.shape[1] - 1):
                minvals.append(np.min(tab[:, i + 1]))
                maxvals.append(np.max(tab[:, i + 1]))
            cfg.min_vals.append(copy.deepcopy(minvals))
            cfg.max_vals.append(copy.deepcopy(maxvals))
            cfg.lower_bounds_list.append(copy.deepcopy(minvals))
            cfg.upper_bounds_list.append(copy.deepcopy(maxvals))

        # Find weighted average data and update lower/upper bounds.
        fullclusterdata = np.nan_to_num((np.vstack(fullclusterdata)))
        if cfg.num_imgs > 1:
            weighted_average = np.zeros((len(np.unique(to_values)), fullclusterdata.shape[1] - 2))
            for i in range(len(fullclusterdata)):
                currcluster = i % len(weighted_average)
                weighted_average[currcluster, 0] += fullclusterdata[i, 2]
            for i in range(len(fullclusterdata)):
                currcluster = i % len(weighted_average)
                weighted_average[currcluster, 1:] += fullclusterdata[i, 3:] * fullclusterdata[i, 2] / weighted_average[
                    currcluster, 0]
            cfg.data_list.append(weighted_average)
            cfg.current_table_orders_filtered.append(list(range(len(weighted_average))))
            minvals = []
            maxvals = []
            for i in range(weighted_average.shape[1] - 1):
                minvals.append(np.min(weighted_average[:, i + 1]))
                maxvals.append(np.max(weighted_average[:, i + 1]))
            cfg.min_vals.append(copy.deepcopy(minvals))
            cfg.max_vals.append(copy.deepcopy(maxvals))
            cfg.lower_bounds_list.append(copy.deepcopy(minvals))
            cfg.upper_bounds_list.append(copy.deepcopy(maxvals))

        # Relabel the segmented images with cluster IDs.
        for i in range(cfg.num_imgs):
            relabeledgreyimages[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]][
                cfg.labeled_imgs[analysisnum + i] == 0] = 0
        unique = np.unique(relabeledgreyimages)
        for i in range(len(unique)):
            relabeledgreyimages[relabeledgreyimages == unique[i]] = i
        cfg.labeled_imgs += [
            utils.convert_dtype(relabeledgreyimages[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]]) for i in
            range(len(relabeledgreyimages))]

        # Save the dataset to the output folder as a csv file.
        mergemarkerlist = list(fulltab.columns[4:].values)
        clusterdf = pd.DataFrame(np.nan_to_num(fullclusterdata))
        clusterdf.columns = np.hstack([["Sample", "Cluster", "# Cells"], mergemarkerlist])
        clusterdf.to_csv(os.path.join(outfolder, "ObjectClusterAvgExpressionVals.csv"))

        # Generate MST plot for the clustered data.
        tabledata, datascaled, DistMatrix, uniqueClusters = \
            prep_for_mst(clustertable=clusterdf,
                         minclustersize=1,
                         clustersizes=clusterdf["# Cells"],
                         includedmarkers=mergemarkerlist,
                         )
        generate_mst(distancematrix=DistMatrix,
                     normalizeddf=datascaled[datascaled.columns],
                     colors=color,
                     randomseed=0,
                     outfolder=outfolder,
                     clusterheatmap=True,
                     displaymarkers=mergemarkerlist,
                     uniqueclusters=uniqueClusters,
                     samplenames=list(np.unique(clusterdf['Sample'])),
                     displaysingle=False,
                     values="# Cells",
                     )
        cfg.viewer.add_image(imread(os.path.join(outfolder, "MeanExpressionHeatmap.png")),
                             name=f"Object Clusters {cfg.object_cluster_count + 1} Heatmap",
                             blending="additive",
                             visible=False,
                             )

        # Update the table widget dropdown options.
        for i in range(cfg.num_imgs):
            cfg.table_img_names.append(
                f"Object Cluster {cfg.object_cluster_count + 1} - {cfg.file_names[i].split('/')[-1]}")
            cfg.object_cluster_indices.append(cfg.table_count)
            cfg.table_count += 1
            cfg.currently_selected.append([])
        if cfg.num_imgs > 1:
            cfg.table_img_names.append(f"Object Cluster {cfg.object_cluster_count + 1} - Combined Average")
            cfg.object_cluster_indices.append(cfg.table_count)
            cfg.table_count += 1
            cfg.currently_selected.append([])

        # Update any necessary variables.
        cfg.segmentation_clustering_rounds[0].append(cfg.object_cluster_count)
        cfg.object_cluster_count += 1
        cfg.analysis_log.append("Object")
        cfg.clusters_are_pixel_based.append(False)
        cfg.cluster_names.append([])
        cfg.update_log_file = False
        cfg.sort_table_widget.data.choices = tuple(cfg.table_img_names)
        cfg.sort_table_widget.data.value = f"Object Cluster {cfg.object_cluster_count} - {cfg.file_names[0].split('/')[-1]}"
        cfg.sort_table_widget.reset_choices()
        cfg.update_log_file = True
        utils.log_actions(f"gui.load_object_clusters(csvpath=\"{csvpath}\", segindex={segindex}, "
                          f"add_grey_img={add_grey_img}, add_color_img={add_color_img})")

    def load_pixel_results(self,
                           datapath="",
                           output_folder="",
                           add_grey_img=None,
                           add_color_img=None,
                           ):
        """
        Open a directory for the user to select which pixel-based results they would like to load.

        Args:
            datapath (str, optional): Path to data folder with RAPID results being loaded (Default: "").
            output_folder (str, optional): Path to output folder where results will be saved (Default: "").
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).

        :return: datapath *(str)*: \n
            Path to data folder with RAPID results being loaded.
        """
        # User cannot load pixel-based results multiple times due to potential image incompatibility.
        if cfg.has_loaded_pixel:
            utils.display_error_message("Results already loaded",
                                        "You have already loaded results. Please open another window if you would like to load different data")
            return ""

        # Prompt user to indicate the path to the results being loaded, and ensure the selected path contains compatible
        # RAPID-P results.
        if datapath == "":
            datapath = QFileDialog().getExistingDirectory(None, "Select Folder")
            if datapath == "":
                return ""
            if not datapath.endswith("/RAPID_Data"):
                datapath = os.path.join(datapath, "RAPID_Data")

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        inputzarr = zarr.open(datapath, mode='r')
        col_list, data, grey, imageshapelist, minmax, prob, tab, filenames, selmarkernames, totalpixels, \
        percentile, columns, arg, flipimg = self.load_pixel_zarr(inputzarr)

        # Prompt user to indicate the root folder where new results will be saved.
        if output_folder == "":
            utils.OKButtonPopup("Select Output Folder").exec()
            dialog = QFileDialog()
            output_folder = dialog.getExistingDirectory(None, "Select Output Folder")
        cfg.output_folder = utils.create_new_folder("RAPID_GUI", output_folder)
        utils.initialize_logger(pixel_results_path=datapath,
                                add_grey_img=add_grey_img,
                                add_color_img=add_color_img,
                                )
        cfg.viewer.status = "Loading analysis..."

        # Save image attributes to the output folder.
        results_folder = utils.create_new_folder("RAPIDPixel_", cfg.output_folder)
        cfg.pixel_cluster_directories.append(results_folder)

        paths = glob.glob(os.path.join(os.path.split(datapath)[0], "*"))
        paths.remove(os.path.join(datapath))
        for path in paths:
            if os.path.isfile(path):
                shutil.copy(path, os.path.join(results_folder, os.path.split(path)[-1]))

        datafolder = os.path.join(results_folder, "RAPID_Data")
        outputzarr = zarr.open(datafolder, 'w')
        outputzarr['color'] = col_list
        outputzarr['data'] = data
        outputzarr['grey'] = grey
        outputzarr['imageshapelist'] = imageshapelist
        outputzarr['minmax'] = minmax
        outputzarr['prob'] = prob
        outputzarr['tab'] = tab
        outputzarr['tab'].attrs['columns'] = columns
        outputzarr.attrs['imageslist'] = filenames
        outputzarr.attrs['selmarkernames'] = selmarkernames
        outputzarr.attrs['totalpixels'] = totalpixels
        outputzarr.attrs['percentile'] = percentile
        outputzarr.attrs['arg'] = arg
        outputzarr.attrs['flipimg'] = flipimg
        outputzarr.attrs['markers'] = selmarkernames

        # Prompt user to select which image(s) to load.
        imgnames = []
        for path in filenames:
            name = path.split("/")
            imgnames.append(name[-1])
        imagenums = [0]
        if len(filenames) > 1:
            selectimages = utils.SelectLoadImages(imgnames)
            selectimages.exec()
            if not selectimages.OK:
                return False
            imagenums = selectimages.images

        # Retrieve data from the results being loaded.
        imageshapelist = inputzarr["imageshapelist"][:]
        cfg.img_shape_list = [(int(imageshapelist[i][0]), int(imageshapelist[i][1]), int(imageshapelist[i][2])) for i
                              in imagenums]
        cfg.num_imgs = len(imagenums)
        args = runRAPIDzarr.get_parameters()
        args.ncluster = int(len(tab) / len(imgnames))

        # Load cell marker names and store them where applicable.
        cfg.markers = inputzarr.attrs['selmarkernames']
        cfg.pixel_cluster_markers.append(cfg.markers)
        cfg.num_markers = len(cfg.markers)
        for name in cfg.markers:
            cfg.table_params.append(name)
        for name in ["Area", "Eccentricity", "Perimeter", "Major Axis"]:
            cfg.table_params.append(name)

        # Add raw images to the GUI, only for those that have been included by the user.
        vdim = max([s[0] for s in imageshapelist])
        hdim = max([s[1] for s in imageshapelist])
        cfg.max_img_shape = np.array([vdim, hdim])

        colors = generate_colormap(cfg.num_markers + 1)
        for i in range(cfg.num_markers):
            data = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]), dtype=np.uint8)
            currentmarkerdata = np.array(inputzarr['data'][:, i])
            currentmarkerdata = img_as_ubyte(currentmarkerdata)
            pixcount = 0
            imgcount = 0
            for j in range(len(imageshapelist)):
                s0 = imageshapelist[j][0]
                s1 = imageshapelist[j][1]
                if j in imagenums:
                    data[imgcount, :s0, :s1] = currentmarkerdata[pixcount:pixcount + s0 * s1].reshape((s0, s1))
                    imgcount += 1
                pixcount += s0 * s1
            cmap = Colormap(ColorArray([(0, 0, 0), (colors[i, 0] / 255., colors[i, 1] / 255., colors[i, 2] / 255.)]))
            cfg.viewer.add_image(data, contrast_limits=[0, 255], colormap=cmap, name=cfg.markers[i],
                                 blending="additive")

        # Reshape flattened label values to the proper shape for each image being loaded into the GUI.
        pixcount = 0
        imgcount = 0
        greyimgs = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]))
        for i in range(len(imageshapelist)):
            s0 = np.array(imageshapelist)[i][0]
            s1 = np.array(imageshapelist)[i][1]
            if i in imagenums:
                temp = grey[pixcount:pixcount + s0 * s1].reshape((s0, s1)) + 1
                temp[:, np.array(imageshapelist)[i][1]:] = 0
                temp[np.array(imageshapelist)[i][0]:, :] = 0
                greyimgs[imgcount, :s0, :s1] = temp
                imgcount += 1
            pixcount += s0 * s1

        # By default, initialize sample groupings so that each image is in its own group.
        cfg.file_names = [filenames[i] for i in imagenums]
        d = {}
        for name in cfg.file_names:
            n = os.path.split(name)[-1]
            d[n] = n
        cfg.groups_list.append(d)

        # Exclude table entries for images not being loaded.
        tab = np.vstack(
            [tab[i * args.ncluster:(i + 1) * args.ncluster, :] for i in range(len(imgnames)) if i in imagenums])
        old_clusters = np.arange(args.ncluster)
        new_clusters = np.unique(greyimgs)[np.unique(greyimgs) > 0] - 1
        excluded_clusters = np.array(list(set(old_clusters) - set(new_clusters)))

        # Account for case when some clusters are no longer present if only appearing in images that have been excluded.
        if len(excluded_clusters) > 0:
            # Re-index grey image.
            greyimgs = self.method_searchsort(np.unique(greyimgs),
                                              np.arange(np.min(greyimgs),
                                                        len(np.unique(greyimgs)) + np.min(greyimgs),
                                                        ),
                                              greyimgs,
                                              )
            # Delete excluded clusters from table.
            excludedrows = []
            for cluster in excluded_clusters:
                excludedrows += [int(i * args.ncluster + cluster) for i in range(len(imagenums))]
            tab = np.delete(tab,
                            np.array(excludedrows,
                                     dtype=int,
                                     ),
                            axis=0,
                            )
            args.ncluster -= len(excluded_clusters)

        col_list = col_list[:args.ncluster,:]

        # Update any necessary variables.
        cfg.img_is_flipped = [inputzarr.attrs['flipimg'][i] for i in imagenums]
        cfg.max_pixel_clustervals.append(list(inputzarr['minmax'][:]))
        if not max(cfg.max_pixel_clustervals[0]) > 1.0:
            cfg.max_pixel_clustervals[0] = [a * 255. for a in cfg.max_pixel_clustervals[0]]
        cfg.marker_inds = [i for i in range(len(cfg.markers))]
        cfg.analysis_mode = "Pixel"
        cfg.labeled_imgs += [utils.convert_dtype(greyimgs[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]])
                             for i in range(len(greyimgs))]
        cfg.analysis_log.append("Pixel")

        self.apply_pixel_clustering(tab,
                                    args,
                                    col_list,
                                    add_grey_img,
                                    add_color_img,
                                    results_folder,
                                    )
        cfg.viewer.dims.set_current_step(0, 0)
        cfg.pixel_cluster_count += 1
        cfg.cluster_names.append([])
        cfg.update_log_file = False
        cfg.sort_table_widget.reset_choices()
        cfg.update_log_file = True
        cfg.has_loaded_pixel = True

        return datapath

    def load_pixel_zarr(self,
                        zarrpath,
                        ):
        """
        Load all necessary zarr files when loading pixel-based clustering results.

        Args:
            zarrpath (str): Path to the root directory where zarr files are being loaded from.

        :return: *(tuple)*: \n
            Tuple of zarr attributes that must be loaded when loading pixel-based clustering results.
        """
        return zarrpath['color'][:], zarrpath['data'][:], zarrpath['grey'][:], zarrpath['imageshapelist'][:], \
               zarrpath['minmax'][:], zarrpath['prob'][:], zarrpath['tab'][:], zarrpath.attrs['imageslist'], \
               zarrpath.attrs['selmarkernames'], zarrpath.attrs['totalpixels'], zarrpath.attrs['percentile'], \
               zarrpath['tab'].attrs['columns'], zarrpath.attrs['arg'], zarrpath.attrs['flipimg']

    def load_segmentation_results(self,
                                  filenames=[],
                                  output_folder="",
                                  quant_avg=None,
                                  add_grey_img=None,
                                  add_color_img=None,
                                  ):
        """
        Open a directory for the user to select which segmentation results they would like to load.

        Args:
            filenames (list, optional): List of paths to segmentation label images being loaded (Default: []).
            output_folder (str, optional): Path to folder where results will be saved (Default: "").
            quant_avg (bool): If True, use mean expression values for quantification. Otherwise, calculate root-mean-square values.
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).

        :return: filenames *(list)*: \n
            List of paths to the labeled segmented images being loaded. Return False if no files are selected.
        """

        # Prompt user to select labeled image to load.
        if filenames == []:
            filenames, _ = QFileDialog.getOpenFileNames(parent=cfg.viewer.window.qt_viewer,
                                                        caption='Select Label image', )
            if len(filenames) == 0:
                return False

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        # Allow user to define wither to quantify using mean expression, or root-mean-square.
        if quant_avg is None:
            quantmode = utils.QuantificationMode()
            quantmode.exec()
            if not quantmode.OK:
                return
            quant_avg = quantmode.avg

        # Prompt user to choose path to output folder where data will be saved.
        if output_folder == "":
            utils.OKButtonPopup("Select Output Folder").exec()
            dialog = QFileDialog()
            output_folder = dialog.getExistingDirectory(None, "Select Output Folder")
        cfg.output_folder = utils.create_new_folder("RAPID_GUI", output_folder)
        outfolder = utils.create_new_folder("Segmentation", cfg.output_folder)
        utils.initialize_logger(segmentation_file_names=filenames,
                                quant_avg=quant_avg,
                                add_grey_img=add_grey_img,
                                add_color_img=add_color_img,
                                )

        # Automatically load images from saved zarr files if using results from RAPID.
        if os.path.exists(os.path.join(os.path.split(filenames[0])[0], "RawImages")):
            # Copy zarr files for segmented image being loaded to new output folder.
            shutil.copytree(os.path.join(os.path.split(filenames[0])[0], "RawImages"),
                            os.path.join(outfolder, "RawImages"),
                            )
            if os.path.exists(os.path.join(os.path.split(filenames[0])[0], "MergedImage")):
                shutil.copytree(os.path.join(os.path.split(filenames[0])[0], "MergedImage"),
                                os.path.join(outfolder, "MergedImage"),
                                )
            if os.path.exists(os.path.join(os.path.split(filenames[0])[0], "Features0")):
                features_paths = glob.glob(os.path.join(os.path.split(filenames[0])[0], "Features*"))
                for features_path in features_paths:
                    shutil.copytree(features_path,
                                    os.path.join(outfolder, os.path.split(features_path)[-1]),
                                    )

            # Retrieve raw image data and attributes from saved zarr file.
            rootfold = os.path.join(os.path.split(filenames[0])[0], "RawImages")
            subfolders = glob.glob(rootfold + "/*")
            subfolders.sort()
            fh = zarr.open(rootfold)
            cfg.num_markers = len(subfolders)
            cfg.has_loaded_image = True
            cfg.file_names = fh.attrs['filenames']
            cfg.max_img_shape = np.array(fh.attrs['maximageshape'])
            cfg.img_shape_list = fh.attrs['imageshapelist']
            cfg.markers = fh.attrs['markers']
            cfg.marker_inds = fh.attrs['markernums']
            cfg.num_imgs = len(filenames)

            # Store file names.
            d = {}
            for name in cfg.file_names:
                n = os.path.split(name)[-1]
                d[n] = n
            cfg.groups_list.append(d)
            newfilenames = [fn for fn in cfg.file_names if
                            os.path.split(fn)[-1].split(".")[0] in [os.path.split(fn)[-1].split(".")[0][16:] for fn in
                                                                    filenames]]
            imginds = [cfg.file_names.index(fn) for fn in newfilenames]
            cfg.file_names = newfilenames

            # Add raw image data to the viewer.
            for i in range(cfg.num_markers):
                file = os.path.split(subfolders[i])[-1]
                data = np.array(fh[file])
                cmap = Colormap(ColorArray([(0, 0, 0), (fh[file].attrs["Colormap0"] / 255.,
                                                        fh[file].attrs["Colormap1"] / 255.,
                                                        fh[file].attrs["Colormap2"] / 255.)]))
                cfg.viewer.add_image(data[imginds, :, :], contrast_limits=fh[file].attrs["CLRange"],
                                     gamma=fh[file].attrs["Gamma"], opacity=fh[file].attrs["Opacity"],
                                     colormap=cmap, visible=fh[file].attrs["Visible"], name=fh[file].attrs["Name"],
                                     blending="additive")
                cfg.viewer.layers[fh[file].attrs["Name"]].contrast_limits = fh[file].attrs["CL"]

            # Add merged image data to the viewer.
            fh = zarr.open(os.path.join(os.path.split(filenames[0])[0]))
            mergedimg = np.array(fh["MergedImage"])
            if len(np.unique(mergedimg[0, imginds, :, :])) == 1:
                cfg.viewer.add_image(mergedimg[1, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                     blending="additive")
            elif len(np.unique(mergedimg[1, imginds, :, :])) == 1:
                cfg.viewer.add_image(mergedimg[0, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                     blending="additive")
            else:
                cfg.viewer.add_image(mergedimg[:, imginds, :, :], contrast_limits=[0, 255], name="Merged Image",
                                     blending="additive")

            # Load segmented label images.
            cfg.table_params += cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            cfg.sort_table_widget.marker.choices = tuple(cfg.table_params)

        # Prompt user to load raw image files if loading results that were not generated using RAPID.
        else:
            # Open selected images.
            utils.OKButtonPopup("Open Raw Images").exec()
            openedimgs = self.open_images(filenames)
            if not openedimgs:
                return False

            # Sort file names and segmented image names to be consistent with each other and alphabetical.
            imgfilenames = [os.path.split(name)[-1].split(".")[0] for name in cfg.file_names]
            fnames = copy.deepcopy(imgfilenames)
            fnames.sort()
            orders = [fnames.index(name) for name in imgfilenames]
            origimgnames = [fnames[i] for i in orders]
            filenames.sort()
            filenames = [filenames[i] for i in orders]
            for i in range(len(origimgnames)):
                # Make sure image names correspond to segmented images
                filename = os.path.split(filenames[i])[-1].split(".")[0]
                if not origimgnames[i] in os.path.split(filenames[i])[-1].split(".")[0]:
                    utils.display_error_message("Mismatching image names",
                                                "Please ensure the raw images correspond to the segmented "
                                                "image and are named consistently. Acceptable segmented "
                                                "image names are in the format \"[prefix][Raw Image Name]"
                                                "[Suffix], with the prefix and suffix consistent across all "
                                                "images\"")
                    for j in range(len(cfg.viewer.layers)):
                        cfg.viewer.layers.pop(0)
                    cfg.groups_list = []
                    cfg.has_loaded_image = False
                    cfg.img_shape_list = []
                    cfg.num_imgs = 0
                    return

                # Make sure all segmented image names have the same prefix and suffix.
                if i == 0:
                    prefixsuffix = filename.split(origimgnames[i])
                else:
                    if filename.split(origimgnames[i]) != prefixsuffix:
                        utils.display_error_message("Mismatching image names",
                                                    "Please ensure the raw images correspond to the segmented "
                                                    "image and are named consistently with the raw images. "
                                                    "Acceptable names are in the format \"[prefix][Raw Image "
                                                    "Name][Suffix], with the prefix and suffix consistent "
                                                    "across all images\"")
                        for j in range(len(cfg.viewer.layers)):
                            cfg.viewer.layers.pop(0)
                        cfg.groups_list = []
                        cfg.has_loaded_image = False
                        cfg.img_shape_list = []
                        cfg.num_imgs = 0
                        return

        self.apply_segmentation(add_grey_img,
                                add_color_img,
                                quant_avg,
                                outfolder,
                                loadedresultspaths=filenames,
                                )

        return filenames

    def manual_annotation(self,
                          umapind=None,
                          add_grey_img=None,
                          add_color_img=None,
                          labelnames=[],
                          shapeverts=[],
                          shapetypes=[],
                          ):
        """
        Allow user to draw shapes on a UMAP plot to define clusters, with each shape corresponding to a cluster.

        Args:
            umapind (int, optional): Index of UMAP plot being annotated (Default: None).
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            labelnames (list, optional): List of names for the clusters corresponding to each shape (Default: []).
            shapeverts (list, optional): List of vertices for each shape drawn by the user (Default: []).
            shapetypes (list, optional): List of geometries for each shape drawn by the user (Default: []).
        """
        # Ensure there is at least one UMAP plot to annotate.
        if cfg.umap_count == 1:
            utils.display_error_message("No UMAP detected",
                                        "You must first generate a UMAP in order to select cells to be displayed")
            return

        # Prompt user to select which UMAP plot they would like to use if more than one have been generated.
        if umapind is None:
            umapind = 0
            umapplots = [b for b in cfg.plot_is_umap if b]
            if len(umapplots) > 1:
                selectplot = utils.BiaxialUMAPIterations(umapplots)
                selectplot.exec()
                if not selectplot.OK:
                    return
                umapind = selectplot.iteration

        # Determine which plot index this corresponds to, factoring in biaxial plots.
        inds = [i for i, x in enumerate(cfg.plot_is_umap) if x]
        it = inds[umapind]
        cfg.viewer.status = "Annotating UMAP"

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        if shapeverts == [] or shapetypes == []:
            # Ensure there is at least one shape drawn in order to define the region to be quantified.
            ind = -1
            for i in reversed(range(len(cfg.viewer.layers))):
                if isinstance(cfg.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and cfg.viewer.layers[i].visible:
                    ind = i
                    break
            if ind == -1:
                utils.display_error_message("Please draw a shape first",
                                            "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
                return

            # Keep track of the bounding box vertices and geometries of each shape.
            shapeverts = [cfg.viewer.layers[ind].data[i][:, -2:] for i in range(len(cfg.viewer.layers[ind].data))]
            shapetypes = [cfg.viewer.layers[ind].shape_type[i] for i in range(len(cfg.viewer.layers[ind].data))]
            cfg.viewer.layers.pop(ind)
        else:
            shapeverts = [np.array(verts) for verts in shapeverts]

        # Label each shape and adjust their colors.
        labels = []
        for i in range(len(shapeverts)):
            labels.append(f"Region {i + 1}")
        properties = {'class': labels, }
        text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
        cfg.viewer.add_shapes(shapeverts, shape_type=shapetypes, edge_width=0, face_color=[np.array([0.2, 0.2, 0.2])],
                              name="Manual Annotation", properties=properties, text=text_properties)

        # Allow user to name the different regions and add them as labels to the shapes.
        if labelnames == []:
            regionnamespopup = utils.ManualAnnotationPopup(len(shapeverts))
            regionnamespopup.exec()
            if regionnamespopup.OK:
                labelnames = list(regionnamespopup.headernames)
                if not labelnames == labels:
                    cfg.viewer.layers.pop(len(cfg.viewer.layers) - 1)
                    properties = {'class': labelnames, }
                    text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                    cfg.viewer.add_shapes(shapeverts, shape_type=shapetypes, edge_width=0, name="Manual Annotation",
                                          properties=properties, text=text_properties,
                                          face_color=[np.array([0.2, 0.2, 0.2])])
                labelnames += ["Other"]
            else:
                cfg.viewer.layers.pop(len(cfg.viewer.layers) - 1)
                return
        else:
            cfg.viewer.layers.pop(len(cfg.viewer.layers) - 1)
            properties = {'class': [name for name in labelnames if name != "Other"], }
            text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
            cfg.viewer.add_shapes(shapeverts, shape_type=shapetypes, edge_width=0, name="Manual Annotation",
                                  properties=properties, text=text_properties,
                                  face_color=[np.array([0.2, 0.2, 0.2])])

        # Create a new output folder to save output files to.
        results_folder = utils.create_new_folder("RAPIDObject_", cfg.output_folder)
        cfg.object_cluster_directories.append(results_folder)
        self.set_invisible(cfg.viewer)

        # Initialize list of arrays of cell IDs for each cluster ID.
        clusterids = [np.zeros(len(v)) for v in cfg.plot_coordinates[it]]

        # Find the cells corresponding to the vertices within each of the shapes to define clusters.
        for shape in range(len(shapeverts)):
            # Scale the vertices from 0-1 to map to coordinates on the plot.
            tupverts = copy.deepcopy(shapeverts[shape])
            tupverts[:, 0] = ((cfg.plot_x_maxs[it] - tupverts[:, 0]) / (
                    cfg.plot_x_maxs[it] - cfg.plot_x_mins[it])) * 1.1 - 0.05
            tupverts[:, 1] = ((tupverts[:, 1] - cfg.plot_y_mins[it]) / (
                    cfg.plot_y_maxs[it] - cfg.plot_y_mins[it])) * 1.1 - 0.05
            tupverts[:, [0, 1]] = tupverts[:, [1, 0]]
            tupverts = [tuple(x) for x in tupverts.tolist()]
            p = self.create_shape_path(tupverts,
                                       shapetypes[shape],
                                       )
            for i in range(cfg.num_imgs):
                # Find the vertices on the plot within the shape, and the cells corresponding to those vertices.
                rows = list(p.contains_points(cfg.plot_coordinates[it][i]))
                rows = [i for i, b in enumerate(rows) if b]
                clusterids[i][rows] = shape + 1

        # All remaining cells not within any of the shapes will be in one additional cluster together.
        for i in range(cfg.num_imgs):
            for j in range(len(clusterids[i])):
                if clusterids[i][j] == 0:
                    clusterids[i][j] = len(shapeverts) + 1
        clusterids = np.hstack(clusterids)

        tabindex = cfg.plot_segmentation_indices[it]
        # Stack segmented data tables for each image
        segmentedtab = []
        for i in range(cfg.num_imgs):
            segmentedtab.append(cfg.data_list[cfg.segmentation_indices[i + tabindex]])
        segmentedtab = np.vstack(segmentedtab)

        if np.max(clusterids) < len(labelnames):
            labelnames.remove("Other")
        cfg.cluster_names.append(labelnames)

        self.apply_object_clustering(clusterids,
                                     tabindex,
                                     segmentedtab,
                                     results_folder,
                                     add_grey_img,
                                     add_color_img,
                                     labelnames,
                                     )

        utils.log_actions(f"gui.manual_annotation(umapind={umapind}, add_grey_img={add_grey_img}, "
                          f"add_color_img={add_color_img}, labelnames={labelnames}, "
                          f"shapeverts={[verts.tolist() for verts in shapeverts]}, shapetypes={shapetypes})")

    def merge_clusters(self,
                       clusters_list=[],
                       add_grey_img=None,
                       add_color_img=None,
                       ):
        """
        Merge together all clusters that are checked in the currently-displayed table.

        Args:
            clusters_list (list, optional): List of lists of cluster IDs to be merged together (Default: []).
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """

        ### TODO: Only works for the current table... give an option to select clustering round if auto-merging.

        # Can't merge cells together, only clusters.
        if cfg.analysis_mode == "Segmentation":
            utils.display_error_message("Cannot merge cells together",
                                        "Please ensure that the table being displayed represents clusters, not cells.")
            return

        # One table for each image, plus a combined average table if using multiple images.
        analysisnum, numtabs = utils.find_analysis_round()

        # Initialize variables depending on whether user is working with pixel-based or object-based results.
        if cfg.analysis_mode == "Pixel":
            cluster_indices = cfg.pixel_cluster_indices
            column_labels = np.hstack([["Sample", "Cluster", "# Pixels"],
                                       cfg.pixel_cluster_markers[analysisnum]])
            cluster_directory = cfg.pixel_cluster_directories[analysisnum]
            paramnames = cfg.pixel_cluster_markers[analysisnum]
            num_objects_label = "# Pixels"
            min_cluster_size = 1000
            colors_list = cfg.pixel_cluster_colors
            ind = [i for i, m in enumerate(cfg.clusters_are_pixel_based) if m][analysisnum]
        else:
            cluster_indices = cfg.object_cluster_indices
            column_labels = np.hstack([["Sample", "Cluster", "# Cells"],
                                       cfg.markers,
                                       ["Area", "Eccentricity", "Perimeter", "Major Axis"]])
            cluster_directory = cfg.object_cluster_directories[analysisnum]
            paramnames = cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            num_objects_label = "# Cells"
            min_cluster_size = 1
            colors_list = cfg.object_cluster_colors
            ind = [i for i, m in enumerate(cfg.clusters_are_pixel_based) if not m][analysisnum]

        # Allow user to decide whether to select merged clusters manually or algorithmically.
        if clusters_list == []:
            merge_cluster_mode = utils.MergeClusterMode()
            merge_cluster_mode.exec()
            if not merge_cluster_mode.OK:
                return
            if merge_cluster_mode.manual_merge:
                clusters_list = [cfg.currently_selected[cfg.table_index]]
            else:
                tab_ind = cluster_indices[(analysisnum + 1) * numtabs - 1]
                col_list = colors_list[analysisnum]
                combined_avg_tab = cfg.data_list[tab_ind]
                desired_num_clusters = 90
                cluster_list = [85, 75, 65, 60, 55, 50]
                clustermap = ColoredDendrogramClustermap(
                    csv_path=pd.DataFrame(combined_avg_tab),
                    desired_num_clusters=desired_num_clusters,
                    window_size=3,
                    num_clusters=5,
                    num_simulations=100,
                    distance="euclidean",
                )
                for i, clusters in enumerate(cluster_list):
                    clustermap.create_colored_dendrogram_clustermap(col_list)
                    clustermap.desired_num_clusters = clusters
                    clustermap.merged_clustermap()
                    clustermap.csv_path = clustermap.merged_data_df
                    clustermap.round = 1
                clustermap.get_merged_ids()
                clusters_list = clustermap.merged_list

        # User must select more than one cluster to merge.
        if len(clusters_list[0]) <= 1:
            utils.display_error_message("Fewer than 2 clusters selected",
                                        "Please select at least 2 clusters from the table to be merged together.")
            return

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        utils.log_actions(f"gui.merge_clusters(clusters_list={clusters_list}, add_grey_img={add_grey_img}, "
                          f"add_color_img={add_color_img})")

        numclusters = len(colors_list[analysisnum])
        imganalysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == cfg.analysis_mode][
                             cfg.analysis_index // numtabs] * cfg.num_imgs

        merged_clusters = [cluster for sublist in clusters_list for cluster in sublist]
        old_cluster_ids = np.arange(numclusters + 1)
        new_cluster_ids = np.arange(numclusters + 1)
        for i, clusters in enumerate(clusters_list):
            for cluster in clusters:
                new_cluster_ids[cluster + 1] = np.max(old_cluster_ids) + i + 1
        new_cluster_ids = self.method_searchsort(np.unique(new_cluster_ids),
                                                 np.arange(len(np.unique(new_cluster_ids)) + 1),
                                                 new_cluster_ids,
                                                 )

        # Update each data table with weighted average data for each cluster being merged.
        data_index = cluster_indices[analysisnum * numtabs]
        for i in range(numtabs):
            data = cfg.data_list[data_index + i]
            for clusters in clusters_list:
                newcluster = np.zeros((1, data.shape[1]))
                newcluster[0, 0] = np.sum(data[clusters, 0])
                if newcluster[0, 0] > 0:
                    pixel_counts = data[clusters, 0]
                    if cfg.analysis_mode == "Object":
                        pixel_counts *= data[clusters, -4]
                    newcluster[0, 1:] = np.average(data[clusters, 1:], axis=0, weights=pixel_counts)
                data = np.vstack((data, newcluster))
            data = np.delete(data, merged_clusters, axis=0)
            cfg.data_list[data_index + i] = data

        # Save combined data table with all clusters across all images to output folder.
        data_tab = np.vstack([cfg.data_list[ind] for ind in range(data_index, data_index + cfg.num_imgs)])
        img_ids = np.array([np.repeat(ind + 1, len(cfg.data_list[data_index + ind])) for ind in range(cfg.num_imgs)])
        img_ids = np.expand_dims(img_ids.flatten(), 1)
        cluster_ids = np.array([np.arange(1, len(cfg.data_list[data_index + ind]) + 1) for ind in range(cfg.num_imgs)])
        cluster_ids = np.expand_dims(cluster_ids.flatten(), 1)
        full_tab = np.hstack((img_ids, cluster_ids, data_tab))
        combined_dataframe = pd.DataFrame(np.nan_to_num((full_tab)))
        combined_dataframe.columns = column_labels
        outfolder = utils.create_new_folder(os.path.join(os.path.split(cluster_directory)[-1],
                                                         "Merged_",
                                                         ),
                                            cfg.output_folder,
                                            )
        combined_dataframe.to_csv(os.path.join(outfolder,
                                               f"{cfg.analysis_mode}ClusterAvgExpressionVals.csv",
                                               ))
        if cfg.analysis_mode == "Pixel":
            combined_dataframe["Cluster"] = combined_dataframe["Cluster"] - 1

        # Update cluster names where necessary.
        if not cfg.cluster_names[ind] == []:
            for clusters in clusters_list:
                newname = cfg.cluster_names[ind][clusters[-1]]
                for cluster in clusters:
                    oldname = cfg.cluster_names[ind].pop(cluster)
                    if cfg.analysis_mode == "Object":
                        cells_in_current_cluster = cfg.object_cluster_dfs[analysisnum]['Cluster'] == oldname
                        cfg.object_cluster_dfs[analysisnum]['Cluster'][cells_in_current_cluster] = newname
                cfg.cluster_names[ind].append(newname)

        elif cfg.cluster_names[ind] == [] and cfg.analysis_mode == "Object":
            clusterids = np.array(cfg.object_cluster_dfs[analysisnum]["Cluster"]).astype(int)
            clusterids = self.method_searchsort(old_cluster_ids,
                                                new_cluster_ids,
                                                clusterids,
                                                )
            cfg.object_cluster_dfs[analysisnum]['Cluster'] = [str(id) for id in clusterids]

        # Relabel clustered results and table order variables to account for new cluster labels.
        for i in range(cfg.num_imgs):
            cfg.labeled_imgs[imganalysisnum + i] = self.method_searchsort(old_cluster_ids,
                                                                          new_cluster_ids,
                                                                          cfg.labeled_imgs[imganalysisnum + i],
                                                                          )

        cfg.current_table_order_full = self.method_searchsort(old_cluster_ids - 1,
                                                              new_cluster_ids - 1,
                                                              cfg.current_table_order_full,
                                                              )
        cfg.current_table_orders_filtered[cfg.table_index] = self.method_searchsort(old_cluster_ids - 1,
                                                                                    new_cluster_ids - 1,
                                                                                    cfg.current_table_orders_filtered[
                                                                                        cfg.table_index],
                                                                                    )

        # Remove old cluster mask images from the GUI
        if cfg.cluster_names[ind] == []:
            cluster_names = [f"Cluster {cluster + 1} ({cfg.analysis_mode} [{analysisnum}])" for cluster in
                             merged_clusters]
        else:
            cluster_names = [cfg.cluster_names[ind][cluster] for cluster in merged_clusters]
        for i in reversed(range(len(cfg.viewer.layers))):
            if cfg.viewer.layers[i].name in cluster_names:
                cfg.viewer.layers.pop(i)

        # Update clustering dataframe and cell-cluster mappings that are specific for object-based analysis.
        if cfg.analysis_mode == "Object":
            cfg.object_cluster_dfs[analysisnum].to_csv(os.path.join(outfolder, "SegmentationClusterIDs.csv"))
            for i in range(cfg.num_imgs):
                cfg.cell_cluster_vals[analysisnum * cfg.num_imgs + i] = self.method_searchsort(old_cluster_ids,
                                                                                               new_cluster_ids,
                                                                                               cfg.cell_cluster_vals[
                                                                                                   analysisnum * cfg.num_imgs + i])

        # Create a colored image from the newly-labeled image, and add it to the viewer.
        newrgb = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1], 3)).astype(np.uint8)
        colors = colors_list[analysisnum]
        newcolors = colors[[clusters[-1] for clusters in clusters_list], :]
        colors = np.delete(colors, merged_clusters, 0)
        colors = np.append(colors, newcolors, 0)
        if cfg.analysis_mode == "Pixel":
            cfg.pixel_cluster_colors[analysisnum] = colors
        else:
            cfg.object_cluster_colors[analysisnum] = colors

        labelimg = self.concat_label_imgs(
            [cfg.labeled_imgs[ind] for ind in range(imganalysisnum, imganalysisnum + cfg.num_imgs)])
        for i in range(cfg.num_imgs):
            for j in range(len(colors)):
                mask = np.zeros((newrgb.shape[1], newrgb.shape[2]), dtype=np.bool)
                mask[:cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = cfg.labeled_imgs[imganalysisnum + i] == j + 1
                newrgb[i, :, :, :][mask] = colors[j, :]

        np.save(os.path.join(outfolder, "color.npy"), colors)
        samplenames = [os.path.splitext(os.path.split(imgname)[-1])[0] for imgname in cfg.file_names]
        tabledata, my_data_scaled, distmatrix, uniqueclusters = prep_for_mst(clustertable=combined_dataframe,
                                                                             minclustersize=min_cluster_size,
                                                                             clustersizes=combined_dataframe[
                                                                                 num_objects_label],
                                                                             includedmarkers=paramnames,
                                                                             )
        generate_mst(distancematrix=distmatrix,
                     normalizeddf=my_data_scaled[my_data_scaled.columns],
                     colors=colors,
                     randomseed=0,
                     outfolder=outfolder,
                     clusterheatmap=True,
                     displaymarkers=paramnames,
                     uniqueclusters=uniqueclusters,
                     samplenames=samplenames,
                     displaysingle=False,
                     values=num_objects_label,
                     )

        # Add image(s) to the viewer.
        self.set_invisible(cfg.viewer)
        if add_grey_img:
            cfg.viewer.add_image(labelimg,
                                 name=f"Merged {cfg.analysis_mode} Cluster IDs {analysisnum}",
                                 blending="additive",
                                 contrast_limits=[0, np.max(labelimg)],
                                 )
        if add_color_img:
            cfg.viewer.add_image(newrgb,
                                 name=f"Merged {cfg.analysis_mode} Clusters {analysisnum}",
                                 blending="additive",
                                 )
        cfg.viewer.layers[-1].visible = True

        cfg.viewer.add_image(imread(os.path.join(outfolder, "MeanExpressionHeatmap.png")),
                             name=f"Merged {cfg.analysis_mode} Clusters {analysisnum} Heatmap",
                             blending="additive",
                             visible=False,
                             )

        # Save both the label and colored images to the output folder.
        for i in range(cfg.num_imgs):
            imgname = os.path.splitext(os.path.split(cfg.file_names[i])[-1])[0]
            utils.save_img(os.path.join(outfolder, f"{cfg.analysis_mode}Clusters_{imgname}.tif"),
                           newrgb[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1], :],
                           cfg.img_is_flipped[i],
                           )
            utils.save_img(os.path.join(outfolder, f"{cfg.analysis_mode}ClusterLabels_{imgname}.tif"),
                           labelimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] + 1,
                           cfg.img_is_flipped[i],
                           )

        # Reset the current selected cells for each of the corresponding tables to be empty.
        clustermodeindex = cluster_indices.index(cfg.table_index)
        startind = cfg.table_index - clustermodeindex % numtabs
        for i in range(startind, startind + numtabs):
            cfg.currently_selected[i] = []

        # Update the table to reflect the merged clusters.
        newdisplaydata = cfg.data_list[cfg.table_index][cfg.current_table_orders_filtered[cfg.table_index], :]
        self.update_table(newdisplaydata,
                          cfg.lower_bounds_list[cfg.table_index],
                          cfg.upper_bounds_list[cfg.table_index],
                          len(cfg.current_table_orders_filtered[cfg.table_index]),
                          cfg.current_table_orders_filtered[cfg.table_index],
                          headernames=cfg.cluster_names[ind],
                          )

        self.sort_table_image()

    def merge_markers(self,
                      nucmarkernums=[],
                      nucalg="",
                      memmarkernums=[],
                      memalg="",
                      nuccls=[],
                      memcls=[],
                      ):
        """
        Merge together all nuclear and/or membrane markers, as defined by the user, to prepare for segmentation.

        Args:
            nucmarkernums (list, optional): List of indices of each nuclear cell marker being combined (Default: []).
            nucalg (str, optional): Algorithm being used to combine the nuclear cell markers (Default: "").
            memmarkernums (list, optional): List of indices of each membrane cell marker being combined (Default: []).
            memalg (str, optional): Algorithm being used to combine the membrane cell markers (Default: "").
            nuccls (list, optional): List of lists containing lower and upper contrast limits for each of the nuclear markers being merged (Default: []).
            memcls (list, optional): List of lists containing lower and upper contrast limits for each of the membrane markers being merged (Default: []).
        """
        # At least one image must be loaded in order to merge markers.
        if len(cfg.markers) == 0:
            utils.display_error_message("Please open an image first",
                                        "Begin by opening the image(s) that you would like to train RAPID on")
            return

        if (nucmarkernums == [] or nucalg == "") and (memmarkernums == [] or memalg == ""):
            # Notify user that contrast limits are accounted for when merging markers.
            if len(cfg.merge_mem_markers) == 0:
                utils.display_error_message("Double-check contrast limits before proceeding",
                                            "Current contrast limits for each of the markers being merged together will be "
                                            "accounted for when segmenting. If you would like to use the raw data values "
                                            "for this, exit out of the next popup window and reset the contrast limits "
                                            "either manually or by clicking the \"Reset Metadata\" button in the \"Image "
                                            "Visualization\" module")

            # Define which nuclear markers to use for segmentation
            nucmarkers = utils.MergeMarkers(False, nucmarkernums, nucalg)
            nucmarkers.exec()
            if not nucmarkers.OK:
                return
            nucmarkernums = nucmarkers.markernums
            nucalg = nucmarkers.alg

            # Define which membrane markers to use for segmentation
            memmarkers = utils.MergeMarkers(True, memmarkernums, memalg)
            memmarkers.exec()
            if not memmarkers.OK:
                return
            memmarkernums = memmarkers.markernums
            memalg = memmarkers.alg

        mergednucmarkers = [cfg.markers[i] for i in nucmarkernums]
        mergedmemmarkers = [cfg.markers[i] for i in memmarkernums]

        # Check that the user defined at least one cell marker to use.
        if len(memmarkernums) == 0 and len(nucmarkernums) == 0:
            utils.display_error_message("No cell markers selected",
                                        "Please select at least one nuclear and/or membrane marker to use for segmentation.")
            return

        # Open zarr file where data will be saved.
        path = utils.create_new_folder("MergedImage", cfg.output_folder)
        cfg.merge_img_paths.append(path)
        fh = zarr.open(path, mode='a')
        cfg.segment_counts.append([-1, -1, -1])
        cfg.histogram_counts.append([-1, -1])

        # Merge nuclear markers together if any nuclear markers were selected.
        cfg.viewer.status = "Merging nuclear markers..."
        nucdata = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]), dtype=np.uint8)

        if nuccls == []:
            for i in range(len(nucmarkernums)):
                nuccls.append(cfg.viewer.layers[nucmarkernums[i]].contrast_limits)

        if len(nucmarkernums) > 0:
            if nucalg == "avg":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(cfg.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       nuccls[i],
                                                       )
                    nucdata += (image / len(nucmarkernums)).astype(np.uint8)
                    cfg.viewer.status = f"Merged {cfg.markers[nucmarkernums[i]]}"
            if nucalg == "sum":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(cfg.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       nuccls[i],
                                                       )
                    nucdata += np.minimum(255 - nucdata, image)
                    cfg.viewer.status = f"Merged {cfg.markers[nucmarkernums[i]]}"
            if nucalg == "max":
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(cfg.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       nuccls[i],
                                                       )
                    nucdata = np.maximum(nucdata, image)
                    cfg.viewer.status = f"Merged {cfg.markers[nucmarkernums[i]]}"
            if nucalg == "median":
                img = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1], len(nucmarkernums)),
                               dtype=np.uint8)
                for i in range(len(nucmarkernums)):
                    image = copy.deepcopy(cfg.viewer.layers[nucmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       nuccls[i],
                                                       )
                    img[:, :, :, i] = image
                    cfg.viewer.status = f"Merged {cfg.markers[nucmarkernums[i]]}"
                nucdata = np.median(img, axis=3)
        fh.create_dataset("Nucleus", data=nucdata, dtype=np.uint8)
        cfg.merge_nuc_markers.append(len(nucmarkernums) > 0)

        # Merge membrane markers together if any membrane markers were selected.
        cfg.viewer.status = "Merging membrane markers..."
        memdata = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]), dtype=np.uint8)

        if memcls == []:
            for i in range(len(memmarkernums)):
                memcls.append(cfg.viewer.layers[memmarkernums[i]].contrast_limits)

        if len(memmarkernums) > 0:
            if memalg == "avg":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(cfg.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       memcls[i],
                                                       )
                    memdata += (image / len(memmarkernums)).astype(np.uint8)
                    cfg.viewer.status = f"Merged {cfg.markers[memmarkernums[i]]}"
            if memalg == "sum":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(cfg.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       memcls[i],
                                                       )
                    memdata += np.minimum(255 - memdata, image)
                    cfg.viewer.status = f"Merged {cfg.markers[memmarkernums[i]]}"
            if memalg == "max":
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(cfg.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       memcls[i],
                                                       )
                    memdata = np.maximum(memdata, image)
                    cfg.viewer.status = f"Merged {cfg.markers[memmarkernums[i]]}"
            if memalg == "median":
                img = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1], len(memmarkernums)),
                               dtype=np.uint8)
                for i in range(len(memmarkernums)):
                    image = copy.deepcopy(cfg.viewer.layers[memmarkernums[i]].data)
                    image = self.apply_contrast_limits(image,
                                                       memcls[i],
                                                       )
                    img[:, :, :, i] = image
                    cfg.viewer.status = f"Merged {cfg.markers[memmarkernums[i]]}"
                memdata = np.median(img, axis=3)
        fh.create_dataset("Membrane", data=memdata, dtype=np.uint8)
        self.set_invisible(cfg.viewer)
        cfg.merge_mem_markers.append(len(memmarkernums) > 0)

        # Add merged image to the viewer
        if mergednucmarkers and mergedmemmarkers:
            cfg.viewer.add_image(np.stack([memdata, nucdata],
                                          axis=0,
                                          ),
                                 name=f'Merged Image {len(cfg.segment_counts)}',
                                 blending="additive",
                                 contrast_limits=[0, 255],
                                 )
        elif mergednucmarkers:
            cfg.viewer.add_image(nucdata,
                                 name=f'Merged Image {len(cfg.segment_counts)}',
                                 blending="additive",
                                 contrast_limits=[0, 255],
                                 )
        else:
            cfg.viewer.add_image(memdata,
                                 name=f'Merged Image {len(cfg.segment_counts)}',
                                 blending="additive",
                                 contrast_limits=[0, 255],
                                 )

        utils.log_actions(f"gui.merge_markers(nucmarkernums={nucmarkernums}, nucalg=\"{nucalg}\", "
                          f"memmarkernums={memmarkernums}, memalg=\"{memalg}\", nuccls={nuccls}, memcls={memcls})")
        cfg.viewer.status = "Finished merging markers"

    def method_searchsort(self,
                          from_values,
                          to_values,
                          array,
                          ):
        """
        Relabels an array.

        Args:
            from_values (numpy.ndarray): Original values from the array.
            to_values (numpy.ndarray): Final values defining the transformation.
            array (numpy.ndarray): Input array whose values will be updated.

        :return: out *(numpy.ndarray)*: \n
            Relabeled array.
        """

        sort_idx = np.argsort(from_values)
        idx = np.searchsorted(from_values,
                              array,
                              sorter=sort_idx,
                              )
        out = to_values[sort_idx][idx]
        return out

    ### TODO: Add option for user to select which parameters to use for this (Currently -- cell markers, no morphology)
    def minimum_spanning_tree(self,
                              clusteringindex=None,
                              ):
        """
        Generate a minimum spanning tree plot to illustrate phenotypic similarity of clusters for a user-defined round
        of clustering.

        Args:
            clusteringindex (int, optional): Index of clustering round being used for analysis (Default: None).
        """
        # Random seed for reproducibility.
        np.random.seed(0)

        # Check that the user has performed at least one clustering algorithm.
        if len(cfg.clusters_are_pixel_based) == 0:
            utils.display_error_message("No clustering results found",
                                        "MST can only be performed on the results of pixel or object clustering.")
            return

        # If clustering has only been performed once, use those results.
        if len(cfg.clusters_are_pixel_based) == 1:
            clusteringindex = 0

        # If multiple rounds of clustering have been performed, prompt the user to select which one to use.
        elif clusteringindex is None:
            selectclusteringround = utils.SelectClusteringRound()
            selectclusteringround.exec()
            if not selectclusteringround.OK:
                return
            clusteringindex = selectclusteringround.clusteringindex

        ispixelcluster = cfg.clusters_are_pixel_based[clusteringindex]
        clustermodeindex = [i for i, ispixelbased in enumerate(cfg.clusters_are_pixel_based) if
                            ispixelbased == ispixelcluster].index(clusteringindex)

        # Retrieve the dataset being used for MST and create the output folder where images will be saved.
        if ispixelcluster:
            if cfg.num_imgs == 1:
                currentdata = np.expand_dims(cfg.data_list[cfg.pixel_cluster_indices[clustermodeindex]], axis=0)
            else:
                startindex = clustermodeindex * (cfg.num_imgs + 1)
                s = cfg.data_list[cfg.pixel_cluster_indices[startindex]].shape
                currentdata = np.zeros((cfg.num_imgs + 1, s[0], s[1]))
                for i in range(cfg.num_imgs + 1):
                    currentdata[i, :, :] = cfg.data_list[cfg.pixel_cluster_indices[i + startindex]]
            outfolder = utils.create_new_folder("PixelMST", cfg.output_folder)
        else:
            if cfg.num_imgs == 1:
                currentdata = np.expand_dims(cfg.data_list[cfg.object_cluster_indices[clustermodeindex]], axis=0)
            else:
                startindex = clustermodeindex * (cfg.num_imgs + 1)
                s = cfg.data_list[cfg.object_cluster_indices[startindex]].shape
                currentdata = np.zeros((cfg.num_imgs + 1, s[0], s[1]))
                for i in range(cfg.num_imgs + 1):
                    currentdata[i, :, :] = cfg.data_list[cfg.object_cluster_indices[i + startindex]]
            outfolder = utils.create_new_folder("ObjectMST", cfg.output_folder)

        # Generate an MST for each image, plus the combined results if using multiple images.
        pathlist = []
        for i in range(len(currentdata)):
            # Retrieve the clustered data table for the current image.
            tabdata = DataFrame(currentdata[i, :, 1:-4])

            # Convert data to a distance matrix, and use that to generate the MST.
            distmatrix = np.nan_to_num(distance.cdist(currentdata[i, :, 1:-4], currentdata[i, :, 1:-4], 'euclidean'))
            pd.DataFrame(distmatrix).to_csv(os.path.join(outfolder, f"DistMatrix{i + 1}.csv"))
            G = nx.from_numpy_matrix(distmatrix)
            rowname = tabdata.iloc[[i for i in range(len(tabdata.values))]].astype(int).index.tolist()
            rowname = [round(x) + 1 for x in rowname]
            dictionary = dict(zip(G.nodes, rowname))
            G = nx.relabel_nodes(G, dictionary)
            T = nx.minimum_spanning_tree(G)

            # Plot MST on a graph, with nodes colored consistently with their corresponding clusters.
            colorlist = generate_colormap(len(tabdata) + 1)[:, [2, 1, 0]]
            plt.figure(figsize=(10, 10))
            ax = plt.axes()
            ax.set_facecolor("#F8F9F9")
            colormap = []
            for node in T:
                colormap.append(matplotlib.colors.rgb2hex(colorlist[int(node) - 1, :] / 255))
            nx.draw_networkx(T, node_color=colormap, with_labels=True, node_size=100, font_size=5,
                             font_family='sans-serif')
            plt.show(block=False)

            # Define name if using multi-image object-clustering results for combined average data, and save the
            # plot.
            if not ispixelcluster and i == len(currentdata) - 1 and cfg.num_imgs > 1:
                plt.title("Minimum spanning tree (Combined Images) - Object")
                plt.savefig(os.path.join(outfolder, "MST_Combined.png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, "MST_Combined.png"))
            # Define name if using object-clustering results for single-image data, and save the plot.
            elif not ispixelcluster:
                imgname = os.path.splitext(os.path.split(cfg.file_names[i])[-1])[0]
                plt.title(f"Minimum spanning tree ({imgname}) - Object")
                plt.savefig(os.path.join(outfolder, imgname + ".png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, imgname + ".png"))
            # Define name if using multi-image pixel-clustering results for combined average data, and save the
            # plot.
            elif ispixelcluster and i == len(currentdata) - 1 and cfg.num_imgs > 1:
                plt.title("Minimum spanning tree (Combined Images) - Pixel")
                plt.savefig(os.path.join(outfolder, "MST_Combined.png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, "MST_Combined.png"))
            # Define name if using pixel-clustering results for single-image data, and save the plot.
            elif ispixelcluster:
                imgname = os.path.splitext(os.path.split(cfg.file_names[i])[-1])[0]
                plt.title(f"Minimum spanning tree ({imgname}) - Pixel")
                plt.savefig(os.path.join(outfolder,
                                         imgname + ".png",
                                         ),
                            format="PNG",
                            dpi=300,
                            )
                pathlist.append(os.path.join(outfolder, imgname + ".png"))

        # Add all MST plots to the viewer as a single stacked image.
        arrays = np.array([imread(fn) for fn in pathlist])
        self.set_invisible(cfg.viewer)
        cfg.viewer.add_image(arrays,
                             name=f"MST (Pixel {clustermodeindex + 1}" if ispixelcluster else f"MST (Object {clustermodeindex + 1})",
                             blending="additive",
                             )
        utils.log_actions(f"gui.minimum_spanning_tree(clusteringindex={clusteringindex})")

    ### TODO: Rename images to reflect clustering round and NN count.
    def nearest_neighbours(self,
                           imgname="",
                           clusteringindex=None,
                           sourcecluster=None,
                           targetcluster=None,
                           radius=None,
                           numnn=None,
                           ):
        """
        Perform a nearest neighbours analysis to find the cells in one cluster that are within a specified radius or
        number of nearest neighbours from any cell in a different cluster, display those cells in the GUI, and quantify
        how the phenotypes of those cells compare to those of the cluster as a whole.

        Args:
            imgname (str, optional): Name of image to be used for NN analysis (Default: "").
            clusteringindex (int, optional): Round of clustering to be used for NN analysis (Default: None).
            sourcecluster (int, optional): ID for the source cluster (Default: None).
            targetcluster (int, optional): ID for the target cluster (Default: None).
            radius (float, optional): Maximum distance from source cluster to search for cells from target cluster (Default: None).
            numnn (int, optional): Maximum number of nearest neighbours from each cell in the source cluster to search for cells from target cluster (Default: None).
        """
        # Can either use an individual image, or all images combined.
        imgnames = [str(file.split("/")[-1].split(".")[0]) for file in cfg.file_names] + ["All"]
        if imgname == "":
            if len(cfg.file_names) > 1:
                imgname = utils.SelectNNImgs()
                imgname.exec()
                if not imgname.OK:
                    return
                imgname = imgname.selimg
            else:
                imgname = "All"

        if cfg.num_imgs == 1:
            selectedimgindex = 0
        elif imgname == "All":
            selectedimgindex = len(cfg.file_names)
        else:
            selectedimgindex = imgnames.index(imgname)

        # Determine which round of segmentation to use.
        if clusteringindex is None:
            clusteredsegresults = [cfg.object_img_names[i] for i, l in enumerate(cfg.segmentation_clustering_rounds) if
                                   len(l) > 0]
            if len(clusteredsegresults) > 1:
                segmentedimage = utils.SelectSegmentedImage(clusteredsegresults)
                segmentedimage.exec()
                if not segmentedimage.OK:
                    return
                segindex = cfg.object_img_names.index(segmentedimage.image)
            elif len(clusteredsegresults) == 1:
                segindex = cfg.object_img_names.index(clusteredsegresults[0])
            else:
                utils.display_error_message("No object-based clustering results found.",
                                            "Must perform object-based clustering before running nearest neighbour analysis.")
                return

            if len(cfg.segmentation_clustering_rounds[segindex]) > 1:
                iteration = utils.ObjectClusterIteration(cfg.segmentation_clustering_rounds[segindex])
                iteration.exec()
                if not iteration.OK:
                    return
                clusteringindex = iteration.iteration
            else:
                clusteringindex = cfg.segmentation_clustering_rounds[segindex][0]

        for i, segmentationclusteringrounds in enumerate(cfg.segmentation_clustering_rounds):
            if clusteringindex in segmentationclusteringrounds:
                segindex = i
        analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Segmentation"][segindex] * cfg.num_imgs

        # Get all the cluster IDs in the selected clustered image, and prompt the user to define source and
        # target clusters.
        tabdata = cfg.object_cluster_dfs[clusteringindex]
        numtabs = 1
        if len(cfg.file_names) > 1:
            numtabs += len(cfg.file_names)
        clusteringround = clusteringindex * numtabs + selectedimgindex
        print(clusteringindex)
        print(numtabs)
        print(selectedimgindex)
        tableindex = cfg.object_cluster_indices[clusteringround]
        data = cfg.data_list[tableindex]

        # Find current names of clusters.
        annotatedobjectclusters = [cfg.cluster_names[i] for i in range(len(cfg.cluster_names)) if
                                   not cfg.clusters_are_pixel_based[i]]

        cluster_ids = [ind for ind in range(len(data)) if data[ind, 0] > 0.0]
        if len(annotatedobjectclusters[clusteringindex]) == 0:
            currentnames = [ind + 1 for ind in cluster_ids]
        else:
            currentnames = [annotatedobjectclusters[clusteringindex][ind] for ind in cluster_ids]

        if any(param is None for param in (sourcecluster, targetcluster, radius, numnn)):
            nndis = utils.NNInRadius(currentnames)
            nndis.exec()
            if not nndis.OK:
                return
            sourcecluster = nndis.sourcecluster
            targetcluster = nndis.targetcluster
            radius = nndis.radius
            numnn = nndis.numnn

        # Generate heatmap demonstrating differential marker expression between NN cells and cluster average,
        # and add to the viewer.
        if imgname == "All":
            # Show all cells from the target cluster within specified radius and/or number of nearest neighbours
            # from a cell in the source cluster.
            for i in range(cfg.num_imgs):
                cellind = utils.get_nn_in_radius(data=tabdata[tabdata['ImgID'] == i + 1],
                                                 clusterid1=sourcecluster,
                                                 clusterid2=targetcluster,
                                                 radius=radius,
                                                 nn=numnn,
                                                 )
                nnimg = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1]),
                                 dtype=np.bool,
                                 )
                mask = np.in1d(cfg.labeled_imgs[analysisnum + i],
                               cellind,
                               )
                mask = mask.reshape((cfg.img_shape_list[i][0], cfg.img_shape_list[i][1]))
                nnimg[0, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = mask
                if i == 0:
                    cfg.viewer.add_image(nnimg,
                                         name="NN",
                                         blending="additive",
                                         visible=True,
                                         )
                else:
                    cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, nnimg))
            sbb = utils.nn_to_heatmap(data=tabdata,
                                      clusterid1=sourcecluster,
                                      radius=radius,
                                      nn=numnn,
                                      )
        else:
            # Show all cells from the target cluster within specified radius and/or number of nearest neighbours
            # from a cell in the source cluster.
            cellind = utils.get_nn_in_radius(data=tabdata[tabdata['ImgID'] == selectedimgindex + 1],
                                             clusterid1=sourcecluster,
                                             clusterid2=targetcluster,
                                             radius=radius,
                                             nn=numnn,
                                             )
            mask = np.in1d(cfg.labeled_imgs[analysisnum + selectedimgindex].astype(np.uint32),
                           cellind,
                           )
            mask = mask.reshape((cfg.img_shape_list[selectedimgindex][0], cfg.img_shape_list[selectedimgindex][1]))
            cfg.viewer.add_image(mask,
                                 name="NN",
                                 blending="additive",
                                 visible=True,
                                 )
            sbb = utils.nn_to_heatmap(data=tabdata[tabdata['ImgID'] == selectedimgindex + 1],
                                      clusterid1=sourcecluster,
                                      radius=radius,
                                      nn=numnn,
                                      )
        plt.setp(sbb.ax_heatmap.yaxis.get_majorticklabels(),
                 rotation=0,
                 )
        buf = io.BytesIO()
        sbb.savefig(buf)
        buf.seek(0)
        heatimg = Image.open(buf)
        self.set_invisible(cfg.viewer)
        cfg.viewer.add_image(np.array(heatimg),
                             name="NN Enrichment",
                             blending="additive",
                             visible=True,
                             )
        utils.log_actions(f"gui.nearest_neighbours(imgname=\"{imgname}\", clusteringindex={clusteringindex}, "
                          f"sourcecluster={sourcecluster}, targetcluster={targetcluster}, radius={radius}, "
                          f"numnn={numnn})")

    def object_clustering(self,
                          markernums=[],
                          segindex=None,
                          algname="",
                          modelpath="",
                          add_grey_img=None,
                          add_color_img=None,
                          continuetraining=None,
                          normalize="",
                          pca=False,
                          modelparams=[],
                          ):
        """
        Perform object-based clustering on a segmented image using the algorithm selected by the user.

        Args:
            markernums (list, optional): List of indices of parameters to be considered for clustering (Default: []).
            segindex (int, optional): Index of segmentation round being clustered (Default: None).
            algname (str, optional): Name of the specified algorithm to be used for clustering (Default: "").
            modelpath (str, optional): Path to the model being used if loading a pretrained model (Default: "").
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            continuetraining (bool, optional): If True, continue training the model after loading it. Otherwise, predict without further training (Default: None).
            normalize (str, optional): Normalization algorithm to be used for data preprocessing (Default: "").
            pca (bool, optional): If True, apply PCA reduction to normalized data. Otherwise, do nothing (Default: None).
            modelparams (iterable, optional): List of parameters for the desired clustering algorithm (Default: []).
        """
        # Can only perform clustering if segmentation has been done
        if cfg.segment_count == 0:
            utils.display_error_message("You must segment before running object-based clustering",
                                        "Object-based clustering cannot be done until the image has been segmented")
            return

        # Define which markers will be used for clustering
        if markernums == []:
            trainmarkers = utils.RAPIDObjectParams()
            trainmarkers.exec()
            if not trainmarkers.OK:
                return
            markernums = trainmarkers.markernums

        # Define which algorithm will be used for clustering
        if segindex is None and algname == "" or algname == "Pretrained" and modelpath == "":
            alg = utils.ClusteringAlgorithm()
            alg.exec()
            if not alg.OK:
                return
            segindex = alg.segindex
            algname = alg.algname
            if algname == "Pretrained":
                modelpath = alg.dirpath
        imagenum = segindex * cfg.num_imgs

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        # Load model, indicate whether to continue training or use for prediction, and define parameters for
        # whichever algorithm was selected by the user
        if algname == "Pretrained":
            try:
                hf = zarr.open("/".join(modelpath[:-1]), 'r')
                loadedargs = hf.attrs['arg']
            except:
                return

            if continuetraining is None:
                loadoptions = utils.LoadModelOptions()
                loadoptions.exec()
                if not loadoptions.OK:
                    return
                continuetraining = not loadoptions.prediction

            args = Namespace(**loadedargs)

            if continuetraining:
                if modelparams == []:
                    params = utils.RAPIDObjectTrainLoadedParameters(args)
                    params.exec()
                    if not params.OK:
                        return
                    args.nit = int(params.nit)
                    args.bs = int(params.bs)
                    args.lr = float(params.lr)
                    args.blankpercent = float(params.blankpercent)
                    modelparams = args.nit, args.bs, args.lr, args.blankpercent
                else:
                    args.nit, args.bs, args.lr, args.blankpercent = modelparams
                args.epoch = 1
                args.GUI = True
                args.distance = 'YES'

        elif algname == "RAPID":
            continuetraining = True
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = utils.RAPIDObjectParameters(len(markernums))
                params.exec()
                if not params.OK:
                    return
                args.ncluster = int(params.nc)
                args.nit = int(params.nit)
                args.bs = int(params.bs)
                if params.mse == "True":
                    args.mse = True
                args.normalize = params.normalize
                args.lr = float(params.lr)
                args.blankpercent = float(params.blankpercent)
                pca = params.pca
                modelparams = args.ncluster, args.nit, args.bs, args.mse, args.normalize, args.lr, args.blankpercent, pca
            else:
                args.ncluster, args.nit, args.bs, args.mse, args.normalize, args.lr, args.blankpercent, pca = modelparams
            args.epoch = 1
            args.GUI = True
            args.distance = 'YES'

        elif algname == "SciPy":
            continuetraining = True
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = utils.SciPyParameters()
                params.exec()
                if not params.OK:
                    return
                args.normalize = params.normalize
                args.scipyalgo = params.scipyalgo
                args.scipykwarg = params.scipykwarg
                pca = params.pca
                modelparams = args.normalize, args.scipyalgo, args.scipykwarg, pca
            else:
                args.normalize, args.scipyalgo, args.scipykwarg, pca = modelparams
            args.GUI = True

        else:
            continuetraining = True
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = utils.PhenographParameters()
                params.exec()
                if not params.OK:
                    return
                args.PGdis = str(params.PGdis)
                args.PGnn = int(params.PGnn)
                args.PGres = float(params.PGres)
                args.normalize = params.normalize
                args.graphalgo = params.graphalgo
                pca = params.pca
                modelparams = args.PGdis, args.PGnn, args.PGres, args.normalize, args.graphalgo, pca
            else:
                args.PGdis, args.PGnn, args.PGres, args.normalize, args.graphalgo, pca = modelparams
            args.GUI = True

        # Count total number of cells for segmented image used for clustering
        numcells = 0
        for i in range(cfg.num_imgs):
            numcells += len(cfg.data_list[cfg.segmentation_indices[i + imagenum]])

        # Store normalized cell marker expression
        expressionavgs = np.zeros((numcells, len(markernums)))
        if args.normalize == "zscale":
            scaler = StandardScaler()
            count = 0
            for i in range(cfg.num_imgs):
                numcells = len(cfg.data_list[cfg.segmentation_indices[i + imagenum]])
                img = copy.deepcopy(cfg.data_list[cfg.segmentation_indices[i + imagenum]][:, markernums])
                scaler.fit(img)
                expressionavgs[count:count + numcells, :] = scaler.transform(img)
                count += numcells
        else:
            count = 0
            for i in range(cfg.num_imgs):
                numcells = len(cfg.data_list[cfg.segmentation_indices[i + imagenum]])
                expressionavgs[count:count + numcells, :] = cfg.data_list[cfg.segmentation_indices[i + imagenum]][:,
                                                            markernums]
                count += numcells

            if args.normalize == "all":
                scaler = StandardScaler()
                scaler.fit(expressionavgs)
                expressionavgs = scaler.transform(expressionavgs)
                if pca:
                    expressionavgs = run_pca(data=expressionavgs, numcomponents=0.999)
            elif args.normalize == "log10":
                expressionavgs = np.nan_to_num(np.log10(expressionavgs),
                                               nan=0,
                                               posinf=0,
                                               neginf=0,
                                               )
            elif args.normalize == "log2":
                expressionavgs = np.nan_to_num(np.log2(expressionavgs),
                                               nan=0,
                                               posinf=0,
                                               neginf=0,
                                               )

        # Train algorithm if necessary, and then apply to segmented image.
        cfg.viewer.status = "RAPID clustering..."
        self.set_invisible(cfg.viewer)
        results_folder = utils.create_new_folder("RAPIDObject_", cfg.output_folder)
        cfg.object_cluster_directories.append(results_folder)
        if not continuetraining:
            model = RAPIDMixNet(dimension=len(markernums),
                                nummodules=5,
                                mse=args.mse,
                                numclusters=int(args.ncluster),
                                )
            optimizer = optim.AdamW(model.parameters(),
                                    lr=float(args.lr),
                                    betas=(0.9, 0.999),
                                    eps=1e-08,
                                    weight_decay=0.01,
                                    amsgrad=False,
                                    )
            model.apply(weight_init)
            model = load_checkpoint("/".join(modelpath), model, optimizer)
            self.test_object(model,
                             expressionavgs,
                             args,
                             list(range(len(cfg.markers) + 4)),
                             add_grey_img,
                             add_color_img,
                             "RAPID",
                             imagenum,
                             optimizer=optimizer,
                             results_folder=results_folder,
                             predict=True,
                             )
        else:
            if algname == "Phenograph":
                model = 0
                self.test_object(model,
                                 expressionavgs,
                                 args,
                                 list(range(len(cfg.markers) + 4)),
                                 add_grey_img,
                                 add_color_img,
                                 "Phenograph",
                                 imagenum,
                                 results_folder=results_folder,
                                 )
                pass
            elif algname == "SciPy":
                model = 0
                self.test_object(model,
                                 expressionavgs,
                                 args,
                                 list(range(len(cfg.markers) + 4)),
                                 add_grey_img,
                                 add_color_img,
                                 args.scipyalgo,
                                 imagenum,
                                 results_folder=results_folder,
                                 )
                pass
            else:
                hf = zarr.open(results_folder, 'a')
                hf.attrs['arg'] = vars(args)
                hf.attrs['RAPIDObject'] = True
                torch.manual_seed(args.seed)
                np.random.seed(args.seed)
                torch.cuda.manual_seed(args.seed)
                model = RAPIDMixNet(dimension=len(markernums),
                                    nummodules=5,
                                    mse=args.mse,
                                    numclusters=int(args.ncluster),
                                    )
                model.apply(weight_init)
                optimizer = optim.AdamW(model.parameters(),
                                        lr=float(args.lr),
                                        betas=(0.9, 0.999),
                                        eps=1e-08,
                                        weight_decay=0.01,
                                        amsgrad=False,
                                        )
                if algname == "Pretrained":
                    model = load_checkpoint("/".join(modelpath),
                                            model,
                                            optimizer,
                                            )
                print(model)
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                model.to(device)
                self.train_object(model,
                                  expressionavgs,
                                  optimizer,
                                  args,
                                  )
                self.test_object(model,
                                 expressionavgs,
                                 args,
                                 list(range(len(cfg.markers) + 4)),
                                 add_grey_img,
                                 add_color_img,
                                 "RAPID",
                                 imagenum,
                                 optimizer=optimizer,
                                 results_folder=results_folder,
                                 )

        utils.log_actions(f"gui.object_clustering(markernums={markernums}, segindex={segindex}, algname=\"{algname}\", "
                          f"modelpath=\"{modelpath}\", add_grey_img={add_grey_img}, add_color_img={add_color_img}, "
                          f"continuetraining={continuetraining}, normalize=\"{normalize}\", pca={pca}, "
                          f"modelparams={modelparams})")
        cfg.viewer.status = "RAPID clustering done."

    def open_docs(self):
        """
        Open the RAPID documentation in a web browser.
        """
        rootfold = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(rootfold + "/../docs"):
            gdown.download("https://drive.google.com/uc?id=1JhpIjMd_Rq-i1_laivxzavwZDJPOa4b1",
                           rootfold + "/../docs.zip", verify=False)
            shutil.unpack_archive(rootfold + "/../docs.zip", rootfold + "/../")
        webbrowser.open(f"file://{rootfold}/../docs/_build/html/index.html", new=2)

    ### TODO: Delayed function? Pyramid/multiscale?
    def open_images_gui(self):
        """
        Trigger the "Open Images" popup from the GUI.
        """
        self.open_images()

    def open_images(self,
                    segmentedimgpaths=[],
                    filenames=[],
                    cfirst=None,
                    markerstring="",
                    loadedmatrix=None,
                    imagenames=[],
                    indiceslist=[],
                    markernums=[],
                    ):
        """
        Open a directory for the user to select which images they would like to use, and load them into the viewer.

        Args:
            segmentedimgpaths (list, optional): List of paths to segmented images if loading segmentation results (Default: []).
            filenames (list, optional): List of paths to each of the iamges being loaded (Default: []).
            cfirst (bool, optional): If True, assume (c,z,x,y) order for 4D images. Otherwise, assume (z,c,x,y) order (Default: None).
            markerstring (str, optional): Comma-separated names of cell markers for the image(s) being loaded (Default: "").
            loadedmatrix (bool, optional): If True, prompt user to load matrix of markers for each image. Otherwise, allow user to load a list of markers (Default: None).
            imagenames (list, optional): List of names of images being loaded in a matrix of markers (Default: []).
            indiceslist (list, optional): List of indices for each image in a matrix that are shared between all other images (Default: []).
            markernums (list, optional): List of indices of cell markers to include in the viewer (Default: []).

        :return: *(bool)*: \n
            True if user has loaded images, False if none are selected.
        """

        # Only open images at the start, not after performing downstream analysis.
        if len(cfg.viewer.layers) > len(cfg.markers):
            utils.display_error_message("Cannot open additional images",
                                        "If you have done downstream analysis, please open images in a new session")
            return

        # Prompt user to select paths to images to load.
        if len(filenames) == 0:
            filenames, _ = QFileDialog.getOpenFileNames(
                parent=cfg.viewer.window.qt_viewer,
                caption='Select images...',
                filter='*.afm *.nef *.lif *.nhdr *.ps *.bmp *.frm *.pr3 *.tif *.aim *.dat *.fits *.pcoraw *.qptiff *.acff '
                       '*.xys *.mrw *.xml *.svs *.arf *.dm4 *.ome.xml *.v *.pds *.zvi *.apl *.mrcs *.i2i *.mdb *.ipl *.oir '
                       '*.ali *.fff *.vms *.jpg *.inr *.pcx *.vws *.html *.al3d *.ims *.bif *.labels *.dicom *.par *.map '
                       '*.ome.tf2 *.htd *.tnb *.mrc *.obf *.xdce *.png *.jpx *.fli *.psd *.pgm *.obsep *.jpk *.ome.tif '
                       '*.rcpnl *.pbm *.grey *.raw *.zfr *.klb *.spc *.sdt *.2fl *.ndpis *.ipm *.pict *.st *.seq *.nii *.lsm '
                       '*.epsi *.cr2 *.zfp *.wat *.lim *.1sc *.ffr *.liff *.mea *.nd2 *.tf8 *.naf *.ch5 *.afi *.ipw *.img '
                       '*.ids *.mnc *.crw *.mtb *.cxd *.gel *.dv *.jpf *.tga *.vff *.ome.tiff *.ome *.bin *.cfg *.dti '
                       '*.ndpi *.c01 *.avi *.sif *.flex *.spe *.ics *.jp2 *.xv *.spi *.lms *.sld *.vsi *.lei *.sm3 '
                       '*.hx *.czi *.nrrd *.ppm *.exp *.mov *.xqd *.dm3 *.im3 *.pic *.his *.j2k *.rec *.top *.pnl *.tf2 '
                       '*.oif *.l2d *.stk *.fdf *.mng *.ome.btf *.tfr *.res *.dm2 *.eps *.hdr *.am *.stp *.sxm *.ome.tf8 '
                       '*.dib *.mvd2 *.wlz *.nd *.h5 *.cif *.mod *.nii.gz *.bip *.oib *.amiramesh *.scn *.gif *.sm2 '
                       '*.tiff *.hdf *.hed *.r3d *.wpi *.dcm *.btf *.msr *.xqf'
            )

        # If loading segmentation, make sure the images being loaded correspond to the segmented images.
        if segmentedimgpaths and len(filenames) != len(segmentedimgpaths):
            utils.display_error_message("Mismatching number of images",
                                        "Please ensure the raw images correspond to the segmented image and are in the correct order")
            return False

        # User must load at least one image.
        if len(filenames) == 0:
            return False

        # If this is the first time loading images.
        if not cfg.has_loaded_image:
            # Initialize lists of image paths and image arrays, and keep track of number of cell markers being loaded.
            imagelist = []

            if markerstring == "" and (loadedmatrix == None or imagenames == [] or indiceslist == []):
                loadedimgnames = [os.path.split(path)[-1].split(".")[0] for path in filenames]
                markernames = utils.MarkerNames(loadedimgnames)
                markernames.exec()
                if not markernames.OK:
                    if markernames.matrix:
                        utils.display_error_message("No images loaded",
                                                    "Please ensure the image names in the matrix correspond with the names of the images being loaded.")
                    return
                markerstring = markernames.markers
                loadedmatrix = markernames.matrix
                if loadedmatrix:
                    imagenames = markernames.imagenames
                    indiceslist = markernames.indiceslist

            # Loop through each image path.
            for path in filenames:
                # Read the image into a numpy array.
                filename = os.path.join(os.path.abspath(path))

                if loadedmatrix and os.path.split(path)[-1].split(".")[0] not in imagenames:
                    continue

                img, imgisflipped = self.parse_img(filename)

                # If loading a single z-slice, load the image as is.
                if len(img.shape) == 3:
                    if indiceslist != []:
                        img = img[indiceslist[cfg.num_imgs], :, :]
                    imagelist.append(img)
                    cfg.file_names.append(path)
                    if cfg.num_markers == 0:
                        cfg.num_markers = len(img)
                    cfg.img_is_flipped.append(imgisflipped)
                    cfg.num_imgs += 1

                # If loading multiple z-slices, load as separate images for each z-slice.
                elif len(img.shape) == 4:
                    name_ext = path.split(".")
                    if cfirst is None:
                        channelorder = utils.ChannelOrder4D()
                        channelorder.exec()
                        if not channelorder.OK:
                            return
                        cfirst = channelorder.cfirst

                    if cfirst:
                        for i in range(img.shape[1]):
                            currentz = copy.deepcopy(img[:, i, :, :])
                            if indiceslist != []:
                                currentz = currentz[indiceslist[cfg.num_imgs], :, :]
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            cfg.file_names.append('.'.join(currentname))
                            cfg.img_is_flipped.append(imgisflipped)
                            cfg.num_imgs += 1

                    else:
                        for i in range(len(img)):
                            currentz = copy.deepcopy(img[i, :, :, :])
                            if indiceslist != []:
                                currentz = currentz[indiceslist[cfg.num_imgs], :, :]
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            cfg.file_names.append('.'.join(currentname))
                            cfg.img_is_flipped.append(imgisflipped)
                            cfg.num_imgs += 1

                    if cfg.num_markers == 0:
                        cfg.num_markers = len(currentz)

                # cfg.num_imgs += 1

                # If this image has a different number of markers than previous images, and a matrix was not loaded,
                # prompt user to load matrix of markers instead of one singular set of markers.
                if len(imagelist[-1]) != cfg.num_markers and path != filenames[0]:
                    utils.display_error_message("Incompatible number of channels",
                                                "Some images contain different numbers of channels. Please load a matrix containing ordered lists of cell markers for each image.")
                    cfg.file_names = []
                    cfg.img_is_flipped = []
                    cfg.num_imgs = 0
                    cfg.num_markers = 0
                    return

            if cfg.num_imgs == 0:
                utils.display_error_message("No images loaded",
                                            "If you are loading a cell marker matrix, please ensure the image names in the matrix correspond with the names of the images being loaded.")
                return

            inputmarkernames = markerstring.replace(" ", "").split(",")

            # Store the names of the cell markers that are being included.
            markers = []
            for i in range(cfg.num_markers):
                markers.append(f"Marker {i}")
            if not (len(inputmarkernames) == 1 and inputmarkernames[0] == ""):
                if len(inputmarkernames) > len(markers):
                    markers = [inputmarkernames[i] for i in range(len(markers))]
                elif len(inputmarkernames) == len(markers):
                    markers = inputmarkernames
                else:
                    for i in range(len(inputmarkernames)):
                        markers[i] = inputmarkernames[i]

            # Allow user to remove any markers that they do not want to include.
            if markernums == []:
                removemarkernames = utils.RemoveMarkerNames(markers)
                removemarkernames.exec()
                if not removemarkernames.OK:
                    cfg.num_imgs = 0
                    cfg.num_markers = 0
                    return
                markernums = removemarkernames.markernums
            cfg.markers = [markers[ind].replace("/", "_").replace("\\", "_") for ind in markernums]
            cfg.marker_inds = copy.deepcopy(markernums)
            cfg.num_markers = len(cfg.markers)

            # Store the shapes of each of the images being loaded.
            for i in range(len(imagelist)):
                imagelist[i] = imagelist[i][cfg.marker_inds, :, :]
                vdim = imagelist[i].shape[1]
                hdim = imagelist[i].shape[2]
                cfg.img_shape_list.append((vdim, hdim, len(cfg.marker_inds)))

            # Keep track of the maximum x- and y- dimensions to use for the shape of the image in the viewer.
            cfg.max_img_shape = np.array([np.max(cfg.img_shape_list, 0)[0], np.max(cfg.img_shape_list, 0)[1]])

            # Add each image to the viewer.
            colforinput = generate_colormap(cfg.num_markers + 1)
            for ch in range(cfg.num_markers):
                addarr = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]),
                                  dtype=imagelist[0].dtype)
                for i in range(cfg.num_imgs):
                    addarr[i, :imagelist[i].shape[1], :imagelist[i].shape[2]] = imagelist[i][0, :, :]
                    imagelist[i] = imagelist[i][1:, :, :]
                cmap = Colormap(ColorArray(
                    [(0, 0, 0), (colforinput[ch, 0] / 255, colforinput[ch, 1] / 255, colforinput[ch, 2] / 255)]))
                # addarr_downsampled = np.stack([cv.pyrDown(addarr[i,:,:]) for i in range(len(addarr))])
                # cfg.viewer.add_image([addarr, addarr_downsampled], name=cfg.markers[ch], rgb=False, colormap=cmap, contrast_limits=[0, 255],
                #                      blending="additive", visible=False, multiscale=True)
                cfg.viewer.add_image(addarr, name=cfg.markers[ch], rgb=False, colormap=cmap, contrast_limits=[0, 255],
                                     blending="additive", visible=False)
            cfg.has_loaded_image = True

            # By default, initialize sample groupings so that each image is in its own group.
            d = {}
            for name in [os.path.split(path)[-1].split(".")[0] for path in cfg.file_names]:
                n = os.path.split(name)[-1]
                d[n] = n
            cfg.groups_list.append(d)

            # Update the dropdown options for the sort table widget.
            cfg.table_params += cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            cfg.update_log_file = False
            cfg.sort_table_widget.marker.choices = tuple(cfg.table_params)
            cfg.sort_table_widget.reset_choices()
            cfg.update_log_file = True
            cfg.viewer.dims.set_current_step(0, 0)

        # If at least one image has already been loaded.
        else:
            imagelist = []

            markerorder = utils.NewMarkerOrder()
            markerorder.exec()
            if not markerorder.OK:
                return

            if markerorder.usingdifferentorder:
                loadedimgnames = [os.path.split(path)[-1].split(".")[0] for path in filenames]
                markernames = utils.MarkerNames(loadedimgnames)
                markernames.exec()
                if not markernames.OK:
                    if markernames.matrix:
                        utils.display_error_message("No images loaded",
                                                    "Please ensure the image names in the matrix correspond with the names of the images being loaded.")
                    return
                markerstring = markernames.markers
                loadedmatrix = markernames.matrix
                newmarkerlist = markerstring.replace(" ", "").split(",")
                if not all([newmarker in newmarkerlist for newmarker in cfg.markers]):
                    utils.display_error_message("Mismatching cell markers",
                                                "Not all cell markers currently loaded are included in the image(s) you loaded")
                    return

                if loadedmatrix:
                    imagenames = markernames.imagenames
                    indiceslist = markernames.indiceslist
                else:
                    indices = []
                    currentmarkerslist = [re.sub('[^a-zA-Z0-9]', '', marker).lower() for marker in newmarkerlist]
                    for marker in [re.sub('[^a-zA-Z0-9]', '', cm).lower() for cm in cfg.markers]:
                        indices.append(currentmarkerslist.index(marker))
                    indiceslist = [indices] * len(loadedimgnames)

            # Loop through each image path.
            numnewimgs = 0
            filenamesadded = []
            imageisflipped = []
            for path in filenames:
                # Read the image into a numpy array.
                filename = os.path.join(os.path.abspath(path))

                if loadedmatrix and os.path.split(path)[-1].split(".")[0] not in imagenames:
                    continue

                img, imgisflipped = self.parse_img(filename)

                # If loading a single z-slice, load the image as is.
                if len(img.shape) == 3:
                    if indiceslist != []:
                        img = img[indiceslist[numnewimgs], :, :]
                    imagelist.append(img)
                    filenamesadded.append(path)
                    imageisflipped.append(imgisflipped)

                # If loading multiple z-slices, load as separate images for each z-slice.
                elif len(img.shape) == 4:
                    name_ext = path.split(".")
                    if cfirst is None:
                        channelorder = utils.ChannelOrder4D()
                        channelorder.exec()
                        if not channelorder.OK:
                            return
                        cfirst = channelorder.cfirst

                    if cfirst:
                        for i in range(img.shape[1]):
                            currentz = copy.deepcopy(img[:, i, :, :])
                            if indiceslist != []:
                                currentz = currentz[indiceslist[numnewimgs], :, :]
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            filenamesadded.append('.'.join(currentname))
                            imageisflipped.append(imgisflipped)

                    else:
                        for i in range(len(img)):
                            currentz = copy.deepcopy(img[i, :, :, :])
                            if indiceslist != []:
                                currentz = currentz[indiceslist[numnewimgs], :, :]
                            imagelist.append(currentz)
                            currentname = copy.deepcopy(name_ext)
                            currentname[-2] += f"_z{i + 1}"
                            filenamesadded.append('.'.join(currentname))
                            imageisflipped.append(imgisflipped)
                numnewimgs += 1

                # If this image has a different number of markers than previous images, and a matrix was not loaded,
                # prompt user to load matrix of markers instead of one singular set of markers.
                if len(imagelist[-1]) < cfg.num_markers:
                    utils.display_error_message("Incompatible number of channels",
                                                "Some images contain different numbers of channels. Please ensure each image you load contains every cell marker that has already been loaded.")
                    return

            cfg.file_names += filenamesadded
            cfg.num_imgs += numnewimgs
            cfg.img_is_flipped += imageisflipped

            if cfg.num_imgs == 0:
                utils.display_error_message("No images loaded",
                                            "If you are loading a cell marker matrix, please ensure the image names in the matrix correspond with the names of the images being loaded.")
                return

            # Store the shapes of each of the images being loaded.
            for i in range(len(imagelist)):
                vdim = imagelist[i].shape[1]
                hdim = imagelist[i].shape[2]
                cfg.img_shape_list.append((vdim, hdim, cfg.num_markers))

            # Update the maximum x- and y- dimensions to use for the shape of the image in the viewer.
            cfg.max_img_shape = np.array((np.max(cfg.img_shape_list, 0)[0], np.max(cfg.img_shape_list, 0)[1]))
            for ch in range(cfg.num_markers):
                newarr = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1]),
                                  dtype=imagelist[0].dtype)
                prevarr = cfg.viewer.layers[ch].data
                newarr[:len(prevarr), :prevarr.shape[1], :prevarr.shape[2]] = prevarr
                for i in range(len(filenamesadded)):
                    newarr[i + len(prevarr), :imagelist[i].shape[1], :imagelist[i].shape[2]] = imagelist[i][0, :, :]
                    imagelist[i] = imagelist[i][1:, :, :]
                cfg.viewer.layers[ch].data = newarr

            # Add each of the new images to the default grouping.
            for name in [os.path.split(path)[-1].split(".")[0] for path in filenamesadded]:
                n = os.path.split(name)[-1]
                cfg.groups_list[0][n] = n

        utils.log_actions(f"gui.open_images(segmentedimgpaths={segmentedimgpaths}, filenames={filenames}, "
                          f"cfirst={cfirst}, markerstring=\"{markerstring}\", loadedmatrix={loadedmatrix}, "
                          f"imagenames={imagenames}, indiceslist={indiceslist}, markernums={markernums})")
        return True

    def parse_img(self,
                  imgpath,
                  islabel=False,
                  ):
        """
        Read an input image into a numpy array to be loaded in the viewer.

        Args:
            imgpath (str): Path to the image being loaded.
            islabel (bool, optional): True if loading segmentation results. Otherwise, False (Default: False).

        :return: img *(numpy.ndarray)*: \n
            The image in numpy array format.
        """

        try:
            try:
                img = tifffile.imread(imgpath)
            except:
                reader_function = napari_get_reader(imgpath)
                img = reader_function(imgpath)[0][0]
        except:
            msg = QMessageBox()
            msg.setWindowTitle("RAPID Alert")
            msg.setText("Please convert your file to .tif format")
            msg.setDetailedText("Because your Java path is not set, your file must be in .tif format")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return False

        if not islabel:
            img = img_as_ubyte(img)
        else:
            img = img.astype(np.uint32)

        imgisflipped = False
        if img.shape[-2] > img.shape[-1]:
            img = np.moveaxis(img, -1, -2)
            imgisflipped = True

        return img, imgisflipped

    ### TODO: Progress bar in GUI for pixel clustering.
    ### TODO: Markers used for clustering when applying pre-trained model?
    ### TODO: Save binarize/denoise to zarr so it can be loaded when loading model.
    def pixel_clustering(self,
                         isloadingmodel=None,
                         predict=None,
                         randompatchgeneration=None,
                         markerindices=[],
                         modelparams=[],
                         modelpath="",
                         patchesstart=[],
                         add_grey_img=None,
                         add_color_img=None,
                         ):
        """
        Perform RAPID pixel-based clustering, by either training a new model or loading a previously-trained model and
        applying it to each of the images loaded into the GUI.

        Args:
            isloadingmodel (bool, optional): If True, load pre-trained model weights. Otherwise, use random weight initialization (Default: None).
            predict (bool, optional): If True, use pre-trained model weights to predict without further training. Otherwise, train a new model (Default: None).
            randompatchgeneration (bool, optional): If True, randomly generate patches for the training set. Otherwise, use user-defined patches (Default: None).
            markerindices (list, optional): List of indices of cell markers to be considered for clustering (Default: []).
            modelparams (iterable, optional): List of parameters for the desired clustering algorithm (Default: []).
            modelpath (str, optional): Path to pretrained model, if loading a model (Default: "").
            patchesstart (list, optional): List of vertices defining top-left corner for each 64x64 patch, for each image. (Default: []).
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """
        # Can't use RAPID before opening an image.
        if len(cfg.markers) == 0:
            utils.display_error_message("Please open an image first",
                                        "Begin by opening the image(s) that you would like to train RAPID on")
            return

        # Allow user to either load a model and define the path to the model, or train a new model.
        if isloadingmodel is None:
            loadmodel = utils.LoadModel()
            loadmodel.exec()
            if not loadmodel.OK:
                return
            isloadingmodel = loadmodel.load

        # If loading a model, allow user to either continue training or predict. Otherwise, default to training.
        if isloadingmodel:
            if modelpath == "":
                modelpath = loadmodel.dirpath
            if predict is None:
                loadmodeloptions = utils.LoadModelOptions()
                loadmodeloptions.exec()
                if not loadmodeloptions.OK:
                    return
                predict = loadmodeloptions.prediction
            hf = zarr.open("/".join(modelpath[:-1]) + "/RAPID_Data", 'r')
            trainmarkernames = hf.attrs['selmarkernames']
            numtrainmarkers = len(trainmarkernames)
        else:
            predict = False

        # If training, allow user to define specific patches to train on, otherwise default to random patches.
        if not predict and randompatchgeneration is None:
            definepatches = utils.DefinePatches()
            definepatches.exec()
            if not definepatches.OK:
                return
            randompatchgeneration = definepatches.randompatchgeneration
        else:
            randompatchgeneration = True

        # Define which markers to use for pixel clustering.
        if markerindices == []:
            trainmarkers = utils.PixelTrainMarkers()
            trainmarkers.exec()
            if not trainmarkers.OK:
                return
            markerindices = trainmarkers.markernums
        markernames = [cfg.markers[ind] for ind in markerindices]

        # Must use at least 3 cell markers.
        if len(markerindices) < 3:
            utils.display_error_message("Not enough markers selected",
                                        "Please select at least three markers for clustering")
            return

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        # If loading a model, must use the same number of markers as were used when the model was trained.
        if isloadingmodel:
            if len(markerindices) != numtrainmarkers:
                utils.display_error_message("Incompatible number of markers",
                                            "Please ensure you use the same number of markers as the model you loaded")
                return
        cfg.pixel_cluster_markers.append(markernames)

        # Save image attributes to the output folder.
        results_folder = utils.create_new_folder("RAPIDPixel_", cfg.output_folder)
        cfg.pixel_cluster_directories.append(results_folder)
        datafolder = os.path.join(results_folder, "RAPID_Data")
        hf = zarr.open(datafolder, 'w')
        hf.attrs['markers'] = cfg.markers
        hf.attrs['flipimg'] = cfg.img_is_flipped

        # Add a separate popup window for the user to define patches to use for training.
        if not randompatchgeneration and patchesstart == []:
            # Keep track of where the patches are located for each image.
            shapesdata = []
            for i in range(cfg.num_imgs):
                patchesstart.append([])
                shapesdata.append([])

            names = []
            for i in range(len(cfg.file_names)):
                names.append(cfg.file_names[i].split("/")[-1])

            contrastlimits = []
            cl = []
            for i in range(len(markerindices)):
                cl.append([0, 255])
            for i in range(len(cfg.file_names)):
                contrastlimits.append(copy.deepcopy(cl))

            cfg.define_patches_viewer = napari.Viewer()
            cfg.define_patches_viewer_params = modelparams
            cfg.define_patches_viewer_img_id = 0

            @magicgui(auto_call=True, image={"choices": names, "label": ""})
            def change_image_pixelgui(image: str):
                for i in range(len(cfg.define_patches_viewer.layers)):
                    # Loop through each shape within each shapes layer.
                    if isinstance(cfg.define_patches_viewer.layers[i], napari.layers.shapes.shapes.Shapes) and \
                            cfg.define_patches_viewer.layers[i].visible:
                        for shape in range(len(cfg.define_patches_viewer.layers[i].data)):
                            # Split each shape into 64x64 patches, adding padding as necessary.
                            # Information will be stored as the top-right corner x- and y- values of each
                            # of these patches.
                            verts = copy.deepcopy(cfg.define_patches_viewer.layers[i].data[shape])
                            xmin = min(verts[0][1], verts[2][1])
                            xmax = max(verts[0][1], verts[2][1])
                            ymin = min(verts[0][0], verts[2][0])
                            ymax = max(verts[0][0], verts[2][0])
                            xdiff = 64 - ((xmax - xmin) % 64)
                            ydiff = 64 - ((ymax - ymin) % 64)
                            xmin = int(round(xmin - xdiff / 2))
                            xmax = int(round(xmax + xdiff / 2))
                            ymin = int(round(ymin - ydiff / 2))
                            ymax = int(round(ymax + ydiff / 2))
                            if ymin < 0:
                                ymax -= ymin
                                ymin = 0
                            if xmin < 0:
                                xmax -= xmin
                                xmin = 0
                            if ymax > cfg.img_shape_list[cfg.define_patches_viewer_img_id][0]:
                                diff = ymax - cfg.img_shape_list[cfg.define_patches_viewer_img_id][0] + 1
                                ymin -= diff
                                ymax = cfg.img_shape_list[cfg.define_patches_viewer_img_id][0]
                            if xmax > cfg.img_shape_list[cfg.define_patches_viewer_img_id][1]:
                                diff = xmax - cfg.img_shape_list[cfg.define_patches_viewer_img_id][1] + 1
                                xmin -= diff
                                xmax = cfg.img_shape_list[cfg.define_patches_viewer_img_id][1]
                            numxpatches = int((xmax - xmin) / 64)
                            numypatches = int((ymax - ymin) / 64)
                            for j in range(numxpatches):
                                for k in range(numypatches):
                                    cornerx = int(xmin + 64 * j)
                                    cornery = int(ymin + 64 * k)
                                    patchesstart[cfg.define_patches_viewer_img_id].append([cornery, cornerx])
                    else:
                        contrastlimits[cfg.define_patches_viewer_img_id][i] = cfg.define_patches_viewer.layers[
                            i].contrast_limits

                # Go to the selected image.
                cfg.define_patches_viewer_img_id = names.index(image)

                # Change the images in the viewer to display the next image data.
                for i in range(len(markerindices)):
                    cfg.define_patches_viewer.layers[i].data = cfg.viewer.layers[markerindices[i]].data[
                                                               cfg.define_patches_viewer_img_id, :, :]
                    cfg.define_patches_viewer.layers[i].contrast_limits = \
                        contrastlimits[cfg.define_patches_viewer_img_id][i]

                # Store the shapes for the previous image so they can be added again if necessary.
                for i in range(len(cfg.define_patches_viewer.layers) - len(markerindices)):
                    if len(cfg.define_patches_viewer.layers[len(markerindices)].data) > 0:
                        shapesdata[cfg.define_patches_viewer_img_id - 1].append(
                            cfg.define_patches_viewer.layers[len(markerindices)].data)
                    cfg.define_patches_viewer.layers.pop(len(markerindices))

                # Add any shapes that had been previously added for this image.
                for i in range(len(shapesdata[cfg.define_patches_viewer_img_id])):
                    cfg.define_patches_viewer.add_shapes(shapesdata[cfg.define_patches_viewer_img_id][i])
                shapesdata[cfg.define_patches_viewer_img_id] = []
                patchesstart[cfg.define_patches_viewer_img_id] = []

            @magicgui(call_button="Finish")
            def finish_pixelgui() -> Image:
                for i in range(len(cfg.define_patches_viewer.layers)):
                    # Loop through each shape within each shapes layer.
                    if isinstance(cfg.define_patches_viewer.layers[i], napari.layers.shapes.shapes.Shapes) and \
                            cfg.define_patches_viewer.layers[i].visible:
                        for shape in range(len(cfg.define_patches_viewer.layers[i].data)):
                            # Split each shape into 64x64 patches, adding padding as necessary.
                            # Information will be stored as the top-right corner x- and y- values of each of
                            # these patches.
                            verts = copy.deepcopy(cfg.define_patches_viewer.layers[i].data[shape])
                            xmin = min(verts[0][1], verts[2][1])
                            xmax = max(verts[0][1], verts[2][1])
                            ymin = min(verts[0][0], verts[2][0])
                            ymax = max(verts[0][0], verts[2][0])
                            xdiff = 64 - ((xmax - xmin) % 64)
                            ydiff = 64 - ((ymax - ymin) % 64)
                            xmin = int(round(xmin - xdiff / 2))
                            xmax = int(round(xmax + xdiff / 2))
                            ymin = int(round(ymin - ydiff / 2))
                            ymax = int(round(ymax + ydiff / 2))
                            if ymin < 0:
                                ymax -= ymin
                                ymin = 0
                            if xmin < 0:
                                xmax -= xmin
                                xmin = 0
                            if ymax > cfg.img_shape_list[cfg.define_patches_viewer_img_id][0]:
                                diff = ymax - cfg.img_shape_list[cfg.define_patches_viewer_img_id][0]
                                ymin -= diff
                                ymax = cfg.img_shape_list[cfg.define_patches_viewer_img_id][0]
                            if xmax > cfg.img_shape_list[cfg.define_patches_viewer_img_id][1]:
                                diff = xmax - cfg.img_shape_list[cfg.define_patches_viewer_img_id][1]
                                xmin -= diff
                                xmax = cfg.img_shape_list[cfg.define_patches_viewer_img_id][1]
                            numxpatches = int((xmax - xmin) / 64)
                            numypatches = int((ymax - ymin) / 64)
                            for j in range(numxpatches):
                                for k in range(numypatches):
                                    cornerx = int(xmin + 64 * j)
                                    cornery = int(ymin + 64 * k)
                                    patchesstart[cfg.define_patches_viewer_img_id].append([cornery, cornerx])

                modelparams = self.apply_clusters_defined_patches(patchesstart,
                                                                  isloadingmodel,
                                                                  results_folder,
                                                                  cfg.define_patches_viewer_params,
                                                                  markerindices,
                                                                  markernames,
                                                                  modelpath,
                                                                  add_grey_img,
                                                                  add_color_img,
                                                                  )

                utils.log_actions(f"gui.pixel_clustering(isloadingmodel={isloadingmodel}, predict={predict}, "
                                  f"randompatchgeneration={randompatchgeneration}, markerindices={markerindices}, "
                                  f"modelparams={modelparams}, modelpath=\"{modelpath}\", patchesstart={patchesstart},"
                                  f"add_grey_img={add_grey_img}, add_color_img={add_color_img})")
                cfg.define_patches_viewer.window.qt_viewer.close()
                cfg.define_patches_viewer.window._qt_window.close()

            @magicgui(call_button="Toggle Visibility")
            def toggle_visibility_pixelgui() -> Image:
                # If any markers are visible, make them invisible. Otherwise, make all markers visible.
                visible = False
                for le in range(len(cfg.define_patches_viewer.layers)):
                    if cfg.define_patches_viewer.layers[le].visible:
                        visible = True
                if visible:
                    for i in range(len(cfg.define_patches_viewer.layers)):
                        cfg.define_patches_viewer.layers[i].visible = False
                else:
                    for i in range(len(cfg.define_patches_viewer.layers)):
                        cfg.define_patches_viewer.layers[i].visible = True

            # Add widgets to the bottom of the patches window.
            definepatcheswidget = QWidget()
            filterLayout = QGridLayout()
            filterLayout.setSpacing(0)
            filterLayout.setContentsMargins(0, 0, 0, 0)
            togglevisgui = toggle_visibility_pixelgui.native
            togglevisgui.setToolTip("Set all layers to visible/invisible")
            filterLayout.addWidget(togglevisgui, 0, 0)

            # Allow user to toggle between images if there are multiple images.
            if cfg.num_imgs > 1:
                changeimagegui = change_image_pixelgui.native
                changeimagegui.setToolTip("Toggle images")
                filterLayout.addWidget(changeimagegui, 0, 1)
                finishgui = finish_pixelgui.native
                finishgui.setToolTip("Perform Clustering")
                filterLayout.addWidget(finishgui, 0, 2)

            else:
                finishgui = finish_pixelgui.native
                finishgui.setToolTip("Perform Clustering")
                filterLayout.addWidget(finishgui, 0, 1)

            definepatcheswidget.setLayout(filterLayout)
            cfg.define_patches_viewer.window.add_dock_widget(definepatcheswidget, area="bottom")

            # Add the first image to the patches window.
            for i in markerindices:
                cmap = cfg.viewer.layers[i].colormap
                cfg.define_patches_viewer.add_image(cfg.viewer.layers[i].data[0, :, :],
                                                    name=cfg.markers[i],
                                                    rgb=False,
                                                    colormap=cmap,
                                                    contrast_limits=[0, 255],
                                                    visible=True,
                                                    blending="additive",
                                                    )

        elif patchesstart != []:
            modelparams = self.apply_clusters_defined_patches(patchesstart,
                                                              isloadingmodel,
                                                              results_folder,
                                                              modelparams,
                                                              markerindices,
                                                              markernames,
                                                              modelpath,
                                                              add_grey_img,
                                                              add_color_img,
                                                              )
            utils.log_actions(f"gui.pixel_clustering(isloadingmodel={isloadingmodel}, predict={predict}, "
                              f"randompatchgeneration={randompatchgeneration}, markerindices={markerindices}, "
                              f"modelparams={modelparams}, modelpath=\"{modelpath}\", patchesstart={patchesstart})")

        # If randomly generating patches.
        else:
            # If predicting without any further training.
            if isloadingmodel and predict:
                # Update parameters and save them to the output folder.
                hf = zarr.open("/".join(modelpath[:-1]) + "/RAPID_Data", 'r')
                args = Namespace(**hf.attrs['arg'])
                args.nchannels = hf["data"].shape[1]
                args.GUI = True
                args.rfold = "/".join(modelpath[:-1])
                copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(results_folder, "checkpoint.pth"))
                args.train = False
                args.predict = True
                args.testbs = 20000
                print(args)

                # Normalize data for RAPID input.
                cfg.viewer.status = "Generating RAPID data..."
                self.generate_RAPID_data(markerindices,
                                         markernames,
                                         datafolder,
                                         False,
                                         args.normalize,
                                         args.normalizeall,
                                         args.normtype,
                                         args.pca,
                                         )
                cfg.viewer.status = "Applying loaded model..."

            # If training a model.
            else:
                # If training a pretrained model.
                if isloadingmodel:
                    # Update parameters and save them to the output folder.
                    hf = zarr.open("/".join(modelpath[:-1]) + "/RAPID_Data", 'r')
                    args = Namespace(**hf.attrs['arg'])
                    args.rfold = "/".join(modelpath[:-1])
                    copyfile(os.path.join(args.rfold, "checkpoint.pth"), os.path.join(results_folder, "checkpoint.pth"))
                    args.reassume = True
                    if modelparams == []:
                        params = utils.RAPIDTrainLoadedParams(args)
                        params.exec()
                        if not params.OK:
                            return
                        args.ncluster = int(params.nc)
                        args.nit = int(params.nit)
                        args.bs = int(params.bs)
                        args.patchsize = int(params.ps)
                        args.npatches = int(params.nop)
                        args.mse = params.mse == "True"
                        args.rescale = params.RC == "True"
                        args.rescalefactor = float(params.RCN)
                        args.lr = float(params.lr)
                        args.SCANloss = params.SCAN
                        denoise = params.denoise
                        modelparams = [args.ncluster, args.nit, args.bs, args.patchsize, args.npatches, args.mse,
                                       args.rescale, args.rescalefactor, args.lr, args.SCANloss, denoise]
                    else:
                        args.ncluster, args.nit, args.bs, args.patchsize, args.npatches, args.mse, \
                        args.rescale, args.rescalefactor, args.lr, args.SCANloss, denoise = modelparams

                # If training a new model.
                else:
                    # Update parameters and save them to the output folder.
                    args = runRAPIDzarr.get_parameters()
                    maximgshape = np.insert(cfg.max_img_shape, 0, cfg.num_markers)
                    args.rfold = cfg.output_folder
                    args.loadmodel = False
                    if modelparams == []:
                        params = utils.RAPIDPixelParameters(len(markerindices), maximgshape)
                        params.exec()
                        if not params.OK:
                            return
                        args.ncluster = int(params.nc)
                        args.nit = int(params.nit)
                        args.bs = int(params.bs)
                        args.patchsize = int(params.ps)
                        args.npatches = int(params.nop)
                        args.mse = params.mse == "True"
                        args.rescale = params.RC == "True"
                        args.rescalefactor = float(params.RCN)
                        args.lr = float(params.lr)
                        args.SCANloss = params.SCAN
                        normalize = params.normalize
                        denoise = params.denoise
                        modelparams = [args.ncluster, args.nit, args.bs, args.patchsize, args.npatches, args.mse,
                                       args.rescale, args.rescalefactor, args.lr, args.SCANloss, normalize, denoise]
                    else:
                        args.ncluster, args.nit, args.bs, args.patchsize, args.npatches, args.mse, \
                        args.rescale, args.rescalefactor, args.lr, args.SCANloss, normalize, denoise = modelparams
                    args.normalize, args.normalizeall, args.normtype, args.pca = utils.pixel_normtype(normalize)

                cfg.viewer.status = "Generating RAPID data..."
                self.generate_RAPID_data(markerindices,
                                         markernames,
                                         datafolder,
                                         denoise,
                                         args.normalize,
                                         args.normalizeall,
                                         args.normtype,
                                         args.pca,
                                         )
                cfg.viewer.status = "Clustering pixels..."
                args.rescale = True
                args.distance = True
                args.epoch = 1
                args.testbs = 20000
                args.GUI = True
                args.predict = False
                hf = zarr.open(datafolder, mode='r+')
                args.nchannels = hf["data"].shape[1]
                hf.attrs['arg'] = vars(args)

            # Train RAPID algorithm.
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            cfg.viewer.window._status_bar._toggle_activity_dock(True)
            grey, prob, tab, colors, _ = runRAPIDzarr.train_rapid(args,
                                                                  device,
                                                                  datafolder,
                                                                  results_folder,
                                                                  )
            grey += 1
            print(f"UNIQUE: {np.unique(grey)}")
            cfg.viewer.window._status_bar._toggle_activity_dock(False)
            if not cfg.has_added_table:
                cfg.analysis_mode = "Pixel"
            if not os.path.exists(args.rfold):
                os.mkdir(args.rfold)

            # Reshape results into multi-channel image array.
            count = 0
            for i in range(cfg.num_imgs):
                vdim = cfg.img_shape_list[i][0]
                hdim = cfg.img_shape_list[i][1]
                cfg.labeled_imgs.append(utils.convert_dtype(grey[count:count + vdim * hdim].reshape(vdim, hdim)))
                count += vdim * hdim

            # Save colors to the output folder.
            if isloadingmodel:
                colors = np.load("/".join(modelpath[:-1]) + "/color.npy")
            np.save(os.path.join(results_folder, "color.npy"), colors)

            # Update any relevant variables and close the window.
            self.apply_pixel_clustering(tab.values,
                                        args,
                                        colors,
                                        add_grey_img,
                                        add_color_img,
                                        results_folder,
                                        )
            cfg.pixel_cluster_count += 1
            cfg.analysis_log.append("Pixel")

            utils.log_actions(f"gui.pixel_clustering(isloadingmodel={isloadingmodel}, predict={predict}, "
                              f"randompatchgeneration={randompatchgeneration}, markerindices={markerindices}, "
                              f"modelparams={modelparams}, modelpath=\"{modelpath}\", patchesstart={patchesstart},"
                              f"add_grey_img={add_grey_img}, add_color_img={add_color_img})")

    def quantify_object_cluster_region(self,
                                       imgindex,
                                       shapetypes,
                                       clusteriteration,
                                       verts,
                                       ):
        """
        Find number of cells from each object-based cluster in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapetypes (list): List of strings representing shapes for the connected series of vertices.
            clusteriteration (int): Index for the round of object clustering being used for analysis.
            verts (list): List of coordinates for vertices being connected to form the shape(s).
        """
        # Find the round of segmentation that corresponds to the current clustering results.
        for i in range(len(cfg.segmentation_clustering_rounds)):
            if clusteriteration in cfg.segmentation_clustering_rounds[i]:
                segmentimgindex = i

        # Store segmented image with corresponding (x,y)-coordinates.
        shape = (cfg.img_shape_list[imgindex][0], cfg.img_shape_list[imgindex][1])
        segmentedimg = np.zeros((shape[0], shape[1], 3))
        analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Segmentation"][
                          segmentimgindex] * cfg.num_imgs + imgindex
        segmentedimg[:, :, 0] = cfg.labeled_imgs[analysisnum]
        for i in range(shape[0]):
            segmentedimg[i, :, 1] = i
        for i in range(shape[1]):
            segmentedimg[:, i, 2] = i
        segmentedimg = np.reshape(segmentedimg, (shape[0] * shape[1], 3))

        # Find number of cells from each phenotype within each shape drawn by the user.
        avgs = []
        numcells = []
        celldata = []
        for i in range(len(verts)):
            # Find the indices of the cells that are contained within the current shape.
            p = self.create_shape_path(verts[i][:, -2:],
                                       shapetypes[i],
                                       )
            mask = p.contains_points(segmentedimg[:, 1:])
            cellids = segmentedimg[:, 0][mask].astype(np.uint32)
            cellids = np.unique(cellids)
            cellids = copy.deepcopy(cellids[cellids > 0])
            tabdata = cfg.data_list[cfg.segmentation_indices[segmentimgindex * cfg.num_imgs + imgindex]]
            tabdata = np.c_[np.array([i + 1 for i in range(len(tabdata))]), tabdata]
            tabdata = pd.DataFrame(tabdata[[cellid - 1 for cellid in cellids], :])
            tabdata.columns = ["Cell ID"] + cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
            celldata.append(tabdata)

            # Find the cluster IDs that correspond to each of the cells within the current shape.
            clustervals = np.zeros_like(cellids)
            clusternums = cfg.cell_cluster_vals[clusteriteration * cfg.num_imgs + imgindex]
            for i in range(len(clustervals)):
                clustervals[i] = clusternums[int(cellids[i]) - 1]

            # Count total number of cells from each cluster in the current shape, as well as the total number of cells.
            numcellspercluster = []
            analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][clusteriteration] * cfg.num_imgs
            labelimg = self.concat_label_imgs(
                [cfg.labeled_imgs[ind] for ind in range(analysisnum, analysisnum + cfg.num_imgs)])
            for i in range(int(np.max(labelimg))):
                numcellspercluster.append(np.count_nonzero(clustervals == i + 1))
            avgs.append(numcellspercluster)
            numcells.append(sum(numcellspercluster))
        return avgs, int(np.max(labelimg)), numcells, celldata

    def quantify_pixel_cluster_region(self,
                                      imgindex,
                                      shapetypes,
                                      clusteriteration,
                                      verts,
                                      ):
        """
        Find number of pixels from each pixel-based cluster in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapetypes (list): List of strings representing shapes for the connected series of vertices.
            clusteriteration (int): Index for the round of pixel clustering being used for analysis.
            verts (list): List of coordinates for vertices being connected to form the shape(s).
        """
        numpixels = []
        num_shapes = len(verts)
        analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Pixel"][clusteriteration] * cfg.num_imgs
        labelimg = cfg.labeled_imgs[analysisnum + imgindex]
        currentimg = np.zeros((cfg.img_shape_list[imgindex][0], cfg.img_shape_list[imgindex][1], 3))
        currentimg[:, :, 0] = labelimg
        for i in range(len(currentimg)):
            currentimg[i, :, 1] = i
        for i in range(currentimg.shape[1]):
            currentimg[:, i, 2] = i
        currentimg = np.reshape(currentimg, (cfg.img_shape_list[imgindex][0] * cfg.img_shape_list[imgindex][1], 3))
        avgs = []
        for i in range(num_shapes):
            shape = self.create_shape_path(verts[i][:, -2:],
                                           shapetypes[i],
                                           )
            mask = shape.contains_points(currentimg[:, 1:])
            numpixels.append(np.count_nonzero(mask))
            currentimgavgs = []
            clustervals = currentimg[:, 0][mask]
            for cluster_val in range(1, int(np.max(labelimg)) + 1):
                currentimgavgs.append(np.count_nonzero(clustervals == cluster_val))
            avgs.append(currentimgavgs)
        return avgs, int(np.max(labelimg)), numpixels

    def quantify_raw_img_region(self,
                                imgindex,
                                shapetypes,
                                verts,
                                ):
        """
        Find average expression values for each cell marker in user-specified regions on the image.

        Args:
            imgindex (int): Index of image currently displayed in the viewer.
            shapetypes (list): List of strings representing shapes for the connected series of vertices.
            verts (list): List of coordinates for vertices being connected to form the shape(s).
        """
        currentimg = np.zeros((cfg.num_markers, cfg.max_img_shape[0], cfg.max_img_shape[1], 3), dtype=np.uint32)
        for i in range(cfg.num_markers):
            currentimg[i, :, :, 0] = cfg.viewer.layers[i].data[imgindex, :, :]
        for i in range(currentimg.shape[1]):
            currentimg[:, i, :, 1] = i
        for i in range(currentimg.shape[2]):
            currentimg[:, :, i, 2] = i
        dim1 = currentimg.shape[1]
        dim2 = currentimg.shape[2]
        currentimg = np.reshape(currentimg, (cfg.num_markers, dim1 * dim2, currentimg.shape[3]))
        avgs = []
        numpixels = []
        for i in range(len(verts)):
            p = self.create_shape_path(verts[i][:, -2:],
                                       shapetypes[i],
                                       )
            mask = p.contains_points(currentimg[0, :, 1:])
            numpixels.append(np.count_nonzero(mask))
            currentimgavgs = []
            for j in range(cfg.num_markers):
                img = currentimg[j, :, 0]
                avg = np.mean(img[mask])
                currentimgavgs.append(round(avg, 2))
            avgs.append(currentimgavgs)
        return avgs, numpixels

    ### TODO: Reformat this, and make sure that it accounts for shapes across different images
    def quantify_region(self,
                        israwimg=None,
                        clusteringindex=None,
                        shapeverts=[],
                        shapetypes=[],
                        imgnum=None,
                        regionnames=[],
                        ):
        """
        Provide quantitative readouts for the phenotypes of pixels or cells in each shape drawn by the user, either for
        the raw image or for a clustered image.

        Args:
            israwimg (bool, optional): If True, quantify average expression for each marker in each region. Otherwise, use cluster assignments (Default: None).
            clusteringindex (int, optional): Index of clustering round being used for analysis (Default: None).
            shapeverts (list, optional): List of coordinates for vertices being connected to form the shape(s) (Default: None).
            shapetypes (list, optional): List of strings representing shapes for the connected series of vertices (Default: None).
            imgnum (int, optional): Index of the image being quantified (Default: None).
            regionnames (list, optional): List of names for each region being analyzed (Default: None).
        """
        # Find the bounding vertices and the geometries for each of the shapes drawn.
        removeshapeslayer = False
        if shapeverts == [] or shapetypes == [] or imgnum is None:
            # Ensure there is at least one shape drawn in order to define the region to be quantified.
            ind = -1
            for i in reversed(range(len(cfg.viewer.layers))):
                if isinstance(cfg.viewer.layers[i], napari.layers.shapes.shapes.Shapes) and cfg.viewer.layers[
                    i].visible:
                    ind = i
                    break
            if ind == -1:
                utils.display_error_message("Please draw a shape first",
                                            "Draw a shape to indicate which cells you would like to display, and make it visible in the viewer")
                return
            shapeverts = [cfg.viewer.layers[ind].data[i] for i in range(len(cfg.viewer.layers[ind].data))]
            shapetypes = [cfg.viewer.layers[ind].shape_type[i] for i in range(len(cfg.viewer.layers[ind].data))]
            imgnum = cfg.viewer.dims.current_step[0]
            removeshapeslayer = True
        else:
            shapeverts = [np.array(verts) for verts in shapeverts]

        # Can only do this if an image has been loaded or if the current image ID is greater than the number of
        # images (ie, more UMAP plots than there are images).
        if imgnum > cfg.num_imgs:
            utils.display_error_message("No image in the viewer",
                                        "Please make sure that there is a valid image being displayed in the viewer")
            return

        # Prompt user to define whether to quantify average marker expression from raw image, or cluster number
        # of objects from cluster assignments.
        if israwimg is None:
            if len(cfg.clusters_are_pixel_based) > 0:
                selectdatapopup = utils.SelectData()
                selectdatapopup.exec()
                if not selectdatapopup.OK:
                    return
                israwimg = selectdatapopup.rawimg
            else:
                israwimg = True

        # If using raw image, find average expression of each marker in each shape.
        if israwimg:
            # Find averages and number of pixels in each shape.
            avgs, numpixels = self.quantify_raw_img_region(imgnum,
                                                           shapetypes,
                                                           shapeverts,
                                                           )

            # Re-color and label each of the shapes.
            if removeshapeslayer:
                cfg.viewer.layers.pop(ind)
            labels = []
            for i in range(len(avgs)):
                labels.append(f"Region {i + 1}")
            properties = {'class': labels, }
            textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
            cfg.viewer.add_shapes(shapeverts,
                                  shape_type=shapetypes,
                                  edge_width=0,
                                  properties=properties,
                                  name=f"Quantified Regions {cfg.selected_region_count}",
                                  text=textproperties,
                                  face_color=[np.array([0.2, 0.2, 0.2])],
                                  )

            # Add labels for each of the regions for the saved csv file and to add to the shapes.
            outfolder = utils.create_new_folder("QuantifiedRawRegion_", cfg.output_folder)
            addnewshapeslayer = True
            if regionnames == []:
                quantifypopup = utils.QuantifyRegionPopup(avgs,
                                                          "raw",
                                                          len(cfg.markers),
                                                          numpixels,
                                                          outfolder,
                                                          )
                quantifypopup.exec()
                if quantifypopup.saved:
                    regionnames = list(quantifypopup.headernames)[1:]
                addnewshapeslayer = quantifypopup.saved

            else:
                self.save_quantified_region(avgs,
                                            "raw",
                                            len(cfg.markers),
                                            cfg.markers,
                                            numpixels,
                                            outfolder,
                                            cfg.selected_region_count,
                                            )

            if not regionnames == labels and addnewshapeslayer:
                cfg.viewer.layers.pop(len(cfg.viewer.layers) - 1)
                properties = {'class': regionnames, }
                text_properties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                cfg.viewer.add_shapes(shapeverts,
                                      shape_type=shapetypes,
                                      edge_width=0,
                                      name=f"Quantified Regions {cfg.selected_region_count}",
                                      properties=properties,
                                      text=text_properties,
                                      face_color=[np.array([0.2, 0.2, 0.2])],
                                      )
            cfg.selected_region_count += 1

        # If using clustered results, find number of pixels/cells from each cluster within each shape.
        else:
            if clusteringindex is None:
                # If clustering has only been done once, use that by default.
                if len(cfg.clusters_are_pixel_based) == 1:
                    clusteringindex = 0
                # If clustering has been done more than once, prompt the user to choose which one to use.
                else:
                    selectclusteringround = utils.SelectClusteringRound()
                    selectclusteringround.exec()
                    if not selectclusteringround.OK:
                        return
                    clusteringindex = selectclusteringround.clusteringindex
            ispixelcluster = cfg.clusters_are_pixel_based[clusteringindex]

            clustermodeindex = [i for i, ispixelbased in enumerate(cfg.clusters_are_pixel_based) if
                                ispixelbased == ispixelcluster].index(clusteringindex)

            clusteringind = [i for i, m in enumerate(cfg.clusters_are_pixel_based) if m == ispixelcluster][
                clustermodeindex]
            clusternames = cfg.cluster_names[clusteringind]

            # If the user selected pixel-based clustering results.
            if ispixelcluster:
                # Find number of pixels from each cluster in each shape.
                avgs, numrows, numpixels = self.quantify_pixel_cluster_region(imgnum,
                                                                              shapetypes,
                                                                              clustermodeindex,
                                                                              shapeverts,
                                                                              )

                # Re-color and label each of the shapes.
                if removeshapeslayer:
                    cfg.viewer.layers.pop(ind)
                labels = []
                for i in range(len(avgs)):
                    labels.append(f"Region {i + 1}")
                properties = {'class': labels}
                textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white'}
                cfg.viewer.add_shapes(shapeverts,
                                      shape_type=shapetypes,
                                      edge_width=0,
                                      properties=properties,
                                      name=f"Quantified Regions {cfg.selected_region_count}",
                                      text=textproperties,
                                      face_color=[np.array([0.2, 0.2, 0.2])],
                                      )

                # Add labels for each of the regions for the saved csv file and to add to the shapes.
                outfolder = utils.create_new_folder("QuantifiedPixelRegion_",
                                                    cfg.output_folder,
                                                    )
                addnewshapeslayer = True
                if regionnames == []:
                    quantifypopup = utils.QuantifyRegionPopup(avgs,
                                                              "pixel",
                                                              numrows,
                                                              numpixels,
                                                              outfolder,
                                                              clusternames=clusternames,
                                                              )
                    quantifypopup.exec()
                    if quantifypopup.saved:
                        regionnames = list(quantifypopup.headernames)[1:]
                    addnewshapeslayer = quantifypopup.saved
                else:
                    self.save_quantified_region(avgs,
                                                "pixel",
                                                numrows,
                                                cfg.markers,
                                                numpixels,
                                                outfolder,
                                                cfg.selected_region_count,
                                                clusternames=clusternames,
                                                )

                if not regionnames == labels and addnewshapeslayer:
                    cfg.viewer.layers.pop(len(cfg.viewer.layers) - 1)
                    properties = {'class': regionnames, }
                    textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                    cfg.viewer.add_shapes(shapeverts,
                                          shape_type=shapetypes,
                                          edge_width=0,
                                          name=f"Quantified Regions {cfg.selected_region_count}",
                                          properties=properties,
                                          text=textproperties,
                                          face_color=[np.array([0.2, 0.2, 0.2])],
                                          )
                cfg.selected_region_count += 1

            else:
                # Find averages and number of pixels in each shape.
                avgs, numrows, numcells, celldata = self.quantify_object_cluster_region(imgnum,
                                                                                        shapetypes,
                                                                                        clustermodeindex,
                                                                                        shapeverts,
                                                                                        )

                # Re-color and label each of the shapes.
                if removeshapeslayer:
                    cfg.viewer.layers.pop(ind)
                labels = []
                for i in range(len(avgs)):
                    labels.append(f"Region {i + 1}")
                properties = {'class': labels, }
                textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                cfg.viewer.add_shapes(shapeverts,
                                      shape_type=shapetypes,
                                      edge_width=0,
                                      name=f"Quantified Regions {cfg.selected_region_count}",
                                      properties=properties,
                                      text=textproperties,
                                      face_color=[np.array([0.2, 0.2, 0.2])],
                                      )

                # Add labels for each of the regions for the saved csv file and to add to the shapes.
                outfolder = utils.create_new_folder("QuantifiedObjectRegion_",
                                                    cfg.output_folder,
                                                    )

                addnewshapeslayer = True
                if regionnames == []:
                    quantifypopup = utils.QuantifyRegionPopup(avgs,
                                                              "object",
                                                              numrows,
                                                              numcells,
                                                              outfolder,
                                                              celldata=celldata,
                                                              clusternames=clusternames,
                                                              )
                    quantifypopup.exec()
                    if quantifypopup.saved:
                        regionnames = list(quantifypopup.headernames)[1:]
                    addnewshapeslayer = quantifypopup.saved
                else:
                    self.save_quantified_region(avgs,
                                                "object",
                                                numrows,
                                                cfg.markers,
                                                numcells,
                                                outfolder,
                                                cfg.selected_region_count,
                                                celldata=celldata,
                                                clusternames=clusternames,
                                                )

                if not regionnames == labels and addnewshapeslayer:
                    cfg.viewer.layers.pop(len(cfg.viewer.layers) - 1)
                    properties = {'class': regionnames, }
                    textproperties = {'text': '{class}', 'anchor': 'center', 'size': 10, 'color': 'white', }
                    cfg.viewer.add_shapes(shapeverts,
                                          shape_type=shapetypes,
                                          edge_width=0,
                                          name=f"Quantified Regions {cfg.selected_region_count}",
                                          properties=properties,
                                          text=textproperties,
                                          face_color=[np.array([0.2, 0.2, 0.2])],
                                          )
                cfg.selected_region_count += 1
        utils.log_actions(f"gui.quantify_region(israwimg={israwimg}, clusteringindex={clusteringindex}, "
                          f"shapeverts={[verts.tolist() for verts in shapeverts]}, shapetypes={shapetypes}, "
                          f"imgnum={imgnum}, regionnames={regionnames})")

    def reset_metadata(self):
        """
        Reset the contrast limits, gamma, and opacity values to their original values.
        """
        for i in range(len(cfg.viewer.layers)):
            try:
                cfg.viewer.layers[i].contrast_limits = cfg.viewer.layers[i].contrast_limits_range
            except:
                pass
            try:
                cfg.viewer.layers[i].gamma = 1.0
            except:
                pass
            try:
                cfg.viewer.layers[i].opacity = 1.0
            except:
                pass

    ### TODO: Think of which analyses the cluster names should be used for, as well as with saved files.
    def rename_clusters_gui(self):
        """
        Trigger the "Rename Clusters" popup from the GUI.
        """
        self.rename_clusters()

    def rename_clusters(self,
                        clusteringindex=None,
                        newclusternames=[],
                        ):
        """
        Prompt the user to select a round of clustering and assign a name to each cluster.
        """
        # Check that the user has performed at least one clustering algorithm.
        if len(cfg.clusters_are_pixel_based) == 0:
            utils.display_error_message("No clustering results found",
                                        "Spatial analysis can only be performed on the results of pixel or object clustering.")
            return

        # If clustering has only been executed once, use that by default.
        if clusteringindex is None:
            if len(cfg.clusters_are_pixel_based) == 1:
                clusteringindex = 0

            # If clustering has been executed multiple times, allow user to select which one.
            else:
                selectclusteringround = utils.SelectClusteringRound()
                selectclusteringround.exec()
                if not selectclusteringround.OK:
                    return
                clusteringindex = selectclusteringround.clusteringindex

        ispixelcluster = cfg.clusters_are_pixel_based[clusteringindex]
        clustermodeindex = [i for i, ispixelbased in enumerate(cfg.clusters_are_pixel_based) if
                            ispixelbased == ispixelcluster].index(clusteringindex)

        # Find current names of clusters.
        currentnames = copy.deepcopy(cfg.cluster_names[clusteringindex])

        # If list is empty, find number of clusters and use those for the names.
        if len(currentnames) == 0:
            if ispixelcluster:
                analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Pixel"][
                                  clustermodeindex] * cfg.num_imgs
            else:
                analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][
                                  clustermodeindex] * cfg.num_imgs
            labelimg = self.concat_label_imgs(
                [cfg.labeled_imgs[ind] for ind in range(analysisnum, analysisnum + cfg.num_imgs)])
            numclusters = len(np.unique(labelimg)[np.unique(labelimg) > 0])
            currentnames = [f"Cluster {i + 1}" for i in range(numclusters)]
            oldnames = [str(i + 1) for i in range(numclusters)]
        else:
            oldnames = currentnames

        # Prompt user to rename clusters.
        if newclusternames == []:
            renameclusters = utils.RenameClusters(currentnames)
            renameclusters.exec()
            if not renameclusters.OK:
                return
            newclusternames = renameclusters.newclusternames

        # Store new names in list.
        cfg.cluster_names[clusteringindex] = newclusternames

        if not ispixelcluster:
            cfg.object_cluster_dfs[clustermodeindex]['Cluster'] = [newclusternames[oldnames.index(name)] for name in
                                                                   cfg.object_cluster_dfs[clustermodeindex]['Cluster']]
            cfg.object_cluster_dfs[clustermodeindex].to_csv(
                os.path.join(cfg.object_cluster_directories[clustermodeindex], "SegmentationClusterIDs.csv"))

        # If table is currently visible, update the names accordingly.
        index, _ = utils.find_analysis_round()
        if index == clustermodeindex and ((cfg.analysis_mode == "Pixel" and ispixelcluster) or (
                cfg.analysis_mode == "Object" and not ispixelcluster)):
            cfg.current_vertical_header_labels[3:] = [newclusternames[clusternum] for clusternum in
                                                      cfg.current_table_orders_filtered[cfg.table_index]]
            cfg.table_widget.setVerticalHeaderLabels(np.asarray(cfg.current_vertical_header_labels))
            vwidth = utils.font_width("Helvetica", 12, cfg.current_vertical_header_labels)
            cfg.table_widget.verticalHeader().setMinimumWidth(vwidth + 15)

        utils.log_actions(f"gui.rename_clusters(clusteringindex={clusteringindex}, newclusternames={newclusternames})")

    ### TODO: Add other functionalities for this (grouped results for cluster averages, new table entries for combined average within groups, etc.).
    def sample_group_gui(self):
        """
        Trigger the "Sample Grouping" popup from the GUI.
        """
        self.sample_group()

    def sample_group(self,
                     namelist={},
                     name="",
                     ):
        """
        Open a popup window for the user to assign each image to different groups.

        Args:
            namelist (dict, optional): Dictionary mapping each group name to the names of all images in that group (Default: {}).
            name (str, optional):  (Default: "").
        """
        # No necessity to assign groups if fewer than 3 images are loaded.
        if cfg.num_imgs < 3:
            utils.display_error_message("More images required",
                                        "At least 3 images needed to create groups")
            return

        # Prompt user to define the number of groups
        if namelist == {} or name == "":
            ng = utils.NumGroups()
            ng.exec()
            if not ng.OK:
                return

            # Retrieve the names of all loaded images.
            imgnames = [fname.split("/")[-1] for fname in cfg.file_names]

            # Prompt user to assign each image to a group.
            gawidget = utils.GroupAssign(ng.ngroups)
            gawidget.exec()
            if not gawidget.OK:
                return
            namelist = gawidget.namelist
            name = gawidget.name

        cfg.groups_list.append(namelist)
        cfg.groups_names.append(name)
        utils.log_actions(f"gui.sample_group(namelist={namelist}, name=\"{name}\")")

    def save_data_gui(self):
        """
        Trigger the "Save Data" popup from the GUI.
        """
        self.save_data()

    def save_data(self,
                  savedimg="",
                  ispixelcluster=None,
                  clustermodeindex=None,
                  filename="",
                  ):
        """
        Open a popup for the user to save data. Options include "Save Visible Window" (to save exactly what is currently
        visible in the viewer window), "Save Screenshot of GUI" (to save a screenshot of the entire RAPID GUI window),
        "Save Clusters" (to save each individual cluster from a selected round of clustering), "Save Table" (to export
        the exact data table currently being displayed as a csv file), and "Save Full Visible Images" (to save each
        user-selected raw image individually, including contrast limits and colormaps).

        Args:
            savedimg (str, optional) Indicator of what data will be saved (Default: "").
            ispixelcluster (bool, optional) If True, the clusters being saved are pixel-based. Otherwise, the clusters being saved are object-based (Default: "").
            clustermodeindex (int, optional) Round of pixel/object clustering results being saved (Default: "").
            filename (str, optional) Path to root directory where clustering data will be saved (Default: "").
        """
        if savedimg == "":
            savedata = utils.SaveData()
            savedata.exec()
            if not savedata.OK:
                return
            savedimg = savedata.savedimg

        cfg.viewer.status = "Saving..."
        if savedimg == "Visible Window":
            utils.save_visible()
            utils.log_actions(f"gui.save_data(savedimg=\"{savedimg}\")")

        elif savedimg == "Screenshot":
            utils.save_window()
            utils.log_actions(f"gui.save_data(savedimg=\"{savedimg}\")")

        elif savedimg == "Table":
            utils.save_table()
            utils.log_actions(f"gui.save_data(savedimg=\"{savedimg}\")")

        elif savedimg == "Full Visible Images":
            utils.save_visible_full()
            utils.log_actions(f"gui.save_data(savedimg=\"{savedimg}\")")

        elif savedimg == "Clusters":
            # User can only save clusters after having performed clustering.
            if len(cfg.clusters_are_pixel_based) == 0:
                utils.display_error_message("Clustering has not been executed",
                                            "Please run a clustering algorithm first")
                return

            # If clustering has been performed once, use that by default.
            if len(cfg.clusters_are_pixel_based) == 1:
                ispixelcluster = cfg.clusters_are_pixel_based[0]
                clustermodeindex = 0

            # If clustering has been performed more than once, allow user to select which clustering results to use.
            elif ispixelcluster is None and clustermodeindex is None:
                selectclusteringround = utils.SelectClusteringRound()
                selectclusteringround.exec()
                if not selectclusteringround.OK:
                    return
                ispixelcluster = selectclusteringround.ispixelcluster
                clustermodeindex = selectclusteringround.clusteringnum

            if ispixelcluster:
                analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Pixel"][
                                  clustermodeindex] * cfg.num_imgs
            else:
                analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][
                                  clustermodeindex] * cfg.num_imgs
            grey = self.concat_label_imgs([cfg.labeled_imgs[i] for i in range(analysisnum, analysisnum + cfg.num_imgs)])

            # Prompt user to choose path to output folder where clusters will be saved.
            if filename == "":
                filename, _ = QFileDialog.getSaveFileName(parent=cfg.viewer.window.qt_viewer,
                                                          caption='Save clusters',
                                                          directory=cfg.output_folder,
                                                          )
            outfolder = utils.create_new_folder(os.path.split(filename)[-1], os.path.split(filename)[0])

            utils.save_clusters(outfolder,
                                grey,
                                )
            utils.log_actions(f"gui.save_data(savedimg=\"{savedimg}\", ispixelcluster={ispixelcluster}, "
                              f"clustermodeindex={clustermodeindex}, filename=\"{filename}\")")

    def save_environment(self):
        """
        Save a RAPID GUI session so the user may resume it exactly as they are leaving it.
        """
        cfg.viewer.status = "Saving environment..."
        utils.log_actions("gui.save_environment()")

        # Store variables.
        config = configparser.ConfigParser()
        config.add_section("Variables")
        config.set("Variables", 'hasaddedtable', unicode(cfg.has_added_table))
        config.set("Variables", 'haseditedimage', unicode(cfg.has_edited_image))
        config.set("Variables", 'hasloadedpixel', unicode(cfg.has_loaded_pixel))
        config.set("Variables", 'hasloadedimage', unicode(cfg.has_loaded_image))

        config.set("Variables", 'action_logger_path', unicode(cfg.action_logger_path))
        config.set("Variables", 'analysisindex', unicode(cfg.analysis_index))
        config.set("Variables", 'analysismode', unicode(cfg.analysis_mode))
        config.set("Variables", 'biaxialcount', unicode(cfg.biaxial_count))
        config.set("Variables", 'displayselectedcount', unicode(cfg.display_selected_count))
        config.set("Variables", 'editimagepath', unicode(cfg.edit_img_path))
        config.set("Variables", 'numimgs', unicode(cfg.num_imgs))
        config.set("Variables", 'nummarkers', unicode(cfg.num_markers))
        config.set("Variables", 'objectclustercount', unicode(cfg.object_cluster_count))
        config.set("Variables", 'pixelclustercount', unicode(cfg.pixel_cluster_count))
        config.set("Variables", 'resolution', unicode(cfg.resolution))
        config.set("Variables", 'segmentcount', unicode(cfg.segment_count))
        config.set("Variables", 'selectedregioncount', unicode(cfg.selected_region_count))
        config.set("Variables", 'tableimgcount', unicode(cfg.table_count))
        config.set("Variables", 'tableindex', unicode(cfg.table_index))
        config.set("Variables", 'umapcount', unicode(cfg.umap_count))

        config.set("Variables", 'analysislog', unicode(cfg.analysis_log))
        config.set("Variables", 'cellclustervals', unicode([arr.tolist() for arr in cfg.cell_cluster_vals]))
        config.set("Variables", 'cellcoordinates', unicode(cfg.cell_coordinates))
        config.set("Variables", 'clustersarepixelbased', unicode(cfg.clusters_are_pixel_based))
        config.set("Variables", 'clusternames', unicode(cfg.cluster_names))
        config.set("Variables", 'currentlyselected', unicode(cfg.currently_selected))
        config.set("Variables", 'currentstep', unicode(cfg.viewer.dims.current_step[:-2]))
        config.set("Variables", 'currenttableordersfiltered', unicode(cfg.current_table_orders_filtered))
        config.set("Variables", 'currenttableorderfull', unicode(cfg.current_table_order_full))
        config.set("Variables", 'currentverticalheaderlabels', unicode(cfg.current_vertical_header_labels.tolist()))
        config.set("Variables", 'datalist', unicode([arr.tolist() for arr in cfg.data_list]))
        config.set("Variables", 'editactions', unicode(cfg.edit_actions))
        config.set("Variables", 'filenames', unicode(cfg.file_names))
        config.set("Variables", 'fulltab', unicode(cfg.full_tab.to_json()))
        config.set("Variables", 'groupslist', unicode(cfg.groups_list))
        config.set("Variables", 'groupsnames', unicode(cfg.groups_names))
        config.set("Variables", 'histogramcounts', unicode(cfg.histogram_counts))
        config.set("Variables", 'imageisflipped', unicode(cfg.img_is_flipped))
        config.set("Variables", 'imageshapelist', unicode(cfg.img_shape_list))
        config.set("Variables", 'labeledimgs', unicode([arr.tolist() for arr in cfg.labeled_imgs]))
        config.set("Variables", 'lowerboundslist', unicode(cfg.lower_bounds_list))
        config.set("Variables", 'markers', unicode(cfg.markers))
        config.set("Variables", 'maximageshape', unicode([arr.tolist() for arr in cfg.max_img_shape]))
        config.set("Variables", 'maxpixelclustervals', unicode(cfg.max_pixel_clustervals))
        config.set("Variables", 'maxvals', unicode(cfg.max_vals))
        config.set("Variables", 'mergedimagespaths', unicode(cfg.merge_img_paths))
        config.set("Variables", 'mergememmarkers', unicode(cfg.merge_mem_markers))
        config.set("Variables", 'mergenucmarkers', unicode(cfg.merge_nuc_markers))
        config.set("Variables", 'minvals', unicode(cfg.min_vals))
        config.set("Variables", 'objectclustercolors', unicode([arr.tolist() for arr in cfg.object_cluster_colors]))
        config.set("Variables", 'objectclusterdfs', unicode([d.to_json() for d in cfg.object_cluster_dfs]))
        config.set("Variables", 'objectclusterdirectories', unicode(cfg.object_cluster_directories))
        config.set("Variables", 'objectclusterindices', unicode(cfg.object_cluster_indices))
        config.set("Variables", 'objectimgnames', unicode(cfg.object_img_names).replace('%', '%%'))
        config.set("Variables", 'pixelclustercolors', unicode([arr.tolist() for arr in cfg.pixel_cluster_colors]))
        config.set("Variables", 'pixelclusterdirectories', unicode(cfg.pixel_cluster_directories))
        config.set("Variables", 'pixelclusterindices', unicode(cfg.pixel_cluster_indices))
        config.set("Variables", 'pixelclustermarkers', unicode(cfg.pixel_cluster_markers))
        coords = []
        for i in range(len(cfg.plot_coordinates)):
            coords.append([arr.tolist() for arr in cfg.plot_coordinates[i]])
        config.set("Variables", 'plotcoordinates', unicode(coords))
        config.set("Variables", 'plotisumap', unicode(cfg.plot_is_umap))
        config.set("Variables", 'plotsegmentationindices', unicode(cfg.plot_segmentation_indices))
        config.set("Variables", 'plotxmins', unicode(cfg.plot_x_mins))
        config.set("Variables", 'plotxmaxs', unicode(cfg.plot_x_maxs))
        config.set("Variables", 'plotymins', unicode(cfg.plot_y_mins))
        config.set("Variables", 'plotymaxs', unicode(cfg.plot_y_maxs))
        config.set("Variables", 'segmentationclusteringrounds', unicode(cfg.segmentation_clustering_rounds))
        config.set("Variables", 'segmentationindices', unicode(cfg.segmentation_indices))
        config.set("Variables", 'segmentationzarrpaths', unicode(cfg.segmentation_zarr_paths))
        config.set("Variables", 'segmentcounts', unicode(cfg.segment_counts))
        config.set("Variables", 'tableimagenames', unicode(cfg.table_img_names).replace('%', '%%'))
        config.set("Variables", 'tableparams', unicode(cfg.table_params))
        config.set("Variables", 'totalnumcells', unicode(cfg.total_num_cells))
        config.set("Variables", 'upperboundslist', unicode(cfg.upper_bounds_list))
        if cfg.has_added_table:
            config.set("Variables", 'currenttabdata', unicode(cfg.current_tab_data.tolist()))
            config.set("Variables", 'tableorder', unicode(cfg.table_order))
            config.set("Variables", 'tablecurrentmarker', unicode(cfg.sort_table_widget.marker.value))
            config.set("Variables", 'tablecurrentdata', unicode(cfg.sort_table_widget.data.value).replace('%', '%%'))
            config.set("Variables", 'tablecurrentsort', unicode(cfg.sort_table_widget.sort.value))
            config.set("Variables", 'totalnumrows', unicode(cfg.total_num_rows))

        # Save variables to a config file.
        outfolder = utils.create_new_folder("SavedEnvironment", cfg.output_folder)
        cfgfile = open(os.path.join(outfolder, "savedenvironment.ini"), "w")
        config.write(cfgfile)
        cfgfile.close()

        # Store metadata for all layers in the GUI.
        fh = zarr.open(outfolder, mode='a')
        for i in range(len(cfg.viewer.layers)):
            if isinstance(cfg.viewer.layers[i], napari.layers.shapes.shapes.Shapes):
                data = fh.create_dataset(f"ShapeLayer_{i + 1}", data=np.array([0]))
                data.attrs["Data"] = [arr.tolist() for arr in cfg.viewer.layers[i].data]
                data.attrs["ShapeType"] = cfg.viewer.layers[i].shape_type
                data.attrs["Properties"] = cfg.viewer.layers[i].properties["class"].tolist() if "class" in \
                                                                                                cfg.viewer.layers[
                                                                                                    i].properties else ""
                data.attrs["Name"] = cfg.viewer.layers[i].name
                data.attrs["Text"] = [cfg.viewer.layers[i].text.size,
                                      cfg.viewer.layers[i].text.color.tolist()]
                data.attrs["FaceColor"] = cfg.viewer.layers[i].face_color.tolist()
                data.attrs["Visible"] = cfg.viewer.layers[i].visible
            else:
                data = fh.create_dataset(f"ImageLayer_{i + 1}", data=cfg.viewer.layers[i].data)
                data.attrs["Visible"] = cfg.viewer.layers[i].visible
                data.attrs["Name"] = cfg.viewer.layers[i].name
                try:
                    data.attrs["CL"] = [float(j) for j in cfg.viewer.layers[i].contrast_limits]
                    data.attrs["CLRange"] = [float(j) for j in cfg.viewer.layers[i].contrast_limits_range]
                    data.attrs["Gamma"] = cfg.viewer.layers[i].gamma
                    data.attrs["Opacity"] = cfg.viewer.layers[i].opacity
                    data.attrs["Colormap0"] = int(cfg.viewer.layers[i].colormap.colors[-1][0] * 255)
                    data.attrs["Colormap1"] = int(cfg.viewer.layers[i].colormap.colors[-1][1] * 255)
                    data.attrs["Colormap2"] = int(cfg.viewer.layers[i].colormap.colors[-1][2] * 255)
                except:
                    pass
        cfg.viewer.status = "Completed saving environment"

    def save_quantified_region(self,
                               avgs,
                               imgtype,
                               numrows,
                               markernames,
                               numregions,
                               outfolder,
                               selectedregioncount,
                               celldata=np.array([]),
                               clusternames=[],
                               ):
        horizontalheaders = [f"Region {j + 1}" for j in range(len(avgs))]

        verticalheaders = []
        if imgtype == 'object':
            verticalheaders.append('# Cells')
        else:
            verticalheaders.append('# Pixels')
        for i in range(numrows):
            if imgtype == "raw":
                verticalheaders.append(markernames[i])
            else:
                if clusternames == []:
                    verticalheaders.append(f"Cluster {i + 1}")
                else:
                    verticalheaders.append(clusternames[i])

        arr = np.array(avgs)
        arr = np.transpose(arr)
        arr = np.vstack((np.array(numregions), arr))
        df = pd.DataFrame(arr)
        df.columns = horizontalheaders
        df.insert(0, '', verticalheaders)
        df.to_csv(os.path.join(outfolder, f"QuantifiedRegionClusters_{selectedregioncount}.csv"), index=False)
        if imgtype == 'object':
            for i in range(len(celldata)):
                celldata[i].to_csv(os.path.join(outfolder, f"QuantifiedRegionCellIDs_{i}.csv"), index=False)

    def segment(self,
                modelindex=None,
                imageres=None,
                mergemarkerindex=None,
                add_grey_img=None,
                add_color_img=None,
                quantavg=None,
                probthreshold=None,
                minsize=None,
                maxsize=None,
                histogramnormalize=None,
                ):
        """
        Use the RAPID segmentation algorithm on the images loaded into the RAPID GUI.

        Args:
            modelindex (int, optional): Index corresponding to segmentation model being used (Default: None).
            imageres (float, optional): Resolution of the image, in units of nanometers per pixel (Default: None).
            mergemarkerindex (int, optional): Index of merged-marker image being used for segmentation (Default: None).
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            quantavg (bool, optional): If True, use mean expression values for quantification. Otherwise, calculate root-mean-square values (Default: None).
            probthreshold (float, optional): Value in the range [0,1] defining model prediction probability threshold for cells to include (Default: None).
            minsize (int, optional): Minimum pixel area of cells to include in segmentation (Default: None).
            maxsize (int, optional): Maximum pixel area of cells to include in segmentation (Default: None).
            histogramnormalize (bool, optional): If True, perform histogram normalization. Otherwise, do nothing (Default: False).
        """
        # Can only segment if markers have been merged.
        if len(cfg.segment_counts) == 0:
            utils.display_error_message("Please merge markers first",
                                        "Begin by opening the image(s) that you would like to segment, then merge the markers to be used for segmentation.")
            return

        if modelindex is None:
            # Indicate whether to use RAPID or RAPID+ segmentation model.
            segmentationmodel = utils.SegmentationModel()
            segmentationmodel.exec()
            if not segmentationmodel.OK:
                return
            modelindex = segmentationmodel.modelindex

        if histogramnormalize is None:
            # Indicate whether to use RAPID or RAPID+ segmentation model.
            histogram = utils.HistogramNormalize()
            histogram.exec()
            if not histogram.OK:
                return
            histogramnormalize = histogram.normalize

        rootfolder = os.path.dirname(os.path.abspath(__file__))
        modelpaths = [rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6.pth",
                      rootfolder + "/../models/RAPID-O_RDSB_DC_Fin__MemMix_UnetPlus_Model__resnet50_nclass_2_nchannels_2_gpu_4_seed_100_DCBD38_theta_0.6.pth",
                      rootfolder + "/../models/Model__vgg19_nclass_2_nchannels_2_gpu_0_seed_10049_theta_0.6_Plus.pth"]
        fileurls = ["https://drive.google.com/uc?id=1JiYrohWce5-uLjI_-yovDUUxroorwE5W",
                    "https://drive.google.com/uc?id=1MQjnmpmflQ-BvWgRbsQXwyeQjjfod4mw",
                    "https://drive.google.com/uc?id=1Ji6XmIITbcKR05wt86USEWuous_K5SWl"]
        for i, path in enumerate(modelpaths):
            if not os.path.exists(path):
                gdown.download(fileurls[i], path, verify=False)
        modelpath = modelpaths[modelindex]

        # Prompt user to indicate the resolution of the images.
        if cfg.segment_count == 0:
            if imageres is None:
                res = utils.ImageRes()
                res.exec()
                if not res.OK:
                    return
                cfg.resolution = res.imageres
            else:
                cfg.resolution = imageres

        # If user has merged markers multiple times, prompt to indicate which one to use.
        if len(cfg.segment_counts) == 1:
            mergemarkerindex = 0
        elif mergemarkerindex is None:
            mergememiteration = utils.MergeMarkerIteration()
            mergememiteration.exec()
            if not mergememiteration.OK:
                return
            mergemarkerindex = mergememiteration.iteration

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        # Allow user to define wither to quantify using mean expression, or root-mean-square.
        if quantavg is None:
            quantmode = utils.QuantificationMode()
            quantmode.exec()
            if not quantmode.OK:
                return
            quantavg = quantmode.avg

        # Save images to zarr so they can be easily added when loading segmentation results in the future.
        outfolder = utils.create_new_folder("Segmentation", cfg.output_folder)
        os.mkdir(os.path.join(outfolder, "RawImages"))
        fh = zarr.open(os.path.join(outfolder, "RawImages"), mode='a')
        for i in range(cfg.num_markers):
            data = fh.create_dataset(f"{i + 1}_{cfg.viewer.layers[i].name}", data=cfg.viewer.layers[i].data)
            data.attrs["CL"] = [float(j) for j in cfg.viewer.layers[i].contrast_limits]
            data.attrs["CLRange"] = [float(j) for j in cfg.viewer.layers[i].contrast_limits_range]
            data.attrs["Gamma"] = cfg.viewer.layers[i].gamma
            data.attrs["Opacity"] = cfg.viewer.layers[i].opacity
            data.attrs["Colormap0"] = int(cfg.viewer.layers[i].colormap.colors[-1][0] * 255)
            data.attrs["Colormap1"] = int(cfg.viewer.layers[i].colormap.colors[-1][1] * 255)
            data.attrs["Colormap2"] = int(cfg.viewer.layers[i].colormap.colors[-1][2] * 255)
            data.attrs["Visible"] = cfg.viewer.layers[i].visible
            data.attrs["Name"] = cfg.viewer.layers[i].name
        fh.attrs['filenames'] = cfg.file_names
        fh.attrs['maximageshape'] = cfg.max_img_shape.tolist()
        fh.attrs['markers'] = cfg.markers
        fh.attrs['markernums'] = cfg.marker_inds
        fh.attrs['imageshapelist'] = cfg.img_shape_list
        fh.attrs['numimgs'] = cfg.num_imgs
        hf = zarr.open(cfg.merge_img_paths[mergemarkerindex], mode='r')
        memimg = hf['Membrane']
        nucimg = hf['Nucleus']
        fh = zarr.open(outfolder, mode='a')
        fh.create_dataset("MergedImage", data=np.stack([memimg, nucimg], axis=0))

        if not cfg.has_added_table:
            cfg.analysis_mode = "Segmentation"

        # Check if the user has already segmented on the selected merged image.
        alreadysegmented = True
        if cfg.segment_counts[mergemarkerindex][modelindex] == -1 or cfg.histogram_counts[mergemarkerindex][
            histogramnormalize] == -1:
            alreadysegmented = False
            cfg.segment_counts[mergemarkerindex][modelindex] = np.max(np.array(cfg.segment_counts) + 1)
            cfg.histogram_counts[mergemarkerindex][histogramnormalize] = 0

        # No need to segment again on a merged image that has already been passed through the algorithm.
        if not alreadysegmented:
            cfg.viewer.status = "Segmenting..."
            cfg.segmentation_zarr_paths.append(outfolder)
            cfg.viewer.window._status_bar._toggle_activity_dock(True)
            with progress(cfg.file_names, desc='Image', total=0 if len(cfg.file_names) == 1 else None, ) as pbr:
                for name in pbr:
                    i = cfg.file_names.index(name)
                    memimage = memimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]]
                    nucimage = nucimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]]
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    feature = objectmodels.unet_featurize(memimg=memimage, nucimg=nucimage,
                                                          containsmem=cfg.merge_mem_markers[mergemarkerindex],
                                                          containsnuc=cfg.merge_nuc_markers[mergemarkerindex],
                                                          device=device, segmodelpath=modelpath,
                                                          histogramnormalize=histogramnormalize)
                    fh.create_dataset(f"Features{i}", data=feature, dtype=np.float)
            cfg.viewer.window._status_bar._toggle_activity_dock(False)
        zarrpath = cfg.segmentation_zarr_paths[cfg.segment_counts[mergemarkerindex][modelindex]]

        if all(prob is not None for prob in (probthreshold, minsize, maxsize)):
            self.apply_segmentation(add_grey_img,
                                    add_color_img,
                                    quantavg,
                                    outfolder,
                                    zarrpath,
                                    probthreshold,
                                    minsize,
                                    maxsize,
                                    )
            utils.log_actions(f"gui.segment(modelindex={modelindex}, imageres={imageres}, "
                              f"mergemarkerindex={mergemarkerindex}, add_grey_img={add_grey_img}, "
                              f"add_color_img={add_color_img}, quantavg={quantavg}, probthreshold={probthreshold}, "
                              f"minsize={minsize}, maxsize={maxsize}, histogramnormalize={histogramnormalize})")

        else:
            # Initialize thresholds to use for segmentation preview popup window.

            # Populate the segmentation preview popup window.
            fh = zarr.open(zarrpath, mode='r')
            binarized = np.array(fh["Features0"]) >= 1.0
            blobs = measure.label(binarized, connectivity=1)
            blobs = morphology.remove_small_objects(blobs, min_size=int(round(10 * 0.284 / cfg.resolution)))
            blobs = utils.remove_large_objects(blobs, maxsize=int(round(2000 * 0.284 / cfg.resolution)))
            binarized[blobs == 0] = 0
            cfg.segment_viewer = napari.Viewer()
            cfg.segment_viewer_prob_thresh = 1.0
            cfg.segment_viewer_img_id = 0
            cfg.segment_viewer_min_size = round(10 * 0.284 / cfg.resolution)
            cfg.segment_viewer_max_size = round(2000 * 0.284 / cfg.resolution)
            cfg.segment_viewer.add_image(binarized[:cfg.img_shape_list[0][0], :cfg.img_shape_list[0][1]],
                                         name="Segmentation", blending="additive", colormap="red",
                                         contrast_limits=[0, 1])
            if cfg.merge_nuc_markers[mergemarkerindex]:
                cfg.segment_viewer.add_image(nucimg[0, :cfg.img_shape_list[0][0], :cfg.img_shape_list[0][1]],
                                             name="Merged Nuclear Markers", blending="additive")
            if cfg.merge_mem_markers[mergemarkerindex]:
                cfg.segment_viewer.add_image(memimg[0, :cfg.img_shape_list[0][0], :cfg.img_shape_list[0][1]],
                                             name="Merged Membrane Markers", blending="additive")

            # Find names of images to populate dropdown.
            names = []
            for i in range(len(cfg.file_names)):
                names.append(cfg.file_names[i].split("/")[-1])

            # Allow user to toggle between images.
            @magicgui(auto_call=True, image={"choices": names, "label": ""})
            def change_image_segmentgui(image: str):
                cfg.segment_viewer_img_id = names.index(image)
                segmented = np.array(
                    fh[f"Features{cfg.segment_viewer_img_id}"]) >= cfg.segment_viewer_prob_thresh
                blobs = measure.label(segmented, connectivity=1)
                blobs = morphology.remove_small_objects(blobs, min_size=int(cfg.segment_viewer_min_size))
                blobs = utils.remove_large_objects(blobs, maxsize=int(cfg.segment_viewer_max_size))
                segmented[blobs == 0] = 0
                cfg.segment_viewer.layers["Segmentation"].data = segmented[
                                                                 :
                                                                 cfg.img_shape_list[cfg.segment_viewer_img_id][
                                                                     0],
                                                                 :
                                                                 cfg.img_shape_list[cfg.segment_viewer_img_id][
                                                                     1]]
                if cfg.merge_nuc_markers[mergemarkerindex]:
                    cfg.segment_viewer.layers["Merged Nuclear Markers"].data = nucimg[
                                                                               cfg.segment_viewer_img_id, :
                                                                                                          cfg.img_shape_list[
                                                                                                              cfg.segment_viewer_img_id][
                                                                                                              0],
                                                                               :
                                                                               cfg.img_shape_list[
                                                                                   cfg.segment_viewer_img_id][
                                                                                   1]]
                if cfg.merge_mem_markers[mergemarkerindex]:
                    cfg.segment_viewer.layers["Merged Membrane Markers"].data = memimg[
                                                                                cfg.segment_viewer_img_id, :
                                                                                                           cfg.img_shape_list[
                                                                                                               cfg.segment_viewer_img_id][
                                                                                                               0],
                                                                                :
                                                                                cfg.img_shape_list[
                                                                                    cfg.segment_viewer_img_id][
                                                                                    1]]

            # Apply filters for final segmented results.
            @magicgui(call_button="Finish")
            def finish_segmentgui() -> Image:
                self.apply_segmentation(add_grey_img,
                                        add_color_img,
                                        quantavg,
                                        outfolder,
                                        cfg.segmentation_zarr_paths[cfg.segment_counts[mergemarkerindex][modelindex]],
                                        cfg.segment_viewer_prob_thresh,
                                        cfg.segment_viewer_min_size,
                                        cfg.segment_viewer_max_size,
                                        )

                utils.log_actions(f"gui.segment(modelindex={modelindex}, imageres={cfg.resolution}, "
                                  f"mergemarkerindex={mergemarkerindex}, add_grey_img={add_grey_img}, "
                                  f"add_color_img={add_color_img}, quantavg={quantavg}, "
                                  f"probthreshold={cfg.segment_viewer_prob_thresh}, "
                                  f"minsize={cfg.segment_viewer_min_size}, maxsize={cfg.segment_viewer_max_size}, "
                                  f"histogramnormalize={histogramnormalize})")

                cfg.segment_viewer.window.qt_viewer.close()
                cfg.segment_viewer.window._qt_window.close()

            # Allow user to select maximum size for cells. Any cells above this are filtered out.
            @magicgui(auto_call=True,
                      threshold={"widget_type": "FloatSlider", "max": cfg.segment_viewer_max_size * 4,
                                 "label": "Maximum Size:"}, )
            def max_size_threshold_segmentgui(threshold: int = cfg.segment_viewer_max_size) -> Image:
                cfg.segment_viewer_max_size = round(threshold)
                segmented = np.array(
                    fh[f"Features{cfg.segment_viewer_img_id}"]) >= cfg.segment_viewer_prob_thresh
                blobs = measure.label(segmented, connectivity=1)
                blobs = morphology.remove_small_objects(blobs, min_size=int(cfg.segment_viewer_min_size))
                blobs = utils.remove_large_objects(blobs, maxsize=int(cfg.segment_viewer_max_size))
                segmented[blobs == 0] = 0
                cfg.segment_viewer.layers["Segmentation"].data = segmented
                if cfg.merge_nuc_markers[mergemarkerindex]:
                    cfg.segment_viewer.layers["Merged Nuclear Markers"].data = nucimg[
                                                                               cfg.segment_viewer_img_id, :, :]
                if cfg.merge_mem_markers[mergemarkerindex]:
                    cfg.segment_viewer.layers["Merged Membrane Markers"].data = memimg[
                                                                                cfg.segment_viewer_img_id, :,
                                                                                :]

            # Allow user to select minimum size for cells. Any cells below this are filtered out.
            @magicgui(auto_call=True,
                      threshold={"widget_type": "FloatSlider", "max": cfg.segment_viewer_min_size * 10,
                                 "label": "Minimum Size:"}, )
            def min_size_threshold_segmentgui(threshold: int = cfg.segment_viewer_min_size) -> Image:
                cfg.segment_viewer_min_size = round(threshold)
                segmented = np.array(
                    fh[f"Features{cfg.segment_viewer_img_id}"]) >= cfg.segment_viewer_prob_thresh
                blobs = measure.label(segmented, connectivity=1)
                blobs = morphology.remove_small_objects(blobs, min_size=int(cfg.segment_viewer_min_size))
                blobs = utils.remove_large_objects(blobs, maxsize=int(cfg.segment_viewer_max_size))
                segmented[blobs == 0] = 0
                cfg.segment_viewer.layers["Segmentation"].data = segmented
                if cfg.merge_nuc_markers[mergemarkerindex]:
                    cfg.segment_viewer.layers["Merged Nuclear Markers"].data = nucimg[
                                                                               cfg.segment_viewer_img_id, :, :]
                if cfg.merge_mem_markers[mergemarkerindex]:
                    cfg.segment_viewer.layers["Merged Membrane Markers"].data = memimg[
                                                                                cfg.segment_viewer_img_id, :,
                                                                                :]

            # Allow user to set a minimum confidence value for segmentation.
            @magicgui(auto_call=True,
                      threshold={"widget_type": "FloatSlider", "max": 1, "label": "Probability Threshold:"}, )
            def prob_threshold_segmentgui(threshold: float = cfg.segment_viewer_prob_thresh) -> Image:
                cfg.segment_viewer_prob_thresh = round(threshold, 2)
                segmented = np.array(
                    fh[f"Features{cfg.segment_viewer_img_id}"]) >= cfg.segment_viewer_prob_thresh
                blobs = measure.label(segmented, connectivity=1)
                blobs = morphology.remove_small_objects(blobs, min_size=int(cfg.segment_viewer_min_size))
                blobs = utils.remove_large_objects(blobs, maxsize=int(cfg.segment_viewer_max_size))
                segmented[blobs == 0] = 0
                cfg.segment_viewer.layers["Segmentation"].data = segmented
                if cfg.merge_nuc_markers[mergemarkerindex]:
                    cfg.segment_viewer.layers["Merged Nuclear Markers"].data = nucimg[
                                                                               cfg.segment_viewer_img_id, :, :]
                if cfg.merge_mem_markers[mergemarkerindex]:
                    cfg.segment_viewer.layers["Merged Membrane Markers"].data = memimg[
                                                                                cfg.segment_viewer_img_id, :,
                                                                                :]

            # Add widgets to the segmentation popup window.
            segmentwidget = QWidget()
            segmentlayout = QGridLayout()
            segmentlayout.setSpacing(0)
            segmentlayout.setContentsMargins(0, 0, 0, 0)
            if cfg.num_imgs > 1:
                changeimagegui = change_image_segmentgui.native
                changeimagegui.setToolTip("Choose a different image to edit")
                segmentlayout.addWidget(changeimagegui, 0, 0)
                reindex = 0
            else:
                reindex = 1
            probfiltergui = prob_threshold_segmentgui.native
            probfiltergui.setToolTip("Set probability threshold")
            segmentlayout.addWidget(probfiltergui, 0, 1 - reindex)
            minsizegui = min_size_threshold_segmentgui.native
            minsizegui.setToolTip("Set minimum size")
            segmentlayout.addWidget(minsizegui, 0, 2 - reindex)
            maxsizegui = max_size_threshold_segmentgui.native
            maxsizegui.setToolTip("Set maximum size")
            segmentlayout.addWidget(maxsizegui, 0, 3 - reindex)
            finishgui = finish_segmentgui.native
            finishgui.setToolTip("Finish")
            segmentlayout.addWidget(finishgui, 1, 1, 1, 2 - reindex)
            segmentwidget.setLayout(segmentlayout)
            cfg.segment_viewer.window.add_dock_widget(segmentwidget, area="bottom")

    def set_invisible(self, viewer):
        """
        Set all layers within a viewer window to become invisible.

        Args:
            viewer (napari.Viewer): Viewer window whose layers are to be set to invisible.
        """
        for le in range(len(viewer.layers)):
            if viewer.layers[le].visible:
                viewer.layers[le].visible = False

    def sort_table_image(self,
                         data="",
                         marker="",
                         sort="",
                         ):
        """
        Populate the table according to the currently selected image and round of analysis, the parameter that it is
        sorted according to, and whether the user indicated for it to sort in ascending or descending order.

        Args:
            data (str, optional): Name of analysis round being displayed in the table (Default: "").
            marker (str, optional): Name of the cell marker or parameter that the table will be sorted by (Default: "").
            sort (str, optional): Indicator to sort in either increasing or decreasing order (Default: "").
        """
        if data == "":
            data = cfg.sort_table_widget.data.value
        else:
            cfg.sort_table_widget.data.value = data
        if marker == "":
            marker = cfg.sort_table_widget.marker.value
        else:
            cfg.sort_table_widget.marker.value = marker
        if sort == "":
            sort = cfg.sort_table_widget.sort.value
        else:
            cfg.sort_table_widget.sort.value = sort

        # Make sure analysis has been done and that there is a table to be displayed.
        if (cfg.segment_count > 0 or cfg.pixel_cluster_count > 0) and not cfg.is_loading_env:
            # Get the index of the round of analysis being displayed in the table.
            index = cfg.table_img_names.index(data)
            cfg.table_index = copy.deepcopy(index)

            # If displaying segmentation results.
            if index in cfg.segmentation_indices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                cfg.analysis_mode = "Segmentation"
                cfg.analysis_index = cfg.segmentation_indices.index(index)
                datatab = copy.deepcopy(cfg.data_list[cfg.table_index])

                # Get the column being used to sort the table and sort the clusters according to user selection.
                m = cfg.table_params.index(marker)

                # Find the order by which to sort the cells in the table.
                if m > 0:
                    cfg.current_table_order_full = np.argsort(cfg.data_list[cfg.table_index][:, m - 1]).astype(
                        np.int).tolist()
                else:
                    cfg.current_table_order_full = [i for i in range(len(cfg.data_list[cfg.table_index]))]
                if sort == "▼":
                    cfg.current_table_order_full.reverse()

                # Filter out cells that don't fall within the user-defined lower/upper bounds.
                filtereddata = np.append(cfg.data_list[cfg.table_index][cfg.current_table_order_full, :],
                                         np.expand_dims(np.arange(len(cfg.data_list[cfg.table_index])), 1), 1)
                for chan in range(len(cfg.lower_bounds_list[cfg.table_index])):
                    filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(
                        cfg.upper_bounds_list[cfg.table_index][chan], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(
                        cfg.lower_bounds_list[cfg.table_index][chan], 3))
                    filtereddata = filtereddata[filtermask]
                cfg.current_table_orders_filtered[cfg.table_index] = [cfg.current_table_order_full[j] for j in
                                                                      filtereddata[:, -1].astype(np.int).tolist()]

                # Get the cell indices to be used as the vertical header labels.
                cellnumlabels = [cfg.current_table_order_full[j] + 1 for j in
                                 filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the cells according to user selection and update the table accordingly.
                displaytab = datatab[cfg.current_table_orders_filtered[cfg.table_index], :]
                self.update_table(displaytab,
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(datatab),
                                  cellnumlabels,
                                  )

            # If displaying object-based clustering results.
            elif index in cfg.object_cluster_indices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                cfg.analysis_mode = "Object"
                cfg.analysis_index = cfg.object_cluster_indices.index(index)
                currentdata = copy.deepcopy(cfg.data_list[cfg.table_index])

                # Find any clusters for the current round of analysis that have at least one cell.
                clusters = []
                for i in range(len(currentdata)):
                    if currentdata[i, 0] != 0.0:
                        clusters.append(i)

                # Get the column being used to sort the table and sort the clusters according to user selection.
                m = cfg.table_params.index(marker)
                if m == 0:
                    cfg.current_table_order_full = np.arange(len(currentdata)).tolist()
                else:
                    cfg.current_table_order_full = np.argsort(currentdata[:, m]).astype(np.int).tolist()
                if sort == "▼":
                    cfg.current_table_order_full.reverse()

                # Filter out clusters that don't fall within the user-defined lower/upper bounds.
                filtereddata = currentdata[cfg.current_table_order_full, 1:]
                filtereddata = np.append(filtereddata, np.expand_dims(np.arange(len(cfg.current_table_order_full)), 1),
                                         1)
                for chan in range(len(cfg.lower_bounds_list[cfg.table_index])):
                    filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(
                        cfg.upper_bounds_list[cfg.table_index][chan], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(
                        cfg.lower_bounds_list[cfg.table_index][chan], 3))
                    filtereddata = filtereddata[filtermask]
                cfg.current_table_orders_filtered[cfg.table_index] = [cfg.current_table_order_full[i] for i in
                                                                      filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the clusters according to user selection and update the table accordingly.
                displaydata = currentdata[cfg.current_table_orders_filtered[cfg.table_index], :]

                # Find names for the clusters for the round of clustering being displayed in the table.
                clusterindex, _ = utils.find_analysis_round()
                annotationindex = [j for j, n in enumerate(cfg.clusters_are_pixel_based) if not n][clusterindex]

                # Update the display table in the GUI.
                self.update_table(displaydata,
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(clusters),
                                  cfg.current_table_orders_filtered[cfg.table_index],
                                  headernames=cfg.cluster_names[annotationindex],
                                  )

            # If displaying pixel-based clustering results.
            elif index in cfg.pixel_cluster_indices:
                # Store which type of analysis is being displayed and the corresponding dataset.
                cfg.analysis_mode = "Pixel"
                cfg.analysis_index = cfg.pixel_cluster_indices.index(index)
                currentdata = copy.deepcopy(cfg.data_list[cfg.table_index])

                # Sort the clusters according to user selection.
                if marker in cfg.markers:
                    m = cfg.markers.index(marker) + 1
                    cfg.current_table_order_full = np.argsort(currentdata[:, m]).astype(np.int).tolist()
                else:
                    cfg.current_table_order_full = np.arange(len(currentdata)).tolist()
                if sort == "▼":
                    cfg.current_table_order_full.reverse()

                # Filter out clusters that don't fall within the user-defined lower/upper bounds.
                filtereddata = currentdata[cfg.current_table_order_full, 1:]
                filtereddata = np.append(filtereddata, np.expand_dims(np.arange(len(filtereddata)), 1), 1)
                for chan in range(len(cfg.lower_bounds_list[cfg.table_index])):
                    filtermask = (np.round(filtereddata[:, chan], 3) <= np.round(
                        cfg.upper_bounds_list[cfg.table_index][chan], 3))
                    filtereddata = filtereddata[filtermask]
                    filtermask = (np.round(filtereddata[:, chan], 3) >= np.round(
                        cfg.lower_bounds_list[cfg.table_index][chan], 3))
                    filtereddata = filtereddata[filtermask]
                cfg.current_table_orders_filtered[cfg.table_index] = [cfg.current_table_order_full[i] for i in
                                                                      filtereddata[:, -1].astype(np.int).tolist()]

                # Sort the clusters according to user selection and update the table accordingly.
                displaydata = currentdata[cfg.current_table_orders_filtered[cfg.table_index], :]

                # Find names for the clusters for the round of clustering being displayed in the table.
                clusterindex, _ = utils.find_analysis_round()
                annotationindex = [i for i, n in enumerate(cfg.clusters_are_pixel_based) if n][clusterindex]

                # Update the display table in the GUI.
                self.update_table(displaydata,
                                  cfg.lower_bounds_list[cfg.table_index],
                                  cfg.upper_bounds_list[cfg.table_index],
                                  len(currentdata),
                                  cfg.current_table_orders_filtered[cfg.table_index],
                                  headernames=cfg.cluster_names[annotationindex],
                                  )

            if cfg.update_log_file:
                utils.log_actions(f"gui.sort_table_image(data=\"{data}\", marker=\"{marker}\", sort=\"{sort}\")")

    ### TODO: Problems with this (get rid of background cluster from KNN file?)
    def spatial_analysis(self,
                         clusteringindex=None,
                         npix=None,
                         nsim=None,
                         ):
        """
        Perform spatial codistribution analysis on a user-defined clustered image.

        Args:
            clusteringindex (int, optional): Index of clustering round being used for analysis (Default: None).
            npix (int, optional): Number of pixels included per simulation (Default: None).
            nsim (int, optional): Number of simulations to use for spatial analysis (Default: None).
        """
        # Check that the user has performed at least one clustering algorithm.
        if len(cfg.clusters_are_pixel_based) == 0:
            utils.display_error_message("No clustering results found",
                                        "Spatial analysis can only be performed on the results of pixel or object clustering.")
            return

        if clusteringindex is None:
            # If clustering has only been executed once, use that by default.
            if len(cfg.clusters_are_pixel_based) == 1:
                clusteringindex = 0

            # If clustering has been executed multiple times, allow user to select which one.
            else:
                selectclusteringround = utils.SelectClusteringRound()
                selectclusteringround.exec()
                if not selectclusteringround.OK:
                    return
                clusteringindex = selectclusteringround.clusteringindex
        ispixelcluster = cfg.clusters_are_pixel_based[clusteringindex]
        clustermodeindex = [i for i, ispixelbased in enumerate(cfg.clusters_are_pixel_based) if
                            ispixelbased == ispixelcluster].index(clusteringindex)

        # Retrieve the labeled cluster images for the selected round of clustering.
        if ispixelcluster:
            analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Pixel"][clustermodeindex] * cfg.num_imgs
        else:
            analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][clustermodeindex] * cfg.num_imgs

        for i in range(cfg.num_imgs):
            clusterimg = np.zeros((cfg.max_img_shape[0], cfg.max_img_shape[1]),
                                  dtype=cfg.labeled_imgs[analysisnum + i].dtype)
            print(np.unique(cfg.labeled_imgs[analysisnum + i]))
            if i == 0:
                rclusters = np.zeros((cfg.max_img_shape[0], cfg.max_img_shape[1]),
                                     dtype=cfg.labeled_imgs[analysisnum + i].dtype)
                rclusters[:cfg.img_shape_list[0][0], :cfg.img_shape_list[0][1]] = cfg.labeled_imgs[analysisnum]
            else:
                clusterimg[:cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = cfg.labeled_imgs[analysisnum + i]
                rclusters = KNN.concat_images(rclusters, clusterimg)

        ### TODO: Make default parameters intelligent.
        if npix is None or nsim is None:
            spatialparams = utils.SpatialParameters()
            spatialparams.exec()
            if not spatialparams.OK:
                return
            npix = spatialparams.npix
            nsim = spatialparams.nsim
        pval, tab = KNN.random_kdtree_single(rclusters - 1, npix, nsim, objectclusters=True)
        for i in range(len(tab)):
            val = copy.deepcopy(tab[i, i])
            tab[i:, i] = tab[i:, i] - val
            tab[i, :i] = tab[i, :i] - val
        outfolder = utils.create_new_folder("SpatialAnalysis", cfg.output_folder)
        pd.DataFrame(tab).to_csv(os.path.join(outfolder, "FCVals.csv"))

        tab += tab.transpose()
        tab = np.max(tab) - tab
        lowerrange = np.median(tab) - np.min(tab)
        upperrange = np.max(tab) - np.median(tab)
        ratio = lowerrange / upperrange
        tab[tab > np.median(tab)] = (tab[tab > np.median(tab)] - np.median(tab)) * ratio + np.median(tab)
        self.set_invisible(cfg.viewer)

        DataTab = pd.DataFrame(tab)
        plt.figure(figsize=(40, 40))

        clustervals = np.array(DataTab.columns)
        clustervals[clustervals >= rclusters[5, 5]] += 1
        if ispixelcluster:
            clustervals += 1

        ClusterDend = sns.clustermap(DataTab,
                                     row_cluster=True,
                                     col_cluster=True,
                                     linewidth=0.05,
                                     center=np.median(tab),
                                     vmax=np.max(tab),
                                     vmin=0,
                                     yticklabels=clustervals,
                                     xticklabels=clustervals,
                                     cmap="RdBu_r",
                                     )
        plt.setp(ClusterDend.ax_heatmap.yaxis.get_majorticklabels(),
                 rotation=0,
                 )
        plt.show(block=False)
        plt.title("Spatial Analysis")
        plt.savefig(os.path.join(outfolder,
                                 "Codistribution.png",
                                 ),
                    format="PNG",
                    dpi=300,
                    )
        heatmap = imread(os.path.join(outfolder, "Codistribution.png"))
        self.set_invisible(cfg.viewer)
        cfg.viewer.add_image(heatmap,
                             name='Codistribution',
                             blending="additive",
                             )

        df = pd.DataFrame(pval)
        df.to_csv(os.path.join(outfolder, "PVals.csv"))
        pval[pval < 0.00000001] = 255
        pval[pval < 0.000001] = 150
        pval[pval < 0.0001] = 75
        pval[pval < 0.05] = 25
        pval[pval < 25] = 0
        df_pval = pd.DataFrame(pval)
        df_pval.index.astype(str).str.replace(r"^", "RP-")
        df_pval.index = ([f"RP-{i + 1}" for i in df_pval.index])
        df_pval.columns = ([f"RP-{i + 1}" for i in df_pval.columns.values])
        df_pval.to_csv(os.path.join(outfolder, "NormalizedPVals.csv"))
        utils.log_actions(f"gui.spatial_analysis(clusteringindex={clusteringindex}, npix={npix}, nsim={nsim})")

    def subcluster(self,
                   segindex=None,
                   clusteringindex=None,
                   markernums=[],
                   clusternum=None,
                   algname="",
                   modelpath="",
                   add_grey_img=None,
                   add_color_img=None,
                   continuetraining=None,
                   modelparams=[],
                   ):
        """
        Allow user to select an object-based cluster and clustering algorithm to further subdivide the chosen cluster.

        Args:
            segindex (int, optional): Index of segmentation round being clustered (Default: None).
            clusteringindex (int, optional): Index of object clustering round being subclustered (Default: None).
            markernums (list, optional): List of indices of parameters to be considered for clustering (Default: []).
            clusternum (int, optional): Index of cluster subclustered (Default: None).
            algname (str, optional): Name of the specified algorithm to be used for clustering (Default: "").
            modelpath (str, optional): Path to the model being used if loading a pretrained model (Default: "").
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            continuetraining (bool, optional): If True, continue training the model after loading it. Otherwise, predict without further training (Default: None).
            modelparams (iterable, optional): List of parameters for the desired clustering algorithm (Default: []).
        """
        # Determine which round of segmentation to use.
        if segindex is None:
            segindex = 0
            if len(cfg.object_img_names) > 1:
                segmentedimage = utils.SelectSegmentedImage(cfg.object_img_names)
                segmentedimage.exec()
                if not segmentedimage.OK:
                    return
                segindex = segmentedimage.imageindex

        # Determine which round of clustering to use.
        if len(cfg.segmentation_clustering_rounds[segindex]) == 0:
            utils.display_error_message("Must run clustering first",
                                        "Please run a clustering algorithm (\"Object Clustering\" or \"UMAP Annotation\") first")
            return
        elif len(cfg.segmentation_clustering_rounds[segindex]) == 1:
            clusteringindex = cfg.segmentation_clustering_rounds[segindex][0]
        elif clusteringindex is None:
            iteration = utils.ObjectClusterIteration(cfg.segmentation_clustering_rounds[segindex])
            iteration.exec()
            if not iteration.OK:
                return
            clusteringindex = cfg.segmentation_clustering_rounds[segindex][iteration.iteration]

        # Define which markers to use to train the sub-clustering algorithm.
        if markernums == []:
            trainmarkers = utils.RAPIDObjectParams()
            trainmarkers.exec()
            if not trainmarkers.OK:
                return
            markernums = trainmarkers.markernums
        startindex = clusteringindex * cfg.num_imgs

        # Select which cluster to subdivide.
        analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][clusteringindex] * cfg.num_imgs
        outfolder = utils.create_new_folder(os.path.join(os.path.split(cfg.object_cluster_directories[clusteringindex])[-1],
                                                         "Subclustered_",
                                                         ),
                                            cfg.output_folder,
                                            )
        if clusternum is None:
            labelimg = self.concat_label_imgs(
                [cfg.labeled_imgs[ind] for ind in range(analysisnum, analysisnum + cfg.num_imgs)])
            clusternums = [i + 1 for i in range(len(np.unique(labelimg)) - 1)]
            selectcluster = utils.SubCluster(clusternums)
            selectcluster.exec()
            if not selectcluster.OK:
                return
            clusternum = selectcluster.cluster

        # Define the algorithm to be used to sub-divide the cluster.
        if algname == "" or algname == "Pretrained" and modelpath == "":
            alg = utils.ClusteringAlgorithm(issubclustering=True)
            alg.exec()
            if not alg.OK:
                return
            algname = alg.algname
            if algname == "Pretrained":
                modelpath = alg.dirpath

        # Retrieve the full segmented data table for the defined cluster and the number of cells from that
        # cluster in each image.
        numcellsperimage = []
        currentimage = []
        cellids = []
        for i in range(cfg.num_imgs):
            currentsegmentedimg = cfg.data_list[cfg.segmentation_indices[i + segindex * cfg.num_imgs]]
            numcellstotal = len(cfg.data_list[cfg.segmentation_indices[i + segindex * cfg.num_imgs]])
            clusterids = cfg.cell_cluster_vals[startindex + i]
            cellids.append([j + 1 for j in range(numcellstotal) if int(clusterids[j]) == int(clusternum)])
            numcellsperimage.append(len(cellids[-1]))
            currentimage.append(currentsegmentedimg[[id - 1 for id in cellids[-1]], :])
        currentimage = np.vstack(currentimage)

        # Allow user to decide whether to add the labeled and/or colored image.
        if add_grey_img is None and add_color_img is None:
            selectimagesadded = utils.GreyColorImages()
            selectimagesadded.exec()
            if not selectimagesadded.OK:
                return
            add_grey_img = selectimagesadded.grey
            add_color_img = selectimagesadded.color
        if add_grey_img is None:
            add_grey_img = False
        if add_color_img is None:
            add_color_img = False

        # If using the RAPID algorithm for sub-clustering.
        if algname == "RAPID":
            # Define the parameters used to train the model.
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = utils.RAPIDObjectParameters(len(markernums))
                params.exec()
                if not params.OK:
                    return
                args.ncluster = int(params.nc)
                args.nit = int(params.nit)
                args.bs = int(params.bs)
                if params.mse == "True":
                    args.mse = True
                else:
                    args.mse = False
                args.lr = float(params.lr)
                args.blankpercent = float(params.blankpercent)
                modelparams = [args.ncluster, args.nit, args.bs, args.mse, args.normalize, args.lr, args.blankpercent]
            else:
                args.ncluster, args.nit, args.bs, args.mse, args.normalize, args.lr, args.blankpercent = modelparams
            args.epoch = 1
            args.GUI = True
            args.distance = 'YES'

            # Initialize the model and train the algorithm.
            cfg.viewer.status = "Training RAPID..."
            model = RAPIDMixNet(dimension=len(markernums),
                                nummodules=5,
                                mse=args.mse,
                                numclusters=args.ncluster,
                                )
            model.apply(weight_init)
            print(model)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            optimizer = optim.AdamW(model.parameters(),
                                    lr=float(args.lr),
                                    betas=(0.9, 0.999),
                                    eps=1e-08,
                                    weight_decay=0.01,
                                    amsgrad=False,
                                    )
            self.train_object(model,
                              currentimage[:, markernums],
                              optimizer,
                              args,
                              )

        elif algname == "Phenograph":
            # Define the parameters used for phenograph clustering.
            model = 0
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = utils.PhenographParameters()
                params.exec()
                if not params.OK:
                    return
                args.PGdis = str(params.PGdis)
                args.PGnn = int(params.PGnn)
                args.PGres = float(params.PGres)
                args.graphalgo = params.graphalgo
                args.normalize = params.normalize
                modelparams = [args.PGdis, args.PGnn, args.PGres, args.graphalgo, args.normalize]
            else:
                args.PGdis, args.PGnn, args.PGres, args.graphalgo, args.normalize = modelparams
            args.GUI = True

        elif algname == "SciPy":
            # Define the parameters used for the specified SciPy clustering algorithm.
            model = 0
            args = runRAPIDzarr.get_parameters()
            if modelparams == []:
                params = utils.SciPyParameters()
                params.exec()
                if not params.OK:
                    return
                args.normalize = params.normalize
                args.scipyalgo = params.scipyalgo
                args.scipykwarg = params.scipykwarg
                algname = params.scipyalgo
                modelparams = [args.normalize, args.scipyalgo, args.scipykwarg]
            else:
                args.normalize, args.scipyalgo, args.scipykwarg = modelparams
            args.GUI = True

        else:
            # Load a pretrained RAPID-O model.
            model = 0

            try:
                hf = zarr.open("/".join(modelpath[:-1]), 'r')
                loadedargs = hf.attrs['arg']
            except:
                return

            if continuetraining is None:
                loadoptions = utils.LoadModelOptions()
                loadoptions.exec()
                if not loadoptions.OK:
                    return
                continuetraining = not loadoptions.prediction

            args = Namespace(**loadedargs)
            if continuetraining:
                if modelparams == []:
                    params = utils.RAPIDObjectTrainLoadedParameters(args)
                    params.exec()
                    if not params.OK:
                        return
                    args.nit = int(params.nit)
                    args.bs = int(params.bs)
                    args.lr = float(params.lr)
                    args.blankpercent = float(params.blankpercent)
                    modelparams = [args.nit, args.bs, args.lr, args.blankpercent]
                else:
                    args.nit, args.bs, args.lr, args.blankpercent = modelparams
                args.epoch = 1
                args.GUI = True
                args.distance = 'YES'

        # If the cluster being subdivided is selected in the table, remove it from the layers list.
        index = f"Cluster {clusternum} (Object [{clusteringindex}])"
        for i in reversed(range(len(cfg.viewer.layers))):
            if cfg.viewer.layers[i].name == index:
                cfg.viewer.layers.pop(i)
                break

        # Apply subclustering algorithm and relabel cells.
        cfg.viewer.status = "Performing subclustering..."
        self.set_invisible(cfg.viewer)
        self.test_object_subcluster(model,
                                    currentimage,
                                    args,
                                    numcellsperimage,
                                    clusteringindex,
                                    clusternum,
                                    outfolder,
                                    segindex,
                                    startindex,
                                    markernums,
                                    algname,
                                    cellids,
                                    add_grey_img,
                                    add_color_img,
                                    )
        cfg.viewer.status = "RAPID subclustering complete"
        utils.log_actions(f"gui.subcluster(segindex={segindex}, clusteringindex={clusteringindex}, "
                          f"markernums={markernums}, clusternum={clusternum}, algname=\"{algname}\", "
                          f"modelpath=\"{modelpath}\", add_grey_img={add_grey_img}, add_color_img={add_color_img}, "
                          f"continuetraining={continuetraining}, modelparams={modelparams})")

    def test_object(self,
                    model,
                    quantifiedvals,
                    args,
                    markerindices,
                    add_grey_img,
                    add_color_img,
                    alg,
                    tabindex=0,
                    optimizer="",
                    results_folder="",
                    predict=False,
                    ):
        """
        Apply a clustering algorithm to segmented results.

        Args:
            model (RAPID.network.f): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            args (Namespace): Additional user-defined parameters used for training.
            markerindices (list): List of ints corresponding to the indices of the markers being used for clustering.
            add_color_img (bool): True if generating an RGB-colored image, otherwise False.
            add_grey_img (bool): True if generating a grey labeled image, otherwise False.
            tabindex (int, optional): Index value of the table for the first image being clustered on (Default: 0).
            optimizer (torch.optim.AdamW, optional): Initialized optimizer to be used for training (Default: "").
            results_folder (str, optional): Path to the folder where the model will be saved (Default: "").
            predict (bool, optional): True if the model is only being used to predict and no further training, otherwise False (Default: False).
        """
        np.random.seed(args.seed)

        # Stack segmented data tables for each image
        segmentedtab = []
        for i in range(cfg.num_imgs):
            segmentedtab.append(cfg.data_list[cfg.segmentation_indices[i + tabindex]][:, markerindices])
        segmentedtab = np.vstack(segmentedtab)

        # Pass segmentation results through clustering algorithm of choice.
        if alg == "Phenograph":
            os.chdir(cfg.output_folder)
            phenopgraphin = segmentedtab[:, 1:]
            if args.normalize:
                phenopgraphin = MinMaxScaler().fit_transform(phenopgraphin)
            clusterids, graph, Q = phenograph.cluster(phenopgraphin, n_jobs=1, clustering_algo=str(args.graphalgo),
                                                      resolution_parameter=float(args.PGres), k=int(args.PGnn),
                                                      primary_metric=str(args.PGdis), seed=args.seed)

        elif alg == "RAPID":
            torch.manual_seed(args.seed)
            torch.cuda.manual_seed(args.seed)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            if device == "cuda":
                torch.set_deterministic(True)
                torch.backends.cudnn.deterministic = True
            model.eval()
            with torch.no_grad():
                testdata = quantifiedvals.reshape((-1, quantifiedvals.shape[1]))
                clusterids = np.zeros(len(testdata), dtype=np.uint8)
                for bstart in range(0, len(testdata), 50000):
                    x = torch.from_numpy(testdata[bstart:bstart + 50000, :]).float().to(device)
                    outputs, AA = model(torch.unsqueeze(x, 1))
                    clusterids[bstart:bstart + 50000] = outputs[0].argmax(dim=1).cpu()
            if not predict:
                checkpoint = {'model': RAPIDMixNet(dimension=len(markerindices),
                                                   nummodules=5,
                                                   mse=args.mse,
                                                   numclusters=int(args.ncluster),
                                                   ),
                              'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict()}
                torch.save(checkpoint, os.path.join(results_folder, 'checkpoint.pth'))

        else:
            import sklearn.cluster as cluster
            import json
            if alg == "KMeans":
                algo = cluster.KMeans
            if alg == "AffinityPropagation":
                algo = cluster.AffinityPropagation
            if alg == "SpectralClustering":
                algo = cluster.SpectralClustering
            if alg == "AgglomerativeClustering":
                algo = cluster.AgglomerativeClustering
            if alg == "DBSCAN":
                algo = cluster.DBSCAN
            if alg == "HDBSCAN":
                import hdbscan
                algo = hdbscan.HDBSCAN
            print(json.loads(str(args.scipykwarg)))
            clusterids = algo(**json.loads(args.scipykwarg)).fit_predict(segmentedtab[:, 1:])

        clusterids = clusterids.astype(np.uint8)
        self.apply_object_clustering(clusterids,
                                     tabindex,
                                     segmentedtab,
                                     results_folder,
                                     add_grey_img,
                                     add_color_img,
                                     [],
                                     )

    def test_object_subcluster(self,
                               model,
                               quantifiedvals,
                               args,
                               numcellsperimage,
                               iteration,
                               clusternum,
                               outfolder,
                               segindex,
                               objectclustersstartindex,
                               markerindices,
                               alg,
                               cellids,
                               add_grey_img,
                               add_color_img,
                               ):
        """
        Apply a clustering algorithm to a specified cluster from an image that has already been passed through an object
        clustering algorithm.

        Args:
            model (RAPID.network.RAPIDMixNet): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            args (Namespace): Additional user-defined parameters used for training.
            numcellsperimage (list): List of the number of cells that are in each image.
            iteration (int): Index for the round of clustering being subclustered.
            clusternum (int): Index for the cluster that is being subclustered.
            segindex (int): Index value of the table for the first image being clustered on.
            objectclustersstartindex (int): Index for the table corresponding to the first object clustering round being subclustered.
            markerindices (list): List of indices of each of the cell markers included in the table.
            alg (str): String representing the algorithm being used. Options include "Phenograph", "RAPID", "KMeans", "AffinityPropagation", "SpectralClustering", "AgglomerativeClustering", "DBSCAN", and "HDBSCAN".
            cellids (list): List containing the IDs of the cells in the cluster being divided.
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
        """
        np.random.seed(args.seed)
        clusterimg = quantifiedvals[:, markerindices]

        if alg == "Phenograph":
            os.chdir(cfg.output_folder)
            if args.normalize:
                for ch in range(clusterimg.shape[1]):
                    tmpData = clusterimg[:, ch]
                    lowpercentile = np.percentile(clusterimg[clusterimg[:, ch] > 0], 1)
                    toppercentile = np.percentile(clusterimg[clusterimg[:, ch] > 0], 99)
                    tmpData[tmpData <= lowpercentile] = lowpercentile
                    tmpData[tmpData >= toppercentile] = toppercentile
                    tmpData = (tmpData - lowpercentile) / (toppercentile - lowpercentile)
                    clusterimg[:, ch] = tmpData
            to_values, graph, Q = phenograph.cluster(clusterimg, n_jobs=1,
                                                     resolution_parameter=float(args.PGres), k=int(args.PGnn),
                                                     primary_metric=str(args.PGdis), seed=args.seed)

        elif alg == "RAPID":
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            torch.manual_seed(args.seed)
            torch.cuda.manual_seed(args.seed)
            model.eval()
            with torch.no_grad():
                clusterimg = clusterimg.reshape((-1, clusterimg.shape[1]))
                to_values = np.zeros(len(clusterimg))
                for bstart in range(0, len(clusterimg), 50000):
                    x = torch.from_numpy(clusterimg[bstart:bstart + 50000, :]).float().to(device)
                    outputs, AA = model(torch.unsqueeze(x, 1))
                    to_values[bstart:bstart + 50000] = outputs[0].argmax(dim=1).cpu()

        else:
            import sklearn.cluster as cluster
            import json
            if alg == "KMeans":
                algo = cluster.KMeans
            if alg == "AffinityPropagation":
                algo = cluster.AffinityPropagation
            if alg == "SpectralClustering":
                algo = cluster.SpectralClustering
            if alg == "AgglomerativeClustering":
                algo = cluster.AgglomerativeClustering
            if alg == "DBSCAN":
                algo = cluster.DBSCAN
            if alg == "HDBSCAN":
                import hdbscan
                algo = hdbscan.HDBSCAN
            print(json.loads(str(args.scipykwarg)))
            to_values = algo(**json.loads(args.scipykwarg)).fit_predict(clusterimg)

        relabeled_table = np.hstack((to_values.reshape((len(to_values), 1)), quantifiedvals))
        startindex = 0
        images = [i for i in range(len(numcellsperimage)) if numcellsperimage[i] != 0]
        numtabs = 1
        if cfg.num_imgs > 1:
            numtabs += cfg.num_imgs
        data = np.zeros((numtabs, len(np.unique(to_values)), len(cfg.markers) + 5))
        it = iteration * numtabs
        numclusters = len(cfg.data_list[cfg.object_cluster_indices[it]]) - 1 + len(np.unique(to_values))
        samplenums = []
        for i in range(cfg.num_imgs):
            tmp_tab = relabeled_table[startindex:startindex + numcellsperimage[images[i]]]
            startindex += numcellsperimage[images[i]]
            tmp_tab_df = pd.DataFrame(tmp_tab)
            grouped = tmp_tab_df.groupby(0)
            tabres = grouped.apply(np.mean)
            unique, counts = np.unique(tmp_tab[:, 0], return_counts=True)
            count = 0
            for j in range(len(np.unique(to_values))):
                if j in unique:
                    data[i, j, 0] = counts[count]
                    count += 1
            data[i, [int(j) for j in unique], 1:] = tabres.values[:, 1:]
            samplenums += [i + 1] * numclusters
        if cfg.num_imgs > 1:
            data[-1, :, 0] = np.sum(data[:-1, :, 0], axis=0)
            for i in range(data.shape[1]):
                data[-1, i, 1:] = np.average(data[:-1, i, 1:], axis=0, weights=data[:-1, i, 0])

        for i in range(numtabs):
            olddata = copy.deepcopy(cfg.data_list[cfg.object_cluster_indices[it + i]])
            indices = [j for j in range(len(olddata))]
            indices.remove(clusternum - 1)
            newtable = np.zeros((numclusters, len(cfg.markers) + 5))
            newtable[:len(olddata) - 1, :] = copy.deepcopy(olddata)[indices, :]
            newtable[len(olddata) - 1:, :] = data[i, :, :]
            cfg.data_list[cfg.object_cluster_indices[it + i]] = newtable
            minvals = []
            maxvals = []
            for j in range(1, newtable.shape[1]):
                minvals.append(np.min(newtable[:, j]))
                maxvals.append(np.max(newtable[:, j]))
            cfg.min_vals[cfg.object_cluster_indices[it + i]] = copy.deepcopy(minvals)
            cfg.max_vals[cfg.object_cluster_indices[it + i]] = copy.deepcopy(maxvals)
            cfg.lower_bounds_list[cfg.object_cluster_indices[it + i]] = copy.deepcopy(minvals)
            cfg.upper_bounds_list[cfg.object_cluster_indices[it + i]] = copy.deepcopy(maxvals)
            if cfg.analysis_mode == "Object" and cfg.analysis_index == it + i:
                self.update_table(newtable,
                                  minvals,
                                  maxvals,
                                  len(newtable),
                                  )
                cfg.current_table_orders_filtered[cfg.table_index] = [j for j in range(len(newtable))]

        clusterdata = [cfg.data_list[cfg.object_cluster_indices[i]] for i in range(it, it + cfg.num_imgs)]
        my_data = pd.DataFrame(np.nan_to_num(np.vstack(clusterdata)))
        paramslist = cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        my_data.columns = np.hstack([["# Cells"], paramslist])
        my_data.insert(0, "Cluster", np.array([i + 1 for i in range(numclusters)] * cfg.num_imgs))
        my_data.insert(0, "Sample", np.array(samplenums))
        my_data.to_csv(os.path.join(outfolder, "ObjectClusterAvgExpressionVals.csv"))

        ind = cfg.object_cluster_indices[it]
        for i in range(ind, ind + numtabs):
            cfg.currently_selected[i] = []

        objanalysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][iteration] * cfg.num_imgs
        seganalysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Segmentation"][segindex] * cfg.num_imgs
        labelimg = self.concat_label_imgs(
            [cfg.labeled_imgs[ind] for ind in range(objanalysisnum, objanalysisnum + cfg.num_imgs)])
        labelimg[labelimg == clusternum] = 0
        labelimg[labelimg > clusternum] = labelimg[labelimg > clusternum] - 1
        newstart = copy.deepcopy(np.max(labelimg)) + 1
        count = 0
        counter = 0
        tabdata = cfg.object_cluster_dfs[iteration]
        for i in range(cfg.num_imgs):
            updated_to_values = np.array(cfg.cell_cluster_vals[objectclustersstartindex + i])
            updated_to_values[updated_to_values == clusternum] = -1
            updated_to_values[updated_to_values > clusternum] = updated_to_values[updated_to_values > clusternum] - 1
            segmentedimg = cfg.labeled_imgs[seganalysisnum + i]
            currentgreyimg = labelimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]]
            for j in range(numcellsperimage[i]):
                currentcell = cellids[i][j]
                currentgreyimg[segmentedimg == currentcell] = int(to_values[count] + newstart)
                updated_to_values[currentcell - 1] = int(to_values[count] + newstart)
                count += 1
            cfg.cell_cluster_vals[objectclustersstartindex + i] = updated_to_values
            labelimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = currentgreyimg
            cfg.labeled_imgs[objanalysisnum + i] = currentgreyimg
            tabdata['Cluster'][counter:counter + len(list(updated_to_values))] = [str(val) for val in updated_to_values]
            counter += len(updated_to_values)

        cfg.object_cluster_dfs[iteration] = tabdata
        tabdata.to_csv(os.path.join(outfolder, "SegmentationClusterIDs.csv"))
        colorimg = np.zeros((cfg.num_imgs, cfg.max_img_shape[0], cfg.max_img_shape[1], 3), dtype=np.uint8)

        colors = cfg.object_cluster_colors[iteration]
        colors = np.append(colors, colors[[clusternum - 1], :], 0)
        colors = np.delete(colors, clusternum - 1, 0)
        newcolors = generate_colormap(len(np.unique(labelimg)))
        while len(colors) < len(np.unique(labelimg)):
            if not newcolors[0, :].tolist() in colors.tolist():
                colors = np.append(colors, newcolors[[0], :], 0)
            newcolors = newcolors[1:, :]
        cfg.object_cluster_colors[iteration] = colors

        for i in range(len(np.unique(labelimg))):
            colorimg[:, :, :, 0][labelimg == i + 1] = colors[i, 0]
            colorimg[:, :, :, 1][labelimg == i + 1] = colors[i, 1]
            colorimg[:, :, :, 2][labelimg == i + 1] = colors[i, 2]

        np.save(os.path.join(outfolder, "color.npy"), colors)
        tabledata, my_data_scaled, distmatrix, uniqueclusters = \
            prep_for_mst(clustertable=my_data,
                         minclustersize=1,
                         clustersizes=my_data["# Cells"],
                         includedmarkers=paramslist,
                         )
        generate_mst(distancematrix=distmatrix,
                     normalizeddf=my_data_scaled,
                     colors=colors,
                     randomseed=0,
                     clusterheatmap=True,
                     outfolder=outfolder,
                     displaymarkers=paramslist,
                     uniqueclusters=uniqueclusters,
                     samplenames=list(np.unique(my_data['Sample'])),
                     displaysingle=False,
                     values="# Cells",
                     )

        clusteringround = int(objectclustersstartindex / cfg.num_imgs)
        if add_color_img:
            cfg.viewer.add_image(colorimg,
                                 name=f"Object {clusteringround + 1} Subclustered",
                                 blending="additive",
                                 contrast_limits=(0, 255),
                                 )
        if add_grey_img:
            cfg.viewer.add_image(labelimg,
                                 name=f"Object {clusteringround + 1} Subcluster IDs",
                                 blending="additive",
                                 contrast_limits=(0, np.max(labelimg)),
                                 )

        cfg.viewer.add_image(imread(os.path.join(outfolder, "MeanExpressionHeatmap.png")),
                             name=f"Object {clusteringround + 1} Subclustered Heatmap",
                             blending="additive",
                             visible=False,
                             )

        # Save both the label and colored images to the output folder.
        for i in range(cfg.num_imgs):
            imgname = os.path.splitext(os.path.split(cfg.file_names[i])[-1])[0]
            utils.save_img(os.path.join(outfolder, f"Subclustered_{imgname}.tif"),
                           colorimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1], :],
                           cfg.img_is_flipped[i],
                           )
            utils.save_img(os.path.join(outfolder, f"SubclusterLabels_{imgname}.tif"),
                           labelimg[i, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] + 1,
                           cfg.img_is_flipped[i],
                           )

    def toggle_checkbox(self,
                        row,
                        column,
                        ):
        """
        Add actions for the case when a checkbox is toggled. When a box is checked, the corresponding cell/cluster
        should be made visible in the viewer, and if a box is unchecked then the corresponding cell/cluster should
        be made invisible.

        Args:
            row (int): Row of the checkbox being toggled.
            column (int): Column of the checkbox being toggled.
        """
        if cfg.add_when_checked and (column == 0 and row > 2) or row == 2:
            item = cfg.table_widget.item(row, column)
            col = column - 1
            r = row - 3
            if item.checkState() == QtCore.Qt.Checked:
                if column > 0:
                    if cfg.analysis_mode == "Segmentation":
                        cfg.viewer.layers[cfg.markers[col]].visible = True

                    elif column > 1:
                        cfg.viewer.layers[cfg.markers[col - 1]].visible = True

                else:
                    r = cfg.current_table_orders_filtered[cfg.table_index][r]
                    if cfg.analysis_mode == "Segmentation":
                        analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Segmentation"][
                            cfg.analysis_index // cfg.num_imgs]
                        for i in range(cfg.num_imgs):
                            cellimg = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1]), dtype=np.bool)
                            if i == cfg.analysis_index % cfg.num_imgs:
                                mask = np.in1d(
                                    cfg.labeled_imgs[analysisnum * cfg.num_imgs + cfg.analysis_index % cfg.num_imgs],
                                    r + 1)
                                mask = mask.reshape((1, cfg.img_shape_list[i][0], cfg.img_shape_list[i][1]))
                                cellimg[0, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = mask
                            if i == 0:
                                cfg.viewer.add_image(cellimg,
                                                     name=f"Cell {r + 1}",
                                                     blending="additive",
                                                     visible=True,
                                                     )
                            else:
                                cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, cellimg))
                        cfg.currently_selected[cfg.table_index].append(r)

                    elif cfg.analysis_mode == "Object":
                        analysis_ind, numtabs = utils.find_analysis_round()
                        color = cfg.object_cluster_colors[analysis_ind][r, :] / 255
                        overall_analysis_ind = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][
                                                   analysis_ind] * cfg.num_imgs
                        cmap = Colormap(ColorArray([(0, 0, 0), (color[0], color[1], color[2])]))

                        # Find names for the clusters for the round of clustering being displayed in the table.
                        currentnames = utils.find_current_cluster_names(False)
                        clustername = f"Cluster {r + 1} " if currentnames == [] else currentnames[r]
                        clustername += f"(Object [{analysis_ind}])"

                        for i in range(cfg.num_imgs):
                            clusterimg = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1]))
                            clusterimg[0, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = cfg.labeled_imgs[
                                overall_analysis_ind + i]
                            clusterimg = np.in1d(clusterimg, r + 1)
                            clusterimg = clusterimg.reshape((1, cfg.max_img_shape[0], cfg.max_img_shape[1]))

                            if i == 0:
                                cfg.viewer.add_image(clusterimg,
                                                     name=clustername,
                                                     blending="additive",
                                                     colormap=cmap,
                                                     visible=True,
                                                     )
                            else:
                                cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, clusterimg))

                        objectclusterindex = cfg.object_cluster_indices.index(cfg.table_index)
                        ind = cfg.table_index - objectclusterindex % numtabs
                        for i in range(ind, ind + numtabs):
                            cfg.currently_selected[i].append(r)

                    else:
                        analysis_ind, numtabs = utils.find_analysis_round()
                        color = cfg.pixel_cluster_colors[analysis_ind][r, :] / 255
                        overall_analysis_ind = [i for i, n in enumerate(cfg.analysis_log) if n == "Pixel"][
                                                   analysis_ind] * cfg.num_imgs
                        cmap = Colormap(ColorArray([(0, 0, 0), (color[0], color[1], color[2])]))

                        # Find names for the clusters for the round of clustering being displayed in the table.
                        currentnames = utils.find_current_cluster_names(True)
                        clustername = f"Cluster {r + 1} " if currentnames == [] else currentnames[r]
                        clustername += f"(Pixel [{analysis_ind}])"

                        for i in range(cfg.num_imgs):
                            clusterimg = np.zeros((1, cfg.max_img_shape[0], cfg.max_img_shape[1]))
                            clusterimg[0, :cfg.img_shape_list[i][0], :cfg.img_shape_list[i][1]] = cfg.labeled_imgs[
                                overall_analysis_ind + i]
                            clusterimg = np.in1d(clusterimg, r + 1)
                            clusterimg = clusterimg.reshape((1, cfg.max_img_shape[0], cfg.max_img_shape[1]))
                            if i == 0:
                                cfg.viewer.add_image(clusterimg,
                                                     name=clustername,
                                                     blending="additive",
                                                     colormap=cmap,
                                                     visible=True,
                                                     )
                            else:
                                cfg.viewer.layers[-1].data = np.vstack((cfg.viewer.layers[-1].data, clusterimg))

                        pixelclusterindex = cfg.pixel_cluster_indices.index(cfg.table_index)
                        ind = cfg.table_index - pixelclusterindex % numtabs
                        for i in range(ind, ind + numtabs):
                            cfg.currently_selected[i].append(r)

            else:
                if column > 0:
                    if cfg.analysis_mode == "Segmentation" and col < len(cfg.markers):
                        cfg.viewer.layers[cfg.markers[col]].visible = False
                    elif column > 1:
                        cfg.viewer.layers[cfg.markers[col - 1]].visible = False

                else:
                    r = cfg.current_table_orders_filtered[cfg.table_index][r]

                    if cfg.analysis_mode == "Segmentation":
                        cfg.currently_selected[cfg.table_index].remove(r)
                        layername = f"Cell {r + 1}"

                    elif cfg.analysis_mode == "Object":
                        analysis_ind, numtabs = utils.find_analysis_round()
                        objectclusterindex = cfg.object_cluster_indices.index(cfg.table_index)
                        ind = cfg.table_index - objectclusterindex % numtabs
                        for i in range(ind, ind + numtabs):
                            cfg.currently_selected[i].remove(r)

                        # Find names for the clusters for the round of clustering being displayed in the table.
                        currentnames = utils.find_current_cluster_names(False)
                        layername = f"Cluster {r + 1} " if currentnames == [] else currentnames[r]
                        layername += f"(Object [{analysis_ind}])"

                    else:
                        analysis_ind, numtabs = utils.find_analysis_round()
                        pixelclusterindex = cfg.pixel_cluster_indices.index(cfg.table_index)
                        ind = cfg.table_index - pixelclusterindex % numtabs
                        for i in range(ind, ind + numtabs):
                            cfg.currently_selected[i].remove(r)

                        # Find names for the clusters for the round of clustering being displayed in the table.
                        currentnames = utils.find_current_cluster_names(True)
                        layername = f"Cluster {r + 1} " if currentnames == [] else currentnames[r]
                        layername += f"(Pixel [{analysis_ind}])"

                    for i in range(len(cfg.viewer.layers)):
                        if cfg.viewer.layers[i].name == layername:
                            cfg.viewer.layers.pop(i)
                            break

    def toggle_visibility(self):
        """
        If any layers are currently visible, set all layers invisible. Otherwise, set all layers to be visible.
        """
        if self.count_visible_layers() > 0:
            for i in range(len(cfg.viewer.layers)):
                cfg.viewer.layers[i].visible = False
        else:
            for i in range(len(cfg.viewer.layers)):
                cfg.viewer.layers[i].visible = True

    def train_object(self,
                     model,
                     quantifiedvals,
                     optimizer,
                     args,
                     ):
        """
        Train the RAPID-O clustering model.

        Args:
            model (RAPID.network.RAPIDMixNet): The initialized model being used as the starting point for training.
            quantifiedvals (numpy.ndarray): Quantified marker expression levels for each of the cells being used for clustering.
            optimizer (torch.optim.AdamW): Initialized optimizer to be used for training.
            args (Namespace): Additional user-defined parameters used for training.
        """

        # set the random seed so make results reproducible
        torch.cuda.manual_seed(1000)
        torch.manual_seed(1000)
        np.random.seed(1000)

        bs = args.bs
        numiterations = args.nit
        model.train()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        lossAvg = 0
        loss_fn = nn.MSELoss()
        for batch_idx in range(0, numiterations):
            dataTrain = quantifiedvals
            RANDINDEX = np.random.randint(0, len(quantifiedvals), size=bs)
            data = np.squeeze(dataTrain[RANDINDEX, :])
            NZ = np.ones_like(data.reshape(-1))
            NZ[0:int(len(NZ) * args.blankpercent)] = 0
            np.random.shuffle(NZ)
            NZ = NZ.reshape(data.shape)
            optimizer.zero_grad()
            HOWMANY = 1
            for REP in range(HOWMANY):
                RAWData = dataTrain[RANDINDEX, :]
                RAWData = RAWData * NZ
                RAWData = torch.from_numpy(RAWData).float().to(device)
                output, AA = model(torch.unsqueeze(RAWData, 1))
                NOISE = np.random.normal(loc=0, scale=1, size=dataTrain[RANDINDEX, :].shape).astype(np.float32)
                NOISEADD = dataTrain[RANDINDEX, :] / 80
                NOISE = NOISE * NOISEADD
                newdata = dataTrain[RANDINDEX, :] + NOISE
                newdata = newdata * NZ
                data_perturb = torch.from_numpy(newdata).float().to(device)
                output_alt, BB = model(torch.unsqueeze(data_perturb, 1))
                if REP == 0:
                    loss1 = torch.sum(torch.stack([IID_loss.IID_loss(o, o_perturb) for o, o_perturb in
                                                   zip(output, output_alt)])).mean()
                else:
                    TMP = loss1.clone()
                    loss1 = TMP + torch.sum(torch.stack(
                        [IID_loss.IID_loss(o, o_perturb, AA, BB) for o, o_perturb, AA, BB in
                         zip(output, output_alt, AA, AA)])).mean()
                if args.mse:
                    MSE = loss_fn(torch.unsqueeze(RAWData, 1), AA)
                    loss1 += MSE
            loss1.backward()
            optimizer.step()
            lossAvg = lossAvg + loss1.item()
            if batch_idx % 1 == 0:
                print(
                    'Train Epoch {} -iteration {}/{} - LR {:.6f} -\ttotal loss: {:.6f} -\t IIC loss: {:.3f}'.format(
                        0, batch_idx, numiterations, 10, (lossAvg / 10), loss1))
                lossAvg = 0

    def umap_plot(self,
                  paramindices=[],
                  segindex=None,
                  min_dist=None,
                  n_neighbors=None,
                  metric="",
                  colorbymarkers=None,
                  colorbygroups=[],
                  colorbyindivclusters=None,
                  colorbycombclusters=None,
                  clusteringindex=None,
                  ):
        """
        Generate a UMAP plot according to parameters defined by the user.

        Args:
            paramindices (list, optional): Indices of markers and morphological parameters to be considered for UMAP (Default: []).
            segindex (int, optional): Index of segmentation round to be used for biaxial gating (Default: None).
            min_dist (float, optional): The effective minimum distance between embedded points (Default: None).
            n_neighbors (int, optional): The size of local neighborhood used for manifold approximation (Default: None).
            metric (str, optional): The metric to use to compute distances in high dimensional space (Default: "").
            colorbymarkers (bool, optional): If True, generate a plots for each marker, with color gradients representing expression levels for each respective marker. Otherwise, do nothing (Default: None).
            colorbygroups (list, optional): List of group assignment indices to use for coloring plot(s) (Default: []).
            colorbyindivclusters (bool, optional): If True, generate a plots for each cluster, with vertex colors representing membership of the respective cluster. Otherwise, do nothing (Default: None).
            colorbycombclusters (bool, optional): If True, generate a plot with vertices colored according to cluster assignment. Otherwise, do nothing (Default: None).
            clusteringindex (int, optional): Index of the round of clustering to be used for color assignment, if applicable (Default: None).
        """
        params = cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]

        # User must first run object-based segmentation in order to generate a UMAP.
        if cfg.segment_count == 0:
            utils.display_error_message("You must segment before running UMAP",
                                        "UMAP cannot be generated until the image has been segmented")
            return

        # Prompt user to select which cell markers to use as parameters for UMAP.
        if paramindices == []:
            umapmarkers = utils.RAPIDObjectParams(True)
            umapmarkers.exec()
            if not umapmarkers.OK:
                return
            paramindices = umapmarkers.markernums
        paramnames = [params[ind] for ind in paramindices]

        # Prompt user to define the parameters and coloring schemes used for the UMAP.
        if any(param is None for param in (segindex, min_dist, n_neighbors, colorbymarkers)) or metric == "":
            setumapParams = utils.UMAPParameters()
            setumapParams.exec()
            if not setumapParams.OK:
                return
            segindex = setumapParams.segmentationindex
            min_dist = setumapParams.min_dist
            n_neighbors = setumapParams.n_neighbors
            metric = setumapParams.metric
            colorbymarkers = setumapParams.colorbymarkers
            if cfg.object_cluster_count > 0:
                colorbyindivclusters = setumapParams.colorbyindivclusters
                colorbycombclusters = setumapParams.colorbycombclusters
            if len(cfg.groups_names[1:]) > 0:
                colorbygroups = setumapParams.colorbygroups

        # Count total number of cells in the segmented iteration being used across all images.
        totalcells = 0
        cfg.plot_segmentation_indices.append(segindex * cfg.num_imgs)
        for i in range(cfg.num_imgs):
            totalcells += len(cfg.data_list[cfg.segmentation_indices[segindex * cfg.num_imgs + i]])

        # Compile quantified cells from each individual image into one combined data array.
        currentimage = np.zeros((totalcells, len(paramindices)))
        currentimage2 = np.zeros((totalcells, cfg.num_markers + 4))
        count = 0
        col_list = generate_colormap(cfg.num_imgs + 1)
        cols = np.zeros((totalcells, 3)).astype(np.float)
        cellsperimage = []
        for i in range(cfg.num_imgs):
            cellsincurrimg = []
            numcells = len(cfg.data_list[cfg.segmentation_indices[segindex * cfg.num_imgs + i]])
            currentimage2[count:count + numcells, :] = cfg.data_list[
                cfg.segmentation_indices[segindex * cfg.num_imgs + i]]
            currentimage[count:count + numcells, :] = cfg.data_list[
                                                          cfg.segmentation_indices[segindex * cfg.num_imgs + i]][:,
                                                      paramindices]
            for j in range(count, count + numcells):
                cellsincurrimg.append(j)
                cols[j, :] = col_list[i, :] / np.array([255.0, 255.0, 255.0])
            count += numcells
            cellsperimage.append(cellsincurrimg)

        # Apply UMAP algorithm and remove rows with NaN values.
        reducer = umap.UMAP(min_dist=min_dist, n_neighbors=n_neighbors, metric=metric)
        mapper = reducer.fit_transform(currentimage)
        removerows = np.unique(np.argwhere(np.isnan(mapper))[:, 0])
        mapper = np.delete(mapper, removerows, axis=0)
        for i in range(cfg.num_imgs):
            for cellnum in removerows:
                if cellnum in cellsperimage[i]:
                    cellsperimage[i].remove(cellnum)

        # Color data points according to image ID.
        cols = np.delete(cols, removerows, axis=0)
        cols = np.append(cols, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)

        # Use resulting points to generate a scatterplot and add it to the viewer.
        y = (mapper[:, 0] - np.min(mapper[:, 0])) / (np.max(mapper[:, 0]) - np.min(mapper[:, 0]))
        x = (mapper[:, 1] - np.min(mapper[:, 1])) / (np.max(mapper[:, 1]) - np.min(mapper[:, 1]))
        x = np.append(x, [-0.05, 1.05])
        y = np.append(y, [-0.05, 1.05])
        plt.figure(figsize=(10, 10))
        plt.scatter(x, y, s=1, c=cols, marker='.')
        plt.title("UMAP")
        plt.xlabel("UMAP 1")
        plt.ylabel("UMAP 2")
        # ax = plt.gca()
        plt.xticks([], [])
        plt.yticks([], [])
        outfolder = utils.create_new_folder("UMAP_", cfg.output_folder)
        plt.savefig(os.path.join(outfolder, "UMAP.png"), format="PNG", dpi=300)
        im = imread(os.path.join(outfolder, "UMAP.png"))
        imarray = np.asarray(im)
        locs = np.where((imarray[:, :, 0] == 242) & (imarray[:, :, 1] == 255) & (imarray[:, :, 2] == 242))
        cfg.plot_x_mins.append(np.min(locs[0]))
        cfg.plot_x_maxs.append(np.max(locs[0]))
        cfg.plot_y_mins.append(np.min(locs[1]))
        cfg.plot_y_maxs.append(np.max(locs[1]))
        self.set_invisible(cfg.viewer)
        cfg.viewer.add_image(im,
                             name=f"UMAP {cfg.umap_count}",
                             blending="additive",
                             )

        # If selected by user, add an additional stack of scatterplots with vertices colored on a gradient
        # according to each cell marker or morphological parameter.
        if colorbymarkers:
            self.set_invisible(cfg.viewer)
            pathlist = []
            max = np.percentile(currentimage2[:, :-4], 97)
            min = np.min(currentimage2[:, :-4])
            adj = np.max(currentimage2[:, :-4])
            for i in range(1, 5):
                currentimage2[:, -i] = currentimage2[:, -i] / np.max(currentimage2[:, -i]) * adj
            currentimage2 = currentimage2[:, paramindices]
            for i in range(len(paramindices)):
                plt.figure(figsize=(10, 10))
                col = np.zeros((len(mapper), 3)).astype(np.float)
                for j in range(len(mapper)):
                    col[j, 0] = (currentimage2[j, i] - min) / (max - min)
                    col[j, 2] = 1.0 - (currentimage2[j, i] - min) / (max - min)
                col[col > 1.0] = 1.0
                col[col < 0.0] = 0.0
                col = np.append(col, [[0.95, 1, 0.95], [0.95, 1, 0.95]], axis=0)
                plt.scatter(x, y, s=1, c=col, marker='.')
                ax = plt.gca()
                plt.xticks([], [])
                plt.yticks([], [])
                plt.title(paramnames[i])
                plt.xlabel("UMAP 1")
                plt.ylabel("UMAP 2")
                plt.savefig(os.path.join(outfolder, paramnames[i] + ".png"), format="PNG", dpi=300)
                pathlist.append(os.path.join(outfolder, paramnames[i] + ".png"))
            imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
            cfg.viewer.add_image(imx, name=f"UMAP {cfg.umap_count} (Cell Markers)", blending="additive")

        # If given segmented image iteration has been clustered, check if the user elected to use clustering as
        # a basis for vertex coloring.
        if len(cfg.segmentation_clustering_rounds[segindex]) > 0:
            # If the user is coloring according to cluster assignment, prompt to define which clustering
            # iteration is being used.
            if colorbyindivclusters or colorbycombclusters:
                if len(cfg.segmentation_clustering_rounds[segindex]) > 1:
                    if clusteringindex is None:
                        iteration = utils.ObjectClusterIteration(cfg.segmentation_clustering_rounds[segindex])
                        iteration.exec()
                        if not iteration.OK:
                            return
                        clusteringindex = iteration.iteration
                    startindex = cfg.segmentation_clustering_rounds[segindex][clusteringindex]
                else:
                    startindex = cfg.segmentation_clustering_rounds[segindex][0]
                clusternums = []
                for i in range(cfg.num_imgs):
                    curclusternums = cfg.cell_cluster_vals[startindex * cfg.num_imgs + i]
                    for n in curclusternums:
                        clusternums.append(n - 1)
                analysisnum = [i for i, n in enumerate(cfg.analysis_log) if n == "Object"][startindex] * cfg.num_imgs
                labelimg = self.concat_label_imgs(
                    [cfg.labeled_imgs[ind] for ind in range(analysisnum, analysisnum + cfg.num_imgs)])
                numclusters = len(np.unique(labelimg)) - 1

            # If selected by user, add a stack of scatterplots with vertices colored red if corresponding to a cell in
            # the respective cluster, or blue otherwise.
            if colorbyindivclusters:
                self.set_invisible(cfg.viewer)
                pathlist = []
                for i in range(numclusters):
                    plt.figure(figsize=(10, 10))
                    col = np.zeros((len(mapper), 3)).astype(np.float)
                    for j in range(len(mapper)):
                        if int(clusternums[j]) == i:
                            col[j, 0] = 1.0
                            col[j, 2] = 0.0
                        else:
                            col[j, 0] = 0.0
                            col[j, 2] = 1.0
                    col = np.append(col,
                                    [[0.95, 1, 0.95], [0.95, 1, 0.95]],
                                    axis=0,
                                    )
                    plt.scatter(x,
                                y,
                                s=1,
                                c=col,
                                marker='.',
                                )
                    ax = plt.gca()
                    plt.xticks([], [])
                    plt.yticks([], [])
                    plt.title(f"Cluster {i + 1}")
                    plt.xlabel("UMAP 1")
                    plt.ylabel("UMAP 2")
                    plt.savefig(os.path.join(outfolder,
                                             f"UMAP_Cluster{i + 1}.png",
                                             ),
                                format="PNG",
                                dpi=300,
                                )
                    pathlist.append(os.path.join(outfolder, f"UMAP_Cluster{i + 1}.png"))
                imx = np.array([np.asarray(imread(path, pilmode='RGB')) for path in pathlist])
                cfg.viewer.add_image(imx,
                                     name=f"UMAP {cfg.umap_count} (Individual Clusters)",
                                     blending="additive",
                                     )

            # If selected by user, add a scatterplot colored according to cluster assignment.
            if colorbycombclusters:
                self.set_invisible(cfg.viewer)
                col_list = generate_colormap(numclusters + 1)
                cols = np.zeros((len(mapper), 3)).astype(np.float)
                for i in range(len(mapper)):
                    cols[i, :] = col_list[int(clusternums[i]), :] / np.array([255.0, 255.0, 255.0])
                plt.figure(figsize=(10, 10))
                cols = np.append(cols,
                                 [[0.95, 1, 0.95], [0.95, 1, 0.95]],
                                 axis=0)
                plt.scatter(x,
                            y,
                            s=1,
                            c=cols,
                            marker='.',
                            )
                ax = plt.gca()
                plt.xticks([], [])
                plt.yticks([], [])
                plt.title("Clusters")
                plt.xlabel("UMAP 1")
                plt.ylabel("UMAP 2")
                filename = os.path.join(outfolder, "UMAPClusters.png")
                plt.savefig(filename,
                            format="PNG",
                            dpi=300,
                            )
                cfg.viewer.add_image(imread(filename),
                                     name=f"UMAP {cfg.umap_count} (Combined Clusters)",
                                     blending="additive",
                                     )

        # If selected by user, add a scatterplot colored according to group assignment.
        if colorbygroups != []:
            for ind in colorbygroups:
                group = cfg.groups_list[ind + 1]
                imggroupnames = list(group.values())
                shufflelist = [list(group.keys()).index(name) for name in
                               [os.path.split(fn)[-1] for fn in cfg.file_names]]
                nameindices = list(set(imggroupnames))
                numgroups = len(nameindices)
                imagegroups = []
                for i in range(cfg.num_imgs):
                    imagegroups.append(nameindices.index(imggroupnames[i]))
                imagegroups = [imagegroups[i] for i in shufflelist]
                self.set_invisible(cfg.viewer)
                col_list = generate_colormap(numgroups + 1)
                cols = np.zeros((len(mapper), 3)).astype(np.float)
                count = 0
                for i in range(cfg.num_imgs):
                    for j in range(count, count + len(cellsperimage[i])):
                        cols[j, :] = col_list[imagegroups[i], :] / np.array([255.0, 255.0, 255.0])
                    count += len(cellsperimage[i])
                plt.figure(figsize=(10, 10))
                cols = np.append(cols,
                                 [[0.95, 1, 0.95], [0.95, 1, 0.95]],
                                 axis=0,
                                 )
                plt.scatter(x,
                            y,
                            s=1,
                            c=cols,
                            marker='.',
                            )
                ax = plt.gca()
                plt.xticks([], [])
                plt.yticks([], [])
                plt.title('UMAP (' + cfg.groups_names[ind + 1] + ')')
                plt.xlabel("UMAP 1")
                plt.ylabel("UMAP 2")
                filename = os.path.join(outfolder,
                                        f"UMAPGroups_{cfg.groups_names[ind + 1]}.png",
                                        )
                plt.savefig(filename,
                            format="PNG",
                            dpi=300,
                            )
                cfg.viewer.add_image(imread(filename),
                                     name=f"UMAP {cfg.umap_count} ({cfg.groups_names[ind + 1]})",
                                     blending="additive",
                                     )

        # Keep track of coordinates on UMAP plot, and update variables.
        coordslist = []
        coords = np.hstack((np.expand_dims(x, 1), np.expand_dims(y, 1)))
        count = 0
        for i in range(cfg.num_imgs):
            numcells = len(cfg.data_list[cfg.segmentation_indices[segindex * cfg.num_imgs + i]])
            coordslist.append(coords[count:count + numcells].astype(np.float))
            count += numcells
        cfg.plot_coordinates.append(coordslist)
        cfg.plot_is_umap.append(True)
        cfg.umap_count += 1
        utils.log_actions(f"gui.umap_plot(paramindices={paramindices}, segindex={segindex}, min_dist={min_dist}, "
                          f"n_neighbors={n_neighbors}, metric=\"{metric}\", colorbymarkers={colorbymarkers}, "
                          f"colorbygroups={colorbygroups}, colorbyindivclusters={colorbyindivclusters}, "
                          f"colorbycombclusters={colorbycombclusters}, clusteringindex={clusteringindex})")

    def update_table(self,
                     datavals,
                     lowerbounds,
                     upperbounds,
                     totalnumrows,
                     order=[],
                     headernames=[],
                     ):
        """
        Apply both lower- and upper-bound thresholds to an image array.

        Args:
            datavals (numpy.ndarray): Array containing the data values being represented in the table.
            lowerbounds (list): List of lower bounds for the values in each column in the table.
            upperbounds (list): List of upper bounds for the values in each column in the table.
            totalnumrows (int): Total number of cells/clusters for the image corresponding to the table.
            order (list, optional): List containing the indices corresponding to the cells/clusters that are included in the table, and in the correct order (Default: []).
            headernames (list, optional): List containing the annotated cluster names, if applicable (Default: []).
        """
        numrows = len(datavals)
        numcols = datavals.shape[1]
        vals = []
        for i in range(numrows + 3):
            vals.append(None)
        data = {'': vals}
        params = ["Area", "Eccentricity", "Perimeter", "Major Axis"]
        for i in range(numcols):
            if cfg.analysis_mode == "Segmentation":
                if i < numcols - 4:
                    key = str(cfg.viewer.layers[cfg.markers[i]])
                else:
                    key = params[i + 4 - numcols]
            elif cfg.analysis_mode == "Object":
                if i == 0:
                    key = "# Cells"
                else:
                    keys = cfg.markers + ["Area", "Eccentricity", "Perimeter", "Major Axis"]
                    key = keys[i - 1]
            elif cfg.analysis_mode == "Pixel":
                if i == 0:
                    key = "# Pixels"
                else:
                    ind, _ = utils.find_analysis_round()
                    key = str(cfg.pixel_cluster_markers[ind][i - 1])
            values = [None, None, None]
            rvals = datavals[:, i]
            for j in rvals:
                values.append(j)
            data[key] = values
        df = pd.DataFrame(data=data)
        df.replace(to_replace=[None], value=np.nan, inplace=True)
        df.fillna(0)
        df.columns = data.keys()
        data = df.to_dict()
        count = 0
        for key in data.keys():
            if key != '' and key != '# Cells' and key != '# Pixels' and key != 'Cluster #':
                print(key)
                data[key][0] = lowerbounds[count]
                data[key][1] = upperbounds[count]
                count += 1
        try:
            cfg.table_widget.hide()
        except:
            print("")
        self.create_table(data)
        if cfg.analysis_mode == "Segmentation":
            if len(order) > 0:
                cfg.current_vertical_header_labels = np.asarray(
                    [f"{numrows}/{totalnumrows}", "", ""] + [f"Cell {int(i)}" for i in order]).astype(np.str)
            else:
                cfg.current_vertical_header_labels = np.asarray(
                    [f"{numrows}/{totalnumrows}", "", ""] + [f"Cell {int(i) + 1}" for i in range(numrows)]).astype(
                    np.str)
        else:
            if headernames != []:
                labels = [headernames[i] for i in order]
                cfg.current_vertical_header_labels = np.asarray([f"{numrows}/{totalnumrows}", "", ""]
                                                                + labels).astype(np.str)
            elif len(order) > 0:
                cfg.current_vertical_header_labels = np.asarray([f"{numrows}/{totalnumrows}", "", ""]
                                                                + [f"Cluster {int(i) + 1}" for i in order]).astype(
                    np.str)
            else:
                cfg.current_vertical_header_labels = np.asarray([f"{numrows}/{totalnumrows}", "", ""]
                                                                + [f"Cluster {int(i) + 1}" for i in
                                                                   range(numrows)]).astype(np.str)
                cfg.current_table_order_full = []
                for i in range(numrows):
                    cfg.current_table_order_full.append(i)
        cfg.table_widget.setVerticalHeaderLabels(cfg.current_vertical_header_labels)

        cfg.add_when_checked = False
        if len(order) > 0:
            order = [int(i) for i in order]
            counter = 3
            for a in order:
                if a in cfg.currently_selected[cfg.table_index]:
                    cfg.table_widget.item(counter, 0).setCheckState(QtCore.Qt.Checked)
                counter += 1
        cfg.add_when_checked = True
        cfg.table_widget.verticalHeader().setFont(QFont("Helvetica", pointSize=12))
        cfg.table_widget.horizontalHeader().setFont(QFont("Helvetica", pointSize=12))
        vstrings = [cfg.table_widget.verticalHeaderItem(i).text() for i in range(cfg.table_widget.rowCount())]
        vwidth = utils.font_width("Helvetica", 12, vstrings)
        cfg.table_widget.verticalHeader().setMinimumWidth(vwidth + 15)
        hstrings = [cfg.table_widget.horizontalHeaderItem(i).text() for i in range(cfg.table_widget.columnCount())]
        hwidth = utils.font_width("Helvetica", 12, hstrings)
        cfg.table_widget.horizontalHeader().setMinimumWidth(hwidth + 15)
        cfg.table_widget.horizontalHeader().setMinimumHeight(cfg.table_widget.rowHeight(0))
        if cfg.has_added_table:
            cfg.viewer.window.remove_dock_widget(cfg.viewer.window._qt_window.findChildren(QDockWidget)[-1])
        cfg.viewer.window.add_dock_widget(cfg.table_widget, area="top", name="Table")
        cfg.has_added_table = True
        cfg.full_tab = pd.DataFrame(data).fillna(0)
        cfg.full_tab.insert(0, "Labels", vstrings)
        cfg.current_tab_data = datavals
        cfg.total_num_rows = totalnumrows
        cfg.table_order = order

    def testGUI(self,
                segmentationfilenames=[],
                envpath="",
                pixelresultspath="",
                output_folder="",
                quant_avg=None,
                add_grey_img=None,
                add_color_img=None,
                ):
        """
        Function containing magicgui elements, where the napari window gets populated with RAPID-specific widgets.

        Args:
            segmentationfilenames (list, optional): List of paths to segmentation label images being loaded (Default: []).
            envpath (str, optional): Path to the saved environment file being loaded (Default: "").
            pixelresultspath (str, optional): Path to data folder with RAPID results being loaded (Default: "").
            output_folder (str, optional): Path to folder where results will be saved (Default: "").
            quant_avg (bool): If True, use mean expression values for quantification. Otherwise, calculate root-mean-square values.
            add_grey_img (bool, optional): If True, add greyscale labeled segmented image to the viewer. Otherwise, don't (Default: None).
            add_color_img (bool, optional): If True, add RGB-colored segmented image to the viewer. Otherwise, don't (Default: None).
        """
        with napari.gui_qt():
            cfg.viewer = napari.Viewer()
            cfg.viewer.window.file_menu.clear()
            cfg.viewer.layers.move_selected = lambda a, b: print()

            @magicgui(call_button="Biaxial gating")
            def biaxial_gate_gui() -> Image:
                self.biaxial_gate()

            @magicgui(call_button="Display Selected")
            def display_selected_cells_gui() -> Image:
                self.display_selected_cells()

            @magicgui(call_button="UMAP")
            def umap_plot_gui() -> Image:
                self.umap_plot()

            @magicgui(call_button="Edit Image")
            def edit_image_gui() -> Image:
                self.edit_image()

            @magicgui(call_button="Filter Table")
            def filter_table_gui() -> Image:
                self.filter_table()

            @magicgui(call_button="MST")
            def minimum_spanning_tree_gui():
                self.minimum_spanning_tree()

            @magicgui(call_button="Nearest Neighbours")
            def nearest_neighbours_gui() -> Image:
                self.nearest_neighbours()

            @magicgui(call_button="Load Clusters")
            def load_object_clusters_gui() -> Image:
                self.load_object_clusters()

            @magicgui(call_button="UMAP Annotation")
            def manual_annotation_gui() -> Image:
                self.manual_annotation()

            @magicgui(call_button="Merge Clusters")
            def merge_clusters_gui() -> Image:
                self.merge_clusters()

            @magicgui(call_button="Merge Markers")
            def merge_mem_gui() -> Image:
                self.merge_markers(nucmarkernums=[],
                                   nucalg="",
                                   memmarkernums=[],
                                   memalg="",
                                   nuccls=[],
                                   memcls=[],
                                   )

            @magicgui(call_button="Object Clustering")
            def object_clustering_gui():
                self.object_clustering()

            @magicgui(call_button="Quantify Region")
            def quantify_region_gui():
                self.quantify_region()

            @magicgui(call_button="Reset Metadata")
            def reset_metadata_gui() -> Image:
                self.reset_metadata()

            @magicgui(call_button="Segment")
            def segment_gui() -> Image:
                self.segment()

            @magicgui(auto_call=True,
                      data={"choices": cfg.table_img_names, "label": "Display data:  "},
                      marker={"choices": cfg.table_params, "label": "Parameter:        "},
                      sort={"choices": ["▲", "▼"], "label": "Order:         "})
            def sort_table_image_gui(data: str, marker: str, sort: str) -> Image:
                self.sort_table_image()

            @magicgui(call_button="Sub-Cluster")
            def subcluster_gui() -> Image:
                self.subcluster()

            @magicgui(call_button="Spatial Analysis")
            def spatial_analysis_gui():
                self.spatial_analysis()

            @magicgui(call_button="Pixel Clustering")
            def pixel_clustering_gui():
                self.pixel_clustering()

            @magicgui(call_button="Toggle Visibility")
            def toggle_visibility_gui() -> Image:
                self.toggle_visibility()

            layerswidget = QWidget()
            layerswidgetlayout = QGridLayout()
            layerswidgetlayout.setSpacing(0)
            layerswidgetlayout.setContentsMargins(0, 0, 0, 0)
            layerswidgetlabel = QLabel("Image visualization")
            layerswidgetlabel.setAlignment(Qt.AlignCenter)
            layerswidgetlayout.addWidget(layerswidgetlabel, 0, 0)
            editimagewidget = edit_image_gui.native
            editimagewidget.setToolTip("Apply edits to the raw image")
            layerswidgetlayout.addWidget(editimagewidget, 1, 0)
            togglevisibilitywidget = toggle_visibility_gui.native
            togglevisibilitywidget.setToolTip("Toggle visibility of all layers")
            layerswidgetlayout.addWidget(togglevisibilitywidget, 2, 0)
            resetmetadatawidget = reset_metadata_gui.native
            resetmetadatawidget.setToolTip("Reset the metadata for all of the layers")
            layerswidgetlayout.addWidget(resetmetadatawidget, 3, 0)
            layerswidget.setLayout(layerswidgetlayout)
            layerswidget.setToolTip("This module includes functions that manipulate the layers")
            cfg.viewer.window.add_dock_widget(layerswidget, name="Data visibility", area="bottom")

            clusteringwidget = QWidget()
            clusteringlayout = QGridLayout()
            clusteringlayout.setSpacing(0)
            clusteringlayout.setContentsMargins(0, 0, 0, 0)
            clusteringlabelwidget = QLabel("Pixel-based analysis")
            clusteringlabelwidget.setAlignment(Qt.AlignCenter)
            clusteringlayout.addWidget(clusteringlabelwidget, 0, 0)
            trainrapidwidget = pixel_clustering_gui.native
            trainrapidwidget.setToolTip("Classify each pixel in the image into different clusters")
            clusteringlayout.addWidget(trainrapidwidget, 1, 0)
            emptylabelwidget = QLabel("")
            emptylabelwidget.setAlignment(Qt.AlignCenter)
            clusteringlayout.addWidget(emptylabelwidget, 2, 0, 2, 1)
            clusteringwidget.setLayout(clusteringlayout)
            clusteringwidget.setToolTip("This module includes functions that are specific to pixel-based analysis")
            cfg.viewer.window.add_dock_widget(clusteringwidget, name="Pixel-based pipeline", area="bottom")

            objectBasedWidget = QWidget()
            objectBasedLayout = QGridLayout()
            objectBasedLayout.setSpacing(0)
            objectBasedLayout.setContentsMargins(0, 0, 0, 0)
            objectlabelwidget = QLabel("Object-based pipeline")
            objectlabelwidget.setAlignment(Qt.AlignCenter)
            objectBasedLayout.addWidget(objectlabelwidget, 0, 0, 1, 3)
            mergememwidget = merge_mem_gui.native
            mergememwidget.setToolTip("Select the cell markers that you would like to define the membranes")
            objectBasedLayout.addWidget(mergememwidget, 1, 0)
            segmentwidget = segment_gui.native
            segmentwidget.setToolTip(
                "Segment the cells according to the membranes defined in the \"Merged Membranes\" layer")
            objectBasedLayout.addWidget(segmentwidget, 1, 1)
            trainobjectwidget = object_clustering_gui.native
            trainobjectwidget.setToolTip("Classify the segmented cells into different clusters")
            objectBasedLayout.addWidget(trainobjectwidget, 1, 2)
            biaxialwidget = biaxial_gate_gui.native
            biaxialwidget.setToolTip("Generate a biaxial plot from the segmented cells")
            objectBasedLayout.addWidget(biaxialwidget, 2, 0)
            umapwidget = umap_plot_gui.native
            umapwidget.setToolTip("Generate a UMAP from the segmented cells")
            objectBasedLayout.addWidget(umapwidget, 2, 1)
            displayselectedwidget = display_selected_cells_gui.native
            displayselectedwidget.setToolTip(
                "Display the cells that correspond to the data points in the selected region")
            objectBasedLayout.addWidget(displayselectedwidget, 2, 2)
            nngui = nearest_neighbours_gui.native
            nngui.setToolTip("Run a nearest neighbor analysis based on spatial distributions of cells in clusters")
            objectBasedLayout.addWidget(nngui, 3, 0)
            manualannotationwidget = manual_annotation_gui.native
            manualannotationwidget.setToolTip(
                "Display the cells that correspond to the data points in the selected region")
            objectBasedLayout.addWidget(manualannotationwidget, 3, 1)
            loadclusterswidget = load_object_clusters_gui.native
            loadclusterswidget.setToolTip("Display the cells that correspond to the data points in the selected region")
            objectBasedLayout.addWidget(loadclusterswidget, 3, 2)
            objectBasedWidget.setLayout(objectBasedLayout)
            objectBasedWidget.setToolTip("This module includes functions that are specific to object-based analysis")
            cfg.viewer.window.add_dock_widget(objectBasedWidget, name="Object-based pipeline", area="bottom")

            analysisWidget = QWidget()
            analysisLayout = QGridLayout()
            analysisLayout.setSpacing(0)
            analysisLayout.setContentsMargins(0, 0, 0, 0)
            analysislabelwidget = QLabel("Downstream analysis")
            analysislabelwidget.setAlignment(Qt.AlignCenter)
            analysisLayout.addWidget(analysislabelwidget, 0, 0, 1, 2)
            spatialgui = spatial_analysis_gui.native
            spatialgui.setToolTip(
                "Generate a heatmap according to the relative spatial codistribution of each pair of clusters")
            analysisLayout.addWidget(spatialgui, 1, 0)
            mstgui = minimum_spanning_tree_gui.native
            mstgui.setToolTip(
                "Generate a minimum spanning tree based on relative expression profiles of the clusters in the current table")
            analysisLayout.addWidget(mstgui, 1, 1)
            mergeclusterswidget = merge_clusters_gui.native
            mergeclusterswidget.setToolTip("Merge together all clusters that are selected in the table")
            analysisLayout.addWidget(mergeclusterswidget, 2, 0)
            quantifyregionwidget = quantify_region_gui.native
            quantifyregionwidget.setToolTip(
                "Acquire average cell marker expression information for given regions of the image")
            analysisLayout.addWidget(quantifyregionwidget, 2, 1)
            subclusterwidget = subcluster_gui.native
            subclusterwidget.setToolTip("Divide a given cluster into subclusters")
            analysisLayout.addWidget(subclusterwidget, 3, 0)
            filtertablegui = filter_table_gui.native
            filtertablegui.setToolTip("Set filters for markers in the table")
            analysisLayout.addWidget(filtertablegui, 3, 1)
            analysisWidget.setLayout(analysisLayout)
            analysisWidget.setToolTip(
                "This module includes functions that can be used for either pixel- or object-bnased analysis")
            cfg.viewer.window.add_dock_widget(analysisWidget, name="Downstream analysis", area="bottom")

            tablesortwidget = QWidget()
            tablelayout = QGridLayout()
            tablelayout.setSpacing(0)
            tablelayout.setContentsMargins(0, 0, 0, 0)
            analysislabelwidget = QLabel("Table sort")
            analysislabelwidget.setAlignment(Qt.AlignCenter)
            tablelayout.addWidget(analysislabelwidget, 0, 0)
            cfg.sort_table_widget = sort_table_image_gui
            cfg.sort_table_widget.native.setToolTip("Sort the visible elements in the table")
            tablelayout.addWidget(cfg.sort_table_widget.native, 1, 0)
            tablesortwidget.setLayout(tablelayout)
            tablesortwidget.setToolTip(
                "This module includes functions that can dictate the displayed data in the table")
            cfg.viewer.window.add_dock_widget(tablesortwidget, name="Table sort", area="bottom")

            if output_folder == "" and envpath == "":
                while True:
                    openwindow = utils.OutFolder()
                    openwindow.exec()
                    if openwindow.OK:
                        if openwindow.loadseg:
                            segmentationfilenames = self.load_segmentation_results()
                            if segmentationfilenames:
                                break
                        elif openwindow.loadenv:
                            envpath = self.load_environment(envpath)
                            if not envpath == "":
                                break
                        elif openwindow.loadpixel:
                            pixelresultspath = self.load_pixel_results()
                            if not pixelresultspath == "":
                                break
                        else:
                            dialog = QFileDialog()
                            output_folder = dialog.getExistingDirectory(None, "Select Output Folder")
                            if output_folder != "":
                                cfg.output_folder = utils.create_new_folder("RAPID_GUI", output_folder)
                                utils.initialize_logger()
                                break
                    else:
                        cfg.viewer.window.close()
                        cfg.viewer.close()
                        return
            elif output_folder != "":
                if segmentationfilenames != []:
                    self.load_segmentation_results(segmentationfilenames,
                                                   output_folder,
                                                   quant_avg,
                                                   add_grey_img,
                                                   add_color_img,
                                                   )
                elif pixelresultspath != "":
                    self.load_pixel_results(pixelresultspath,
                                            output_folder,
                                            )
                else:
                    cfg.output_folder = utils.create_new_folder("RAPID_GUI", output_folder)
            else:
                self.load_environment(envpath)

            openimgs = QAction('Open File(s)', cfg.viewer.window._qt_window)
            openimgs.setShortcut('Ctrl+O')
            openimgs.setStatusTip('Open file(s)')
            openimgs.triggered.connect(self.open_images_gui)

            savedata = QAction('Save Data', cfg.viewer.window._qt_window)
            savedata.setShortcut('Ctrl+S')
            savedata.setStatusTip('Save Data')
            savedata.triggered.connect(self.save_data_gui)

            group = QAction('Sample grouping', cfg.viewer.window._qt_window)
            group.setShortcut('Ctrl+G')
            group.setStatusTip('Sample grouping')
            group.triggered.connect(self.sample_group_gui)

            saveenv = QAction('Save Environment', cfg.viewer.window._qt_window)
            saveenv.setShortcut('Ctrl+Shift+S')
            saveenv.setStatusTip('Save Environment')
            saveenv.triggered.connect(self.save_environment)

            cmgroup = QAction('Set colormap', cfg.viewer.window._qt_window)
            cmgroup.setShortcut('Ctrl+Shift+C')
            cmgroup.setStatusTip('Set colormap for clusters')
            cmgroup.triggered.connect(self.colormap_group_gui)

            rename = QAction('Rename clusters', cfg.viewer.window._qt_window)
            rename.setShortcut('Ctrl+R')
            rename.setStatusTip('Change names of clusters')
            rename.triggered.connect(self.rename_clusters_gui)

            opendocs = QAction('Open documentation', cfg.viewer.window._qt_window)
            opendocs.setShortcut('Ctrl+D')
            opendocs.setStatusTip('Open documentation')
            opendocs.triggered.connect(self.open_docs)

            changefolder = QAction('Change output folder', cfg.viewer.window._qt_window)
            changefolder.setStatusTip('Change output folder')
            changefolder.triggered.connect(self.change_folder_gui)

            cfg.viewer.window.file_menu.addAction(openimgs)
            cfg.viewer.window.file_menu.addAction(savedata)
            cfg.viewer.window.file_menu.addAction(group)
            cfg.viewer.window.file_menu.addAction(saveenv)
            cfg.viewer.window.file_menu.addAction(cmgroup)
            cfg.viewer.window.file_menu.addAction(rename)
            cfg.viewer.window.file_menu.addAction(changefolder)
            cfg.viewer.window.help_menu.addAction(opendocs)


def run_rapid_gui():
    gui = RAPIDGUI()
    gui.testGUI()


if __name__ == '__main__':
    try:
        run_rapid_gui()
    except Exception as ex:
        print(ex)
