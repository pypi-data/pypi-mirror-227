import pandas as pd
import numpy as np
import networkx as nx
import re
import ast
import copy
import math
import pkg_resources
from itertools import product
from collections import Counter
from sklearn.cluster import DBSCAN

from glycowork.glycan_data.loader import lib, unwrap, df_species, df_glycan, Hex, dHex, HexA, HexN, HexNAc, Pen, linkages
from glycowork.motif.processing import min_process_glycans, canonicalize_iupac
from glycowork.motif.graph import compare_glycans, glycan_to_nxGraph, graph_to_string

chars = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10, 'K':11,
         'L':12, 'M':13, 'N':14, 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19,
         'V':20, 'W':21, 'Y':22, 'X':23, 'Z':24, 'z':25}

io = pkg_resources.resource_stream(__name__, "mz_to_composition.csv")
mapping_file = pd.read_csv(io)
mass_dict = dict(zip(mapping_file.composition, mapping_file["underivatized_monoisotopic"]))


def constrain_prot(proteins, libr = None):
  """Ensures that no characters outside of libr are present in proteins\n
  | Arguments:
  | :-
  | proteins (list): list of proteins as strings
  | libr (list): sorted list of amino acids occurring in proteins\n
  | Returns:
  | :-
  | Returns list of proteins with only permitted amino acids
  """
  if libr is None:
    libr = chars
  # Check whether any character is not in libr and replace it with a 'z' placeholder character
  forbidden = [k for k in set(list(''.join(proteins))) if k not in libr.keys()]
  for k in forbidden:
    proteins = [j.replace(k, 'z') for j in proteins]
  return proteins


def prot_to_coded(proteins, libr = None, pad_len = 1000):
  """Encodes protein sequences to be used in LectinOracle-flex\n
  | Arguments:
  | :-
  | proteins (list): list of proteins as strings
  | libr (list): sorted list of amino acids occurring in proteins
  | pad_len (int): length up to which the proteins are padded\n
  | Returns:
  | :-
  | Returns list of encoded proteins with only permitted amino acids
  """
  if libr is None:
    libr = chars
  # Cut off protein sequence above pad_len
  prots = [k[:min(len(k), pad_len)] for k in proteins]
  # Replace forbidden characters with 'z'
  prots = constrain_prot(prots, libr = libr)
  # Pad up to a length of pad_len
  prots = [pad_sequence(string_to_labels(str(k).upper(), libr = libr),
                        max_length = pad_len,
                        pad_label = len(libr)-1) for k in prots]
  return prots


def character_to_label(character, libr = None):
  """tokenizes character by indexing passed library\n
  | Arguments:
  | :-
  | character (string): character to index
  | libr (dict): dict of library items\n
  | Returns:
  | :-
  | Returns index of character in library
  """
  if libr is None:
    libr = lib
  return libr[character]


def string_to_labels(character_string, libr = None):
  """tokenizes word by indexing characters in passed library\n
  | Arguments:
  | :-
  | character_string (string): string of characters to index
  | libr (dict): dict of library items\n
  | Returns:
  | :-
  | Returns indexes of characters in library
  """
  if libr is None:
    libr = lib
  return list(map(lambda character: character_to_label(character, libr), character_string))


def pad_sequence(seq, max_length, pad_label = None, libr = None):
  """brings all sequences to same length by adding padding token\n
  | Arguments:
  | :-
  | seq (list): sequence to pad (from string_to_labels)
  | max_length (int): sequence length to pad to
  | pad_label (int): which padding label to use
  | libr (list): list of library items\n\n
  | Returns:
  | :-
  | Returns padded sequence
  """
  if libr is None:
    libr = lib
  if pad_label is None:
    pad_label = len(libr)
  seq += [pad_label for i in range(max_length - len(seq))]
  return seq


