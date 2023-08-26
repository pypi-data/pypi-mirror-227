#!/usr/bin/env python3

import nbformat as nbf
from pathlib import Path, PurePosixPath
from datetime import datetime

nb = nbf.v4.new_notebook()
nb['cells'] = []

date_time = datetime.now()

jupyter = snakemake.output[0]
jupyter = f"{Path(jupyter).resolve()}"
name_jupyter = PurePosixPath(jupyter).stem
dir_jupyter = PurePosixPath(jupyter).parent
csv = f"{dir_jupyter}/{name_jupyter}.csv"

kmer_module_file_list = list(snakemake.params.list_log_kmer_per_sample)
#print (kmer_module_file_list)

rep_table2bed = snakemake.params.kmer_table_rep
#print(rep_table2bed)

##### variables
pvalues_pcadapt = snakemake.params.pvalues_pcadapt
outliers_pcadapt = snakemake.params.outliers_pcadapt
plots_pcadapt = snakemake.params.plots_pcadapt
outliers_pcadapt_position = snakemake.params.outliers_pcadapt_position

phenotype_pca_html = snakemake.params.phenotype_pca_html
outliers_lfmm = snakemake.params.outliers_lfmm
plots_lfmm = snakemake.params.plots_lfmm
outliers_lfmm_position = snakemake.params.outliers_lfmm_position

contigs_lfmm_csv = snakemake.params.contigs_lfmm_csv
contigs_pcadapt_csv = snakemake.params.contigs_pcadapt_csv
contig_size = snakemake.params.contig_size
fastq_stats = snakemake.params.fastq_stats

############################# KMERS BY SAMPLE ########################

code = """
%%html
<style>
       h1 {
            color:#135e96;
            border-bottom: 2px solid black;
            padding: 3px;
            padding_top: 5px
       }
       h2 {
            color:#135e96;
            padding: 3px;
            padding_top: 5px
       }
       h3 {
            color:#135e96;
            padding_top: 10px
            padding_bottom: 10px
       }
        body, p{
            margin-right: 15%;
            margin-left: 15%;
            font-size: 12pt
        }
        .output_png {
            display: table-cell;
            text-align: right;
            vertical-align: middle;
            
        }
}

</style>
"""

code2 = """
from itables import init_notebook_mode
init_notebook_mode(all_interactive=True)
#Styler.format(thousands=True)
#df.style.format(thousands=True)

"""

nb['cells'].append(nbf.v4.new_code_cell(code))
nb['cells'].append(nbf.v4.new_code_cell(code2))


texte = f"""\
# iKISS REPORT 💋

Date:  {date_time}

Software under MIT Licence.

By Julie Orjuela (UMR DIADE - IRD) 

This is an auto-generated jupyter notebook from iKISS package 🐍.
  
# READS INFO
"""

code = f"""\
import pandas as pd

file = "{fastq_stats}"
data = pd.read_csv(file, delimiter="\\t")
data
"""

nb['cells'].append(nbf.v4.new_markdown_cell(texte))
nb['cells'].append(nbf.v4.new_code_cell(code))


texte = f"""\

# KMERS INFO
"""

code = f"""\
from pathlib import Path, PurePosixPath
import pandas as pd
pd.set_option("display.precision", 2)

file_list = {kmer_module_file_list}
output_file = "{csv}"

data = {{}}
for file in file_list:
    file = Path(file).resolve()
    name = PurePosixPath(file).stem.split('_KMERS_MODULE')[0]
    dir = PurePosixPath(file).parent
    with open (file, 'r') as f:
        liste = []
        for line in f:
            #if "Total no. of reads" in line : 
            #    reads = int(line.strip().split(":")[1])
            #    liste.append(reads)
            if "Canonized kmers:" in line : 
                canonized = int(line.strip().split("\\t")[1])
                liste.append(canonized)
            if "Non-canon kmers:" in line : 
                non_canonized = int(line.strip().split("\\t")[1])
                liste.append(non_canonized)
            if "Non-canon kmers found:" in line : 
                non_canonized_founded = int(line.strip().split("\\t")[1])
                liste.append(non_canonized_founded)
            if "kmers to save:" in line : 
                tosave = int(line.strip().split(":")[1])
                liste.append(tosave)               
    data[name] = liste    
df_kmer_module = pd.DataFrame.from_dict(data, orient='index', columns=['Canonized', 'Non-canonized', 'Non-canonized_found','kmers_saved'])
df_kmer_module.to_csv(output_file)
df_kmer_module
"""

