import matplotlib
matplotlib.use('Agg')
import numpy as np
from sklearn import metrics
import argparse
import matplotlib.pyplot as plt
from os import path, makedirs
from matplotlib.patches import Rectangle
from tqdm import tqdm


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    idx = np.where(array == array[idx])[0][-1]

    return idx


def compute_roc(authentic_file, impostor_file):
    print(f'Loading authentic from {authentic_file}')
    if authentic_file[-4:] == '.txt':
        authentic = np.loadtxt(authentic_file, dtype=np.str)
        print(f'Converting authentic to npy')
        np.save(authentic_file[:-4] + '.npy', authentic.astype(float))
    else:
        authentic = np.load(authentic_file)

    if np.ndim(authentic) == 1:
        authentic_score = authentic.astype(float)
    elif np.ndim(authentic) == 2:
        authentic_score = authentic[:, 2].astype(float)
    else:
        authentic_score = authentic[:, 2].astype(float)

    authentic_score = authentic_score
    authentic_y = np.ones(authentic.shape[0])

    print(f'Loading impostor from {impostor_file}')
    if impostor_file[-4:] == '.txt':
        impostor = np.loadtxt(impostor_file, dtype=np.str)
        print(f'Converting impostor to npy')
        np.save(impostor_file[:-4] + '.npy', impostor.astype(float))
    else:
        impostor = np.load(impostor_file)

    if np.ndim(impostor) == 1:
        impostor_score = impostor.astype(float)
    elif np.ndim(impostor) == 2:
        impostor_score = impostor[:, 2].astype(float)
    else:
        impostor_score = impostor[:, 2].astype(float)

    impostor_score = impostor_score

    impostor_y = np.zeros(impostor.shape[0])

    # reverse the scores in case of distance instead of similarity
    # authentic_score *= -1
    # impostor_score *= -1

    y = np.concatenate([authentic_y, impostor_y])
    scores = np.concatenate([authentic_score, impostor_score])

    print(y.shape)

    fpr, tpr, thr = metrics.roc_curve(y, scores, drop_intermediate=False)

    # fnr = np.zeros_like(fpr)
    # total_authentic = authentic_y.shape[0]

    # for i in tqdm(range(thr.shape[0])):
    #     fn = authentic_score[authentic_score < thr[i]].shape[0]
    #     fnr[i] = fn / total_authentic

    fnr = 1 - tpr

    return fpr, tpr, thr, fnr


