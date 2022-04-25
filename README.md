# bioinf-genome_length   
# Get the genome length for all Ensembl species

Get the golden path length (genome length) from ensembl repositories.


## 1. Preprocess the info from the different species availables (Ensembl)
### Download the files
Goal: For the different ENSEMBL species obtain: their division, taxonomy id and species name.   
Download the files for the different divisions:  
- For [vertebrates (ENSEMBL v98):](http://ftp.ensembl.org/pub/release-98/species_EnsemblVertebrates.txt)
  - species_EnsemblVertebrates.txt (header + 227 species)
- For [ENSEMBLGENOMES v49:](http://ftp.ensemblgenomes.org/pub/release-49/species.txt)  
    Check the content of the file:
	```terminal  
	cut -f2,3,4 species.txt | head -n 1   
	species	division	taxonomy_id  
	```
	
	```terminal  
	wc -l species.txt   
	32795 species.txt  
	```
	
	```terminal
	cut -f2,3,4 species.txt | awk '{print $2"\t"$3"\t"$1}' | cut -f1 | sort | uniq -c  
	      1 division  # This is the header
	  31332 EnsemblBacteria  
	   1014 EnsemblFungi  
	    115 EnsemblMetazoa  
	     96 EnsemblPlants  
	    237 EnsemblProtists  
	```
    
### Parse the files
Obtaining ensembl__division_taxid_species.tsv  
```term
cut -f2,3,4 species_EnsemblBacteria.txt | awk '{print $2"\t"$3"\t"$1}' > ensembl__division_taxid_species.tsv  
cut -f2,3,4 species.txt | awk '{print $2"\t"$3"\t"$1}' | awk 'NR>1' >> ensembl__division_taxid_species.tsv # It does not cp the header line
gzip ensembl__division_taxid_species.tsv
```

### Preprocessed file (result)
For simplicity, I collect all the divisions in one file (bzip2 compressed):
```note
name:   ensembl__division_taxid_species.tsv.bz2
header: "division\ttaxonomy_id\tspecies"
```

lines (header + entries)
```term
bzcat ensembl__division_taxid_species.tsv.bz2 | wc -l 
33022
```

content
```term
bzcat ensembl__division_taxid_species.tsv.bz2 | cut -f1 | sort | uniq -c
      1 division # From the header line
  31332 EnsemblBacteria
   1014 EnsemblFungi
    115 EnsemblMetazoa
     96 EnsemblPlants
    237 EnsemblProtists
    227 EnsemblVertebrates
```




## 2. Obtain the genome length for each species:
### genome_length.py  

The code uses http://rest.ensembl.org/documentation/info/assembly_info



**Note: seems to me that after ~10000 does not retrieve more seqs (probably a retriction from ensembl)**  

**Result:** From 33022 species (ensembl98, ensemblgenomes49), the golden_path (genome length) of all but 84 (when current ensembl version was 104) were obtained.  
Note that it looks for the golden path info in the current version of ensembl.  
Some are species from ensembl98 are not in the current genome annotation ensembl104 and some could be emsembl pitfalls. 


(ensembl__taxid_species_goldenPath_division.tsv)

ensembl__taxid_species_goldenPath_division.tsv
The file has 4 columns. For instance
taxid	species	golden_path	division
9606	homo_sapiens	3096649726	EnsemblVertebrates

If there is no golden path genome length for a species (84 cases), it is annotated with "golden_path"==-999


---
## Output file
**Table with the  genome length for all Ensembl species**
Golden_path (genome length) for 33022 species (ensembl98, ensemblgenomes49)

## File: 
ensembl__taxid_species_goldenPath_division.tsv.bz2  (bzip2 compressed)
The file has 4 columns. For instance:  
> taxid\tspecies\tgolden_path\tdivision  
> 9606\thomo_sapiens\t3096649726\tEnsemblVertebrates 