def get_core(sugar):
  """retrieves core monosaccharide from modified monosaccharide\n
  | Arguments:
  | :-
  | sugar (string): monosaccharide or linkage\n
  | Returns:
  | :-
  | Returns core monosaccharide as string
  """
  easy_cores = ['dHexNAc', 'GlcNAc', 'GalNAc', 'ManNAc', 'FucNAc', 'QuiNAc', 'RhaNAc', 'GulNAc',
                'IdoNAc', 'Ins', 'MurNAc', '6dAltNAc', 'AcoNAc', 'HexA', 'GlcA', 'AltA',
                'GalA', 'ManA', 'Tyv', 'Yer', 'Abe', 'GlcfNAc', 'GalfNAc', 'ManfNAc',
                'FucfNAc', 'IdoA', 'GulA', 'LDManHep', 'DDManHep', 'DDGlcHep', 'LyxHep', 'ManHep',
                'DDAltHep', 'IdoHep', 'DLGlcHep', 'GalHep', 'ddHex', 'ddNon', 'Unknown', 'Assigned',
                'MurNGc', '6dTalNAc', '6dGul', 'AllA', 'TalA', 'AllNAc', 'TalNAc', 'Kdn']
  next_cores = ['GlcN', 'GalN', 'ManN', 'FucN', 'QuiN', 'RhaN', 'AraN', 'IdoN' 'Glcf', 'Galf', 'Manf',
                'Fucf', 'Araf', 'Lyxf', 'Xylf', '6dAltf', 'Ribf', 'Fruf', 'Apif', 'Kdof', 'Sedf',
                '6dTal', 'AltNAc', '6dAlt', 'dHex', 'HexNAc', 'dNon', '4eLeg', 'GulN', 'AltN', 'AllN', 'TalN']
  hard_cores = ['HexN', 'Glc', 'Gal', 'Man', 'Fuc', 'Qui', 'Rha', 'Ara', 'Oli', 'Gul', 'Lyx',
                'Xyl', 'Dha', 'Rib', 'Kdo', 'Tal', 'All', 'Pse', 'Leg', 'Asc', 'Hex',
                'Fru', 'Hex', 'Alt', 'Xluf', 'Api', 'Ko', 'Pau', 'Fus', 'Erwiniose',
                'Aco', 'Bac', 'Dig', 'Thre-ol', 'Ery-ol', 'Tag', 'Sor', 'Psi', 'Mur', 'Aci', 'Sia',
                'Par', 'Col', 'Ido']
  if catch := [ele for ele in easy_cores if (ele in sugar)]:
    return catch[0]
  elif catch := [ele for ele in next_cores if (ele in sugar)]:
    return catch[0]
  elif catch := [ele for ele in hard_cores if (ele in sugar)]:
    return catch[0]
  elif (('Neu' in sugar) and ('5Ac' in sugar)):
    return 'Neu5Ac'
  elif (('Neu' in sugar) and ('5Gc' in sugar)):
    return 'Neu5Gc'
  elif (('Neu' in sugar) and ('4Ac' in sugar)):
    return 'Neu4Ac'
  elif 'Neu' in sugar:
    return 'Neu'
  elif sugar.startswith('a') or sugar.startswith('b') or sugar.startswith('?'):
    return sugar
  elif re.match('^[0-9]+(-[0-9]+)+$', sugar):
    return sugar
  else:
    return 'Monosaccharide'


def get_modification(sugar):
  """retrieves modification from modified monosaccharide\n
  | Arguments:
  | :-
  | sugar (string): monosaccharide or linkage\n
  | Returns:
  | :-
  | Returns modification as string
  """
  core = get_core(sugar)
  modification = sugar.replace(core, '')
  return modification


def get_stem_lib(libr):
  """creates a mapping file to map modified monosaccharides to core monosaccharides\n
  | Arguments:
  | :-
  | libr (dict): dictionary of form glycoletter:index\n
  | Returns:
  | :-
  | Returns dictionary of form modified_monosaccharide:core_monosaccharide
  """
  return {k: get_core(k) for k in libr.keys()}


stem_lib = get_stem_lib(lib)