nb['cells'].append(nbf.v4.new_markdown_cell(texte))
nb['cells'].append(nbf.v4.new_code_cell(code))


############################# TABLE ########################
texte = f"""\

# KMER2TABLE STEP

iKISS uses [kmersGWAS](https://github.com/voichek/kmersGWAS) tool to generate a binary table of kmers.  This absence/presence table is splitted in several ones. Here you can see how many kmers are in each bim file.
"""
code = f"""\
from pathlib import Path, PurePosixPath
import pandas as pd
import subprocess

bims = []
nb_lines = []

source = Path("{rep_table2bed}")
for x in source.iterdir():
    if x.name.endswith('.bim'):
        file = f"{rep_table2bed}/{{x.name}}"
        command = ["wc", "-l", file]
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        data = process.communicate()
        lines = int(str(data[0]).strip().split(' ')[0].removeprefix('b').removeprefix("\'"))
        bims.append(x.name)
        nb_lines.append(lines)
        df = pd.DataFrame(list(zip(bims, nb_lines)), columns =['bim_name', 'nb_kmers'])
        total_kmers = df['nb_kmers'].sum()
df
"""

nb['cells'].append(nbf.v4.new_markdown_cell(texte))
nb['cells'].append(nbf.v4.new_code_cell(code))


############################# PCA ########################

texte_pcadapt = f"""\
# PCADAPT ANALYSIS

iKISS uses [pcadapt](https://cran.r-project.org/web/packages/pcadapt/index.html) tool to detect significant kmers under selection.

Number of kmers under selection detected by pcadapt are summary here.

"""
code_pcadapt = f"""\
from pathlib import Path, PurePosixPath
import pandas as pd
import subprocess

file = []
nb_lines = []
source = Path("{outliers_pcadapt}")
#print (source)
file_name = source.stem
#print (file_name)
command = ["wc", "-l", source]
process = subprocess.Popen(command, stdout=subprocess.PIPE)
data = process.communicate()
lines = int(str(data[0]).strip().split(' ')[0].removeprefix('b').removeprefix("\'"))
file.append(file_name)
nb_lines.append(lines)
df = pd.DataFrame(list(zip(file, nb_lines)), columns =['file', 'nb_kmers'])
df
"""

texte_pcadapt_bis = f"""\

## PLOTS 
Explore the [6.PCADAPT]({plots_pcadapt}) directory and check Projection onto PC1 and PC2, Manhattan Plot, Q-Q plot and also statistical distribution of pvalues.
"""

texte_pcadapt_position = f"""\

## PCADAPT OUTLIERS AND POSITIONS 
Some statistics about direct mapping of kmers versus {snakemake.params.ref}.
"""

code_pcadapt_position = f"""
from pathlib import Path, PurePosixPath
import pandas as pd
file = Path("{outliers_pcadapt_position}")
file = Path(file).resolve()
data = {{}}
name = 'KMERS_AND_POSITIONS'
with open (file, 'r') as f:
    liste = []
    for line in f:
        if "selected_df" in line : 
            selected_kmers = int(line.strip().split(":")[1])
            liste.append(selected_kmers)
        if "database_df" in line :
            db_df = int(line.strip().split(":")[1])
            liste.append(db_df)
        if "outliers_with_position" in line : 
            position = int(line.strip().split(":")[1])
            liste.append(position)
    data[name] = liste
df_kmer_module = pd.DataFrame.from_dict(data, orient='index', columns=['nb_kmers_with_position', 'nb_total_kmers', 'nb_outliers_with_position'])
df_kmer_module = df_kmer_module[['nb_total_kmers', 'nb_kmers_with_position', 'nb_outliers_with_position']]
df_kmer_module['percentage_outliers_with_position']= df_kmer_module['nb_outliers_with_position']*100/df_kmer_module['nb_kmers_with_position']
df_kmer_module.columns = ['nb_kmers_mapped_in_ref', 'nb_outliers_pcadapt', 'nb_outliers_with_position','percentage_kmers_with_position']
df_kmer_module.insert(0, "nb_total_kmers", [total_kmers])
df_kmer_module.T
"""


