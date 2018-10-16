Welcome to Moolti, Multiple Organism Optimization Lab Tool for iGEM !
MOOLTi allows for the codon optimization of a DNA sequence for multiple organisms, simultaneously. 

To learn more , go to  http://2018.igem.org/Team:HebrewU/Software

MOOLTi is now available online !  optimize your proteins at http://ec2-52-23-211-181.compute-1.amazonaws.com

Example .fasta protein files and restriction enzymes files can be found at CodonOptimization\example_files
Example .csv files for many model organisms can be found at CodonOptimization\organism_files

Usage instructions:

Run using Python GUI: 
1) Double - Click optimize.bat
2)Pick optimization method
3) upload: 
    a) a .fasta file containing the protein 
    b) an empty file to save the result into 
    c) (optional) a file containing restriction enzymes names, or simply type them in (separated by comma )
4) click "Next"
5) upload  a .csv file containing a codon usage table (see database) for each organism 
6) (optional) add up to 4 organisms
7) click "optimize"
8) the file with the output DNA was saved to the desired destination.


Command Line Run: 
1) open command line
2) Go to the downloaded folder location -> CodonOptimization\ (make sure Main.py is in the same folder !)
3) run (in cmd line): 
python3 Main.py  <protein sequence string> <threshold (defult is 0.05)> <organism 1 codon filename (csv file)>  <organism 2 codon table filename (csv file)>  
4) press enter
5) write the case sensitive restriction enzymes to be avoided, if none press enter
6) the output is printed to the cmd line