def stemify_glycan(glycan, stem_lib = None, libr = None):
  """removes modifications from all monosaccharides in a glycan\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format
  | stem_lib (dictionary): dictionary of form modified_monosaccharide:core_monosaccharide; default:created from lib
  | libr (dict): dictionary of form glycoletter:index; default:lib\n
  | Returns:
  | :-
  | Returns stemmed glycan as string
  """
  if libr is None:
    libr = lib
  if stem_lib is None:
    stem_lib = get_stem_lib(libr)
  if '(' not in glycan:
    glycan = get_core(glycan)
    return glycan
  clean_list = list(stem_lib.values())
  for k in list(stem_lib.keys())[::-1][:-1]:
    # For each monosaccharide, check whether it's modified
    if ((k not in clean_list) and (k in glycan) and not (k.startswith(('a', 'b', '?'))) and not (re.match('^[0-9]+(-[0-9]+)+$', k))):
      county = 0
      # Go at it until all modifications are stemified
      while ((k in glycan) and (sum(1 for s in clean_list if k in s) <= 1)) and county < 5:
        county += 1
        glycan_start = glycan[:glycan.rindex('(')]
        glycan_part = glycan_start
        # Narrow it down to the offending monosaccharide
        if k in glycan_start:
          cut = glycan_start[glycan_start.index(k):]
          try:
            cut = cut[:cut.index('(')]
          except:
            pass
          # Replace offending monosaccharide with stemified monosaccharide
          if cut not in clean_list:
            glycan_part = glycan_start[:glycan_start.index(k)]
            glycan_part = glycan_part + stem_lib[k]
          else:
            glycan_part = glycan_start
        # Check to see whether there is anything after the modification that should be appended
        try:
          glycan_mid = glycan_start[glycan_start.index(k) + len(k):]
          if ((cut not in clean_list) and (len(glycan_mid) > 0)):
            glycan_part = glycan_part + glycan_mid
        except:
          pass
        # Handling the reducing end
        glycan_end = glycan[glycan.rindex('('):]
        if k in glycan_end:
          if ']' in glycan_end:
            filt = ']'
          else:
            filt = ')'
          cut = glycan_end[glycan_end.index(filt)+1:]
          if cut not in clean_list:
            glycan_end = glycan_end[:glycan_end.index(filt)+1] + stem_lib[k]
          else:
            pass
        glycan = glycan_part + glycan_end
  return glycan


def stemify_dataset(df, stem_lib = None, libr = None,
                    glycan_col_name = 'target', rarity_filter = 1):
  """stemifies all glycans in a dataset by removing monosaccharide modifications\n
  | Arguments:
  | :-
  | df (dataframe): dataframe with glycans in IUPAC-condensed format in column glycan_col_name
  | stem_lib (dictionary): dictionary of form modified_monosaccharide:core_monosaccharide; default:created from lib
  | libr (dict): dictionary of form glycoletter:index; default:lib
  | glycan_col_name (string): column name under which glycans are stored; default:target
  | rarity_filter (int): how often monosaccharide modification has to occur to not get removed; default:1\n
  | Returns:
  | :-
  | Returns df with glycans stemified
  """
  if libr is None:
    libr = lib
  if stem_lib is None:
    stem_lib = get_stem_lib(libr)
  # Get pool of monosaccharides, decide which one to stemify based on rarity
  pool = unwrap(min_process_glycans(df[glycan_col_name].values.tolist()))
  pool_count = Counter(pool)
  for k in set(pool):
    if pool_count[k] > rarity_filter:
      stem_lib[k] = k
  # Stemify all offending monosaccharides
  df_out = copy.deepcopy(df)
  df_out[glycan_col_name] = [stemify_glycan(k, stem_lib = stem_lib, libr = libr) for k in df_out[glycan_col_name]]
  return df_out


