#genome=/home/juan/Desktop/juan/bio/data/IWGSC/42/Triticum_aestivum.IWGSC.dna.toplevel.fa

genome=data/IRGSP-1.0_genome.fasta
mites=data/results.csv
families=data/families/
onlyflanking=data/ofs/
flanking=data/fs/
flanking_clusters=data/fs_clusters/
clusters=data/clusters/
clusters_file=data/clusters.csv
fasta_clusters=data/clusters.fasta
fs_clusters_dir=data/fs_cluster/
organism=rice

mkdir $families
mkdir $onlyflanking
mkdir $flanking
mkdir $flanking_clusters
mkdir $flanking_clusters

python blast_filter.py -i $mites -o ${mites}.filtered
python blast2gff.py -i ${mites}.filtered -n MITE -o ${mites}.filtered.gff3
python gff2fastas.py -i ${mites}.filtered.gff3 -g $genome -o $families
python clusterize.py -f $families --clusters $clusters --csv $clusters_file --fasta $fasta_clusters -g $genome
#extract FS of interesting clusters
python 1cluster_extract_fs.py --with_fs $flanking -f $families --fsdir $onlyflanking --clusters $clusters --csv $clusters_file --fasta $fasta_clusters -g $genome
python cluster_fs_compare.py  --onlyflanking $onlyflanking --flankingcluster $flanking_clusters