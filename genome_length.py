# python3
# ################################################################## #
# genome_length.py (C) Oct 2021 Mainz.
# Author: Enrique M. Muro                               
# ################################################################## #
#
# --------------------------------------------------------------------
# Project
#
# Purpose: Get the golden path length (genome length) from ensembl
# repositories.
#
# Elapsed time:... Needs a lot of time, interacts with ensembl
# --------------------------------------------------------------------
# Comments: Unfortunately the main repositories do not have (today)
# the length of the genome available. It is quite odd
# --------------------------------------------------------------------
# Needs:
# Output: 
# --------------------------------------------------------------------
# General use:
# bzip2 -d ensembl__division_taxid_species.tsv.bz2
# python3 genome_length.py >> out.tsv 2> out.err
#
# at the end of the process:
#     mv out.tsv ensembl__taxid_species_goldenPath_division.tsv      
#     bzip2 ensembl__taxid_species_goldenPath_division.tsv
#     bzip2 ensembl__division_taxid_species.tsv
#
# Part of the code is from REST
# http://rest.ensembl.org/documentation/info/assembly_info
#################################################################### #
from time import time
import gzip
import requests, sys


# FUNCTIONS
###########
def golden_path_of(sp):
  """
  obtain the golden path length (genome len) for the species (sp)

  @type  sp: str  #  0-99
  @param sp: an species name (provided by ensembl)

  @rtype: 
  @return: a number (genome length in bp)
  """

  server = "http://rest.ensembl.org"
  ext    = "/info/assembly/"
  r = requests.get(server+ext+sp+"?", headers={ "Content-Type" : "application/json"}) 
  if not r.ok:
    return -999
    #r.raise_for_status()
    #sys.exit()   
  decoded = r.json()
  if 0: #debugging
    print(repr(decoded))
    
  return decoded["golden_path"]


# MAIN CODE
###########
def main():
    start_time = time()

    #retrieve the list of species already processed
    skip_header = True
    l_sp_processed = []
    with open("./out.tsv", "r") as f1:
      for l in f1:
        if skip_header:
          skip_header = False
          continue
        s = l.strip().split('\t')
        l_sp_processed.append(str(s[1]))
        
    #retrieve a list of species names
    species_file="ensembl__division_taxid_species.tsv"
    if not l_sp_processed:
      print("taxid", "species", "golden_path", "division", sep="\t")
    skip_header = True
    with open("./" + species_file, "r") as f:
      for l in f:
        if skip_header:
          skip_header = False
          continue
        s = l.strip().split('\t')
        division = str(s[0])
        taxid    = str(s[1])
        species  = str(s[2])
        if species in l_sp_processed:
          continue
        # get the genome len in bp
        genome_len = golden_path_of(species)
        print(str(taxid), species, str(genome_len), division, sep="\t", flush=True)

    elapsed_time = time() - start_time
    #print("Elapsed time: %.10f seconds" % elapsed_time)

    
if __name__ == "__main__":
    main()