def mz_to_composition(mz_value, mode = 'negative', mass_value = 'monoisotopic', reduced = False,
                      sample_prep = 'underivatized', mass_tolerance = 0.5, kingdom = 'Animalia',
                      glycan_class = 'N', df_use = None, filter_out = set()):
  """Mapping a m/z value to a matching monosaccharide composition within SugarBase\n
  | Arguments:
  | :-
  | mz_value (float): the actual m/z value from mass spectrometry
  | mode (string): whether mz_value comes from MS in 'positive' or 'negative' mode; default:'negative'
  | mass_value (string): whether the expected mass is 'monoisotopic' or 'average'; default:'monoisotopic'
  | reduced (bool): whether glycans are reduced at reducing end; default:False
  | sample_prep (string): whether the glycans has been 'underivatized', 'permethylated', or 'peracetylated'; default:'underivatized'
  | mass_tolerance (float): how much deviation to tolerate for a match; default:0.5
  | kingdom (string): taxonomic kingdom for choosing a subset of glycans to consider; default:'Animalia'
  | glycan_class (string): which glycan class does the m/z value stem from, 'N', 'O', or 'lipid' linked glycans or 'free' glycans; default:'N'
  | df_use (dataframe): species-specific glycan dataframe to use for mapping; default: df_glycan
  | filter_out (set): set of monosaccharide types to ignore during composition finding; default:None\n
  | Returns:
  | :-
  | Returns a list of matching compositions in dict form
  """
  if df_use is None:
    df_use = df_glycan[(df_glycan.glycan_type == glycan_class) & (df_glycan.Kingdom.str.contains(kingdom))]
  if mode == 'negative':
    adduct = mass_dict['Acetate']
  else:
    adduct = mass_dict['Na+']
  if reduced:
    mz_value = mz_value - 1.0078
  multiplier = 1 if mode == 'negative' else -1
  if isinstance(df_use.Composition.tolist()[0], str):
    comp_pool = sorted(df_use.Composition.unique(), reverse = True)
    comp_pool = [ast.literal_eval(k) for k in comp_pool if isinstance(k, str)]
  else:
    tuple_set = {tuple(d.items()) for d in df_use.Composition}
    comp_pool = [dict(t) for t in tuple_set]
  out = []
  cache = {}
  for c in comp_pool:
    m = composition_to_mass(c, mass_value = mass_value, sample_prep = sample_prep)
    cache[m] = c
    if abs(m - mz_value) < mass_tolerance:
      if not filter_out.intersection(c.keys()):
        out = [c]
        break
  if out:
    return out
  else:
    for m, c in cache.items():
      if abs(m+adduct - mz_value) < mass_tolerance:
        if not filter_out.intersection(c.keys()):
          out = [c]
          break
    if out:
      return out
    else:
      mz_value = (mz_value+0.5*multiplier)*2+(reduced*1)
      for m, c in cache.items():
        if abs(m - mz_value) < mass_tolerance:
          if not filter_out.intersection(c.keys()):
            out = [c]
            break
      return out


def match_composition_relaxed(composition, glycan_class = 'N', kingdom = 'Animalia', df_use = None, reducing_end = None):
  """Given a coarse-grained monosaccharide composition (Hex, HexNAc, etc.), it returns all corresponding glycans\n
  | Arguments:
  | :-
  | composition (dict): a dictionary indicating the composition to match (for example {"dHex": 1, "Hex": 1, "HexNAc": 1})
  | glycan_class (string): which glycan class does the m/z value stem from, 'N', 'O', or 'lipid' linked glycans or 'free' glycans; default:N
  | kingdom (string): taxonomic kingdom for choosing a subset of glycans to consider; default:'Animalia'
  | df_use (dataframe): glycan dataframe for searching glycan structures; default:df_glycan\n
  | Returns:
  | :-
  | Returns list of glycans matching composition in IUPAC-condensed
  """
  if df_use is None:
    df_use = df_glycan[(df_glycan.glycan_type == glycan_class) & (df_glycan.Kingdom.str.contains(kingdom))]
  # Subset for glycans with the right number of monosaccharides
  comp_count = sum(composition.values())
  len_distr = [len(k) - (len(k)-1)/2 for k in min_process_glycans(df_use.glycan.values.tolist())]
  idx = [k for k in range(len(df_use)) if len_distr[k] == comp_count]
  output_list = df_use.iloc[idx, :].glycan.values.tolist()
  output_compositions = [glycan_to_composition(k) for k in output_list]
  return [output_list[k] for k in range(len(output_compositions)) if composition == output_compositions[k]]