texte_pcadapt_assembly = f"""\

## CONTIGS USING PCADAPT SELECTED KMERS

Distribution of assembled contigs assembled by merge_tags using significant PCADAPT detected kmers in {contigs_pcadapt_csv}.
"""

code_pcadapt_assembly = f"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("{contigs_pcadapt_csv}", delimiter='\\t')
len(df)

df['len_contig']=df['contig'].apply(len)
df[df['len_contig'] >= {contig_size}]
nb_contigs_user = len(df[df['len_contig'] >= {contig_size}])
print (f'nb contigs selected by contig_size parametter given by user : {{nb_contigs_user}}')

for i in range(0, max(df["len_contig"]), 100):
    start=int(i)
    stop=int(start+100)
    cmd=(len(df[(df["len_contig"]>start) & (df["len_contig"]<stop)]))
    print(f"interval {{start}}-{{stop}}\\t{{cmd}}")

# setting the dimensions of the plot
ax = plt.subplots(figsize=(15, 6))
df2=(df[(df["len_contig"]>0) & (df["len_contig"]<(max(df["len_contig"])+100))])
sns.histplot(data=df2, x="len_contig", log_scale=False, bins=100, stat="count")

# setting the dimensions of the plot
ax = plt.subplots(figsize=(15, 6))
df2=(df[(df["len_contig"]>{contig_size}) & (df["len_contig"]<(max(df["len_contig"])+100))])
sns.histplot(data=df2, x="len_contig", log_scale=False, bins=20, stat="count") """

#<img src="../6.LFMM/output_file.0_1_lfmm.manhattan_plot.png" width="400"/>
#<img src="../6.LFMM/output_file.0_1_lfmm.screen_plot.png" width="400"/>

if "PCADAPT" in snakemake.params.workflow_steps:
    nb['cells'].append(nbf.v4.new_markdown_cell(texte_pcadapt))
    nb['cells'].append(nbf.v4.new_code_cell(code_pcadapt))
    nb['cells'].append(nbf.v4.new_markdown_cell(texte_pcadapt_bis))
    if "MAPPING" in snakemake.params.workflow_steps:
        nb['cells'].append(nbf.v4.new_markdown_cell(texte_pcadapt_position))
        nb['cells'].append(nbf.v4.new_code_cell(code_pcadapt_position))
    if "ASSEMBLY" in snakemake.params.workflow_steps:
        nb['cells'].append(nbf.v4.new_markdown_cell(texte_pcadapt_assembly))
        nb['cells'].append(nbf.v4.new_code_cell(code_pcadapt_assembly))

############################# LFMM ########################
# selected,db, with mapping stats . LOGS/11.OUTLIERS_LFMM_POSITION/OUTLIERS_POSITION.e
texte_lfmm = f"""\
# LFMM ANALYSIS