def plot(title, fpr1, tpr1, thr1, fnr1, l1, fpr2, tpr2, thr2, fnr2, l2,
         fpr3, tpr3, fnr3, thr3, l3):
    label_kwargs1 = {}
    label_kwargs1['bbox'] = dict(
        boxstyle='round,pad=0.5', fc='C1', alpha=0.5,
    )

    label_kwargs2 = {}
    label_kwargs2['bbox'] = dict(
        boxstyle='round,pad=0.5', fc='C0', alpha=0.5,
    )

    label_kwargs3 = {}
    label_kwargs3['bbox'] = dict(
        boxstyle='round,pad=0.5', fc='C3', alpha=0.5,
    )

    # FMR =  FPR (False Match Rate)
    # FNMR = FNR (False Non-Match Rate)
    low_range1 = 1e-6
    low_range2 = 1e-4

    plt.rcParams["figure.figsize"] = [6, 5]
    plt.rcParams['font.size'] = 12

    plt.grid(True, zorder=0, linestyle='dashed')

    # if title is not None:
    #    plt.title(title, y=1.08)

    plt.gca().set_yscale('log')

    plt.plot(thr1[fpr1 > low_range1], fpr1[fpr1 > low_range1], 'C1--', label=l1 + ' FMR')
    plt.plot(thr1[fnr1 > low_range2], fnr1[fnr1 > low_range2], 'C1', label=l1 + ' FNMR')

    if l2 is not None:
        plt.plot(thr2[fpr2 > low_range1], fpr2[fpr2 > low_range1], 'C0--', label=l2 + ' FMR')
        plt.plot(thr2[fnr2 > low_range2], fnr2[fnr2 > low_range2], 'C0', label=l2 + ' FNMR')

    if l3 is not None:
        plt.plot(thr3[fpr3 > low_range1], fpr3[fpr3 > low_range1], 'C3--', label=l3 + ' FMR')
        plt.plot(thr3[fnr3 > low_range2], fnr3[fnr3 > low_range2], 'C3', label=l3 + ' FNMR')

    # colors = []
    # labels = []

    # colors.append('C1')
    # k = int(np.where(np.round(fpr1, 4) == np.round(fnr1, 4))[0][0])
    # labels.append('EER: {}'.format(np.round(fpr1[k], 4)))

    # if l2 is not None:
    #     colors.append('C0')
    #     k = int(np.where(np.round(fpr2, 4) == np.round(fnr2, 4))[0][0])
    #     labels.append('EER: {}'.format(np.round(fpr2[k], 4)))

    # if l3 is not None:
    #     colors.append('C3')
    #     k = int(np.where(np.round(fpr3, 4) == np.round(fnr3, 4))[0][0])
    #     labels.append('EER: {}'.format(np.round(fpr3[k], 4)))

    if l3 is not None:
        ncol = 2
    elif l2 is not None:
        ncol = 2
    else:
        ncol = 1

    legend1 = plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
                         mode="expand", borderaxespad=0, ncol=ncol, fontsize=12, edgecolor='black', handletextpad=0.3)
    # plt.xlim([0, 1])
    plt.ylim([min(low_range1, low_range2), 1e0])
    plt.ylabel('Rate')
    plt.xlabel('Threshold')

    plt.tight_layout(pad=0)

    # colors = np.asarray(colors)
    # labels = np.asarray(labels)

    # handles = []
    # for c in colors:
    #     handles.append(Rectangle((0, 0), 1, 1, color=c, fill=True))

    # handles = np.asarray(handles)

    # plt.legend(handles, labels, loc="lower left", fontsize=10)
    # plt.gca().add_artist(legend1)

    return plt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot FMR/FNMR Curves')
    parser.add_argument('-authentic1', '-a1', help='Authentic scores 1.')
    parser.add_argument('-impostor1', '-i1', help='Impostor scores 1.')
    parser.add_argument('-label1', '-l1', help='Label 1.')
    parser.add_argument('-authentic2', '-a2', help='Authentic scores 2.')
    parser.add_argument('-impostor2', '-i2', help='Impostor scores 2.')
    parser.add_argument('-label2', '-l2', help='Label 2.')
    parser.add_argument('-authentic3', '-a3', help='Authentic scores 3.')
    parser.add_argument('-impostor3', '-i3', help='Impostor scores 3.')
    parser.add_argument('-label3', '-l3', help='Label 3.')
    parser.add_argument('-title', '-t', help='Plot title.')
    parser.add_argument('-dest', '-d', help='Folder to save the plot.')
    parser.add_argument('-name', '-n', help='Plot name (without extension).')

    args = parser.parse_args()

    fpr2, tpr2, thr2, fnr2 = (None, None, None, None)
    fpr3, tpr3, thr3, fnr3 = (None, None, None, None)

    fpr1, tpr1, thr1, fnr1 = compute_roc(args.authentic1, args.impostor1)

    if args.authentic2 is not None:
        fpr2, tpr2, thr2, fnr2 = compute_roc(args.authentic2, args.impostor2)

    if args.authentic3 is not None:
        fpr3, tpr3, thr3, fnr3 = compute_roc(args.authentic3, args.impostor3)

    k = find_nearest(fpr1, 0.00001)
    t1 = np.round(thr1[k], 10)
    print(t1)
    y1 = np.round(fnr1[k], 10)
    print(f'{args.label1} FNMR at 1-in-100,000 FMR: {y1 * 100000}')

    k = find_nearest(thr2, t1)
    y2 = np.round(fnr2[k], 10)
    x2 = np.round(fpr2[k], 10)
    print(f'{args.label2} FNMR at 1-in-100,000 {args.label1} FMR: {y2 * 100000}')
    print(f'{args.label2} FMR at 1-in-100,000 {args.label1} FMR: {x2 * 100000}')

    k = find_nearest(fpr2, 0.00001)
    y2 = np.round(fnr2[k], 10)
    print(f'{args.label2} FNMR at 1-in-100,000 FMR: {y2 * 100000}')

    plot(args.title, fpr1, tpr1, thr1, fnr1, args.label1,
         fpr2, tpr2, thr2, fnr2, args.label2,
         fpr3, tpr3, fnr3, thr3, args.label3)

    if not path.exists(args.dest):
        makedirs(args.dest)

    plot_path = path.join(args.dest, args.name + '.png')

    plt.savefig(plot_path, dpi=150)