def condense_composition_matching(matched_composition, libr = None):
  """Given a list of glycans matching a composition, find the minimum number of glycans characterizing this set\n
  | Arguments:
  | :-
  | matched_composition (list): list of glycans matching to a composition
  | libr (dict): dictionary of form glycoletter:index; default:lib\n
  | Returns:
  | :-
  | Returns minimal list of glycans that match a composition
  """
  if libr is None:
    libr = lib
  # Define uncertainty wildcards
  wildcards = ['?1-?', '?2-?', 'a2-?', 'a1-?', 'b1-?']
  # Establish glycan equality given the wildcards
  match_matrix = [[compare_glycans(k, j, libr = libr, wildcards = True, wildcards_ptm = True,
                                   wildcard_list = wildcards) for j in matched_composition] for k in matched_composition]
  match_matrix = pd.DataFrame(match_matrix)
  match_matrix.columns = matched_composition
  # Cluster glycans by pairwise equality (given the wildcards)
  clustering = DBSCAN(eps = 1, min_samples = 1).fit(match_matrix)
  num_clusters = len(set(clustering.labels_))
  sum_glycans = []
  # For each cluster, get the most well-defined glycan and return it
  for k in range(num_clusters):
    cluster_glycans = [matched_composition[j] for j in range(len(clustering.labels_)) if clustering.labels_[j] == k]
    county = [sum([j.count(w) for w in wildcards]) for j in cluster_glycans]
    idx = np.where(county == np.array(county).min())[0]
    if len(idx) == 1:
      sum_glycans.append(cluster_glycans[idx[0]])
    else:
      for j in idx:
        sum_glycans.append(cluster_glycans[j])
  return sum_glycans


def compositions_to_structures(composition_list, glycan_class = 'N', kingdom = 'Animalia', abundances = None,
                               df_use = None, libr = None, verbose = False):
  """wrapper function to map compositions to structures, condense them, and match them with relative intensities\n
  | Arguments:
  | :-
  | composition_list (list): list of composition dictionaries of the form {'Hex': 1, 'HexNAc': 1}
  | glycan_class (string): which glycan class does the m/z value stem from, 'N', 'O', or 'lipid' linked glycans or 'free' glycans; default:N
  | kingdom (string): taxonomic kingdom for choosing a subset of glycans to consider; default:'Animalia'
  | abundances (dataframe): every row one composition (matching composition_list in order), every column one sample;default:pd.DataFrame([range(len(composition_list))]*2).T
  | df_use (dataframe): glycan dataframe for searching glycan structures; default:df_glycan
  | libr (dict): dictionary of form glycoletter:index; default:lib
  | verbose (bool): whether to print any non-matching compositions; default:False\n
  | Returns:
  | :-
  | Returns dataframe of (matched structures) x (relative intensities)
  """
  if libr is None:
    libr = lib
  if df_use is None:
    df_use = df_glycan[(df_glycan.glycan_type == glycan_class) & (df_glycan.Kingdom.str.contains(kingdom))]
  if abundances is None:
    abundances = pd.DataFrame([range(len(composition_list))]*2).T
  df_out = []
  not_matched = []
  for k in range(len(composition_list)):
    # For each composition, map it to potential structures
    matched = match_composition_relaxed(composition_list[k], glycan_class = glycan_class,
                                        kingdom = kingdom, df_use = df_use)
    # If multiple structure matches, try to condense them by wildcard clustering
    if len(matched) > 0:
        condensed = condense_composition_matching(matched, libr = libr)
        matched_data = [abundances.iloc[k, 1:].values.tolist()]*len(condensed)
        for ele in range(len(condensed)):
            df_out.append([condensed[ele]] + matched_data[ele])
    else:
        not_matched.append(composition_list[k])
  if len(df_out) > 0:
    df_out = pd.DataFrame(df_out)
    df_out.columns = ['glycan'] + ['abundance']*(abundances.shape[1]-1)
  print(str(len(not_matched)) + " compositions could not be matched. Run with verbose = True to see which compositions.")
  if verbose:
    print(not_matched)
  return df_out