iKISS uses [lfmm](https://cran.r-project.org/web/packages/pcadapt/index.html) tool to detect significant kmers associated with a phenotype.

Number of kmers under selection detected by lfmm are summary here.

"""
code_lfmm = f"""\
from pathlib import Path, PurePosixPath
import pandas as pd
import subprocess

file = []
nb_lines = []
source = Path("{outliers_lfmm}")
#print (source)
file_name = source.stem
#print (file_name)
command = ["wc", "-l", source]
process = subprocess.Popen(command, stdout=subprocess.PIPE)
data = process.communicate()
lines = int(str(data[0]).strip().split(' ')[0].removeprefix('b').removeprefix("\'"))
file.append(file_name)
nb_lines.append(lines)
df = pd.DataFrame(list(zip(file, nb_lines)), columns =['file', 'nb_kmers'])
df
"""


texte_lfmm_bis = f"""\
## PLOTS 

Explore the [6.LFMM]({plots_lfmm}) directory and check Manhattan Plot and Q-Q plot.
"""

texte_lfmm_phenotype_pca = f"""\

## PHENOTYPE PCA ANALYSIS

PCA complexity reduction was done in phenotype data in the iKISS package. 
Steps are described the [html phenotype report]({phenotype_pca_html}) in the REPORT directory.
"""


texte_lfmm_position = f"""\

## OUTLIERS AND POSITIONS
 
Some statistics about direct mapping of kmers versus {snakemake.params.ref}.
"""

code_lfmm_position = f"""
from pathlib import Path, PurePosixPath
import pandas as pd
file = Path("{outliers_lfmm_position}")
file = Path(file).resolve()
data = {{}}
name = 'KMERS_AND_POSITIONS'
with open (file, 'r') as f:
    liste = []
    for line in f:
        if "selected_df" in line : 
            selected_kmers = int(line.strip().split(":")[1])
            liste.append(selected_kmers)
        if "database_df" in line :
            db_df = int(line.strip().split(":")[1])
            liste.append(db_df)
        if "outliers_with_position" in line : 
            position = int(line.strip().split(":")[1])
            liste.append(position)
    data[name] = liste
df_kmer_module = pd.DataFrame.from_dict(data, orient='index', columns=['nb_kmers_with_position', 'nb_total_kmers', 'nb_outliers_with_position'])
df_kmer_module = df_kmer_module[['nb_total_kmers', 'nb_kmers_with_position', 'nb_outliers_with_position']]
df_kmer_module['percentage_outliers_with_position']= df_kmer_module['nb_outliers_with_position']*100/df_kmer_module['nb_kmers_with_position']
df_kmer_module.columns = ['nb_kmers_mapped_in_ref', 'nb_outliers_lfmm', 'nb_outliers_with_position','percentage_kmers_with_position']
df_kmer_module.insert(0, "nb_total_kmers", [total_kmers])
df_kmer_module.T
"""



texte_lfmm_assembly = f"""\

## CONTIGS FROM LFMM SELECTED KMERS

Distribution of assembled contigs assembled by merge_tags using significant LFMM detected kmers in {contigs_lfmm_csv}.
"""

code_lfmm_assembly = f"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("{contigs_lfmm_csv}", delimiter='\\t')
len(df)

df['len_contig']=df['contig'].apply(len)
df[df['len_contig'] >= {contig_size}]
nb_contigs_user = len(df[df['len_contig'] >= {contig_size}])
print (f'nb contigs selected by contig_size parametter given by user : {{nb_contigs_user}}')

for i in range(0, max(df["len_contig"]), 100):
    start=int(i)
    stop=int(start+100)
    cmd=(len(df[(df["len_contig"]>start) & (df["len_contig"]<stop)]))
    print(f"interval {{start}}-{{stop}}\\t{{cmd}}")
    
# setting the dimensions of the plot
ax = plt.subplots(figsize=(15, 6))
df2=(df[(df["len_contig"]>0) & (df["len_contig"]<(max(df["len_contig"])+100))])
sns.histplot(data=df2, x="len_contig", log_scale=False, bins=100, stat="count")

# setting the dimensions of the plot
ax = plt.subplots(figsize=(15, 6))
df2=(df[(df["len_contig"]>{contig_size}) & (df["len_contig"]<(max(df["len_contig"])+100))])
sns.histplot(data=df2, x="len_contig", log_scale=False, bins=20, stat="count") """

if "LFMM" in snakemake.params.workflow_steps:
    nb['cells'].append(nbf.v4.new_markdown_cell(texte_lfmm))
    nb['cells'].append(nbf.v4.new_code_cell(code_lfmm))
    if not "" in snakemake.params.phenotype:
        nb['cells'].append(nbf.v4.new_markdown_cell(texte_lfmm_phenotype_pca))
    nb['cells'].append(nbf.v4.new_markdown_cell(texte_lfmm_bis))
    if "MAPPING" in snakemake.params.workflow_steps:
        nb['cells'].append(nbf.v4.new_markdown_cell(texte_lfmm_position))
        nb['cells'].append(nbf.v4.new_code_cell(code_lfmm_position))
    if "ASSEMBLY" in snakemake.params.workflow_steps:
        nb['cells'].append(nbf.v4.new_markdown_cell(texte_lfmm_assembly))
        nb['cells'].append(nbf.v4.new_code_cell(code_lfmm_assembly))

txt_config = Path(snakemake.params.txt_config)


############################# CONFIG ########################
texte_yaml = """
# Configuration file

Here you can find parameters used by iKISS.

"""

code_yaml = f"""\
import yaml
from pprint import pprint
file = "{txt_config}"
experiment_details = yaml.safe_load(open(file))
pprint(experiment_details)
"""

nb['cells'].append(nbf.v4.new_markdown_cell(texte_yaml))
nb['cells'].append(nbf.v4.new_code_cell(code_yaml))


with open(jupyter, 'w') as f:
    nbf.write(nb, f)


############################# ASSEMBLY ########################