def mz_to_structures(mz_list, glycan_class, kingdom = 'Animalia', abundances = None, mode = 'negative',
                     mass_value = 'monoisotopic', sample_prep = 'underivatized', mass_tolerance = 0.5,
                     reduced = False, df_use = None, filter_out = set(), libr = None, verbose = False):
  """wrapper function to map precursor masses to structures, condense them, and match them with relative intensities\n
  | Arguments:
  | :-
  | mz_list (list): list of precursor masses
  | glycan_class (string): which glycan class does the m/z value stem from, 'N', 'O', or 'lipid' linked glycans or 'free' glycans
  | kingdom (string): taxonomic kingdom for choosing a subset of glycans to consider; default:'Animalia'
  | abundances (dataframe): every row one composition (matching mz_list in order), every column one sample; default:pd.DataFrame([range(len(mz_list))]*2).T
  | mode (string): whether mz_value comes from MS in 'positive' or 'negative' mode; default:'negative'
  | mass_value (string): whether the expected mass is 'monoisotopic' or 'average'; default:'monoisotopic'
  | sample_prep (string): whether the glycans has been 'underivatized', 'permethylated', or 'peracetylated'; default:'underivatized'
  | mass_tolerance (float): how much deviation to tolerate for a match; default:0.5
  | reduced (bool): whether glycans are reduced at reducing end; default:False
  | df_use (dataframe): species-specific glycan dataframe to use for mapping; default: df_glycan
  | filter_out (set): set of monosaccharide types to ignore during composition finding; default:None
  | libr (dict): dictionary of form glycoletter:index; default:lib
  | verbose (bool): whether to print any non-matching compositions; default:False\n
  | Returns:
  | :-
  | Returns dataframe of (matched structures) x (relative intensities)
  """
  if libr is None:
    libr = lib
  if df_use is None:
    df_use = df_glycan[(df_glycan.glycan_type == glycan_class) & (df_glycan.Kingdom.str.contains(kingdom))]
  if abundances is None:
    abundances = pd.DataFrame([range(len(mz_list))]*2).T
  # Check glycan class
  if glycan_class not in {'N', 'O', 'free', 'lipid'}:
    print("Not a valid class for mz_to_composition; currently N/O/free/lipid matching is supported. For everything else run composition_to_structures separately.")
  out_structures = []
  # Map each m/z value to potential compositions
  compositions = [mz_to_composition(mz, mode = mode, mass_value = mass_value, reduced = reduced, sample_prep = sample_prep,
                                    mass_tolerance = mass_tolerance, kingdom = kingdom, glycan_class = glycan_class,
                                    df_use = df_use, filter_out = filter_out) for mz in mz_list]
  # Map each of these potential compositions to potential structures
  for m in range(len(compositions)):
    structures = [compositions_to_structures([k], glycan_class = glycan_class, abundances = abundances.iloc[[m]], kingdom = kingdom, df_use = df_use,
                                             libr = libr, verbose = verbose) for k in compositions[m]]
    structures = [k for k in structures if not k.empty]
    # Do not return matches if one m/z value matches multiple compositions that *each* match multiple structures, because of error propagation
    if len(structures) == 1:
      out_structures.append(structures[0])
    else:
      if verbose:
        print("m/z value " + str(mz_list[m]) + " with multiple matched compositions that each would have matching structures is filtered out.")
  if len(out_structures) > 0:
    return pd.concat(out_structures, axis = 0)
  else:
    return []


def mask_rare_glycoletters(glycans, thresh_monosaccharides = None, thresh_linkages = None):
  """masks rare monosaccharides and linkages in a list of glycans\n
  | Arguments:
  | :-
  | glycans (list): list of glycans in IUPAC-condensed form
  | thresh_monosaccharides (int): threshold-value for monosaccharides seen as "rare"; default:(0.001*len(glycans))
  | thresh_linkages (int): threshold-value for linkages seen as "rare"; default:(0.03*len(glycans))\n
  | Returns:
  | :-
  | Returns list of glycans in IUPAC-condensed with masked rare monosaccharides and linkages
  """
  # Get rarity thresholds
  if thresh_monosaccharides is None:
    thresh_monosaccharides = int(np.ceil(0.001*len(glycans)))
  if thresh_linkages is None:
    thresh_linkages = int(np.ceil(0.03*len(glycans)))
  rares = unwrap(min_process_glycans(glycans))
  rare_linkages, rare_monosaccharides = [], []
  # Sort monosaccharides and linkages into different bins
  for x in rares:
    (rare_monosaccharides, rare_linkages)[x in linkages].append(x)
  rares = [rare_monosaccharides, rare_linkages]
  thresh = [thresh_monosaccharides, thresh_linkages]
  # Establish which ones are considered to be rare
  rares = [list({x: count for x, count in Counter(rares[k]).items() if count <= thresh[k]}.keys()) for k in range(len(rares))]
  try:
    rares[0].remove('')
  except:
    pass
  out = []
  # For each glycan, check whether they have rare monosaccharides/linkages and mask them
  for k in glycans:
    for j in rares[0]:
      if (j in k) and ('-'+j not in k):
        k = k.replace(j+'(', 'Monosaccharide(')
        if k.endswith(j):
          k = re.sub(j+'$', 'Monosaccharide', k)
    for m in rares[1]:
      if m in k:
        if m[1] == '1':
          k = k.replace(m, '?1-?')
        else:
          k = k.replace(m, '?2-?')
    out.append(k)
  return out


def check_nomenclature(glycan):
  """checks whether the proposed glycan has the correct nomenclature for glycowork\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format
  | Returns:
  | :-
  | If salvageable, returns the re-formatted glycan; if not, prints the reason why it's not convertable
  """
  if not isinstance(glycan, str):
    print("You need to format your glycan sequences as strings.")
    return
  if '=' in glycan:
    print("Could it be that you're using WURCS? Please convert to IUPACcondensed for using glycowork.")
  if 'RES' in glycan:
    print("Could it be that you're using GlycoCT? Please convert to IUPACcondensed for using glycowork.")
  return canonicalize_iupac(glycan)


def map_to_basic(glycoletter):
  """given a monosaccharide/linkage, try to map it to the corresponding base monosaccharide/linkage\n
  | Arguments:
  | :-
  | glycoletter (string): monosaccharide or linkage\n
  | Returns:
  | :-
  | Returns the base monosaccharide/linkage or the original glycoletter, if it cannot be mapped
  """
  if glycoletter in Hex:
    return 'Hex'
  elif glycoletter in dHex:
    return 'dHex'
  elif glycoletter in HexA:
    return 'HexA'
  elif glycoletter in HexN:
    return 'HexN'
  elif glycoletter in HexNAc:
    return 'HexNAc'
  elif glycoletter in Pen:
    return 'Pen'
  elif glycoletter in linkages:
    return '?1-?'
  elif (g2 := re.sub(r"\d", 'O', glycoletter)) in {k+'OS' for k in Hex}:
    return 'HexOS'
  elif g2 in {k+'OS' for k in HexNAc}:
    return 'HexNAcOS'
  else:
    return glycoletter


def structure_to_basic(glycan, libr = None):
  """converts a monosaccharide- and linkage-defined glycan structure to the base topology\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed nomenclature
  | libr (dict): dictionary of form glycoletter:index\n
  | Returns:
  | :-
  | Returns the glycan topology as a string
  """
  if libr is None:
    libr = lib
  if glycan[-3:] == '-ol':
    glycan = glycan[:-3]
  if '(' not in glycan:
    return map_to_basic(glycan)
  ggraph = glycan_to_nxGraph(glycan, libr = libr)
  nodeDict = dict(ggraph.nodes(data = True))
  temp = {k: map_to_basic(nodeDict[k]['string_labels']) for k in ggraph.nodes}
  nx.set_node_attributes(ggraph, temp, 'string_labels')
  return graph_to_string(ggraph)


def glycan_to_composition(glycan, stem_libr = None):
  """maps glycan to its composition\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format
  | stem_libr (dictionary): dictionary of form modified_monosaccharide:core_monosaccharide; default:created from lib\n
  | Returns:
  | :-
  | Returns a dictionary of form "Monosaccharide" : count
  """
  if stem_libr is None:
    stem_libr = stem_lib
  if '{' in glycan:
    glycan = glycan.replace('{', '').replace('}', '')
  composition = Counter([map_to_basic(stem_libr[k]) for k in min_process_glycans([glycan])[0]])
  allowed_mods = ['Me', 'S', 'P', 'PCho', 'PEtN']
  for m in allowed_mods:
    if m in glycan:
      composition[m] = glycan.count(m)
  if 'PCho' in glycan or 'PEtN' in glycan:
    del composition['P']
  if any([k in glycan for k in ['OAc', '2Ac', '3Ac', '4Ac', '6Ac', '7Ac', '9Ac']]):
    composition['Ac'] = sum([glycan.count(k) for k in ['OAc', '2Ac', '3Ac', '4Ac', '6Ac', '7Ac', '9Ac']])
  del composition['?1-?']
  composition = dict(composition)
  if any([k not in {'Hex', 'dHex', 'HexNAc', 'HexN', 'HexA', 'Neu5Ac', 'Neu5Gc', 'Kdn',
                    'Pen', 'Me', 'S', 'P', 'PCho', 'PEtN', 'Ac'} for k in composition.keys()]):
    return {}
  else:
    return composition


def composition_to_mass(dict_comp, mass_value = 'monoisotopic',
                      sample_prep = 'underivatized'):
  """given a composition, calculates its theoretical mass; only allowed extra-modifications are methylation, sulfation, phosphorylation\n
  | Arguments:
  | :-
  | dict_comp (dict): composition in form monosaccharide:count
  | mass_value (string): whether the expected mass is 'monoisotopic' or 'average'; default:'monoisotopic'
  | sample_prep (string): whether the glycans has been 'underivatized', 'permethylated', or 'peracetylated'; default:'underivatized'\n
  | Returns:
  | :-
  | Returns the theoretical mass of input composition
  """
  if sample_prep + '_' + mass_value == "underivatized_monoisotopic":
    mass_dict_in = mass_dict
  else:
    mass_dict_in = dict(zip(mapping_file.composition, mapping_file[sample_prep + '_' + mass_value]))
  for old_key, new_key in {'S': 'Sulphate', 'P': 'Phosphate', 'Me': 'Methyl', 'Ac': 'Acetate'}.items():
    if old_key in dict_comp:
      dict_comp[new_key] = dict_comp.pop(old_key)
  return sum(mass_dict_in.get(k, 0) * v for k, v in dict_comp.items()) + mass_dict_in['red_end']


def glycan_to_mass(glycan, mass_value = 'monoisotopic', sample_prep = 'underivatized', stem_libr = None):
  """given a glycan, calculates its theoretical mass; only allowed extra-modifications are methylation, sulfation, phosphorylation\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format
  | mass_value (string): whether the expected mass is 'monoisotopic' or 'average'; default:'monoisotopic'
  | sample_prep (string): whether the glycans has been 'underivatized', 'permethylated', or 'peracetylated'; default:'underivatized'
  | stem_libr (dictionary): dictionary of form modified_monosaccharide:core_monosaccharide; default:created from lib\n
  | Returns:
  | :-
  | Returns the theoretical mass of input glycan
  """
  if stem_libr is None:
    stem_libr = stem_lib
  comp = glycan_to_composition(glycan, stem_libr = stem_libr)
  return composition_to_mass(comp, mass_value = mass_value, sample_prep = sample_prep)
